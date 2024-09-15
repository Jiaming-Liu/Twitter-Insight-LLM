from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from twitter_data_ingestion import TwitterExtractor
from config import TWITTER_AUTH_TOKEN

app = FastAPI()

class TokenRequest(BaseModel):
    token: str

class FetchTweetsRequest(BaseModel):
    page_url: str
    start_date: str
    end_date: str

class TweetResponse(BaseModel):
    text: str
    author_name: str
    author_handle: str
    date: str
    lang: str
    url: str
    mentioned_urls: List[str]
    is_retweet: bool
    media_type: str
    images_urls: Optional[List[str]]
    num_reply: int
    num_retweet: int
    num_like: int

twitter_extractor = TwitterExtractor()

@app.post("/set_token")
def set_token(request: TokenRequest):
    try:
        twitter_extractor.set_token(request.token)
        return {"message": "Token set successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/fetch_tweets", response_model=List[TweetResponse])
def fetch_tweets(request: FetchTweetsRequest):
    try:
        tweets = twitter_extractor.fetch_tweets(request.page_url, request.start_date, request.end_date)
        return tweets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
