from __future__ import annotations

import os
import sys
import argparse

from typing import Sequence

from dstasky.commands.show import command_show
from dstasky.commands.create import command_create
from dstasky.commands.init import command_init
from dstasky.logging import logging_handler
from dstasky.utils import use_color
from dstasky.utils import COLOR_CHOICES


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
            prog='dstasky',
            description='A simple task manager'
        )

    parser.add_argument(
            '--color', default='auto',
            type=use_color,
            metavar='{' + ','.join(COLOR_CHOICES) + '}',
            help='Use colored output.  Defaults to `%(default)s`.',
        )

    subparsers = parser.add_subparsers(
            title='subcommands',
            dest='command'
        )

    parser_init = subparsers.add_parser('init', help='init tasks repository')  # noqa: F841,E501
    parser_show = subparsers.add_parser('show', help='show tasks')  # noqa: F841,E501
    parser_create = subparsers.add_parser('create', help='create a dstasky object')  # noqa: F841,E501

    parser_help = subparsers.add_parser(
            'help',
            help='show help for a specific subcommand'
        )
    parser_help.add_argument(
            'help_cmd',
            nargs='?',
            help='Command to show help'
        )

    # Default to show subcommand
    if len(argv) == 0:
        argv = ['show']

    args = parser.parse_args(argv)

    with logging_handler(args.color):
        if args.command == 'help':
            # help for a specific command
            if args.help_cmd:
                parser.parse_args([args.help_cmd, '--help'])
            # defaults to normal help
            else:
                parser.parse_args(['--help'])

            return 0

        if args.command == 'show':
            return command_show()
        if args.command == 'init':
            return command_init()
        if args.command == 'create':
            return command_create()
