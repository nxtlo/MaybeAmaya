# -*- cofing: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 - Present nxtlo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Boxed constants and methods used globally."""

from __future__ import annotations

__all__: list[str] = [
    "COLOR",
    "API",
    "GENRES",
    "iter",
    "randomize",
    "generate_component",
    "naive_datetime",
    "spawn",
    "error",
    "parse_code",
    "with_block",
    "add_help",
]

import datetime
import random
import sys
import typing

import hikari
import tanjun
import yuyo
from hikari.internal import aio

if typing.TYPE_CHECKING:
    import builtins
    import collections.abc as collections
    import types

    _T = typing.TypeVar("_T")

COLOR: typing.Final[
    collections.Mapping[typing.Literal["invis", "random"], hikari.Colourish]
] = {
    "invis": hikari.Colour(0x36393F),
    "random": hikari.Colour(random.randint(0, 0xFFFFFF)),
}
"""Colors."""

API: collections.Mapping[typing.Literal["anime", "urban", "git"], typing.Any] = {
    "anime": "https://api.jikan.moe/v3",
    "urban": "https://api.urbandictionary.com/v0/define",
    "git": {
        "user": "https://api.github.com/users",
        "repo": "https://api.github.com/search/repositories?q={}&page=0&per_page=11&sort=stars&order=desc",
    },
}
"""A dict that holds api endpoints."""

GENRES: dict[str, int] = {
    "Action": 1,
    "Advanture": 2,
    "Drama": 8,
    "Daemons": 6,
    "Ecchi": 9,  # :eyes:
    "Sci-Fi": 24,
    "Shounen": 27,
    "Harem": 35,  # :eyes:
    "Seinen": 42,
    "Saumrai": 21,
    "Games": 11,
    "Psycho": 40,
    "Superpowers": 37,
    "Vampire": 32,
}
"""Anime only genres."""


def naive_datetime(datetime_: datetime.datetime) -> datetime.datetime:
    return datetime_.astimezone(datetime.timezone.utc)


_SlashT = tanjun.commands.SlashCommand[typing.Any]


def add_help(
    summary: str, *, options: dict[str, str] | None = None
) -> collections.Callable[[_SlashT], _SlashT]:
    def AnyWrapper(command: _SlashT) -> _SlashT:
        command.set_metadata("summary", f"**Summary**: {summary}")

        if options is not None:
            ok_options = [
                f"**Options**:\n{oname}: {osumm}" for oname, osumm in options.items()
            ]
            command.set_metadata("options", "\n".join(ok_options))

        return command

    return AnyWrapper


async def generate_component(
    ctx: tanjun.abc.SlashContext | tanjun.abc.MessageContext,
    iterable: (
        collections.Generator[tuple[hikari.UndefinedType, hikari.Embed], None, None]
        | collections.Iterator[tuple[hikari.UndefinedType, hikari.Embed]]
    ),
    component_client: yuyo.ComponentClient,
    timeout: datetime.timedelta | None = None,
) -> None:
    pages = yuyo.ComponentPaginator(
        iterable,
        authors=(ctx.author,),
        triggers=(
            yuyo.pagination.LEFT_DOUBLE_TRIANGLE,
            yuyo.pagination.LEFT_TRIANGLE,
            yuyo.pagination.STOP_SQUARE,
            yuyo.pagination.RIGHT_TRIANGLE,
            yuyo.pagination.RIGHT_DOUBLE_TRIANGLE,
        ),
        timeout=timeout or datetime.timedelta(seconds=90),
    )
    if next_ := await pages.get_next_entry():
        content, embed = next_
        msg = await ctx.respond(
            content=content, embed=embed, component=pages, ensure_result=True
        )
        component_client.set_executor(msg, pages)


def iter(map: collections.Mapping[str, typing.Any]) -> collections.Sequence[typing.Any]:
    return [k for k in map.keys()]


def randomize(seq: collections.Sequence[_T]) -> _T:
    """Return a random element from a sequence."""
    return random.choice(list(seq))


def randomize_genres() -> str:
    """Return a random anime genre."""
    return random.choice(list(GENRES.keys()))


# Since this module is mostly imported everywhere its worth
# having this here.
async def spawn(
    *coros: collections.Awaitable[_T], timeout: float | None = None
) -> collections.Sequence[_T]:
    """Spawn a sequence awaitables and return their results."""
    return await aio.all_of(*coros, timeout=timeout)


def parse_code(*, code: str, lang: str = "sql") -> str:
    """Parse and replace a language specific code.

    Example
    -------
    ```sql
    SELECT * FROM table WHERE id = $1
    ```
    This removes the ```sql``` code blocks and returns the original code.
    """
    if code.startswith(f"```{lang}") and code.endswith("```"):
        code = code.replace("```", "").replace(lang, "")
    return code


def with_block(data: typing.Any, *, lang: str = "hs") -> str:
    """Adds code blocks to a any text."""
    return f"```{lang}\n{data}\n```"


def error(
    source: tuple[
        type[builtins.BaseException], builtins.BaseException, types.TracebackType
    ]
    | tuple[None, None, None]
    | None = None,
    str: bool = False,
) -> BaseException | str | None:
    """Return the last detected exception"""
    if source is None:
        if str:
            return with_block(sys.exc_info()[1])
        return sys.exc_info()[1]
    return source[1]
