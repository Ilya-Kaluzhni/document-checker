from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.enums.check_status import CheckStatus
from app.enums.program_type import ProgramType

from app.schemas.document import DocumentResponse
from app.schemas.issue import IssueResponse


class ExtractedData(BaseModel):

    contractor: str | None = None
    amount: str | None = None
    date: str | None = None
    subject: str | None = None



class CheckResponse(BaseModel):

    check_id: UUID

    status: CheckStatus

    status_label: str

    reason: str | None = None

    issues: list[IssueResponse]

    documents: list[DocumentResponse]

    extracted: ExtractedData | None = None

    checked_at: datetime


class CheckListResponse(BaseModel):

    id: UUID

    checked_at: datetime

    program: ProgramType

    status: CheckStatus

    documents_count: int