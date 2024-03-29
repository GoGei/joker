# joker
## Simple site to get daily jokes

## Installation

## Local setup
clone repo: 
```bash
git clone https://github.com/GoGei/joker.git
```

add hosts to **/etc/hosts** file:
```
127.0.0.1           joker.local
127.0.0.1       api.joker.local
127.0.0.1     admin.joker.local
```

## Database setup
create DB
```sql
create user joker with password 'joker-psw' superuser createdb;
create database joker with owner joker;
```

## Env setup
create virtual env
```bash
python3.8 -m venv env
source env/bin/activate
pip install -r requirements.txt
./manage.py migrate
``` 

setup local settings
```bash
cp config/settings_example.py config/local_settings.py
```

# Useful commands
###run server
```bash
fab runserver
```

### deploy project
- branch (main by default)
- git checkout and pull from the branch
- install requirements.txt
- migrate database
- collect static
```bash
fab deploy_local
```

### scan code for PEP8
```bash
fab check
```

### create class diagram of the project to graphs/
```bash
fab create_graph_models
```
example
```bash
fab create_graph_models:Model1,Model2,Model3
```

# URLs
### Public pages
 http://joker.local:1131/
### API
 http://api.joker.local:1131/v1/
### Admin pages
 http://admin.joker.local:1131/
### Api documentation
http://api.joker.local:1131/swagger/
http://api.joker.local:1131/redoc/