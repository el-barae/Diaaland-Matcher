async def init(session):
    if not session.is_active:
        # Connect to the database
        await session.connection()