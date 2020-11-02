from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from techtest.connector import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(
        Integer,
        name='id',
        nullable=False,
        primary_key=True,
        autoincrement=True
    )

    user_name = Column(
        Text,
        name='user_name'
    )
 
