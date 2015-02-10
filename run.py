#!venv/bin/python
from app import app
from config import config

app.secret_key = config.get('main', 'secret_key')
app.run(host=config.get('main', 'bind_address'),
        port=int(config.get('main', 'bind_port')),
        debug=True)
