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

from __future__ import annotations

__all__: list[str] = ["parse_code", "with_block"]

import typing


def parse_code(*, code: str, lang: str = "sql") -> str:
    """Parse and replace a language specific code.

    Example
    -------
    ```sql
        SELECT * FROM table WHERE id = $1
            INNER JOIN table2
        ON table.id
        GROUP BY <> DESC
        LIMIT 2
    ```
    This removes the ```sql``` code blocks and returns the original code.
    """
    if not code.startswith(f"```{lang}") and code.endswith("```"):
        code = code.replace("```", "").replace(lang, "")
    return code


def with_block(data: typing.Any, *, lang: str = "hs") -> str:
    """Adds code blocks to a any text."""
    return f"```{lang}\n{data}\n```"
