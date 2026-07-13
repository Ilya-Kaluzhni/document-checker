from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.models.check import Check
from app.models.document import Document
from app.models.issue import Issue


class CheckRepository:

    def __init__(self, db: Session):
        self.db = db


    def create_check(
        self,
        check: Check,
    ) -> Check:

        self.db.add(check)
        self.db.commit()
        self.db.refresh(check)

        return check


    def add_documents(
        self,
        documents: list[Document],
    ):

        self.db.add_all(documents)
        self.db.commit()


    def add_issues(
        self,
        issues: list[Issue],
    ):

        self.db.add_all(issues)
        self.db.commit()

    def get_by_id(
            self,
            check_id: UUID,
    ) -> Check | None:
        return (
            self.db.query(Check)
            .options(
                joinedload(Check.documents),
                joinedload(Check.issues),
            )
            .filter(Check.id == check_id)
            .first()
        )


    def get_all(self):

        return (
            self.db.query(Check)
            .order_by(Check.created_at.desc())
            .all()
        )

    def update_check(
            self,
            check: Check,
    ) -> Check:
        self.db.commit()
        self.db.refresh(check)

        return check