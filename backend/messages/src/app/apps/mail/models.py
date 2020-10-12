from typing import TYPE_CHECKING
import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship

from app.database.base_class import Base, BaseModel


class CategoryEnum(enum.Enum):
    """Different types of emails"""
    general = 1
    newaccount = 2
    paswordreset = 3

class EMailType(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

class EMail(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(Integer, index=True)
    recipient = Column(String, index=True)
    cc = Column(String)
    subject = Column(String)
    body = Column(String)
    category = Column(String)   
    sent = Column(Boolean, default=False)    
    date_sent = Column(Boolean, default=False)
    emailtype_id = Column(Integer, ForeignKey("emailtype.id"))
    emailtype = relationship("EMailType", backref="emails")
    category = Column(Enum(CategoryEnum))
