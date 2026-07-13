from app.services.validator import Validator
from app.enums.program_type import ProgramType
from app.enums.document_type import DocumentType


class MockDocument:

    def __init__(
        self,
        filename,
        detected_type,
        size
    ):
        self.filename = filename
        self.detected_type = detected_type
        self.size = size


def test_federal_missing_specification():

    documents = [
        MockDocument(
            "договор.pdf",
            DocumentType.CONTRACT,
            1000
        ),
        MockDocument(
            "счет.pdf",
            DocumentType.INVOICE,
            1000
        ),
        MockDocument(
            "акт.pdf",
            DocumentType.ACT,
            1000
        ),
    ]

    issues = Validator.validate(
        documents,
        ProgramType.FEDERAL
    )

    assert len(issues) == 1
    assert "specification" in issues[0]["message"]