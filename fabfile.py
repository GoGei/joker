import os
import random
from datetime import datetime

from fabric.api import local, lcd, cd
from fabric.contrib import django
from fabric.decorators import task

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/'

django.project('joker')
django.settings_module('config.local_settings')
from config import local_settings as dj_settings


def _launch_django(project_path):
    port = dj_settings.HOST_PORT
    if not port:
        summ = sum([ord(char) for char in project_path.split('/')[-2]])
        random.seed(summ)
        port = random.randrange(1024, 5000)

    server_address = '127.0.0.1'
    if os.path.exists('/etc/hosts'):
        with open('/etc/hosts') as f:
            if f.read().find(dj_settings.SITE_URL) != -1:
                server_address = dj_settings.SITE_URL

    with lcd(project_path):
        insecure = not dj_settings.DEBUG and dj_settings.INSECURE
        local(f'./manage.py runserver {server_address}:{port} {"--insecure" if insecure else ""}', capture=False)


@task
def runserver():
    _launch_django(PROJECT_ROOT)


@task
def dump_db(user='postgres'):
    db_name = dj_settings.DATABASES['default']['NAME']

    date = datetime.now().strftime("%Y-%m-%d_%H%M")
    dump_name = f'dumps/{db_name}_{date}.sql'

    with cd(PROJECT_ROOT):
        local('mkdir -p dumps')
        local(f'sudo -u {user} pg_dump {db_name} > {dump_name} | bzip2 -9 > {dump_name}.bz2')


@task
def restore_db():
    db_user = dj_settings.DATABASES['default']['USER']
    db_name = dj_settings.DATABASES['default']['NAME']

    with cd(PROJECT_ROOT):
        with lcd('dumps'):
            last_dump = 'dumps/' + local('ls -1tr', capture=True).stdout.strip().split('\n')[-1]
        local(f'sudo psql -U {db_user} -d {db_name} < {last_dump}')


@task
def deploy_local(branch=None):
    branch = branch or 'main'

    local('git checkout %s && git pull' % branch)
    local('pip3 install -r requirements.txt')
    local('./manage.py migrate')
    local('./manage.py collectstatic --noinput')


@task
def check():
    local('python manage.py test')
    local('python manage.py check')
    # local('time flake8 ./core ./Api ./Admin')
    local('time flake8 ./core ./Admin')


@task
def create_graph_models(*args):
    date = datetime.now().strftime("%Y-%m-%d_%H%M")
    dot_file_name = f'graphs/project_{date}.dot'

    models = ''
    if args:
        models = f' -I {",".join(args)} '

    with cd(PROJECT_ROOT):
        local('mkdir -p graphs')
        local(f'./manage.py graph_models -a {models} -o {dot_file_name}')
