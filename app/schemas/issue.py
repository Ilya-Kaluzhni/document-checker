from pydantic import BaseModel

from app.enums.issue_level import IssueLevel


class IssueResponse(BaseModel):

    level: IssueLevel
    message: str