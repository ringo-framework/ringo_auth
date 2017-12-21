#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Public API of the user model"""
from tedega_view import config_view_endpoint
from tedega_storage.rdbms import get_storage
from tedega_storage.rdbms.crud import (
    search as _search,
    create as _create,
    read as _read,
    update as _update,
    delete as _delete
)
from tedega_auth.model.user import User


@config_view_endpoint(path="/users", method="GET", auth=None)
def search(limit=100, offset=0, search="", sort="", fields=""):
    """Loads all users.

    .. seealso:: Methods :func:`tedega_core.api.crud.search`

    :limit: Limit number of result to N entries.
    :offset: Return entries with an offset of N.
    :search: Return entries with an offset of N.
    :sort: Define sort and ordering.
    :fields: Only return defined fields.
    :returns: List of dictionary with values of the user

    >>> import tedega_core.api.user
    >>> users = tedega_core.api.user.search()
    >>> isinstance(users, list)
    True
    """
    if fields != "":
        fields = fields.split("|")
    else:
        fields = None
    with get_storage() as storage:
        users = _search(storage, User, limit, offset, search, sort)
        users = [user.get_values(fields) for user in users]
    return users


@config_view_endpoint(path="/users", method="POST", auth=None)
def create(name, password):
    """Creates a new user with the given `name` and `password`.

    .. seealso:: Methods :func:`tedega_core.api.crud.create`

    :name: Name of the new user
    :password: Password (unencrypted) of the new user
    :returns: Dictionary with values of the user

    >>> import tedega_core.api.user
    >>> user = tedega_core.api.user.create(name="foo1", password="bar")
    >>> user['name']
    'foo1'
    """
    with get_storage() as storage:
        user = _create(storage, User, dict(name=name, password=password))
        user = user.get_values()
    return user


@config_view_endpoint(path="/users/{item_id}", method="GET", auth=None)
def read(item_id):
    """Read (load) a existing user from the database.

    .. seealso:: Methods :func:`tedega_core.api.crud.read`

    :item_id: ID of the user to load.
    :returns: Dictionary with values of the user


    >>> import tedega_core.api.user
    >>> # First create a new user.
    >>> newuser = tedega_core.api.user.create(name="foo2", password="bar")
    >>> # Now load the user
    >>> loaduser = tedega_core.api.user.read(item_id = newuser.id)
    >>> loaduser['name']
    'foo2'
    """
    with get_storage() as storage:
        user = _read(storage, User, item_id)
        user = user.get_values()
    return user


@config_view_endpoint(path="/users/{item_id}", method="PUT", auth=None)
def update(item_id, values):
    """Update a user with the given values in the database.

    .. seealso:: Methods :func:`tedega_core.api.crud.update`

    :item_id: ID of the user to update
    :values: Dictionary of values
    :returns: Dictionary with values of the user

    >>> import tedega_core.api.user
    >>> # First create a new user.
    >>> newuser = tedega_core.api.user.create(name="foo3", password="bar")
    >>> # Now load the user
    >>> values = {"name": "baz"}
    >>> updateduser = tedega_core.api.user.update(item_id = newuser.id, values=values)
    >>> updateduser['name']
    'baz'
    """
    with get_storage() as storage:
        user = _update(storage, User, item_id, values)
        user = user.get_values()
    return user


@config_view_endpoint(path="/users/{item_id}", method="DELETE", auth=None)
def delete(item_id):
    """Deletes a user from the database.

    .. seealso:: Methods :func:`tedega_core.api.crud.delete`

    :item_id: ID of the user to update

    >>> import tedega_core.api.user
    >>> # First create a new user.
    >>> newuser = tedega_core.api.user.create(name="foo4", password="bar")
    >>> # Now delete the user
    >>> tedega_core.api.user.delete(item_id = newuser.id)
    >>> # Check that the user was actually deleted.
    >>> loaduser = tedega_core.api.user.read(item_id = newuser.id)
    Traceback (most recent call last):
        ...
    sqlalchemy.orm.exc.NoResultFound: No row was found for one()
    """
    with get_storage() as storage:
        return _delete(storage, User, item_id)


@config_view_endpoint(path="/users/{item_id}/password", method="POST", auth=None)
def reset_password(item_id, password=None):
    """Will reset the password of the user.

    .. seealso:: Methods :func:`tedega_core.model.user.reset_password`

    :item_id: ID of the user to update
    :password: Unencrypted password
    :returns: Unencrypted password

    >>> import tedega_core.api.user
    >>> # First create a new user.
    >>> newuser = tedega_core.api.user.create(name="foo5", password="bar")
    >>> oldpass = newuser.password
    >>> # Set custom password.
    >>> result = tedega_core.api.user.reset_password(item_id = newuser.id, password = "newpass")
    >>> result == "newpass"
    True
    >>> # Set random password.
    >>> result = tedega_core.api.user.reset_password(item_id = newuser.id)
    >>> result != "newpass"
    True
    """
    with get_storage() as storage:
        user = _read(storage, User, item_id)
        new_password = user.reset_password(password)
    return new_password
