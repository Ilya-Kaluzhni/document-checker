from enum import Enum


class IssueLevel(str, Enum):
    ERROR = "error"
    WARNING = "warning"