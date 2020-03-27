import asyncio
import re
from dataclasses import dataclass
from typing import Any, Optional

import websockets

from conway.grid import BaseGrid
from conway.grid.cell_set import Grid

"""Regex for parsing incoming client messages.

We're using our own format here to keep it simple. The syntax is roughly:

    message ::= command [ SP body ]

where `command` is a typical identifier (letters/numbers/underscores/hyphens),
`SP` is one or more whitespace characters, and `body` is anything else.
"""
RE_MSG = re.compile(
    r"""
    (?P<command>[A-Za-z][A-Za-z0-9_-]*)
    (?:
        \s+ (?P<body> .*)
    )?
    """,
    re.VERBOSE,
)

MSG_CLIENT_ERR = "error: {}"
MSG_SYNTAX_ERR = MSG_CLIENT_ERR.format(
    "invalid syntax: could not parse message"
)
MSG_INVALID_CMD = MSG_CLIENT_ERR.format("invalid command `{}`")
MSG_MISSING_VALUE = MSG_CLIENT_ERR.format("missing value for `{}`")
MSG_INVALID_VALUE = MSG_CLIENT_ERR.format(
    "invalid value for `{}`: expected {}"
)

CMD_NEW_GRID = "new-grid"
CMD_TOGGLE_PLAYBACK = "toggle-playback"
CMD_SET_DELAY = "set-delay"
CMD_TICK = "tick"

CHR_LINE_SEP = "/"


class Controller:
    def __init__(
        self, websocket: websockets.WebSocketServerProtocol, grid: BaseGrid
    ):
        self.websocket = websocket

        self.grid = grid

        self.delay = 0.35

        self.paused = True
        self.playback = asyncio.Task(self.pause())

    async def send_grid(self):
        for line in str(self.grid).splitlines():
            await self.websocket.send(line)
        await self.websocket.send("\0")

    async def dispatch(self, command: str, body: Optional[str] = None):
        if command == CMD_TOGGLE_PLAYBACK:
            await self.do_toggle_playback()
        elif command == CMD_SET_DELAY:
            await self.do_set_delay(body)
        elif command == CMD_TICK:
            await self.do_tick(body)
        else:
            await self.websocket.send(MSG_INVALID_CMD.format(command))

    async def do_toggle_playback(self):
        self.playback.cancel()

        if self.paused:
            self.playback = asyncio.Task(self.play())
        else:
            self.playback = asyncio.Task(self.pause())

    async def play(self):
        self.paused = False
        while True:
            await self.send_grid()
            await asyncio.sleep(self.delay)
            self.grid.tick()

    async def pause(self):
        self.paused = True
        await self.send_grid()

    async def do_set_delay(self, delay: Any):
        if delay is None:
            return await self.websocket.send(
                MSG_MISSING_VALUE.format(CMD_SET_DELAY)
            )
        try:
            delay = float(delay)
        except ValueError:
            return await self.websocket.send(
                MSG_INVALID_VALUE.format(
                    CMD_SET_DELAY, "a float in the range [0, 1)"
                )
            )
        self.delay = delay

    async def do_tick(self, n: Any):
        try:
            n = n and int(n) or 1
        except ValueError:
            pass
        if not isinstance(n, int) or n < 1:
            return await self.websocket.send(
                MSG_INVALID_VALUE.format(CMD_TICK, "a positive integer")
            )
        for _ in range(n):
            self.grid.tick()
        await self.send_grid()


async def init_controller(
    websocket: websockets.WebSocketServerProtocol,
) -> Controller:
    async for msg in websocket:
        match = RE_MSG.fullmatch(str(msg).strip())
        if not match:
            await websocket.send(MSG_SYNTAX_ERR)
            continue

        command, body = match.groups()
        if command != CMD_NEW_GRID:
            await websocket.send(
                MSG_CLIENT_ERR.format(
                    f"setup incomplete: client must send `{CMD_NEW_GRID}` to"
                    " initialize the game grid"
                )
            )
            continue

        if not body:
            await websocket.send(MSG_MISSING_VALUE.format(CMD_NEW_GRID))
            continue

        break

    body = body.replace(CHR_LINE_SEP, "\n")
    grid = Grid.from_str(body)
    return Controller(websocket, grid)


async def server_handler(
    websocket: websockets.WebSocketServerProtocol, path: str
):
    controller = await init_controller(websocket)

    async for msg in websocket:
        match = RE_MSG.fullmatch(str(msg).strip())
        if not match:
            await websocket.send(MSG_SYNTAX_ERR)
            continue

        command, body = match.groups()
        await controller.dispatch(command, body)


async def main():
    await websockets.serve(server_handler, "localhost", 8765)


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
    event_loop.run_forever()
