from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from .auth import authenticate_user, create_access_token, decode_token
from .models import UserLogin, Token
from .services.aggregator import get_news_by_interest
from .services.summarizer import summarize_text

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBearer()

@app.post("/api/login", response_model=Token)
def login(login_data: UserLogin):
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token({"sub": login_data.username, "interest": user["interest"]})
    return {"access_token": token, "token_type": "bearer", "interest": user["interest"]}

@app.get("/api/news")
def get_news(domain: str = None, credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalide")
    interest = domain or payload.get("interest", "general")
    articles = get_news_by_interest(interest)
    for a in articles:
        if len(a["summary"]) > 150:
            a["summary"] = summarize_text(a["summary"])
    return articles