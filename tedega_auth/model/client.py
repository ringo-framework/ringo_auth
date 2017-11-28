import sqlalchemy as sa
from tedega_storage import RDBMSStorageBase as Base
from tedega_core.model.base import BaseItem
from tedega_core.model.mixins import Protocol


class Client(Protocol, BaseItem, Base):
    __tablename__ = 'clients'
    client_id = sa.Column(sa.String(40), nullable=False)
    client_secret = sa.Column(sa.String(55), nullable=False)
    name = sa.Column(sa.String())

    user_id = sa.Column(sa.ForeignKey('users.id'))
    user = sa.orm.relationship('User')

    _redirect_uris = sa.Column(sa.Text)
    _default_scopes = sa.Column(sa.Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []
