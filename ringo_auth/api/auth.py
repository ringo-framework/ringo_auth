#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt
from ringo_service import config_service_endpoint, AuthError
from ringo_storage import get_storage
from ringo_core.lib.security import verify_password, generate_password
from ringo_auth.model.user import User
from ringo_auth.model.client import Client


@config_service_endpoint(path="/login", method="POST")
def login(values):
    client_id = values["client_id"]
    client_secret = values["client_secret"]

    with get_storage() as storage:
        try:
            query = storage.session.query(Client)
            query = query.filter(Client.client_id == client_id,
                                 Client.client_secret == client_secret)
            query.one()
        except:
            raise AuthError("Client can not be authenticated")

    encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
    return encoded


@config_service_endpoint(path="/clients", method="POST")
def add_client(values):
    """Registers a new client. To register a new client the request must
    be autheticated by providing the username and password of the
    existing user.
    The function will return a dictionary with the client_id and
    client_secret which will than be used to request authorization for a
    certain service endpoint."""
    username = values["username"]
    password = values["password"]

    with get_storage() as storage:
        try:
            user = storage.session.query(User).filter(User.name == username).one()
            if verify_password(password, user.password):
                user_id = user.id
            else:
                raise AuthError("User can not be authorized.")
        except:
            raise AuthError("User can not be authorized.")

    client = Client()
    client.name = values['name']
    client.client_id = generate_password(40)
    client.client_secret = generate_password(50)
    client._redirect_uris = None  # values['redirect_uris']
    client._default_scopes = None  # values['scopes']
    client.user_id = user_id

    with get_storage() as storage:
        storage.create(client)
        client_id = client.client_id
        client_secret = client.client_secret

    return dict(client_id=client_id, client_secret=client_secret)
