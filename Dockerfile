# Python 3.8 베이스 이미지 사용
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 MySQL 클라이언트 설치
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 8000 노출
EXPOSE 8000

# Django 개발 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]