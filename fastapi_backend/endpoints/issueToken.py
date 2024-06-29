from fastapi import APIRouter, HTTPException, Request
from security.issue_jwt_token import create_access_token
from config import settings

app = APIRouter()

@app.post("/issue_token")
async def issue_token(request: Request):
    data = await request.json()
    api_key = data.get("api_key")
    print(f"Received API key: {api_key}")  # Debug print
    if api_key == settings.API_KEY:
        token = create_access_token({"sub": "user_id"})
        print(f"Issued token: {token}")  # Debug print
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")
