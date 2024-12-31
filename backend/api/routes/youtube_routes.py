from fastapi import APIRouter, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

router = APIRouter()

@router.post("/analyze")
async def analyze_video(url: str, api_key: str):
    try:
        video_id = url.split('v=')[1].split('&')[0]
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        genai.configure(api_key=api_key)
        extracted_text = extract_korean_text_from_image_url(thumbnail_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        
        question, answer = generate_question_and_answer(extracted_text, transcript)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
async def summarize_video(url: str, api_key: str):
    try:
        video_id = url.split('v=')[1].split('&')[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        
        genai.configure(api_key=api_key)
        summary = generate_summary(transcript)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
