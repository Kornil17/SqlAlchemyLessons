from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Annotated

Base = declarative_base()
metadata = MetaData()

intpk = Annotated[int, mapped_column(primary_key=True)]

# class Users(Base):
#     __tablename__ = 'workers'
#     id = Column(Integer, primary_key=True)
#     username = Column(String)

# Принимаемы типы данных мы может задавать через аннтоцию.
# Пример: Mapped[int | None] тоже самое что mapped_column(nullable=True). Задает ограничение  что данные могут не придти.
class Users(Base):
    __tablename__ = 'workers'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column()

class ResumeOrm(Base):
    __tablename__ = 'resumes'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column()
    salary: Mapped[int] = mapped_column(nullable=True)
    worker_id: Mapped[int] = mapped_column(ForeignKey(Users.id, ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class VacancyORM:
    """
    Table many to many relationship
    """
    __tablename__ = 'vacancy'

    resume_id: Mapped[int] = mapped_column(
        ForeignKey(ResumeOrm.id, ondelete='CASCADE'),
        primary_key=True
    )
    worker_id: Mapped[int] = mapped_column(
        ForeignKey(Users.id, ondelete='CASCADE'),
        primary_key=True
    )




