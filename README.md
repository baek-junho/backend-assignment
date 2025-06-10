# Issue Management API

## 1. Project Structure
/ (project root)
├── app.py # Flask application and API implementation
├── issues.db # SQLite database (auto-generated)
├── venv/ # Python virtual environment
└── README.md # 실행 방법 및 테스트 가이드

## 2. Prerequisites

- Python 3.7 이상
- 가상환경 도구(venv)

## 3. Installation

1. 프로젝트 루트로 이동:
   ```bash
   cd <project-directory>

2. 가상환경 생성 및 활성화:
   bash
   복사
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate

3. 패키지 설지:
   pip install Flask Flask-SQLAlchemy

## 4. Running the Server
   python app.py
   서버 기본 주소 : http://localhost:8080

## 5. API Test
### 5.1 Create Issue
    post / Issue
