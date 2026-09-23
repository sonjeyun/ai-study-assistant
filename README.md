# 📝 AI 학습 비서 (AI Study Assistant)

## 📌 서비스 소개
학습자가 매일의 **학습 기록(과목·시간·날짜)** 을 남기고,
AI가 이 데이터를 분석해 **맞춤형 피드백**을 제공하는 풀스택 웹 서비스입니다.

**해결하는 문제**
- 학습 기록을 흩어지지 않게 한 곳에 저장/관리
- 단순 기록을 넘어, AI가 데이터를 기반으로 학습 습관을 분석·조언
- 과거 AI 대화 내역을 다시 불러와 복습 가능

---

## 🛠 기술 스택

| 구분 | 기술 |
|------|------|
| **Frontend** | HTML, CSS, JavaScript (Vanilla) |
| **Backend** | Python 3.10 이상, FastAPI |
| **Database** | Firebase Firestore |
| **AI** | OpenAI SDK (Codyssey API, gpt-5-mini) |
| **배포** | Vercel(프론트) / Render(백엔드) |

---

## 🌐 배포 URL

| 구분 | 주소 |
|------|------|
| 🎨 **프론트엔드** | https://ai-study-assistant-beta-six.vercel.app/ |
| 🔧 **백엔드 API** | https://ai-study-assistant-2o8n.onrender.com |
| 📚 **Swagger 문서** | https://ai-study-assistant-2o8n.onrender.com/docs |

> ⚠️ Vercel 주소는 본인 실제 주소로 교체하세요!

---

## 💻 로컬 실행 방법

```bash
# 1. 저장소 클론
git clone https://github.com/사용자명/저장소명.git
cd 저장소명

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 환경 변수(.env) 파일 생성 (아래 참고)

# 5. 서버 실행
uvicorn main:app --reload
```
→ 실행 후 브라우저에서 `http://localhost:8000/docs` 접속

---

## 🔑 환경 변수 목록 (.env)

```env
# OpenAI(Codyssey) API 키
OPENAI_API_KEY=your_api_key_here

# Firebase 서비스 계정 (JSON 전체를 한 줄 문자열로)
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account", ...}
```

| 변수명 | 설명 |
|--------|------|
| `OPENAI_API_KEY` | AI 챗봇 호출용 API 키 |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Firestore 연동용 인증 정보 |

> ⚠️ `.env`는 절대 GitHub에 올리지 마세요! (`.gitignore`에 포함)

---

## 📸 제출 스크린샷

### 1. 데이터 요약이 보이는 채팅 화면 (질문 + 답변)
> AI에게 질문하고, 학습 데이터 기반 답변을 받는 화면


<img width="814" height="611" alt="image" src="https://github.com/user-attachments/assets/d33c302a-61e9-4140-8afd-f67a7af1e6b2" />


<img width="768" height="159" alt="image" src="https://github.com/user-attachments/assets/b630a052-fc9d-4f2c-aecc-b0ad0a14975e" />


### 2. 데이터 관리 화면 (CRUD 동작)
> 학습 기록 추가/수정/삭제가 동작하는 화면

<img width="813" height="564" alt="image" src="https://github.com/user-attachments/assets/ae1ac76c-38e6-4d0c-8e30-eb3fc629505c" />


### 3. 대화 기록 화면 (불러오기 동작)
> 저장된 과거 대화를 클릭해 다시 불러오는 화면


<img width="280" height="214" alt="image" src="https://github.com/user-attachments/assets/e85d5069-0a7d-4410-85af-c0a1c2d3ab4f" />

---

## 📂 주요 API 목록

| 메서드 | 경로 | 기능 |
|--------|------|------|
| GET | `/api/data` | 학습 기록 조회 |
| POST | `/api/data` | 기록 추가 |
| PUT | `/api/data/{id}` | 기록 수정 |
| DELETE | `/api/data/{id}` | 기록 삭제 |
| GET | `/api/data/summary` | 학습 요약 통계 |
| POST | `/api/chat` | AI 챗봇 질문 |
| GET | `/api/conversations` | 대화 기록 조회 |


