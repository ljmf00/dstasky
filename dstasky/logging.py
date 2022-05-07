from __future__ import annotations

import contextlib
import logging
import sys

from typing import Generator
from typing import Any
from typing import IO

from dstasky import utils

logger = logging.getLogger('dstasky')


def _write(s: str, stream: IO[bytes] = sys.stdout.buffer) -> None:
    stream.write(s.encode())
    stream.flush()


def _write_line_b(
        s: bytes | None = None,
        stream: IO[bytes] = sys.stdout.buffer,
        logfile_name: str | None = None,
) -> None:
    with contextlib.ExitStack() as exit_stack:
        output_streams = [stream]
        if logfile_name:
            stream = exit_stack.enter_context(open(logfile_name, 'ab'))
            output_streams.append(stream)

        for output_stream in output_streams:
            if s is not None:
                output_stream.write(s)
            output_stream.write(b'\n')
            output_stream.flush()


def _write_line(s: str | None = None, **kwargs: Any) -> None:
    _write_line_b(s.encode() if s is not None else s, **kwargs)


LOG_LEVEL_COLORS = {
    'DEBUG': utils.COLOR_CYAN_BG,
    'INFO': utils.COLOR_GREEN_BG,
    'WARNING': utils.COLOR_YELLOW_BG,
    'ERROR': utils.COLOR_RED_BG,
}

class LoggingHandler(logging.Handler):
    def __init__(self, use_color: bool) -> None:
        super().__init__()
        self.use_color = use_color

    def emit(self, record: logging.LogRecord) -> None:
        level_msg = utils.format_color(
            f'{record.levelname}:',
            LOG_LEVEL_COLORS[record.levelname],
            self.use_color,
        )
        _write_line(f'{level_msg} {record.getMessage()}')


@contextlib.contextmanager
def logging_handler(use_color: bool) -> Generator[None, None, None]:
    handler = LoggingHandler(use_color)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    try:
        yield
    finally:
        logger.removeHandler(handler)


