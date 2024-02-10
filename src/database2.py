from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)
metadata = MetaData()
class DB:
    """
    class to work database
    """
    @staticmethod
    def select() -> None:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            print(result.scalar())
    @staticmethod
    def create_table():
        user_table = Table(
            "user",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(30))
        )
        print(user_table.c.keys())
        addresses = Table(
            "address",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", Integer, ForeignKey("user.id")),
            Column("district", String(20))
        )
        metadata.create_all(engine)
        metadata.drop_all(engine)

if __name__ == "__main__":
    DB.select()
    DB.create_table()



