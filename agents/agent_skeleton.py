"""
🧬 신약개발 해커톤용 에이전트 템플릿

해커톤 참가자들이 커스텀 에이전트를 만들 때 사용할 수 있는 템플릿 파일입니다.
이 파일을 복사해서 수정하여 자신만의 전문 에이전트를 만들어보세요.

사용법:
1. 이 파일을 새로운 이름으로 복사 (예: my_custom_agent.py)
2. 특정 용도에 맞게 시스템 프롬프트 수정
3. 필요한 도구들 추가 또는 수정
4. 에이전트 생성 함수 업데이트
5. 애플리케이션에서 import하여 사용

작성자: [이름을 입력하세요]
생성일: [날짜를 입력하세요]
목적: [에이전트의 목적을 설명하세요]
"""

import boto3
from strands import Agent
from strands.models import BedrockModel
from config.settings import Settings

# 여기에 커스텀 도구들을 import하세요
# from tools.your_custom_tool import your_custom_tool

def create_custom_agent(model_name: str = None, conversation_manager=None):
    """
    신약개발용 커스텀 에이전트 생성
    
    Args:
        model_name (str): 사용할 모델명 (선택사항)
        conversation_manager: 대화 이력 관리자 (선택사항)
    
    Returns:
        Agent: 설정된 Strands 에이전트
    """
    
    # 모델 설정
    model_id = Settings.get_model_id(model_name)
    
    # BedrockModel 인스턴스 생성
    bedrock_model = BedrockModel(
        model_id=model_id,
        region_name=Settings.AWS_REGION
    )
    
    # 커스텀 시스템 프롬프트 정의
    system_prompt = """
    당신은 신약개발 전문 AI 어시스턴트입니다.
    
    [이 부분을 커스터마이징하세요]
    - 에이전트의 역할과 전문성 정의
    - 처리할 질문 유형 명시
    - 응답 톤과 스타일 설정
    - 도메인별 특수 지침 포함
    
    전문화 예시:
    - 임상시험 데이터 분석
    - 분자 특성 예측
    - 약물 상호작용 검사
    - 규제 준수 지원
    - 문헌 검토 및 요약
    
    응답 가이드라인:
    1. 정확하고 근거 기반의 정보 제공
    2. 명확하고 전문적인 언어 사용
    3. 가능한 경우 관련 출처 포함
    4. 중요한 결정에는 항상 전문가 상담 권장
    5. 가독성을 위한 응답 포맷팅
    
    주의: 이는 교육 및 연구 목적입니다.
    의학적 결정에는 반드시 자격을 갖춘 전문가와 상담하도록 안내하세요.
    """
    
    # 에이전트가 사용할 도구 목록
    # 여기에 커스텀 도구들을 추가하세요
    agent_tools = [
        # 예시: your_custom_tool,
        # 필요에 따라 더 많은 도구 추가
    ]
    
    # 대화 관리자 포함 여부에 따른 에이전트 생성
    if conversation_manager:
        agent = Agent(
            model=bedrock_model,
            system_prompt=system_prompt + "\n\n이전 대화 맥락을 활용하여 관련성 있는 응답을 제공하세요.",
            tools=agent_tools,
            conversation_manager=conversation_manager
        )
    else:
        agent = Agent(
            model=bedrock_model,
            system_prompt=system_prompt,
            tools=agent_tools
        )
    
    return agent

# 사용 예시 및 테스트
if __name__ == "__main__":
    """
    여기서 커스텀 에이전트를 테스트하세요
    """
    print("커스텀 신약개발 에이전트 테스트")
    print("=" * 40)
    
    try:
        # 에이전트 인스턴스 생성
        agent = create_custom_agent()
        
        # 샘플 쿼리로 테스트
        test_query = "안녕하세요, 어떤 도움을 받을 수 있나요?"
        response = agent(test_query)
        
        print(f"질문: {test_query}")
        print(f"응답: {response}")
        
    except Exception as e:
        print(f"에이전트 테스트 오류: {e}")
        print("AWS 자격 증명이 올바르게 설정되었는지 확인하세요.")

"""
🚀 해커톤 팁:

1. **전문화 아이디어:**
   - 화합물 라이브러리 분석
   - ADMET 특성 예측
   - 부작용 예측
   - 약물 재창출 분석
   - 임상시험 설계 지원

2. **도구 통합:**
   - 함께 작동하는 도구들 생성
   - 기존 도구를 빌딩 블록으로 활용
   - 도구 간 데이터 흐름 고려

3. **사용자 경험:**
   - 직관적인 프롬프트 설계
   - 유용한 오류 메시지 제공
   - 사용 예시 포함

4. **성능:**
   - 다양한 입력으로 테스트
   - 예외 상황 우아하게 처리
   - 응답 시간 최적화

5. **문서화:**
   - 에이전트 기능 문서화
   - 사용 예시 제공
   - 제한사항과 가정 포함

해커톤 프로젝트 화이팅! 🧬💊
"""
