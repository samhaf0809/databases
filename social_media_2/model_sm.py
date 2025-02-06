from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import ForeignKey

class Base(so.DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    username: so.Mapped[str]


likes = sa.Table("likes",
                 Base.metadata,
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
                 sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id')),
                 )


class Post(Base):
    __tablename__ = 'posts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'))
    post: so.Mapped[str]
