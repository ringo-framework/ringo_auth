#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import session
from flask_oauthlib.provider import OAuth2Provider as BaseOAuth2Provider

from ringo_auth.storage import db
from ringo_auth.model.client import Client
from ringo_auth.model.token import Grant, Token
from ringo_auth.model.user import User


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


class OAuth2Provider(BaseOAuth2Provider):

    def _clientgetter(self, client_id):
        return Client.query.filter_by(client_id=client_id).first()

    def _grantgetter(self, client_id, code):
        return Grant.query.filter_by(client_id=client_id, code=code).first()

    def _grantsetter(self, client_id, code, request, *args, **kwargs):
        # decide the expires time yourself
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            _scopes=' '.join(request.scopes),
            user=current_user(),
            expires=expires
        )
        db.session.add(grant)
        db.session.commit()
        return grant

    def _tokengetter(self, access_token=None, refresh_token=None):
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()

    def _tokensetter(self, token, request, *args, **kwargs):
        toks = Token.query.filter_by(
            client_id=request.client.client_id,
            user_id=request.user.id
        )
        # make sure that every client has only one token connected to a user
        for t in toks:
            db.session.delete(t)

        expires_in = token.pop('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        tok = Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            _scopes=token['scope'],
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user.id,
        )
        db.session.add(tok)
        db.session.commit()
        return tok

oauth = OAuth2Provider()
