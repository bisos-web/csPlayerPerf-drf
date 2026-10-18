#!/bin/bash
#
# csPlayerPerf-manage.sh <manage.py arguments> --- server/manage.py as the service runs it:
# as csplayer, with /etc/default/csPlayerPerf, in the asc venv. Paths as in csPlayerPerfInfo.py.
#
#   csPlayerPerf-manage.sh showmigrations
#   csPlayerPerf-manage.sh superuserRead
#   csPlayerPerf-manage.sh register_library <name> <module> LibraryAPIImpl --description '...'
#
# CSPLAYERPERF_SUDO_ENV=VAR[,VAR] passes those variables through sudo (a password, kept off the
# command line that sudo logs).

exec sudo ${CSPLAYERPERF_SUDO_ENV:+--preserve-env=$CSPLAYERPERF_SUDO_ENV} -u csplayer bash -c '
set -a ; . /etc/default/csPlayerPerf ; set +a
cd /bisos/git/bxRepos/bisos-web/csPlayerPerf-drf/server
exec /bisos/venv/py3/asc/bin/python manage.py "$@"
' csPlayerPerf-manage "$@"
