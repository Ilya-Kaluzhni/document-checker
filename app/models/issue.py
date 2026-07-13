import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.enums.issue_level import IssueLevel


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    check_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("checks.id", ondelete="CASCADE"),
    )

    level: Mapped[IssueLevel] = mapped_column(
        Enum(IssueLevel, name="issue_level"),
    )

    message: Mapped[str] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    check = relationship(
        "Check",
        back_populates="issues",
    )