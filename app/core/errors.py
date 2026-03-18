class AppError(Exception):
    """Base application error"""
    pass

class ConflictError(AppError):
    """Resource already exists"""
    pass

class UnauthorizedError(AppError):
    """Invalid credentials"""
    pass

class ForbiddenError(AppError):
    """Insufficient permissions"""
    pass

class NotFoundError(AppError):
    """Resource not found"""
    pass

class ExternalServiceError(AppError):
    """External service error"""
    pass