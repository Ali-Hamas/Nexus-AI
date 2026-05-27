import asyncio
from app.db.models import AsyncSessionLocal, WebSnapshot
import json

async def seed_minimal_replay_baseline():
    """Seeds a single, deterministic baseline snapshot into SQLite for emergency recovery."""
    print("Seeding minimal replay baseline...")
    async with AsyncSessionLocal() as session:
        # Check if already seeded
        from sqlalchemy import select
        result = await session.execute(select(WebSnapshot).where(WebSnapshot.competitor_name == "Notion"))
        if result.scalars().first():
            print("Baseline already exists. Skipping.")
            return

        emergency_snapshot = WebSnapshot(
            snapshot_version=1,
            competitor_name="Notion",
            source_url="https://notion.com/pricing",
            fetch_source="DETERMINISTIC_REPLAY_SEED",
            snapshot_status="REPLAYED",
            integrity_score=100,
            scraped_data={
                "pricing": [
                    {"tier_name": "Pro", "price": "$20/mo", "billing": "annually"},
                    {"tier_name": "Enterprise", "price": "Contact Us"}
                ],
                "features": ["Enterprise SSO", "Priority Support"]
            },
            dom_hash="emergency_recovery_baseline_hash_001"
        )
        session.add(emergency_snapshot)
        await session.commit()
        print("Emergency baseline seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_minimal_replay_baseline())
