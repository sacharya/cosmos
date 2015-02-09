#!venv/bin/python
from app import app
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.run(host='0.0.0.0', port=80, debug=True)
