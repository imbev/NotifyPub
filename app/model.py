from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Text
from sqlalchemy.sql import func

meta = MetaData()

messages = Table(
    'messages', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('summary', Text),
    Column('content', Text),
    Column('time_created', DateTime(timezone=True), server_default=func.now())
)

tokens = Table(
    'tokens', meta,
    Column('id', Integer, primary_key=True),
    Column('description', String),
    Column('token', String)
)