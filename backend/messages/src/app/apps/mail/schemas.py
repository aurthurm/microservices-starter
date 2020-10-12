from typing import Optional

from pydantic import BaseModel

#
# ........ EMailType Schemas .........
#
class EMailTypeBase(BaseModel):
    title: str

class EMailType(EMailTypeBase):
    id: int

    class Config:
        orm_mode = True

class EMailTypeUpdate(EMailType):
    title: Optional[str] = None

class EMailTypeCreate(EMailTypeBase):
    pass


# Shared properties
class EmailBase(BaseModel):    
    sender: str     # e.g username
    recipient: str  # email_adress
    subject: str
    body: str    

# Properties to receive on Email creation
class EMailCreate(EmailBase):
    cc: Optional[str] = None
    category: str = "general"
    

# Properties to receive on item update
class EMailUpdate(EmailBase):
    emailtype_id: Optional[int] = None
    emailtype: Optional[EMailType] = None
    sent: Optional[bool] = False
    date_sent: Optional[str] = None


# Properties shared by models stored in DB
class EMailInDBBase(EmailBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class EMail(EMailInDBBase):
    pass


# Properties properties stored in DB
class EMailInDB(EMailInDBBase):
    pass