import asyncio
import sqlite3
import aiosqlite

async def check_exception():
    try:
        async with aiosqlite.connect(':memory:') as db:
            await db.execute('CREATE TABLE users (username TEXT UNIQUE, password_hash TEXT)')
            await db.execute('INSERT INTO users VALUES (?, ?)', ('testuser', 'hash'))
            print('First insert successful')
            try:
                await db.execute('INSERT INTO users VALUES (?, ?)', ('testuser', 'hash'))
            except sqlite3.IntegrityError as e:
                print(f'Expected error: {e}')
                print(f'Error type: {type(e)}')
            except Exception as e:
                print(f'Unexpected error: {e}')
                print(f'Error type: {type(e)}')
    except Exception as e:
        print(f'Outer exception: {e}')
        print(f'Outer exception type: {type(e)}')
    finally:
        print('Done')

if __name__ == "__main__":
    asyncio.run(check_exception())
