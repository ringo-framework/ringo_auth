#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from tedega_core.lib.security import generate_password
from tedega_storage import init_storage, get_storage

# Initialise a SQLite Database for doctests. Doctests can not use the
# fixtures and contexts of py.test. So default sqlite db in memory is
# not present at the time the doctests are executed. As a workaround we
# create a temporary sqlite database on "make doctests". This call
# initialises this database.
init_storage()


@pytest.fixture(scope='session')
def dbmodel(request):
    init_storage()


@pytest.fixture()
def storage(request, dbmodel):
    return get_storage()


@pytest.fixture()
def randomstring(request):
    return generate_password
