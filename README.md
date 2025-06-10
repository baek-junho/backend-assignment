Issue Management API

1. Project Structure

/ (project root)
├── app.py            # Flask application and API implementation
├── issues.db         # SQLite database (auto-generated)
├── venv/             # Python virtual environment
└── README.md         # 실행 방법 및 테스트 가이드

2. Prerequisites

Python 3.7 이상

가상환경 도구(venv)

3. Installation

프로젝트 루트로 이동:

cd <project-directory>

가상환경 생성 및 활성화:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

의존 패키지 설치:

pip install Flask Flask-SQLAlchemy

4. Running the Server

python app.py

서버 기본 주소: http://localhost:8080

5. API Endpoints & Testing

5.1 Create Issue

POST /issue

Request Body (JSON):

{
  "title": "버그 수정 필요",      # 필수
  "description": "로그인 오류 발생",  # 선택
  "userId": 1                     # 선택
}

Example:

curl -X POST http://localhost:8080/issue \
     -H "Content-Type: application/json" \
     -d '{"title":"버그 수정 필요","description":"로그인 오류 발생","userId":1}'

5.2 List Issues

GET /issues

Query Parameter: status (옵션)

Examples:

# 전체 조회
curl http://localhost:8080/issues

# 상태 필터링
curl http://localhost:8080/issues?status=IN_PROGRESS

5.3 Get Issue Details

GET /issue/<id>

Example:

curl http://localhost:8080/issue/1

5.4 Update Issue

PATCH /issue/<id>

Request Body (JSON):

title, description, status, userId 중 변경할 필드만 포함

Example:

curl -X PATCH http://localhost:8080/issue/1 \
     -H "Content-Type: application/json" \
     -d '{"status":"COMPLETED"}'

6. Error Responses

모든 오류는 JSON 형태로 반환됩니다:

{
  "error": "에러 메시지",
  "code": 400
}

적절한 HTTP 상태 코드(400, 404 등)와 함께 응답됩니다.

