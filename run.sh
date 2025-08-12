#!/bin/bash

echo "******** 신약개발 어시스턴트 환경 설정 중 ********"

# Python 3.11 사용 확인
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11이 필요합니다. strands-agents는 Python 3.10+ 버전이 필요합니다."
    exit 1
fi

# 가상환경 생성 (최초 1회)
if [ ! -d "venv" ]; then
    echo "******** 가상환경 생성 중 (Python 3.11 사용) ********"
    python3.11 -m venv venv
fi

# 가상환경 활성화
echo "******** 가상환경 활성화 중 ********"
source venv/bin/activate

# 패키지 설치 확인 및 설치
if [ ! -f "venv/.packages_installed" ]; then
    echo "******** pip 업그레이드 중 ********"
    pip install --upgrade pip
    
    echo "******** 패키지 설치 중 ********"
    pip install -r requirements.txt
    
    # 설치 완료 마커 생성
    touch venv/.packages_installed
    echo "******** 패키지 설치 완료! ********"
else
    echo "******** 패키지가 이미 설치되어 있습니다 ********"
fi

# 환경변수 파일 확인
if [ ! -f ".env" ]; then
    echo "******** 환경변수 파일 생성 중 ********"
    cp .env.example .env
fi

# Streamlit 실행
echo "******** 🚀 애플리케이션 실행 중 ********"
streamlit run app.py
