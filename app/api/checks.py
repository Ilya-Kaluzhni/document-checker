from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    UploadFile,
)

from uuid import UUID
from typing import Annotated
from app.schemas.check import (
    CheckListResponse,
)
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.enums.program_type import ProgramType
from app.services.check_service import CheckService
from app.schemas.check import CheckResponse


router = APIRouter(
    prefix="/api/checks",
    tags=["checks"]
)

@router.post("", response_model=CheckResponse)
async def create_check(
    files: Annotated[list[UploadFile], File(...)],
    program: Annotated[ProgramType, Form(...)],
    db: Session = Depends(get_db),
):
    if not files:
        raise HTTPException(
            status_code=400,
            detail="Files are required",
        )

    service = CheckService(db)

    return await service.create_check(
        files,
        program,
    )

@router.get(
    "",
    response_model=list[CheckListResponse],
)
def get_checks(
    db: Session = Depends(get_db),
):

    service = CheckService(db)

    checks = service.get_checks_list()

    return checks


@router.get(
    "/{check_id}",
    response_model=CheckResponse,
)
def get_check(
    check_id: UUID,
    db: Session = Depends(get_db),
):

    service = CheckService(db)

    result = service.get_check(check_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Check not found",
        )

    return result