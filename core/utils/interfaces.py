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
"""Interfaces for our api wrappers."""

from __future__ import annotations

__all__: tuple[str, ...] = ("APIWrapper", "GithubRepo", "GithubUser", "HashView")

import abc
import typing

import attr

if typing.TYPE_CHECKING:
    import datetime

    import hikari
    import tanjun

_T = typing.TypeVar("_T")


@attr.define(weakref_slot=False, hash=False, repr=True)
class HashView(typing.Generic[_T]):
    key: _T = attr.field()
    value: _T = attr.field()


class APIWrapper(abc.ABC):
    """An abctract interface for our wrapper class."""

    __slots__: typing.Sequence[str] = ()

    @abc.abstractmethod
    async def get_anime(
        self,
        _: tanjun.abc.SlashContext,
        name: str | None = None,
        *,
        random: bool | None = None,
        genre: str,
    ) -> hikari.Embed | None:
        """Fetch an anime from jikan api.

        Parameters
        ----------
        _ | ctx : `tanjun.abc.SlashContext`
            The discord slash context.
        name : `str` | `None`
            The anime name. If kept to None, A random anime will be returned.
        genre : `str`
            The anime's genre. If kept to None. A random genre will be selected.

        Notes
        -----
        * If random was `True` and genre is `None`,
        A random anime with a random genre will be returned.

        * If random was `None` and the genre is selected.
        A random anime based on the selected genre will be returned.

        Returns
        -------
        `hikari.Embed`
            A hikari embed contains the anime data
            if the the request was succesfulanime was found.
        `None`
            The anime was not found.
        """

    @abc.abstractmethod
    async def get_manga(
        self, _: tanjun.abc.SlashContext, name: str, /
    ) -> hikari.Embed | None:
        """Fetch an manga from jikan api and returns the first one found.

        Parameters
        ----------
        _ | ctx : `tanjun.abc.SlashContext`
            The discord's slash context.
        name : `str`
            The manga name.

        Returns
        -------
        hikari.Embed
            A hikari embed contains the manga data
            if the the request was successful manga was found.
        `None`
            The manga was not found.
        """

    @abc.abstractmethod
    async def get_definition(
        self, ctx: tanjun.abc.SlashContext, name: str
    ) -> hikari.Embed | None:
        """Get the definition by its name from urban dictionary.

        Parameters
        ----------
        ctx : `tanjun.abc.SlashContext`
            The discord's slash context.
        name : `str`
            The name of the definition.

        Returns
        -------
        `hikari.Embed`
            A hikari embed contains the definition data
            if the the request was successful definition was found.
        `None`
            The definition was not found.
        """

    @abc.abstractmethod
    async def get_git_user(self, name: str) -> GithubUser | None:
        """Fetch a Github user.

        Parameters
        -----------
        name : `str`
            The user name.

        Returns
        --------
        `GithubUser`
            A github user object.
        """

    @abc.abstractmethod
    async def get_git_repo(self, name: str) -> typing.Sequence[GithubRepo] | None:
        """Fetch a Github repo.

        Parameters
        -----------
        name : `str`
            The repo name.

        Returns
        --------
        `GithubRepo`
            A github repo object
        """


# TODO: impl this for github component.


@attr.define(hash=False, weakref_slot=False, kw_only=True)
class GithubRepo:
    """Represents a repo on github."""

    owner: GithubUser | None = attr.field(repr=True)
    """The repo's owner."""

    id: int = attr.field()

    name: str = attr.field()

    description: str | None = attr.field()

    is_forked: bool = attr.field()

    url: str = attr.field()

    is_archived: bool = attr.field()

    forks: int = attr.field()

    open_issues: int = attr.field()

    # We only need the License name
    license: str | None = attr.field()

    size: int = attr.field()

    created_at: datetime.datetime = attr.field()

    last_push: str = attr.field()

    page: str | None = attr.field()

    stars: int = attr.field()

    language: str | hikari.UndefinedType = attr.field()


@attr.define(hash=False, weakref_slot=False, kw_only=True, repr=False)
class GithubUser:
    """Represents a user on github."""

    # We only care about the fields we need.

    api: APIWrapper = attr.field()

    name: hikari.UndefinedOr[str] = attr.field(repr=True)

    id: int = attr.field(repr=True, hash=True)

    avatar_url: typing.Optional[str] = attr.field()

    url: str = attr.field()

    type: str = attr.field()

    email: typing.Optional[str] = attr.field()

    location: typing.Optional[str] | None = attr.field()

    public_repors: int | hikari.UndefinedType = attr.field()

    bio: hikari.UndefinedOr[str] | None = attr.field()

    followers: int | hikari.UndefinedType = attr.field()

    following: int | hikari.UndefinedType = attr.field()

    created_at: datetime.datetime | None = attr.field()

    repos_url: str = attr.field()

    async def fetch_repos(self) -> typing.Sequence[GithubRepo]:
        ...
