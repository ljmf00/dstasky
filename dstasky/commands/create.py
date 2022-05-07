from __future__ import annotations

import logging

from dstasky.commands.init import ensure_init_command
from dstasky.tasks import ObjectEntry

logger = logging.getLogger('dstasky')

def command_create() -> int:
    """
    Runs create command

    This command creates a task
    """

    if not ensure_init_command():
        return 1

    return 0
