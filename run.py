#!venv/bin/python
from app import app
from config import config

app.secret_key = config.get('secret_key')
app.run(host=config.get('bind_address'),
        port=int(config.get('bind_port')),
        debug=True)
