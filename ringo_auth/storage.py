#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = None


def get_db():
    global db
    if db is None:
        db = SQLAlchemy()
    return db

db = get_db()
