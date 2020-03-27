import argparse
import pprint
import shlex
import sys
from argparse import Namespace
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import (
    NestedCompleter,
    PathCompleter,
    WordCompleter,
)
from prompt_toolkit.validation import Validator as PTValidator

SAMPLE_DIR = Path(__file__).parent.parent.absolute() / "sample_patterns"
SAMPLE_CHOICES = ("beacon", "blinker", "glider", "toad")

"""
COMMANDS
--------

set-grid --random WIDTH HEIGHT
set-grid --file FILE
set-grid --sample SAMPLE
set-delay DELAY
set-outfile ( OUTFILE | "-" )
set-turns TURNS
tick [ TURNS ]
toggle-playback
play
pause
"""

ValidatorT = Callable[[Any], Any]


class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"error: {self.message}"


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message: str):
        self.print_usage(sys.stdout)
        raise ValidationError(message)


class Argument:
    def __init__(
        self,
        *name_or_flags: str,
        validator: Optional[ValidatorT] = None,
        **kwargs,
    ):
        self.validator = validator
        self.parser = CustomArgumentParser(add_help=False)
        action = self.parser.add_argument(*name_or_flags, **kwargs)

        self.name = action.dest
        self.completions = {}
        if action.option_strings:
            if len(action.option_strings) > 1:
                self.completions[action.option_strings[-2]] = ""
            self.completions[action.option_strings[-1]] = action.help or ""

    def parse(
        self, argv: List[str], ns: Namespace
    ) -> Tuple[Namespace, List[str]]:
        ns, rest = self.parser.parse_known_args(argv, namespace=ns)
        if self.validator:
            value = getattr(ns, self.name)
            setattr(ns, self.name, self.validator(value))
        return ns, rest


class Command:
    name: str
    description: str
    arguments: List[Argument]
    validators: List[ValidatorT]

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.arguments = []
        self.validators = []

    def add_arguments(self, *arguments: Argument):
        self.arguments.extend(arguments)

    def parse(self, argv: List[str]) -> Namespace:
        ns = Namespace()
        for argument in self.arguments:
            ns, argv = argument.parse(argv, ns)
        return ns

    def get_completions(self) -> dict:
        completions: dict = {}
        for argument in self.arguments:
            completions.update(argument.completions)
        return completions


def define_commands() -> Dict[str, Command]:
    # --------------------------------------------
    # set_grid

    set_grid = Command("set-grid", "Set the Grid.")
    set_grid.add_arguments(
        Argument("-w", "--width", type=int, help="the width of the grid"),
        Argument("-h", "--height", type=int, help="the height of the grid"),
        Argument(
            "--random",
            type=float,
            nargs="?",
            const=0.5,
            metavar="K",
            help=(
                "randomly generate the initial grid. if given, %(metavar)s must"
                " be a number in the range [0, 1) and sets the probability that a"
                " cell will be living (default: %(const)s)"
            ),
        ),
        Argument(
            "--sample",
            type=str,
            choices=SAMPLE_CHOICES,
            metavar="PATTERN",
            help="set the initial grid to a predefined sample pattern",
        ),
        Argument(
            "--file",
            type=argparse.FileType("r"),
            default=sys.stdin,
            metavar="FILE",
            help="set the initial grid to a custom pattern file",
        ),
    )

    # --------------------------------------------
    # toggle_playback

    toggle_playback = Command(
        "toggle-playback", "Toggle the playback state (play/pause)."
    )

    # --------------------------------------------
    # tick

    tick = Command("tick", "Advance the game by one or more ticks.")

    def validate_gt_zero(n: int):
        if n < 1:
            raise ValidationError("number must be > 0")
        return n

    tick.add_arguments(
        Argument("TURNS", type=int, default=1, validator=validate_gt_zero)
    )

    return {cmd.name: cmd for cmd in (set_grid, toggle_playback, tick)}


COMMANDS = define_commands()


def is_valid_command(text: str) -> bool:
    return bool(text) and (text.split(maxsplit=1)[0] in COMMANDS)


def start_session(prefix: str = "> ", **session_kwargs) -> PromptSession:
    completion_dict = {
        cmd.name: cmd.get_completions() for cmd in COMMANDS.values()
    }

    return PromptSession(
        prefix,
        completer=NestedCompleter(
            {
                name: WordCompleter(list(completions), meta_dict=completions)
                for name, completions in completion_dict.items()
            }
        ),
        complete_in_thread=True,
        complete_while_typing=True,
        validator=PTValidator.from_callable(
            is_valid_command, error_message="invalid command"
        ),
        **session_kwargs,
    )


def run_cli():
    session = start_session()
    while True:
        input_ = session.prompt()
        cmd_name, *args = shlex.split(input_)
        print(f"CMD => {cmd_name}")
        cmd = COMMANDS[cmd_name]
        ns = cmd.parse(args)
        pprint.pprint(vars(ns))


def main():
    run_cli()


if __name__ == "__main__":
    main()
