#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_model
----------------------------------

Tests for `tedega_auth.model.user` module.
"""

import pytest


def test_not_found():
    from tedega_view.exceptions import NotFound
    import tedega_auth.api.user
    with pytest.raises(NotFound):
        tedega_auth.api.user.read(9999)


def test_search(randomstring):
    import tedega_auth.api.user
    name = randomstring(8)
    tedega_auth.api.user.create(name=name, password="password")
    users = tedega_auth.api.user.search()
    assert isinstance(users, list)
    assert len(users) > 0


def test_search_filters(randomstring):
    import tedega_auth.api.user
    from tedega_view.exceptions import ClientError
    name = randomstring(8)
    tedega_auth.api.user.create(name=name, password="password")

    offset = 0
    limit = 10
    search = "id::1|name::test"
    sort = "id|-name"
    fields = "id|name"
    users = tedega_auth.api.user.search(offset=offset, limit=limit,
                                       search=search, sort=sort,
                                       fields=fields)

    with pytest.raises(ClientError):
        search = "id:1|name::test"
        users = tedega_auth.api.user.search(offset=offset, limit=limit,
                                           search=search, sort=sort,
                                           fields=fields)
    with pytest.raises(ClientError):
        search = "id::1|xxx::test"
        users = tedega_auth.api.user.search(offset=offset, limit=limit,
                                           search=search, sort=sort,
                                           fields=fields)

    with pytest.raises(ClientError):
        search = "id::1|name::test"
        sort = "id,updated"
        users = tedega_auth.api.user.search(offset=offset, limit=limit,
                                           search=search, sort=sort,
                                           fields=fields)

    assert isinstance(users, list)
    assert len(users) == 0


def test_create(randomstring):
    import tedega_auth.api.user
    name = randomstring(8)
    user = tedega_auth.api.user.create(name=name, password="password")
    assert user['name'] == name


def test_create_unique_name(randomstring):
    import sqlalchemy as sa
    import tedega_auth.api.user
    name = randomstring(8)
    user = tedega_auth.api.user.create(name=name, password="password")
    assert user['name'] == name
    with pytest.raises(sa.exc.IntegrityError):
        user = tedega_auth.api.user.create(name=name, password="password")


def test_read(randomstring):
    import tedega_auth.api.user
    name = randomstring(8)
    user = tedega_auth.api.user.create(name=name, password="password")
    loaded = tedega_auth.api.user.read(user['id'])
    assert loaded['name'] == name


def test_update(randomstring):
    from tedega_view.exceptions import NotFound
    import tedega_auth.api.user
    name = randomstring(8)
    user = tedega_auth.api.user.create(name=name, password="password")
    values = {"name": "updated"}
    updated = tedega_auth.api.user.update(user['id'], values)
    assert updated['name'] == "updated"
    assert updated['updated'] != user['updated']

    with pytest.raises(NotFound):
        updated = tedega_auth.api.user.update(9999, values)


def test_delete(randomstring):
    from tedega_view.exceptions import NotFound
    import tedega_auth.api.user
    name = randomstring(8)
    user = tedega_auth.api.user.create(name=name, password="password")
    tedega_auth.api.user.delete(user['id'])
    with pytest.raises(NotFound):
        user = tedega_auth.api.user.delete(user['id'])


def test_reset_password(randomstring):
    import tedega_auth.api.user
    password = randomstring(8)
    name = randomstring(8)
    user = tedega_auth.api.user.create(name=name, password="password")
    result = tedega_auth.api.user.reset_password(user['id'], password)
    assert result == password
    result = tedega_auth.api.user.reset_password(user['id'])
    assert result != password
