import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect('postgresql://restaurant_booking_db_khto_user:XsgZODyDV62wKPtUdEWCiJwz6yt8cWru@dpg-d6u1ub75r7bs73fp72hg-a.singapore-postgres.render.com/restaurant_booking_db_khto')
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    print('Tables:', [t['table_name'] for t in tables])
    await conn.close()

asyncio.run(check())