from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so


class Base(so.DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = 'persons'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement = True)
    first_name: so.Mapped[Optional[str]]
    last_name: so.Mapped[str]
    def __repr__(self) -> str:
        return f"Person(first_name='{self.first_name}', last_name='{self.last_name}')>"

    def greeting(self) -> None:
        print(f'{self.first_name} says "hello"!')