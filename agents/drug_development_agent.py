"""
신약개발 어시스턴트 에이전트
해커톤용 위트있는 신약개발 관련 도구들을 제공하는 에이전트
"""

import boto3
from strands import Agent
from strands.models import BedrockModel
from tools.molecular_calculator import molecular_weight_calculator
from config import Settings


def create_drug_development_agent(model_name: str = None, temperature: float = None, conversation_manager=None):
    """신약개발 어시스턴트 에이전트 생성"""
    
    # 모델 설정
    model_id = Settings.get_model_id(model_name)
    temp = temperature if temperature is not None else Settings.DEFAULT_TEMPERATURE
    
    # BedrockModel 생성
    bedrock_model = BedrockModel(
        model_id=model_id,
        region_name=Settings.AWS_REGION,
        temperature=temp,
    )
    
    # 공통 시스템 프롬프트 (도구 사용 안내 문구 제거)
    system_prompt = """
    당신은 신약개발 전문 AI 어시스턴트입니다.
    
    신약개발 해커톤에 참여한 연구자들을 도와주는 것이 목표입니다.
    다음과 같은 기능을 제공합니다:
    
    - molecular_weight_calculator: 화학식을 입력받아 분자량을 계산합니다
      예: "C8H10N4O2" (카페인) 입력 시 분자량과 관련 정보 제공
    
    답변 형식 규칙:
    1. 깔끔하고 읽기 쉽게 문단을 나누어 답변하세요
    2. 필요시 줄바꿈을 적절히 사용하세요
    3. 이모지는 답변당 최대 1개만 사용하세요
    4. HTML 태그를 사용하지 마세요. 순수한 마크다운 텍스트로만 답변하세요
    5. 긴 답변은 적절히 문단으로 나누어 가독성을 높이세요
    6. 도구 사용 안내는 하지 마세요. UI에서 별도로 표시됩니다.
    7. 바로 결과와 설명으로 시작하세요.
    
    전문적이고 정확한 정보를 제공하되, 친근하게 답변해주세요.
    실제 의학적 조언이나 신약개발 결정에는 전문가와 상담하라고 안내해주세요.
    해커톤 참가자들에게 도움이 되는 정보와 격려를 제공하세요.
    
    신약개발의 복잡성을 이해하고, 연구자들을 지원하는 톤으로 대화하세요.
    """
    
    # 에이전트 생성 (대화 이력 관리자 포함 여부에 따라)
    if conversation_manager:
        agent = Agent(
            model=bedrock_model,
            system_prompt=system_prompt + "\n이전 대화 내용을 참고하여 맥락에 맞는 답변을 제공하세요.",
            tools=[molecular_weight_calculator],
            conversation_manager=conversation_manager
        )
    else:
        agent = Agent(
            model=bedrock_model,
            system_prompt=system_prompt,
            tools=[molecular_weight_calculator]
        )
    
    return agent


# 기본 에이전트 인스턴스 (하위 호환성을 위해)
simple_agent = create_drug_development_agent()
