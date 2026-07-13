from pathlib import Path

from app.enums.document_type import DocumentType
from app.enums.issue_level import IssueLevel
from app.enums.program_type import ProgramType


class Validator:

    MAX_FILE_SIZE = 20 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".jpg",
        ".jpeg",
        ".png",
    }

    REQUIRED_DOCUMENTS = {
        ProgramType.FEDERAL: {
            DocumentType.CONTRACT,
            DocumentType.SPECIFICATION,
            DocumentType.INVOICE,
            DocumentType.ACT,
        },
        ProgramType.REGIONAL: {
            DocumentType.CONTRACT,
            DocumentType.INVOICE,
            DocumentType.ACT,
        },
    }

    @classmethod
    def validate(cls, documents, program):
        issues = []

        issues.extend(
            cls.check_required_documents(
                documents,
                program
            )
        )

        issues.extend(
            cls.check_file_properties(
                documents
            )
        )

        return issues

    @classmethod
    def check_required_documents(cls, documents, program):

        issues = []

        existing_types = {
            document.detected_type
            for document in documents
        }

        required = cls.REQUIRED_DOCUMENTS[program]

        for document_type in required:
            if document_type not in existing_types:

                issues.append(
                    {
                        "level": IssueLevel.ERROR,
                        "message": (
                            f"Отсутствует обязательный документ: "
                            f"{document_type.value}"
                        )
                    }
                )

        return issues

    @classmethod
    def check_file_properties(cls, documents):

        issues = []

        for document in documents:

            extension = Path(
                document.filename
            ).suffix.lower()

            if extension not in cls.ALLOWED_EXTENSIONS:

                issues.append(
                    {
                        "level": IssueLevel.ERROR,
                        "message": (
                            f"Недопустимый формат файла: "
                            f"{document.filename}"
                        )
                    }
                )


            if document.size > cls.MAX_FILE_SIZE:

                issues.append(
                    {
                        "level": IssueLevel.ERROR,
                        "message": (
                            f"Размер файла больше 20 МБ: "
                            f"{document.filename}"
                        )
                    }
                )


            if document.detected_type == DocumentType.UNKNOWN:

                issues.append(
                    {
                        "level": IssueLevel.WARNING,
                        "message": (
                            f"Не удалось определить тип документа: "
                            f"«{document.filename}»"
                        )
                    }
                )

        return issues