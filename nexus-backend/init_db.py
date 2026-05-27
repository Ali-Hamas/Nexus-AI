import asyncio
from app.db.models import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
    print("Database tables initialized successfully.")
