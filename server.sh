#!/bin/bash
DDIR=${2:-$(readlink -e ${BASH_SOURCE[0]%/*})}
echo ${DDIR}
cd ${DDIR} >/dev/null 2>&1

. venv/bin/activate
exec /usr/bin/gunicorn3 --name=hackspace-events --bind unix:/run/hspacegunicorn.socket "api:app" 
