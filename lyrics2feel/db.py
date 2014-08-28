from flask import current_app, g
from alembic.config import Config
from alembic.script import ScriptDirectory
from werkzeug.local import LocalProxy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


__all__ = ('Base', 'ensure_shutdown_session', 'get_engine', 'get_session',
           'get_alembic_config')


def get_alembic_config(engine):
    if engine is not None:
        url = str(engine.url)
        config = Config(current_app.config.get('CONFIG_ABSPATH', None))
        return config
    else:
        raise Exception('no engine founded. [alembic] sqlalchemy.url'
                        ' could be misconfigured.')


def ensure_shutdown_session(app):
    def remove_or_rollback(exc=None):
        if hasattr(g, 'sess'):
            if exc:
                g.sess.rollback()
            g.sess.close()

    app.teardown_appcontext(remove_or_rollback)


def get_engine(app=None):
    app = app if app else current_app
    url = app.config['alembic']['sqlalchemy.url']
    if url is None:
        return None
    return create_engine(url)


def get_session(engine=None):
    if engine is None:
        engine = get_engine()
    if not hasattr(g, 'sess'):
        setattr(g, 'sess', Session(bind=engine))
    return getattr(g, 'sess')


Base = declarative_base()
Session = sessionmaker()
session = LocalProxy(get_session)
