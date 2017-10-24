import sqlalchemy as sa
from ringo_storage import RDBMSStorageBase as Base
from ringo_core.model.base import BaseItem
from ringo_core.model.mixins import Protocol


class Grant(Protocol, BaseItem, Base):
    __tablename__ = 'grants'

    user_id = sa.Column(
        sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')
    )
    user = sa.orm.relationship('User')

    client_id = sa.Column(
        sa.String(40), sa.ForeignKey('clients.client_id'),
        nullable=False,
    )
    client = sa.orm.relationship('Client')

    code = sa.Column(sa.String(255), index=True, nullable=False)

    redirect_uri = sa.Column(sa.String(255))
    expires = sa.Column(sa.DateTime)

    _scopes = sa.Column(sa.Text)

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
    #     return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(Protocol, BaseItem, Base):
    __tablename__ = 'tokens'
    client_id = sa.Column(
        sa.String(40), sa.ForeignKey('clients.client_id'),
        nullable=False,
    )
    client = sa.orm.relationship('Client')

    user_id = sa.Column(
        sa.Integer, sa.ForeignKey('users.id')
    )
    user = sa.orm.relationship('User')

    # currently only bearer is supported
    token_type = sa.Column(sa.String(40))

    access_token = sa.Column(sa.String(255), unique=True)
    refresh_token = sa.Column(sa.String(255), unique=True)
    expires = sa.Column(sa.DateTime)
    _scopes = sa.Column(sa.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
