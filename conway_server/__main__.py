import asyncio
import re
from dataclasses import dataclass
from typing import NamedTuple, Optional

import websockets

from conway.grid import BaseGrid
from conway.grid.cell_set import Grid

"""Regex for parsing incoming client messages.

We're using our own format here to keep it simple. The syntax is roughly:

    message ::= command [ "<<<" body ]

where `command` is a typical identifier (letters/numbers/underscores/hyphens)
and `body` is anything after the "<<<" delimiter.
"""
RE_MSG = re.compile(
    r"""
    (?P<command>[A-Za-z][A-Za-z0-9_-]*)
    (?:
        \s* <<<
        \s* (?P<body> .*)
    )?
    """,
    re.VERBOSE,
)

MSG_CLIENT_ERR = "client-error <<< {}"
MSG_SYNTAX_ERR = MSG_CLIENT_ERR.format("syntax error: could not parse message")
MSG_MISSING_VALUE = MSG_CLIENT_ERR.format("missing value for `{}`")

CMD_NEW_GRID = "new-grid"
CMD_TOGGLE_PLAYBACK = "toggle-playback"
CMD_SET_DELAY = "set-delay"
CMD_RESTART = "restart"
CMD_TICK = "tick"


class Controller:
    def __init__(
        self, websocket: websockets.WebSocketServerProtocol, grid: BaseGrid
    ):
        self.websocket = websocket

        self.grid = grid

        self.delay = 0.35

        self.paused = True
        self.playback = asyncio.Task(self.pause())

    async def dispatch(self, command: str, body: Optional[str] = None):
        if command == CMD_TOGGLE_PLAYBACK:
            await self.toggle_playback()
        elif command == CMD_SET_DELAY:
            if body is None:
                await self.websocket.send(
                    MSG_MISSING_VALUE.format(CMD_SET_DELAY)
                )
            try:
                delay = float(body)  # type: ignore
            except TypeError:
                await self.websocket.send(
                    MSG_CLIENT_ERR.format(
                        f"invalid value for `{CMD_SET_DELAY}`; expected"
                        " a float in the range [0, 1)"
                    )
                )
            await self.set_delay(delay)
        elif command == CMD_RESTART:
            await self.restart()
        elif command == CMD_TICK:
            n = body and int(body) or None
            await self.tick(n)

    async def toggle_playback(self):
        self.playback.cancel()

        if self.paused:
            self.playback = asyncio.Task(self.play())
        else:
            self.playback = asyncio.Task(self.pause())

    async def play(self):
        self.paused = False
        while True:
            await self.websocket.send(str(self.grid))
            await asyncio.sleep(self.delay)
            self.grid.tick()

    async def pause(self):
        self.paused = True
        await self.websocket.send(str(self.grid))

    async def set_delay(self, delay: float):
        self.delay = delay

    async def restart(self):
        pass

    async def tick(self, n: Optional[int] = None):
        for _ in range(n or 1):
            self.grid.tick()
        await self.websocket.send(str(self.grid))


async def server_handler(
    websocket: websockets.WebSocketServerProtocol, path: str
):
    async for msg in websocket:
        match = RE_MSG.fullmatch(str(msg))
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

        grid = Grid.from_str(body)
        controller = Controller(websocket, grid)
        break

    async for msg in websocket:
        match = RE_MSG.fullmatch(str(msg))
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
