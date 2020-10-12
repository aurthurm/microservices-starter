from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..core.crud import CRUDBase, ACRUDBase
from .models import EMail
from .schemas import EMailCreate, EMailUpdate


class CRUDEMail(CRUDBase[EMail, EMailCreate, EMailUpdate]):
    def create(
        self, db: Session, *, obj_in: EMailCreate
    ) -> EMail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_sender(
        self, db: Session, *, sender_id: int, skip: int = 0, limit: int = 100
    ) -> List[EMail]:
        return (
            db.query(self.model)
            .filter(EMail.sender == sender_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


email = CRUDEMail(EMail)


class ACRUDEMail(ACRUDBase[EMail, EMailCreate, EMailUpdate]):
    pass

aemail = ACRUDEMail(EMail)