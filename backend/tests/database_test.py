from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio

DATABASE_URL = "postgresql+asyncpg://postgres:jqbjBfWeENLQrFkYZVtAvkoWWrlhtvdl@maglev.proxy.rlwy.net:14823/railway"

async def test_connection():
    engine = create_async_engine(DATABASE_URL)
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1;"))
        print(result.fetchone())

asyncio.run(test_connection())