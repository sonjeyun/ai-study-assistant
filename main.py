import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from datetime import datetime
from openai import OpenAI
from typing import List, Optional

load_dotenv()
app = FastAPI()

# OpenAI 클라이언트 설정
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://copa.codyssey.kr/v1" 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase 초기화
if not firebase_admin._apps:
    firebase_raw_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if firebase_raw_json:
        try:
            firebase_info = json.loads(firebase_raw_json)
            cred = credentials.Certificate(firebase_info)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"❌ Firebase 에러: {e}")

db = firestore.client()

# --- 데이터 모델 정의 ---
class StudyData(BaseModel):
    date: str
    minutes: int
    subject: str

class Conversation(BaseModel):
    user_msg: str
    ai_msg: str

class ChatRequest(BaseModel):
    message: str

# --- 1. 학습 데이터 API (CRUD + Summary) ---

@app.post("/api/data")
async def add_data(log: StudyData):
    doc_ref = db.collection("data").document()
    doc_ref.set({
        "date": log.date,
        "minutes": log.minutes,
        "subject": log.subject,
        "created_at": datetime.now()
    })
    return {"id": doc_ref.id, "status": "success"}

@app.get("/api/data")
async def get_data_list():
    logs = []
    docs = db.collection("data").order_by("created_at", direction=firestore.Query.DESCENDING).stream()
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        logs.append(d)
    return logs

@app.put("/api/data/{doc_id}")
async def update_data(doc_id: str, log: StudyData):
    doc_ref = db.collection("data").document(doc_id)
    doc_ref.update({
        "date": log.date,
        "minutes": log.minutes,
        "subject": log.subject
    })
    return {"status": "success"}

@app.delete("/api/data/{doc_id}")
async def delete_data(doc_id: str):
    db.collection("data").document(doc_id).delete()
    return {"status": "success"}

@app.get("/api/data/summary")
async def get_data_summary():
    docs = db.collection("data").stream()
    total_minutes = 0
    count = 0
    subjects = []
    
    for doc in docs:
        d = doc.to_dict()
        total_minutes += d['minutes']
        count += 1
        subjects.append(d['subject'])
    
    summary = {
        "total_count": count,
        "total_minutes": total_minutes,
        "average_minutes": round(total_minutes / count, 1) if count > 0 else 0,
        "subjects": list(set(subjects))
    }
    return summary

# --- 2. 대화 기록 API (요구사항 6번) ---

@app.post("/api/conversations")
async def save_conversation(conv: Conversation):
    doc_ref = db.collection("conversations").document()
    doc_ref.set({
        "user_msg": conv.user_msg,
        "ai_msg": conv.ai_msg,
        "timestamp": datetime.now()
    })
    return {"id": doc_ref.id, "status": "success"}

@app.get("/api/conversations")
async def get_conversations():
    convs = []
    docs = db.collection("conversations").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        if "timestamp" in d and d["timestamp"]:
            d["timestamp"] = d["timestamp"].isoformat()
        convs.append(d)
    return convs

@app.get("/api/conversations/{doc_id}")
async def get_conversation_detail(doc_id: str):
    doc = db.collection("conversations").document(doc_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다.")
    d = doc.to_dict()
    d["id"] = doc.id
    if "timestamp" in d and d["timestamp"]:
        d["timestamp"] = d["timestamp"].isoformat()
    return d

@app.delete("/api/conversations/{doc_id}")
async def delete_conversation(doc_id: str):
    db.collection("conversations").document(doc_id).delete()
    return {"status": "success"}

# --- 3. AI 챗봇 API ---

@app.post("/api/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        summary = await get_data_summary()
        summary_text = f"총 학습 횟수: {summary['total_count']}회, 총 시간: {summary['total_minutes']}분. 과목: {', '.join(summary['subjects'])}"

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": f"당신은 학습 비서입니다. 사용자의 데이터({summary_text})를 참고하여 따뜻하게 답변하세요."},
                {"role": "user", "content": request.message}
            ]
        )
        ai_answer = response.choices[0].message.content

        # 대화 자동 저장
        db.collection("conversations").add({
            "user_msg": request.message,
            "ai_msg": ai_answer,
            "timestamp": datetime.now()
        })

        return {"answer": ai_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "AI 학습 비서 서버 작동 중"}