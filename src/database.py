import asyncio
from typing import Annotated, Callable
from sqlalchemy import String, create_engine, text, Table, Column, Integer, MetaData, insert, select, update, func, \
    cast, and_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, Mapped, MappedColumn
from config import settings
from models import metadata, Base, Users, ResumeOrm



sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)

async_engine = create_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)

metadata.reflect(bind=sync_engine)

session = sessionmaker(sync_engine)


class DB:
    @staticmethod
    def sync_connect():
        with sync_engine.connect() as conn:
            # res = conn.execute(text('SELECT VERSION()'))
            res = conn.execute(text('SELECT datname FROM pg_database;'))
            print(res.all())
            return conn

    @staticmethod
    async def async_connetc():
        async with AsyncSession(async_engine) as conn:
            res = await conn.execute(text('SELECT VERSION()'))
            print(res.all())

    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

# def insert_data():
#     # query = """INSERT INTO workers(username) VALUES('Bobr')"""
#     query = insert(Users).values(
#         [
#             {"username": 'Bobr'},
#             {"username": 'Valera'}
#         ]
#     )
#     with sync_engine.connect() as conn:
#         # conn.execute(text(query))
#         conn.execute(query)
#         conn.commit()
    @staticmethod
    def insert_data():
        # query = """INSERT INTO workers(username) VALUES('Bobr')"""
        worker_bobr = Users(username='Bobr')
        worker_valera = Users(username='Valera')
        with session() as conn:
            conn.add_all([worker_bobr, worker_valera])
            conn.commit()

    @staticmethod
    def select_data():
        with session() as conn:
            result_workers = conn.execute(select(Users))
            result_resumes = conn.execute(select(ResumeOrm))
            print(f"workers all -> {result_workers.first()[0].username}")
            print(f"resumes all -> {result_resumes.all()}")
    @staticmethod
    def update_data_sql(id: int, name: str):
        with session() as conn:
            query = text("UPDATE workers SET username=:username WHERE id=:id")
            query = query.bindparams(username=name, id=id)
            conn.execute(query)
            conn.commit()

    @staticmethod
    def update_data_update_method(id: int, name: str):
        with session() as conn:
            query = update(Users).values(username=name).where(Users.id==id)
            conn.execute(query)
            conn.commit()

    @staticmethod
    def update_data_orm(id: int, name: str):
        with session() as conn:
            conn.refresh() #Обновить все данные из БД
            object = conn.get(Users, id)
            object.username = name
            conn.commit()
    @staticmethod
    def insert_data_orm(tablename: Callable, parametrs) -> None:
        ex = tablename(**parametrs)
        with session() as conn:
            conn.add(ex)
            conn.commit()
    @staticmethod
    def select_data_resume():
        """select r.worker_id, avg(r.salary)::int  from resumes r
                where r.salary > 200000 and r.title like '%Python%'
                group by r.worker_id """
        query = select(ResumeOrm.worker_id, cast(func.avg(ResumeOrm.salary), Integer).label('round_salary')).select_from(ResumeOrm).filter(and_(ResumeOrm.salary > 200000, ResumeOrm.title.contains("Python"))).group_by(ResumeOrm.worker_id).order_by(ResumeOrm.worker_id)
        with session() as conn:
            result = conn.execute(query)
            print(*result.first())
if __name__ == "__main__":
    # DB.sync_connect()
    # DB.create_tables()
    # DB.insert_data()
    # DB.select_data()
    # DB.update_data_update_method(1, 'Dima')
    # DB.update_data_orm(4, 'Dima')
    # DB.insert_data_orm(ResumeOrm, {"title":"Python developer", "salary":250000, "worker_id":1})
    DB.select_data_resume()