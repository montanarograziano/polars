from __future__ import annotations

import contextlib
from pathlib import Path
from typing import IO, TYPE_CHECKING

from polars._utils.various import normalize_filepath
from polars._utils.wrap import wrap_df
from polars.io._utils import parse_columns_arg

with contextlib.suppress(ImportError):  # Module not available when building docs
    from polars.polars import PyDataFrame

if TYPE_CHECKING:
    from polars import DataFrame


def read_avro(
    source: str | Path | IO[bytes] | bytes,
    *,
    columns: list[int] | list[str] | None = None,
    n_rows: int | None = None,
) -> DataFrame:
    """
    Read into a DataFrame from Apache Avro format.

    Parameters
    ----------
    source
        Path to a file or a file-like object (by "file-like object" we refer to objects
        that have a `read()` method, such as a file handler like the builtin `open`
        function, or a `BytesIO` instance).
    columns
        Columns to select. Accepts a list of column indices (starting at zero) or a list
        of column names.
    n_rows
        Stop reading from Apache Avro file after reading `n_rows`.

    Returns
    -------
    DataFrame

    Examples
    --------
    Read a DataFrame from an Apache Avro file, with columns

    >>> pl.read_avro("data.avro")
    ... shape: (3, 3)
    ... ┌─────┬────────┬──────┐
    ... │ id  ┆ name   ┆ age  │
    ... │ --- ┆ ---    ┆ ---  │
    ... │ i64 ┆ str    ┆ i64  │
    ... ├─────┼────────┼──────┤
    ... │ 1   ┆ Alice  ┆ 20   │
    ... │ 2   ┆ Bob    ┆ 30   │
    ... │ 3   ┆ Alex   ┆ 40   │
    ... └─────┴────────┴──────┘
    """
    if isinstance(source, (str, Path)):
        source = normalize_filepath(source)
    projection, column_names = parse_columns_arg(columns)

    pydf = PyDataFrame.read_avro(source, column_names, projection, n_rows)
    return wrap_df(pydf)
