"""Database manager for report statistics storage and retrieval."""

import datetime
import logging
from typing import Dict
import aiosqlite

from configs.config import DATABASE_PATH

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database operations for report tracking."""

    def __init__(self) -> None:
        """Initialize database manager."""
        self.database_path = str(DATABASE_PATH)

    async def initialize(self) -> None:
        """Create database tables if they don't exist."""
        try:
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        day TEXT NOT NULL,
                        iso_week TEXT NOT NULL,
                        month TEXT NOT NULL
                    )
                """)
                await db.commit()
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.exception("Failed to initialize database")
            raise

    async def increment(self) -> None:
        """Add a new report entry for the current timestamp."""
        now = datetime.datetime.now()
        day = now.strftime("%Y-%m-%d")
        iso_week = f"{now.year}-W{now.isocalendar()[1]:02d}"
        month = now.strftime("%Y-%m")
        
        try:
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute(
                    "INSERT INTO reports (timestamp, day, iso_week, month) VALUES (?, ?, ?, ?)",
                    (now.isoformat(), day, iso_week, month)
                )
                await db.commit()
                logger.debug(f"Report added for {day}")
        except Exception as e:
            logger.exception("Failed to increment report count")
            raise

    async def decrement(self) -> None:
        """Remove the most recent report entry for today."""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        try:
            async with aiosqlite.connect(self.database_path) as db:
                async with db.execute(
                    "SELECT id FROM reports WHERE day = ? ORDER BY timestamp DESC LIMIT 1",
                    (today,)
                ) as cur:
                    row = await cur.fetchone()
                    if row is None:
                        logger.warning("No reports to decrement for today")
                        return
                    record_id = row[0]

                await db.execute("DELETE FROM reports WHERE id = ?", (record_id,))
                await db.commit()
                logger.debug(f"Report removed for {today}")
        except Exception as e:
            logger.exception("Failed to decrement report count")
            raise

    async def set_today_to(self, target: int) -> None:
        """
        Set today's report count to a specific value.
        
        Args:
            target: Target number of reports for today
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        now = datetime.datetime.now()
        iso_week = f"{now.year}-W{now.isocalendar()[1]:02d}"
        month = now.strftime("%Y-%m")

        try:
            async with aiosqlite.connect(self.database_path) as db:
                # Get current count for today
                async with db.execute(
                    "SELECT COUNT(*) FROM reports WHERE day = ?",
                    (today,)
                ) as cur:
                    current = (await cur.fetchone())[0]

                diff = target - current

                if diff > 0:
                    # Add missing entries for today
                    values = [(now.isoformat(), today, iso_week, month) for _ in range(diff)]
                    await db.executemany(
                        "INSERT INTO reports (timestamp, day, iso_week, month) VALUES (?, ?, ?, ?)",
                        values
                    )
                    logger.info(f"Added {diff} reports for {today}")
                elif diff < 0:
                    # Remove excess entries for today
                    for _ in range(-diff):
                        await db.execute(
                            """
                            DELETE FROM reports
                            WHERE id = (
                                SELECT id FROM reports
                                WHERE day = ?
                                ORDER BY timestamp DESC
                                LIMIT 1
                            )
                            """,
                            (today,)
                        )
                    logger.info(f"Removed {-diff} reports for {today}")
                
                await db.commit()
        except Exception as e:
            logger.exception("Failed to set today's report count")
            raise

    async def reset_all(self) -> None:
        """Delete all report entries from the database."""
        try:
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("DELETE FROM reports")
                await db.commit()
                logger.info("All reports reset")
        except Exception as e:
            logger.exception("Failed to reset reports")
            raise

    async def get_statistics(self) -> Dict[str, int]:
        """
        Get report statistics for current day, week, and month.
        
        Returns:
            Dictionary with keys 'day', 'week', 'month' and their counts
        """
        now = datetime.datetime.now()
        day = now.strftime("%Y-%m-%d")
        iso_week = f"{now.year}-W{now.isocalendar()[1]:02d}"
        month = now.strftime("%Y-%m")

        try:
            async with aiosqlite.connect(self.database_path) as db:
                async with db.execute("SELECT COUNT(*) FROM reports WHERE day = ?", (day,)) as cur:
                    day_count = (await cur.fetchone())[0]
                async with db.execute("SELECT COUNT(*) FROM reports WHERE iso_week = ?", (iso_week,)) as cur:
                    week_count = (await cur.fetchone())[0]
                async with db.execute("SELECT COUNT(*) FROM reports WHERE month = ?", (month,)) as cur:
                    month_count = (await cur.fetchone())[0]

            logger.debug(f"Statistics: day={day_count}, week={week_count}, month={month_count}")
            return {"day": day_count, "week": week_count, "month": month_count}
        except Exception as e:
            logger.exception("Failed to get statistics")
            raise
