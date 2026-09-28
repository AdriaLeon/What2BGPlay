from fastapi import HTTPException, status


def get_current_user():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not implemented yet",
    )