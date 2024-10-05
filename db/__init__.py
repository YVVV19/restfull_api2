from typing import Optional
from decimal import Decimal
from sqlmodel import(
    Relationship,
    SQLModel,
    Field,
    Session,
    create_engine,
)
from sqlalchemy.orm import sessionmaker

class ToDoId(SQLModel):
    id: Optional[int] = Field(
        primary_key=True,
        default=None
    )


class Model(ToDoId, table=True):
    name:str


class Task(ToDoId, table=True):
    name: str
    for_what_id: Optional[int] = Field(
        default=None,
        foreign_key=f"{Model.__name__.lower()}.id"
    )
    for_what: Model = Relationship()
    money: Decimal = Field(default=0, max_digits=5000)
    result: str


class TaskCreate(ToDoId):
    name: str
    for_what: str
    money: Decimal = Field(default=0, max_digits=5000)
    result: str



class Config():
    ENGINE = create_engine("sqlite:///my_db.db", echo=True)
    SESSION = sessionmaker(bind=ENGINE)
    session = Session(bind=ENGINE)
    @classmethod
    def migrate(cls):
        SQLModel.metadata.drop_all(bind=cls.ENGINE)
        SQLModel.metadata.create_all(bind=cls.ENGINE)

    