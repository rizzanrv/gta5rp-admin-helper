import datetime
import aiosqlite

class DatabaseManager:
    """
    Manages the SQLite database for storing report entries and retrieving statistics.
    """

    DATABASE_PATH = "reports.db"

    async def initialize(self) -> None:
        """
        Creates the reports table if it does not exist.
        """
        async with aiosqlite.connect(self.DATABASE_PATH) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    day TEXT NOT NULL,
                    week TEXT NOT NULL,
                    month TEXT NOT NULL
                )
            """)
            await db.commit()

    async def increment(self) -> None:
        """
        Inserts a new report entry for the current timestamp.
        """
        now = datetime.datetime.now()
        day = now.strftime("%Y-%m-%d")
        week = now.strftime("%Y-W%U")
        month = now.strftime("%Y-%m")
        async with aiosqlite.connect(self.DATABASE_PATH) as db:
            await db.execute(
                "INSERT INTO reports (timestamp, day, week, month) VALUES (?, ?, ?, ?)",
                (now.isoformat(), day, week, month)
            )
            await db.commit()

    async def decrement(self) -> None:
        """
        Deletes the most recent report entry for the current day.
        """
        day = datetime.datetime.now().strftime("%Y-%m-%d")
        async with aiosqlite.connect(self.DATABASE_PATH) as db:
            await db.execute(
                "DELETE FROM reports WHERE day = ? ORDER BY timestamp DESC LIMIT 1",
                (day,)
            )
            await db.commit()

    async def set_today_to(self, target: int) -> None:
        """
        Adjusts the count for the current day to the specified target value.
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        async with aiosqlite.connect(self.DATABASE_PATH) as db:
            async with db.execute("SELECT COUNT(*) FROM reports WHERE day = ?", (today,)) as cur:
                current = (await cur.fetchone())[0]
            diff = target - current
            now = datetime.datetime.now()
            week = now.strftime("%Y-W%U")
            month = now.strftime("%Y-%m")
            if diff > 0:
                values = [(now.isoformat(), today, week, month) for _ in range(diff)]
                await db.executemany(
                    "INSERT INTO reports (timestamp, day, week, month) VALUES (?, ?, ?, ?)",
                    values
                )
            elif diff < 0:
                for _ in range(-diff):
                    await db.execute(
                        "DELETE FROM reports WHERE day = ? ORDER BY timestamp DESC LIMIT 1",
                        (today,)
                    )
            await db.commit()

    async def reset_all(self) -> None:
        """
        Deletes all report entries from the database.
        """
        async with aiosqlite.connect(self.DATABASE_PATH) as db:
            await db.execute("DELETE FROM reports")
            await db.commit()

    async def get_statistics(self) -> dict[str, int]:
        """
        Retrieves the report counts for the current day, week, and month.

        Returns:
            A dictionary with keys 'day', 'week', and 'month'.
        """
        now = datetime.datetime.now()
        day = now.strftime("%Y-%m-%d")
        week = now.strftime("%Y-W%U")
        month = now.strftime("%Y-%m")
        async with aiosqlite.connect(self.DATABASE_PATH) as db:
            async with db.execute("SELECT COUNT(*) FROM reports WHERE day = ?", (day,)) as cur:
                day_count = (await cur.fetchone())[0]
            async with db.execute("SELECT COUNT(*) FROM reports WHERE week = ?", (week,)) as cur:
                week_count = (await cur.fetchone())[0]
            async with db.execute("SELECT COUNT(*) FROM reports WHERE month = ?", (month,)) as cur:
                month_count = (await cur.fetchone())[0]
        return {"day": day_count, "week": week_count, "month": month_count}