from __future__ import unicode_literals, print_function

import os
import random
from datetime import datetime

from fabric import task
from django.conf import settings as dj_settings
from invocations.console import confirm

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.local_settings')
VIRTUAL_ENV = os.environ.get('VIRTUAL_ENV') or os.path.join(PROJECT_ROOT, 'env')
VIRTUAL_ENV_ACTIVATE = '. %s' % os.path.join(VIRTUAL_ENV, 'bin/activate')


@task
def runserver(c):
    port = dj_settings.HOST_PORT
    if not port:
        summ = sum([ord(char) for char in PROJECT_ROOT.split('/')[-1]])
        random.seed(summ)
        port = random.randrange(1024, 5000)

    server_address = '127.0.0.1'
    if os.path.exists('/etc/hosts'):
        with open('/etc/hosts') as f:
            host_name = dj_settings.SITE_URL
            if f.read().find(host_name) != -1:
                server_address = host_name

    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            c.run('./manage.py runserver %s:%s' % (server_address, str(port)), pty=True)


@task
def celeryd(c):
    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            c.run('celery -A celery_runner worker -l DEBUG -c 8 -Q celery', pty=True)


@task
def celerybeat(c):
    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            c.run('celery -A celery_runner beat', pty=True)


@task
def deploy_local(c, branch=None):
    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        if not branch:
            branch_name = 'main'
        else:
            branch_name = branch

        if not confirm(
                "Are you sure? It will make changes on the remote system and deploy branch: %s" % branch_name):
            c.abort("Ok, aborting launch...")

        c.run('git checkout %s && git pull' % branch_name)
        c.run('pip install -r requirements.txt')
        c.run('./manage.py migrate')
        c.run('./manage.py collectstatic --noinput')


@task
def check(c):
    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        c.run('python manage.py check')
        c.run('time flake8 ./core ./Api ./Admin')


@task
def create_graph_models(c, *args):
    date = datetime.now().strftime("%Y-%m-%d_%H%M")
    dot_file_name = f'graphs/project_{date}.dot'

    models = ''
    if args:
        models = f' -I {",".join(args)} '

    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            c.run('mkdir -p graphs')
            c.run(f'./manage.py graph_models -a {models} -o {dot_file_name}')
