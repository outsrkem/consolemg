#!/bin/bash
SHHOME=$(cd `dirname $0`; pwd)
cd ${SHHOME}

export DB_USERNAME="blognote"
export DB_PASSWORD="123456"
export DB_HOSTIP="10.10.10.24"
export DB_PORT="3306"
export DB_DATABASE="blognote"

python3 -m venv myvenv
. myvenv/bin/activate
pip install --upgrade pip
pip install -r static/requirements.txt

# 启动flask
gunicorn -c gunicorn_config.py main:app
