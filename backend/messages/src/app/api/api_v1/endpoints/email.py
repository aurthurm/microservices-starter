from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.apps.mail import crud, models, schemas
from app.apps.core import schemas as core_schemas
from app.api import deps
from app.core.config import settings
from app.apps.mail.utils import (
    send_reset_password_email
)

router = APIRouter()


@router.post("/mail-processor", response_model=core_schemas.Msg)
def process_email(
    *,
    db: Session = Depends(deps.get_db),
    email_in: schemas.EMailCreate,
):
    """
    Create new EMail.
    """
    crud.email.create(db, obj_in=email_in)
    rsp = {"msg": "EMail Received, it will be processed soon"}
    return rsp