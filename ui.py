"""
Streamlit UI 컴포넌트
"""

import streamlit as st
import asyncio
import logging
from agents.drug_development_agent import create_drug_development_agent
from agents.meta_tooling_agent import create_meta_agent
from config import Settings
from strands.agent.conversation_manager import SlidingWindowConversationManager

logger = logging.getLogger("streamlit")


def setup_page():
    """페이지 설정"""
    st.set_page_config(
        page_title="신약개발 어시스턴트",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def initialize_session():
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


def create_agent_if_needed(model_name):
    """필요시 에이전트 생성"""
    try:
        Settings.validate()
        agent = create_drug_development_agent(
            model_name=model_name,
            conversation_manager=st.session_state.conversation_manager
        )
        return agent, None
    except Exception as e:
        return None, str(e)


async def process_streaming_response(agent, question, placeholder):
    """스트리밍 응답 처리"""
    full_response = ""
    try:
        agent_stream = agent.stream_async(question)
        async for event in agent_stream:
            if isinstance(event, dict) and "data" in event:
                full_response += event["data"]
            elif isinstance(event, str):
                full_response += event
            formatted = full_response.replace('. ', '.\n\n').replace('! ', '!\n\n').replace('? ', '?\n\n')
            placeholder.markdown(formatted)
    except Exception as e:
        logger.error(f"스트리밍 오류: {e}")
        placeholder.markdown("응답 생성 중 오류가 발생했습니다.")
    return full_response.replace('. ', '.\n\n').replace('! ', '!\n\n').replace('? ', '?\n\n')


def run_agent(agent, question):
    """에이전트 실행"""
    with st.chat_message("assistant", avatar="data/images/peccy.jpg"):
        placeholder = st.empty()
        try:
            return asyncio.run(process_streaming_response(agent, question, placeholder))
        except Exception as e:
            logger.error(f"에이전트 실행 오류: {e}")
            try:
                response = str(agent(question))
                placeholder.markdown(response)
                return response
            except Exception:
                error_msg = "응답 생성 중 오류가 발생했습니다."
                placeholder.markdown(error_msg)
                return error_msg


def render_header():
    """헤더 렌더링"""
    st.title("💊 신약개발 어시스턴트 💊")
    st.subheader("생명과학 해커톤에 오신 걸 환영합니다!")
    st.divider()


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.header("⚙️ AI 모델 설정")
        
        selected_model = st.selectbox(
            "모델 선택:",
            ('Claude Sonnet 4.0', 'Claude 3.7 Sonnet', 'Claude 3.5 Sonnet v2', 'Claude 3.5 Haiku'),
            index=0
        )
        
        st.info(f"**현재 모델:** {Settings.get_model_id(selected_model)}")
        
        if (st.session_state.agent is None or st.session_state.current_model != selected_model):
            with st.spinner("AI 모델 설정 중..."):
                agent, error = create_agent_if_needed(selected_model)
                if agent:
                    st.session_state.agent = agent
                    st.session_state.current_model = selected_model
                    st.success("모델 설정 완료!")
                else:
                    st.error(f"모델 설정 실패: {error}")
                    st.stop()
        
        st.divider()
        
        st.header("🔧 메타툴링 설정")
        st.session_state.meta_tooling_enabled = st.toggle(
            "메타툴링 활성화", 
            value=False, 
            help="도구 생성 요청이 메타툴링 에이전트로 전달됩니다"
        )
        
        st.divider()
        
        st.header("🔬 실험실 도구함")
        with st.expander("사용 가능한 기능", expanded=False):
            st.markdown("""
            **분자량 계산기**: "C8H10N4O2의 분자량은?"
            **메타툴링**: "약물 상호작용 분석 도구 만들어줘"
            **연구 상담**: "신약개발 과정 설명해줘"
            """)
        
        if st.button("🔄 대화 초기화", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.greetings = False
            st.session_state.conversation_manager = SlidingWindowConversationManager(window_size=10)
            st.success("대화 이력이 초기화되었습니다!")
            st.rerun()
        
        st.divider()
        
        st.header("💡 샘플 질문")
        samples = ["C8H10N4O2 분자량 계산해줘", "약물 상호작용 분석 도구 만들어줘"]
        for i, question in enumerate(samples):
            if st.button(f"📝 {question}", key=f"sample_{i}", use_container_width=True):
                st.session_state.sample_question = question


def display_messages():
    """메시지 표시"""
    for message in st.session_state.messages:
        avatar = "🧑‍🔬" if message["role"] == "user" else "data/images/peccy.jpg"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(str(message["content"]))


def handle_input():
    """사용자 입력 처리"""
    user_input = None
    
    if "sample_question" in st.session_state:
        user_input = st.session_state.sample_question
        del st.session_state.sample_question
    else:
        user_input = st.chat_input("연구 질문을 입력하세요... (예: 카페인 분자량 계산해줘)")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍🔬"):
            st.markdown(user_input)
        
        try:
            if st.session_state.get('meta_tooling_enabled', False):
                meta_agent = create_meta_agent(st.session_state.current_model)
                response = run_agent(meta_agent, user_input)
            else:
                response = run_agent(st.session_state.agent, user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.balloons()
        except Exception as e:
            error_msg = f"실험 실패: {e}\n\n다시 시도해주세요."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant", avatar="data/images/peccy.jpg"):
                st.markdown(error_msg)
        
        st.rerun()


def add_greeting():
    """초기 인사말"""
    if not st.session_state.greetings:
        intro = "안녕하세요! 신약개발 어시스턴트입니다. 분자량 계산, 연구 상담 등을 도와드릴 수 있어요. 편안하게 질문해주세요!"
        st.session_state.messages.append({"role": "assistant", "content": intro})
        st.session_state.greetings = True
