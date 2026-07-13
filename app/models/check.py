import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.enums.check_status import CheckStatus
from app.enums.program_type import ProgramType


class Check(Base):
    __tablename__ = "checks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    program: Mapped[ProgramType] = mapped_column(
        Enum(ProgramType, name="program_type"),
        nullable=False,
    )

    status: Mapped[CheckStatus] = mapped_column(
        Enum(CheckStatus, name="check_status"),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(Text)

    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    documents = relationship(
        "Document",
        back_populates="check",
        cascade="all, delete-orphan",
    )

    issues = relationship(
        "Issue",
        back_populates="check",
        cascade="all, delete-orphan",
    )