import argparse
import sys
from argparse import Namespace
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import prompt_toolkit.shortcuts.prompt
from prompt_toolkit.completion import FuzzyWordCompleter, PathCompleter
from prompt_toolkit.validation import ValidationError, Validator

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


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message: str):
        self.print_usage(sys.stdout)
        raise ValidationError(message=message)


class Argument:
    def __init__(
        self,
        *name_or_flags: str,
        validator: Optional[ValidatorT] = None,
        **kwargs,
    ):
        self.parser = CustomArgumentParser()
        action = self.parser.add_argument(*name_or_flags, **kwargs)
        self.name = action.dest
        self.validator = validator

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


def define_commands() -> Dict[str, Command]:
    # --------------------------------------------
    # set_grid

    set_grid = Command("set-grid", "Set the Grid.")
    set_grid.add_arguments(
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
            raise ValidationError(message="number must be > 0")
        return n

    tick.add_arguments(
        Argument("TURNS", type=int, default=1, validator=validate_gt_zero)
    )

    return {cmd.name: cmd for cmd in (set_grid, toggle_playback, tick)}


COMMANDS = define_commands()


def prompt(prefix: str = "> ", **prompt_kwargs) -> str:
    return prompt_toolkit.shortcuts.prompt(
        prefix,
        completer=FuzzyWordCompleter(
            list(COMMANDS),
            {name: cmd.description for name, cmd in COMMANDS.items()},
        ),
        complete_in_thread=True,
        complete_while_typing=True,
        **prompt_kwargs,
    )


def run_cli():
    while True:
        cmd = prompt()


def main():
    cmd = prompt()
    print(f"CMD => {cmd}")


if __name__ == "__main__":
    main()
