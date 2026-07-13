from enum import Enum


class CheckStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    CHECK_IN_PROGRESS = "check_in_progress"