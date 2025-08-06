"""
신약개발 어시스턴트 - 스트리밍 및 대화 이력 관리 지원
해커톤용 위트있는 챗봇 인터페이스
"""

import streamlit as st
import time
import asyncio
import logging
import sys
from agents.drug_development_agent import create_drug_development_agent
from agents.meta_tooling_agent import agent as meta_agent  # 메타툴링 에이전트 import
from config import Settings
from strands.agent.conversation_manager import SlidingWindowConversationManager

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d | %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("streamlit")

# 페이지 설정
st.set_page_config(
    page_title="신약개발 어시스턴트",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """세션 상태 초기화"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "current_model" not in st.session_state:
        st.session_state.current_model = None
    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = SlidingWindowConversationManager(window_size=10)
    if "greetings" not in st.session_state:
        st.session_state.greetings = False

def create_agent(model_name, use_history=True):
    """에이전트 생성"""
    try:
        Settings.validate()
        if use_history:
            agent = create_drug_development_agent(
                model_name=model_name,
                conversation_manager=st.session_state.conversation_manager
            )
        else:
            agent = create_drug_development_agent(
                model_name=model_name
            )
        return agent, None
    except Exception as e:
        return None, str(e)

async def process_streaming_response(agent, question, message_placeholder):
    """줄바꿈이 포함된 스트리밍 응답 처리"""
    full_response = ""
    
    try:
        agent_stream = agent.stream_async(question)
        async for event in agent_stream:
            if isinstance(event, dict) and "data" in event:
                data = event["data"]
                full_response += data
                # 줄바꿈을 추가해서 표시
                formatted_response = full_response.replace('. ', '.\n\n').replace('! ', '!\n\n').replace('? ', '?\n\n')
                message_placeholder.markdown(formatted_response)
            elif isinstance(event, str):
                full_response += event
                # 줄바꿈을 추가해서 표시
                formatted_response = full_response.replace('. ', '.\n\n').replace('! ', '!\n\n').replace('? ', '?\n\n')
                message_placeholder.markdown(formatted_response)
                
    except Exception as e:
        logger.error(f"스트리밍 응답 처리 중 오류: {e}")
        message_placeholder.markdown("죄송합니다. 응답 생성 중 오류가 발생했습니다.")
    
    # 최종 응답도 포맷팅해서 반환
    final_formatted_response = full_response.replace('. ', '.\n\n').replace('! ', '!\n\n').replace('? ', '?\n\n')
    return final_formatted_response

def run_streaming_agent(agent, question):
    """스트리밍 에이전트 실행 - 단순화"""
    # Streamlit의 chat_message 컨테이너 사용 (Peccy 아바타)
    with st.chat_message("assistant", avatar="data/images/peccy.jpg"):
        message_placeholder = st.empty()
        
        # 비동기 함수를 동기적으로 실행
        try:
            full_response = asyncio.run(process_streaming_response(agent, question, message_placeholder))
            return full_response
        except Exception as e:
            logger.error(f"스트리밍 실행 중 오류: {e}")
            # 스트리밍 실패 시 일반 응답으로 폴백
            try:
                response = agent(question)
                message_placeholder.markdown(str(response))
                return str(response)
            except Exception as fallback_error:
                logger.error(f"폴백 응답 실행 중 오류: {fallback_error}")
                error_msg = "응답 생성 중 오류가 발생했습니다. 다시 시도해주세요."
                message_placeholder.markdown(error_msg)
                return error_msg

def display_chat_message(role, content):
    """채팅 메시지 표시 - Peccy 아바타 및 연구원 이모지 포함"""
    # AgentResult 객체를 문자열로 변환
    content_str = str(content)
    
    if role == "user":
        with st.chat_message("user", avatar="🧑‍🔬"):
            st.markdown(content_str)
    else:
        # Peccy 이미지를 어시스턴트 아바타로 사용
        with st.chat_message("assistant", avatar="data/images/peccy.jpg"):
            st.markdown(content_str)

def main():
    """메인 함수"""
    initialize_session_state()
    
    # 헤더 - Streamlit 컴포넌트로 변경
    st.title("💊 신약개발 어시스턴트 💊")
    st.subheader("생명과학 해커톤에 오신 걸 환영합니다!")
    st.divider()
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ AI 모델 설정")
        
        # 모델 선택
        model_options = list(Settings.AVAILABLE_MODELS.keys())
        selected_model = st.selectbox(
            "모델 선택:",
            ('Claude Sonnet 4.0', 'Claude 3.7 Sonnet', 'Claude 3.5 Sonnet v2', 'Claude 3.5 Haiku'),
            index=0
        )
        
        # 모델 정보 표시 - Streamlit 컴포넌트로 변경
        current_model_id = Settings.get_model_id(selected_model)
        with st.container():
            st.info(f"""
            **현재 모델:** {current_model_id}
            """)
        
        # 에이전트 생성/업데이트 (대화 이력 관리 무조건 적용)
        if (st.session_state.agent is None or 
            st.session_state.current_model != selected_model):
            
            with st.spinner("AI 모델 설정 중..."):
                agent, error = create_agent(selected_model, use_history=True)
                
                if agent:
                    st.session_state.agent = agent
                    st.session_state.current_model = selected_model
                    st.success("모델 설정 완료!")
                else:
                    st.error(f"모델 설정 실패: {error}")
                    st.stop()
        
        st.divider()
        
        # 메타툴링 설정
        st.header("🔧 메타툴링 설정")
        meta_tooling_enabled = st.toggle("메타툴링 활성화", value=False, help="활성화하면 도구 생성 요청이 메타툴링 에이전트로 전달됩니다")
        st.session_state.meta_tooling_enabled = meta_tooling_enabled
        
        st.divider()
        
        st.header("🔬 실험실 도구함")
        
        # 기능 설명 - Streamlit 컴포넌트로 변경
        with st.expander("사용 가능한 기능", expanded=False):
            st.markdown("""
            **분자량 계산기**  
            예: "C8H10N4O2의 분자량은?"
            
            **메타툴링 (도구 생성)**  
            예: "약물 상호작용 분석 도구 만들어줘"
            
            **연구 상담**  
            예: "신약개발 과정 설명해줘"
            """)
        
        # 대화 초기화 버튼
        if st.button("🔄 대화 초기화", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.greetings = False
            st.session_state.conversation_manager = SlidingWindowConversationManager(window_size=10)
            st.success("대화 이력이 초기화되었습니다!")
            st.rerun()
        
        st.divider()
        
        # 샘플 질문들
        st.header("💡 샘플 질문")
        sample_questions = [
            "C8H10N4O2 분자량 계산해줘",
            "약물 상호작용 분석 도구 만들어줘",
        ]
        
        for i, question in enumerate(sample_questions):
            if st.button(f"📝 {question}", key=f"sample_{i}", use_container_width=True):
                st.session_state.sample_question = question
        
        st.divider()
    
    # 에이전트가 설정되지 않은 경우 중단
    if st.session_state.agent is None:
        st.error("AI 모델을 설정하는 중입니다. 잠시만 기다려주세요.")
        st.stop()
    
    # 초기 인사말
    if not st.session_state.greetings:
        intro = "안녕하세요! 신약개발 어시스턴트입니다. 분자량 계산, 연구 상담 등을 도와드릴 수 있어요. 편안하게 질문해주세요!"
        st.session_state.messages.append({"role": "assistant", "content": intro})
        st.session_state.greetings = True
    
    # 채팅 기록 표시
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])
    
    # 샘플 질문 처리
    if "sample_question" in st.session_state:
        user_input = st.session_state.sample_question
        del st.session_state.sample_question
    else:
        # 사용자 입력
        user_input = st.chat_input("연구 질문을 입력하세요... (예: 카페인 분자량 계산해줘)")
    
    if user_input:
        # 사용자 메시지 추가 및 표시
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍🔬"):
            st.markdown(user_input)
        
        # 스트리밍 응답 생성
        try:
            # 사이드바 토글 상태에 따라 에이전트 선택
            if st.session_state.get('meta_tooling_enabled', False):
                # 메타툴링이 활성화된 경우 메타 에이전트 사용
                response = run_streaming_agent(meta_agent, user_input)
            else:
                # 일반 요청은 기본 에이전트로 처리
                response = run_streaming_agent(st.session_state.agent, user_input)
            
            # 응답 메시지 추가
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 성공 효과
            st.balloons()
            
        except Exception as e:
            error_msg = f"실험 실패: {e}\n\n다시 시도해주세요. 아마 카페인이 부족한 것 같네요!"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant", avatar="data/images/peccy.jpg"):
                st.markdown(error_msg)
        
        # 페이지 새로고침으로 최신 메시지 표시
        st.rerun()

if __name__ == "__main__":
    main()
