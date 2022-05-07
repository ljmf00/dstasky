from __future__ import annotations

import os
import logging

from dstasky.utils import get_data_directory

from pygit2 import discover_repository
from pygit2 import init_repository

logger = logging.getLogger('dstasky')


def is_initialized() -> bool:
    """
    Checks if the data dir is initialized

    Returns true if init is already done, false otherwise.
    """

    data_dir = get_data_directory()

    # data dir doesn't even exist
    if not os.path.isdir(data_dir):
        return False

    # contains a .git folder
    git_data_dir = os.path.join(data_dir, '.git')
    if not os.path.isdir(git_data_dir):
        return False

    # is it actually a repository
    if not discover_repository(git_data_dir):
        return False

    return True

def _ensure_init_folders() -> None:
    """
    Ensure initial folders are created
    """

    data_dir = get_data_directory()
    dirs = [
        "objects",  # All objects/entries
        "namespaces",  # Namespaces subfolder
    ]

    for entry in dirs:
        entry_dir = os.path.join(data_dir, entry)
        if not os.path.exists(entry_dir):
            os.mkdir(entry_dir)



def ensure_init_command() -> bool:
    """
    Ensure if init command was ran
    """

    if not is_initialized():
        logger.error('Please run/rerun \'dstasky init\' first!')
        return False

    _ensure_init_folders()

    return True


def command_init() -> int:
    if is_initialized():
        logger.info('dstasky is already initialized!')
        return 0

    data_dir = get_data_directory()

    # data dir doesn't even exist
    if not os.path.isdir(data_dir):
        logger.info(f'Creating \'{data_dir}\'')
        os.mkdir(data_dir)

    git_data_dir = os.path.join(data_dir, '.git')
    if not discover_repository(git_data_dir):
        logger.info(f'Initializing an empty git repo at \'{data_dir}\'')
        init_repository(data_dir)

    _ensure_init_folders()

    logger.info('Done')
    return 0
