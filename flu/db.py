# coding=utf-8

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import create_engine

from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker

from flask import app

@as_declarative()
class Base(object):
    __json__ = []

    def to_dict(self, fields=None):
        if fields is None:
            fields = self.__json__
        d = {}
        for field in fields:
            value = self.__getattribute__(field)
            if isinstance(value, datetime):
                d[field] = value.isoformat() + 'Z'
            else:
                d[field] = value
            if isinstance(value, uuid.UUID):
                d[field] = str(value)
        return d

class Database(object):

    def __init__(self):
        self._engine = None

    def create_all(self):
        Base.metadata.create_all(self._engine)

    def create_session(self):
        return scoped_session(sessionmaker(bind = self._engine, autocommit=True, autoflush=False))

    def start_engine(self, dsn, **kwargs):
        if app.get_debug_flag():
            if 'echo' not in kwargs:
                kwargs['echo'] = True
        self._engine = create_engine(dsn, **kwargs)

_db = Database()

create_all = _db.create_all
create_session = _db.create_session
start_engine = _db.start_engine

