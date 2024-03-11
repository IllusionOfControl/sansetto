#!/bin/bash

python -m flask -A app.man:app db upgrade
gunicorn -c gunicorn_config.py app.main:app