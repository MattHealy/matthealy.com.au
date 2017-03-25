#!/usr/bin/env python
import os
import subprocess
import sys

from app import create_app
from flask_script import Manager, Shell
from flask_flatpages import FlatPages
from flask_frozen import Freezer

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

pages = FlatPages(app)

freezer = Freezer(app)


def make_shell_context():
    return dict(app=app, pages=pages)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def freeze():
    """Freeze the site to a set of static HTML files."""
    app.config['DEBUG'] = False
    freezer.freeze()


@manager.command
def lint():
    """Runs the code linter"""
    lint = subprocess.call(['flake8', '--ignore=E402']) == 0
    if lint:
        print('OK')
    sys.exit(lint)


if __name__ == '__main__':
    manager.run()
