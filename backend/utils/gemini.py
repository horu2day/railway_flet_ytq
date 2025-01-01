# backend/utils/gemini.py
from PIL import Image
import requests
import io
import google.generativeai as genai

# Gemini Pro Vision 모델 선택
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def extract_korean_text_from_image_url(image_url):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        
        prompt_parts = [
            "이 이미지에서 한국어 문장을 추출해줘. 만약 한국어 문장이 없다면 아무것도 출력하지 마.",
            image
        ]
        response = model.generate_content(prompt_parts, stream=False)
        return response.text.strip()
    except Exception as e:
        print(f"오류 발생: {e}")
        return ""

def generate_question_and_answer(extracted_text, transcript,api_key, question=None):
    try:
        genai.configure(api_key=api_key)
        if question:
            question_text = question
        else:
            question_prompt = f"""
            주어진 문장: "{extracted_text}"
            위 문장에서 사람들이 가장 궁금해할 만한 핵심 질문을 하나 만들어줘.
            질문은 한국어로 작성하고, 간결하게 만들어줘.
            """
            question_response = model.generate_content(question_prompt, stream=False)
            question_text = question_response.text.strip()

        answer_prompt = f"""
        질문: "{question_text}"
        Transcript: "{transcript}"
        위 질문에 대한 답을 Transcript에서 찾아서 한국어로 알려줘.
        답변은 Concise하게 작성하고, 만약 답을 찾을 수 없다면 "답변을 찾을 수 없습니다." 라고 출력해줘.
        """
        answer_response = model.generate_content(answer_prompt, stream=False)
        return question_text, answer_response.text.strip()
    except Exception as e:
        print(f"오류 발생: {e}")
        return None, None

def generate_summary(transcript,api_key: str):
    try:
        genai.configure(api_key=api_key)
        summary_prompt = f"""
        Transcript: "{transcript}"
        다음 유튜브 영상의 내용을 전체적으로 파악하고 주요 포인트들을 빠짐없이 설명해주세요.
        """
        summary_response = model.generate_content(summary_prompt, stream=False)
        return summary_response.text.strip()
    except Exception as e:
        print(f"오류 발생: {e}")
        return None