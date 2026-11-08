import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from psycopg import AsyncConnection
from psycopg.rows import DictRow, dict_row
from psycopg_pool import AsyncConnectionPool

type Conn = AsyncConnection[DictRow]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # DSN da env finché non arriva pydantic-settings (2.6)
    async with AsyncConnectionPool[Conn](
        os.environ["DATABASE_URL"],
        min_size=2,
        max_size=10,
        kwargs={"row_factory": dict_row},
        open=False,
    ) as pool:
        await pool.wait(timeout=10)
        app.state.pool = pool
        yield


async def get_conn(request: Request) -> AsyncIterator[Conn]:
    # commit all'uscita, rollback se la route solleva
    async with request.app.state.pool.connection() as conn:
        yield conn


DbConn = Annotated[Conn, Depends(get_conn)]
