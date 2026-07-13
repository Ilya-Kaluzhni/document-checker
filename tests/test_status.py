from app.services.status_calculator import StatusCalculator
from app.enums.check_status import CheckStatus
from app.enums.issue_level import IssueLevel


def test_empty_issues_is_approved():

    result = StatusCalculator.calculate([])

    assert result == CheckStatus.APPROVED



def test_warning_is_approved():

    issues = [
        {
            "level": IssueLevel.WARNING,
            "message": "unknown document"
        }
    ]

    result = StatusCalculator.calculate(issues)

    assert result == CheckStatus.APPROVED



def test_error_is_rejected():

    issues = [
        {
            "level": IssueLevel.ERROR,
            "message": "missing contract"
        }
    ]

    result = StatusCalculator.calculate(issues)

    assert result == CheckStatus.REJECTED