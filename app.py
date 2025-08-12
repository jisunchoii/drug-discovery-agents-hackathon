"""
신약개발 어시스턴트 - 메인 애플리케이션
"""

import logging
import sys
import streamlit as st
from ui import setup_page, initialize_session, render_header, render_sidebar, display_messages, handle_input, add_greeting

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d | %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)


def main():
    """메인 함수"""
    setup_page()
    initialize_session()
    render_header()
    render_sidebar()
    
    if st.session_state.agent is None:
        st.error("AI 모델을 설정하는 중입니다. 잠시만 기다려주세요.")
        st.stop()
    
    add_greeting()
    display_messages()
    handle_input()


if __name__ == "__main__":
    main()
