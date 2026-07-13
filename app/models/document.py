import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.enums.document_type import DocumentType


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    check_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("checks.id", ondelete="CASCADE"),
    )

    filename: Mapped[str] = mapped_column(String(255))

    detected_type: Mapped[DocumentType] = mapped_column(
        Enum(DocumentType, name="document_type"),
    )

    mime_type: Mapped[str] = mapped_column(String(100))

    size: Mapped[int] = mapped_column(Integer)

    file_path: Mapped[str] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    check = relationship(
        "Check",
        back_populates="documents",
    )