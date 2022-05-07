from __future__ import annotations

import logging

from dstasky.commands.init import ensure_init_command
from dstasky.tasks import ObjectEntry

logger = logging.getLogger('dstasky')

def command_show() -> int:
    """
    Runs command 'show'
    """

    if not ensure_init_command():
        return 1

    print(ObjectEntry.create_task(title='test').to_dict())
    return 0
