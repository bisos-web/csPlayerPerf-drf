import os
from pathlib import Path

# Where each submitted operation gets its folder. Shared with the libraries that run operations
# (csLib reads the same variable). Under systemd it comes from /etc/default/csPlayerPerf.
OPERATION_ROOT_DIRECTORY = Path(
    os.getenv('CSPLAYER_OPERATIONS_DIR', '/bisos/var/csPlayerPerf/operationTasks')
).resolve()
