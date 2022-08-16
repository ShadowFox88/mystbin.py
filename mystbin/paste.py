"""
The MIT License (MIT)

Copyright (c) 2020 - Present, PythonistaGuild

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Optional


if TYPE_CHECKING:
    from typing_extensions import Self

    from mystbin.types.responses import FileResponse, PasteResponse

__all__ = (
    "File",
    "Paste",
)


class File:
    __slots__ = (
        "filename",
        "content",
        "syntax",
        "lines_of_code",
        "character_count",
    )

    def __init__(
        self,
        *,
        filename: str,
        content: str,
        syntax: Optional[str],
        lines_of_code: Optional[int] = None,
        character_count: Optional[int] = None,
    ) -> None:
        self.filename: str = filename
        self.content: str = content
        self.syntax: Optional[str] = syntax
        self.lines_of_code: int = lines_of_code or len(content.split("\n"))
        self.character_count: int = character_count or len(content)

    @classmethod
    def from_data(cls, payload: FileResponse, /) -> Self:
        return cls(
            content=payload["content"],
            filename=payload["filename"],
            syntax=payload["filename"].rsplit(".")[-1],
            lines_of_code=payload["loc"],
            character_count=payload["charcount"],
        )

    def to_dict(self) -> dict[str, Any]:
        ret: dict[str, Any] = {"content": self.content, "filename": self.filename, "syntax": self.syntax}

        return ret


class Paste:
    __slots__ = (
        "id",
        "author_id",
        "created_at",
        "expires",
        "files",
        "notice",
        "views",
        "last_edited",
    )

    def __init__(
        self,
        *,
        id: str,
        created_at: str,
        expires: Optional[str] = None,
        last_edited: Optional[str] = None,
        files: list[File],
        views: Optional[int] = None,
    ) -> None:
        self.id: str = id
        self.created_at: datetime.datetime = datetime.datetime.fromisoformat(created_at)
        self.expires: Optional[datetime.datetime] = datetime.datetime.fromisoformat(expires) if expires else None
        self.last_edited: Optional[datetime.datetime] = datetime.datetime.fromisoformat(last_edited) if last_edited else None
        self.files: list[File] = files
        self.views: Optional[int] = views

    def __str__(self) -> str:
        return f"Paste with ID: {self.id!r}."

    def __repr__(self) -> str:
        return f"<Paste id={self.id!r} files={len(self.files)}>"

    @classmethod
    def from_data(cls, payload: PasteResponse, /) -> Self:
        files = [File.from_data(data) for data in payload["files"]]
        return cls(
            id=payload["id"],
            created_at=payload["created_at"],
            expires=payload["expires"],
            files=files,
            views=payload.get("views"),
            last_edited=payload.get("last_edited"),
        )