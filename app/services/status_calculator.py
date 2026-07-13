from app.enums.check_status import CheckStatus
from app.enums.issue_level import IssueLevel


class StatusCalculator:

    @staticmethod
    def calculate(issues):

        if not issues:
            return CheckStatus.APPROVED

        has_error = any(
            issue["level"] == IssueLevel.ERROR
            for issue in issues
        )

        if has_error:
            return CheckStatus.REJECTED

        return CheckStatus.APPROVED