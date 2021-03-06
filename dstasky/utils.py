from __future__ import annotations

import os
import sys

def get_data_directory() -> str:
    """
    Get default dstasky data directory

    Note: If DSTASKY_HOME or XDG variable is not set, defaults to
    '~/.loca/share/dstasky'.
    """

    data_dir = os.environ.get('XDG_DATA_HOME') or \
        os.path.expanduser('~/.local/share')
    ret = os.environ.get('DSTASKY_HOME') or os.path.join(data_dir, 'dstasky')
    return os.path.realpath(ret)


if sys.platform == 'win32':  # pragma: no cover (windows)
    def _enable() -> None:
        from ctypes import POINTER
        from ctypes import windll
        from ctypes import WinError
        from ctypes import WINFUNCTYPE
        from ctypes.wintypes import BOOL
        from ctypes.wintypes import DWORD
        from ctypes.wintypes import HANDLE
        from typing import Any

        STD_ERROR_HANDLE = -12
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 4

        def bool_errcheck(result: Any, func: Any, args: Any) -> Any:
            if not result:
                raise WinError()
            return args

        GetStdHandle = WINFUNCTYPE(HANDLE, DWORD)(
            ('GetStdHandle', windll.kernel32), ((1, 'nStdHandle'),),
        )

        GetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, POINTER(DWORD))(
            ('GetConsoleMode', windll.kernel32),
            ((1, 'hConsoleHandle'), (2, 'lpMode')),
        )
        GetConsoleMode.errcheck = (  # type: ignore[assignment, misc]
            bool_errcheck  # type: ignore[assignment]
        )

        SetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, DWORD)(
            ('SetConsoleMode', windll.kernel32),
            ((1, 'hConsoleHandle'), (1, 'dwMode')),
        )
        SetConsoleMode.errcheck = (  # type: ignore[assignment, misc]
            bool_errcheck  # type: ignore[assignment]
        )

        # As of Windows 10, the Windows console supports (some) ANSI escape
        # sequences, but it needs to be enabled using `SetConsoleMode` first.
        #
        # More info on the escape sequences supported:
        # https://msdn.microsoft.com/en-us/library/windows/desktop/mt638032(v=vs.85).aspx
        stderr = GetStdHandle(STD_ERROR_HANDLE)
        flags = GetConsoleMode(stderr)
        SetConsoleMode(stderr, flags | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

    try:
        _enable()
    except OSError:
        terminal_supports_color = False
    else:
        terminal_supports_color = True
else:  # pragma: win32 no cover
    terminal_supports_color = True

COLOR_NORMAL = '\033[m'
COLOR_RED_BG = '\033[41m'
COLOR_GREEN_BG = '\033[42m'
COLOR_YELLOW_BG = '\033[43m'
COLOR_CYAN_BG = '\033[46m'


def format_color(text: str, color: str, use_color_setting: bool) -> str:
    """Format text with color.
    Args:
        text - Text to be formatted with color if `use_color`
        color - The color start string
        use_color_setting - Whether or not to color
    """
    if use_color_setting:
        return f'{color}{text}{COLOR_NORMAL}'
    else:
        return text


COLOR_CHOICES = ('auto', 'always', 'never')


def use_color(setting: str) -> bool:
    """Choose whether to use color based on the command argument.
    Args:
        setting - Either `auto`, `always`, or `never`
    """
    if setting not in COLOR_CHOICES:
        raise ValueError(setting)

    return (
        setting == 'always' or (
            setting == 'auto' and
            sys.stderr.isatty() and
            terminal_supports_color and
            os.getenv('TERM') != 'dumb'
        )
    )


def find_file(name: str, path: str) -> bool:
    for root, dirs, files in os.walk(path):
        if name in files:
            return True

    return False
