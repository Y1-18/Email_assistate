from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from model import EmailLog
from schema import EmailLogCreate

class CRUDLogs:
    async def create(self, db: AsyncSession, log: EmailLogCreate) -> EmailLog:
        db_log = EmailLog(**log.dict())
        db.add(db_log)
        await db.commit()
        await db.refresh(db_log)
        return db_log

    async def get(self, db: AsyncSession, id: int):
        result = await db.execute(select(EmailLog).where(EmailLog.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 50):
        result = await db.execute(select(EmailLog).offset(skip).limit(limit))
        return result.scalars().all()

crud_email_logs = CRUDLogs()
