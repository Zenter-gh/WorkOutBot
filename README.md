# Requirements
```
pip install MySQL-python telepot sqlalchemy schedule
```
# Setup
### Create MySql database:

```
CREATE DATABASE 'bot';
GRANT ALL PRIVILEGES ON bot.* TO bot@localhost IDENTIFIED BY 'bot';
flush privileges;
```

### Create config file:

```
cp config.py.sample config.py
```
Set token to yours one.
