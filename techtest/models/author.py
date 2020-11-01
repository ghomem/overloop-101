from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from techtest.connector import BaseModel


class Region(BaseModel):
    __tablename__ = 'author'

    id = Column(
        Integer,
        name='id',
        nullable=False,
        primary_key=True,
        autoincrement=True
    )

    first_name = Column(
        Text,
        name='first_name'
    )

    last_name = Column(
        Text,
        name='last_name'
    )
