"""csPlayerPerf's facts, read by every file in cbm/: the account, paths, port and environment.

csPlayerPerf is csPlayer's performer: webCliGui's Django REST API (server/), run by gunicorn in the
BISOS asc venv as the csplayer account, on 127.0.0.1 only. csPlayerUi.here (bisos-web/csPlayer-webUi)
proxies /api/, /admin/ and /static/ to it.

Not a package: the files beside it import it after putting this directory on sys.path.
"""

import os
import pathlib
import pwd
import secrets

from bisos.banna import sysAccts
from bisos.banna import tcpPorts

cbmDir = pathlib.Path(__file__).resolve().parent
# By the repo's stable path (/bisos/git/bxRepos/...), as units and leaves name it.
repoBase = pathlib.Path("/bisos/git/bxRepos/bisos-web/csPlayerPerf-drf")
serverDir = repoBase / "server"                  # manage.py, csPlayerPerf/ (the project), api/

acctName = "csplayer"
acct = sysAccts.sysAcctOf(acctName)

venv = pathlib.Path("/bisos/venv/py3/asc")       # where django-sbom.pcs and gunicorn-sbom.pcs install
python = venv / "bin" / "python"
gunicorn = venv / "bin" / "gunicorn"

listenIp = "127.0.0.1"
portNu = tcpPorts.tcpPortsAssignedList.tcpPortsList["csPlayerPerf"].portNu
devPortNu = tcpPorts.tcpPortsAssignedList.tcpPortsList["csPlayerPerf_dev"].portNu
uiFqdn = "csPlayerUi.here"                       # where users reach this API

stateDir = pathlib.Path(acct.homeDir)            # /bisos/var/csPlayerPerf, the account's home (755)
dataDir = stateDir / "data"                      # 750: the database holds password hashes and tokens
dbPath = dataDir / "db.sqlite3"
staticRoot = stateDir / "static"                 # collectstatic; nginx serves it (world-readable)
operationsDir = stateDir / "operationTasks"      # one folder per submitted operation

envFile = pathlib.Path("/etc/default/csPlayerPerf")

# The libraries operations come from, installed editable into the venv (webcligui_api first: csLib
# depends on it), and registered with the server by the assemble step.
gitCliGui = pathlib.Path("/bisos/git/bxRepos/cliGui")
editableLibs = [
    gitCliGui / "webCliGui" / "webcligui_api",
    gitCliGui / "csLib",
]
registeredLibs = [
    # (library_name, module_path, class_name, description)
    ("csLib", "csLib", "LibraryAPIImpl", "Command Services Library"),
]

# The Django superuser the assemble step creates when absent; its password is read from this
# file of the invoking user (the convention of server/djangoProc.spcs), generated when missing.
superuserPasswordFile = pathlib.Path("~/credentials/django/password")


def pwdUserName() -> str:
    """The invoking user's name: the superuser the assemble step creates."""
    return pwd.getpwuid(os.getuid()).pw_name


def envFileContent() -> str:
    """/etc/default/csPlayerPerf, written by the sbom only when absent (a fresh secret key each time)."""
    return f"""\
# csPlayerPerf (bisos-web/csPlayerPerf-drf): read by its unit and by cbm/csPlayerPerf-manage.sh.
# Written once by cbm/csPlayerPerf-sbom.pcs; edits survive re-runs.
DJANGO_SECRET_KEY={secrets.token_urlsafe(50)}
DEBUG_FLAG=False
CSPLAYER_ALLOWED_HOSTS={uiFqdn},{listenIp},localhost
CSPLAYER_CSRF_TRUSTED_ORIGINS=http://{uiFqdn}
CSPLAYER_DB_PATH={dbPath}
CSPLAYER_STATIC_ROOT={staticRoot}
CSPLAYER_OPERATIONS_DIR={operationsDir}
"""
