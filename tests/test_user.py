#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_model
----------------------------------

Tests for `ringo_auth.model.user` module.
"""

import pytest


def test_not_found():
    from ringo_service.exceptions import NotFound
    import ringo_auth.api.user
    with pytest.raises(NotFound):
        ringo_auth.api.user.read(9999)


def test_search(randomstring):
    import ringo_auth.api.user
    name = randomstring(8)
    ringo_auth.api.user.create(name=name, password="password")
    users = ringo_auth.api.user.search()
    assert isinstance(users, list)
    assert len(users) > 0


def test_search_filters(randomstring):
    import ringo_auth.api.user
    from ringo_service.exceptions import ClientError
    name = randomstring(8)
    ringo_auth.api.user.create(name=name, password="password")

    offset = 0
    limit = 10
    search = "id::1|name::test"
    sort = "id|-name"
    fields = "id|name"
    users = ringo_auth.api.user.search(offset=offset, limit=limit,
                                       search=search, sort=sort,
                                       fields=fields)

    with pytest.raises(ClientError):
        search = "id:1|name::test"
        users = ringo_auth.api.user.search(offset=offset, limit=limit,
                                           search=search, sort=sort,
                                           fields=fields)
    with pytest.raises(ClientError):
        search = "id::1|xxx::test"
        users = ringo_auth.api.user.search(offset=offset, limit=limit,
                                           search=search, sort=sort,
                                           fields=fields)

    with pytest.raises(ClientError):
        search = "id::1|name::test"
        sort = "id,updated"
        users = ringo_auth.api.user.search(offset=offset, limit=limit,
                                           search=search, sort=sort,
                                           fields=fields)

    assert isinstance(users, list)
    assert len(users) == 0


def test_create(randomstring):
    import ringo_auth.api.user
    name = randomstring(8)
    user = ringo_auth.api.user.create(name=name, password="password")
    assert user['name'] == name


def test_create_unique_name(randomstring):
    import sqlalchemy as sa
    import ringo_auth.api.user
    name = randomstring(8)
    user = ringo_auth.api.user.create(name=name, password="password")
    assert user['name'] == name
    with pytest.raises(sa.exc.IntegrityError):
        user = ringo_auth.api.user.create(name=name, password="password")


def test_read(randomstring):
    import ringo_auth.api.user
    name = randomstring(8)
    user = ringo_auth.api.user.create(name=name, password="password")
    loaded = ringo_auth.api.user.read(user['id'])
    assert loaded['name'] == name


def test_update(randomstring):
    from ringo_service.exceptions import NotFound
    import ringo_auth.api.user
    name = randomstring(8)
    user = ringo_auth.api.user.create(name=name, password="password")
    values = {"name": "updated"}
    updated = ringo_auth.api.user.update(user['id'], values)
    assert updated['name'] == "updated"
    assert updated['updated'] != user['updated']

    with pytest.raises(NotFound):
        updated = ringo_auth.api.user.update(9999, values)


def test_delete(randomstring):
    from ringo_service.exceptions import NotFound
    import ringo_auth.api.user
    name = randomstring(8)
    user = ringo_auth.api.user.create(name=name, password="password")
    ringo_auth.api.user.delete(user['id'])
    with pytest.raises(NotFound):
        user = ringo_auth.api.user.delete(user['id'])


def test_reset_password(randomstring):
    import ringo_auth.api.user
    password = randomstring(8)
    name = randomstring(8)
    user = ringo_auth.api.user.create(name=name, password="password")
    result = ringo_auth.api.user.reset_password(user['id'], password)
    assert result == password
    result = ringo_auth.api.user.reset_password(user['id'])
    assert result != password
