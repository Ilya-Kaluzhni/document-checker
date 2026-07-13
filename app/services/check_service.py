from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.check_status import CheckStatus
from app.models.check import Check
from app.models.document import Document
from app.models.issue import Issue

from app.repositories.check_repository import CheckRepository

from app.services.document_detector import DocumentDetector
from app.services.validator import Validator
from app.services.status_calculator import StatusCalculator

from app.storage.file_storage import FileStorage

from app.schemas.check import (
    CheckResponse,
    ExtractedData,
)

from app.schemas.document import DocumentResponse
from app.schemas.issue import IssueResponse

class CheckService:

    def __init__(self, db: Session):

        self.repository = CheckRepository(db)

    async def create_check(
        self,
        files,
        program,
    ):

        # 1. Создаем пустую проверку

        check = Check(
            program=program,
            status=CheckStatus.CHECK_IN_PROGRESS,
        )

        check = self.repository.create_check(check)


        # 2. Сохраняем файлы

        saved_files = await FileStorage.save_files(
            check.id,
            files,
        )

        # 3. Создаём документы
        documents = []

        for file in saved_files:

            document_type = (
                DocumentDetector.detect(
                    file["filename"]
                )
            )

            document = Document(
                check_id=check.id,
                filename=file["filename"],
                detected_type=document_type,
                mime_type=file["content_type"],
                size=file["size"],
                file_path=file["file_path"],
            )

            documents.append(document)

        # 4. Сохраняем
        self.repository.add_documents(
            documents
        )

        # 5. Запускаем проверку
        issues_data = Validator.validate(
            documents,
            program,
        )

        # 6. Создаем Issue
        issues = []

        for item in issues_data:

            issue = Issue(
                check_id=check.id,
                level=item["level"],
                message=item["message"],
            )

            issues.append(issue)


        self.repository.add_issues(
            issues
        )

        # 7. Читаем статус

        status = StatusCalculator.calculate(
            issues_data
        )


        check.status = status
        check.reason = None

        if status == CheckStatus.REJECTED:
            check.reason = "Нельзя заявлять в банк"
        else:
            check.reason = "Пакет документов прошел проверку"

        self.repository.update_check(check)

        return self.build_response(check)


    def build_response(
            self,
            check: Check,
    ):

        return CheckResponse(

            check_id=check.id,

            status=check.status,

            status_label=(
                "Можно заявлять в банк"
                if check.status == CheckStatus.APPROVED
                else "Нельзя заявлять в банк"
            ),

            reason=check.reason,

            issues=[
                IssueResponse(
                    level=issue.level,
                    message=issue.message,
                )
                for issue in check.issues
            ],

            documents=[
                DocumentResponse(
                    name=document.filename,
                    detected_type=document.detected_type,
                    size_kb=document.size // 1024,
                )
                for document in check.documents
            ],

            extracted=ExtractedData(),

            checked_at=check.checked_at,
        )

    def get_check(
            self,
            check_id,
    ):

        check = self.repository.get_by_id(
            check_id
        )

        if not check:
            return None

        return self.build_response(check)

    def get_checks(self):

        checks = self.repository.get_all()

        return [
            self.build_response(check)
            for check in checks
        ]

    def get_checks_list(self):

        checks = self.repository.get_all()

        return [
            {
                "id": check.id,
                "checked_at": check.checked_at,
                "program": check.program,
                "status": check.status,
                "documents_count": len(check.documents),
            }
            for check in checks
        ]