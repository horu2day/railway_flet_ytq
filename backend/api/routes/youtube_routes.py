from fastapi import APIRouter, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import utils.gemini as genai
from pydantic import BaseModel

router = APIRouter()

# 요청 데이터 모델 정의
class VideoRequest(BaseModel):
    url: str
    api_key: str

@router.post("/analyze")
async def analyze_video(request: VideoRequest):
    try:
        video_id = request.url.split('v=')[1].split('&')[0]
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        extracted_text = genai.extract_korean_text_from_image_url(thumbnail_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        
        question, answer = genai.generate_question_and_answer(extracted_text, transcript,request.api_key)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
async def summarize_video(request: VideoRequest):
    try:
        video_id = request.url.split('v=')[1].split('&')[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        

        summary = genai.generate_summary(transcript,request.api_key)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
