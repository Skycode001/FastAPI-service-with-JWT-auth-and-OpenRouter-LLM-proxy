from datetime import timedelta
from app.core import security
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.repositories.users import UserRepository

class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def register(self, email: str, password: str):
        # Check if user exists
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ConflictError("Email already registered")
        
        # Create user
        password_hash = security.hash_password(password)
        user = await self.user_repo.create(email, password_hash)
        return user
    
    async def login(self, email: str, password: str):
        # Get user
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Invalid email or password")
        
        # Verify password
        if not security.verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        
        # Create token
        access_token = security.create_access_token(
            data={"sub": str(user.id), "role": user.role},
            expires_delta=timedelta(minutes=60)
        )
        return access_token
    
    async def get_profile(self, user_id: int):
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user