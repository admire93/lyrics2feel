# -*- coding: utf-8 -*-
import os

from configparser import ConfigParser
from logging.config import fileConfig

from flask import current_app
from flask.ext.script import Manager, prompt_bool
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.command import downgrade as alembic_downgrade
from alembic.command import history as alembic_history
from alembic.command import branches as alembic_branch
from alembic.command import current as alembic_current

from lyrics2feel.db import get_alembic_config, get_engine, Base
from lyrics2feel.web.app import app

__all__ = 'manager', 'run'


def read_from_ini(app):
    config = ConfigParser()
    config.optionxform = str
    config.read(app.config.get('CONFIG_ABSPATH'))
    assert 'flask' in config, '[flask] section must be required.'
    app_config = config['flask']
    for k, v in app_config.items():
        app.config[k] = v
    assert 'alembic' in config, '[alembic] section must be required.'
    app.config['alembic'] = {}
    for k, v in config['alembic'].items():
        app.config['alembic'][k] = v


@Manager
def manager(config):
    if config is None:
        config = 'dev.ini'
    config = os.path.abspath(config)
    app.config['CONFIG_ABSPATH'] = config
    read_from_ini(app)
    return app


@manager.option('--message', '-m', dest='message', default=None)
def revision(message):
    """Add a revision"""
    fileConfig(current_app.config.get('CONFIG_ABSPATH'))
    engine = get_engine()
    config = get_alembic_config(engine)
    m = "--autogenerate"
    alembic_revision(config,
                     message=message,
                     autogenerate=prompt_bool(m, default=True))


@manager.option('--revision', '-r', dest='revision', default='head')
def upgrade(revision):
    """Upgrade a revision to --revision or newest revision"""
    fileConfig(current_app.config.get('CONFIG_ABSPATH'))
    engine = get_engine()
    config = get_alembic_config(engine)
    alembic_upgrade(config, revision)


@manager.option('--revision', '-r', dest='revision')
def downgrade(revision):
    """Downgrade a revision to --revision"""
    fileConfig(current_app.config.get('CONFIG_ABSPATH'))
    engine = get_engine()
    config = get_alembic_config(engine)
    alembic_downgrade(config, revision)


@manager.command
def history():
    """List of revision history."""
    fileConfig(current_app.config.get('CONFIG_ABSPATH'))
    engine = get_engine()
    config = get_alembic_config(engine)
    return alembic_history(config)


@manager.command
def branches():
    """Show current un-spliced branch point."""
    fileConfig(current_app.config.get('CONFIG_ABSPATH'))
    engine = get_engine()
    config = get_alembic_config(engine)
    return alembic_branch(config)


@manager.command
def current():
    """Current revision."""
    fileConfig(current_app.config.get('CONFIG_ABSPATH'))
    engine = get_engine()
    config = get_alembic_config(engine)
    return alembic_current(config)


manager.add_option('--config', '-c', dest='config')

main = manager.run