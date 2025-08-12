#!/bin/bash

echo "******** 신약개발 어시스턴트 환경 설정 중 ********"

if [ ! -d "venv" ]; then
    echo "******** 가상환경 생성 중 ********"
    python3 -m venv venv
fi

# 가상환경 활성화
echo "******** 가상환경 활성화 중 ********"
source venv/bin/activate

# 패키지 설치
echo "******** 패키지 설치 중 ********"
pip install -r requirements.txt

 환경변수 파일 확인
if [ ! -f ".env" ]; then
    echo "******** 환경변수 파일 생성 중 ********"
    cp .env.example .env
fi

# Streamlit 실행
echo "******** 🚀 애플리케이션 실행 중 ********"
streamlit run app.py
