from fastapi import APIRouter, HTTPException
from auth.authmanager import AuthManager

router = APIRouter()
auth_manager = AuthManager()

@router.post("/google")
async def google_login(id_token: str):
    token, user = await auth_manager.sign_in_with_google(id_token)
    if token and user:
        return {"token": token, "user": user}
    raise HTTPException(status_code=401, message="Authentication failed")