from typing import Optional

from sqlalchemy.orm import session, sessionmaker, declarative_base, as_declarative, Mapped, MappedColumn, declared_attr, \
    Session, relationship
from sqlalchemy import create_engine, Column, Integer, ForeignKey, select, or_, desc, update, bindparam, inspect
from config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)

@as_declarative()
class AbsractModel:
    id: Mapped[int] = MappedColumn(primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class UserModel(AbsractModel):
    __tablename__ = 'user'
    name: Mapped[str]
    fullname: Mapped[str]

    address: Mapped["AddressModel"] = relationship(back_populates="user", uselist=False)


class AddressModel(AbsractModel):
    __tablename__ = 'address'
    email: Mapped[Optional[str]]
    user: Mapped["UserModel"] = relationship(back_populates="address", uselist=False)
    user_id: Mapped[int] = MappedColumn(ForeignKey(UserModel.id, ondelete='CASCADE'))

session = sessionmaker(engine)


def main():
    with (session() as conn):
        AbsractModel.metadata.create_all(engine)
        user = UserModel(name='Jack', fullname='Vorobey')
        inserted = conn.add(user)
        conn.commit()
        query_first = conn.query(UserModel).first()
        print(query_first.name)
        query_with_where = conn.query(UserModel).where(or_(
            UserModel.name.startswith("Jac"),
            UserModel.fullname.contains("b"),
            UserModel.id.in_([1, 2, 3])
        )).order_by(desc(UserModel.id)).first()
        print(query_with_where.id, query_with_where.name, query_with_where.fullname)
        query_update = update(UserModel).where(UserModel.name.startswith('J')).values(name='Jacks')
        print(conn.execute(query_update).mappings())
        conn.commit()
        query_all = conn.query(UserModel).first().name
        print(query_all)
        AbsractModel.metadata.drop_all(engine)

def unit_of_work():
    """
    Состояние объекта
    Transient -> Временный
    Pending -> Ожидающий
    Persistent -> Персистентный
    Deleted -> Удаленный
    Detached -> Отсоединенный
    """
    with session() as conn:
        user = UserModel(name='Test1', fullname='testov')
        insp = inspect(user)
        print(f'Is it transient -> {insp.transient}')
        conn.add(user)
        print(f'Is it Pending -> {insp.pending}')
        conn.flush()
        print(f'Is it Persistent -> {insp.persistent}')
        conn.delete(user)
        print(f'Is it Deleted -> {insp.deleted}')
        conn.flush()
        print(f'Is it Deleted -> {insp.deleted}')





if __name__ == '__main__':
    # main()
    unit_of_work()