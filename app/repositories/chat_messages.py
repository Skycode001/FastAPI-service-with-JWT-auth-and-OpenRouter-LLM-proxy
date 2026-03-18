from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models import ChatMessage

class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message
    
    async def get_user_history(self, user_id: int, limit: int = 10) -> list[ChatMessage]:
        result = await self.session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))  # Возвращаем в хронологическом порядке
    
    async def clear_history(self, user_id: int) -> None:
        await self.session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self.session.commit()