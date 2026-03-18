from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient

class ChatUseCase:
    def __init__(self, chat_repo: ChatMessageRepository, openrouter_client: OpenRouterClient):
        self.chat_repo = chat_repo
        self.openrouter_client = openrouter_client
    
    async def ask(self, user_id: int, prompt: str, system: str = None, 
                  max_history: int = 10, temperature: float = 0.7):
        # Prepare messages for LLM
        messages = []
        
        # Add system message if provided
        if system:
            messages.append({"role": "system", "content": system})
        
        # Add conversation history
        history = await self.chat_repo.get_user_history(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Save user message
        await self.chat_repo.add_message(user_id, "user", prompt)
        
        # Get response from OpenRouter
        answer = await self.openrouter_client.chat_completion(messages, temperature)
        
        # Save assistant message
        await self.chat_repo.add_message(user_id, "assistant", answer)
        
        return answer
    
    async def get_history(self, user_id: int, limit: int = 50):
        return await self.chat_repo.get_user_history(user_id, limit)
    
    async def clear_history(self, user_id: int):
        await self.chat_repo.clear_history(user_id)