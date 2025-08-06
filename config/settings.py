"""
애플리케이션 설정
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Settings:
    """애플리케이션 설정 클래스"""
    
    # AWS 설정
    AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
    
    # 사용 가능한 모델들
    AVAILABLE_MODELS = {
        "Claude Sonnet 4.0": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "Claude 3.7 Sonnet": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        "Claude 3.5 Sonnet v2": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "Claude 3.5 Haiku": "anthropic.claude-3-5-haiku-20241022-v1:0", 
    }
    
    # 기본 모델
    DEFAULT_MODEL = "anthropic.claude-sonnet-4-20250514-v1:0"
    DEFAULT_TEMPERATURE = 0.3
    
    @classmethod
    def get_model_id(cls, model_name: str = None) -> str:
        """모델 이름으로 모델 ID 반환"""
        if not model_name:
            return cls.DEFAULT_MODEL
        return cls.AVAILABLE_MODELS.get(model_name, cls.DEFAULT_MODEL)
    
    @classmethod
    def validate(cls):
        """AWS 자격증명 확인 (boto3가 자동으로 처리)"""
        # boto3는 자동으로 AWS 자격증명을 찾습니다:
        # 1. 환경변수 (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        # 2. AWS credentials 파일 (~/.aws/credentials)
        # 3. IAM 역할 (EC2에서 실행 시)
        return True
