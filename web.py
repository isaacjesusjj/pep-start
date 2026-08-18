"""Inicia a versão web do PEP Start.

Execute com:
    python web.py

Depois acesse:
    http://127.0.0.1:8000
"""

import uvicorn

from web_app import create_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
