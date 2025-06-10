from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

# --- Flask & SQLAlchemy 설정 ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///issues.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 상태 Enum 정의 ---
class StatusEnum(enum.Enum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

# --- 모델 정의 ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Issue(db.Model):
    id = db.Column(db.Integer, Primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.Enum(StatusEnum), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- DB 초기화 및 샘플 사용자 추가 ---
@app.before_first_request
def create_table():
    db.create_all()
    if not User.query.first():
        users = [
            User(id=1, name='김개발'),
            User(id=2, name='이디자인'),
            User(id=3, name='박기획')
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()

# --- 공통 에러 ---
def error_response(message, code=400):
    return jsonify({'error': message, 'code':code}), code

# --- 이슈 생성 [POST] / issue ---
@app.route('/issue', methods=['POST'])
def create_issue():
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return error_response('title은 필수입니다.', 400)
    description = data.get('description')
    user_id = data.get('userid')

    if user_id is not None:
        user = User.query.get(user_id)
        if not user:
            return error_response('존재하지 않는 사용자입니다.', 400)
        status = StatusEnum.IN_PROGRESS
    else:
        user = None
        status = StatusEnum.PENDING

    issue = Issue(title=title, description=description, status=status, user=user)
    db.session.add(issue)
    db.session.commit()
    return jsonify(issue_to_dict(issue)), 201

# --- 이슈 목록 조회 [GET] / issues ---
@app.route('/issue', methods=['GET'])
def list_issues():
    status_param = request.args.get('status')
    query = Issue.query
    if status_param:
        try:
            status_enum = StatusEnum(status_param)
        except ValueError:
            return error_response('잘못된 상태값입니다.', 400)
        query = query.filter_by(status=status_enum)
    issues = query.all()
    return jsonify({'issues': [issue_to_dict(issue) for issue in issues]}), 200

# --- 이슈 상세 조회 [GET] /issue/<id> ---
@app.route('/issue/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify(issue_to_dict(issue)), 200

# --- 이슈 수정 [PATCH] /issue/<id> ---
@app.route('/issue/<int:issue_id>', methods=['PATCH'])
def update_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    if issue.status in (StatusEnum.COMPLETED, StatusEnum.CANCELLED):
        return error_response('완료되거나 취소된 이슈는 수정할 수 없습니다.', 400)

    data = request.get_json() or {}
    if 'title' in data:
        issue.title = data['title']
    if 'description' in data:
        issue.description = data['description']

    if 'status' in data:
        try:
            new_status = StatusEnum(data['status'])
        except ValueError:
            return error_response('잘못된 상태값입니다.', 400)
        # 담당자 없는 상태에서 IN_PROGRESS/COMPLETED 불가
        if new_status not in (StatusEnum.PENDING, StatusEnum.CANCELLED) and issue.user_id is None:
            return error_response('담당자 없는 상태에서 해당 상태로 변경할 수 없습니다.', 400)
        issue.status = new_status

    if 'userId' in data:
        user_id = data['userId']
        if user_id is None:
            issue.user = None
            issue.status = StatusEnum.PENDING
        else:
            user = User.query.get(user_id)
            if not user:
                return error_response('존재하지 않는 사용자입니다.', 400)
            issue.user = user
            if issue.status == StatusEnum.PENDING:
                issue.status = StatusEnum.IN_PROGRESS

    db.session.commit()
    return jsonify(issue_to_dict(issue)), 200

# --- 모델을 dict로 변환 ---
def issue_to_dict(issue):
    result = {
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'status': issue.status.value,
        'createdAt': issue.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updatedAt': issue.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
    if issue.user:
        result['user'] = {'id': issue.user.id, 'name': issue.user.name}
    return result

# --- 앱 실행 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
