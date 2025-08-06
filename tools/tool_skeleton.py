"""
신약개발 해커톤용 도구 템플릿

이 파일을 복사해서 자신만의 도구를 만들어보세요!

사용법:
1. 파일명을 원하는 도구명으로 변경 (예: drug_analyzer.py)
2. 함수명도 파일명과 동일하게 변경
3. 설명과 로직 구현
4. 테스트 후 사용

작성자: [이름]
목적: [도구 목적]
"""

from strands import tool

@tool
def my_custom_tool(input_data: str) -> str:
    """
    커스텀 도구 설명을 여기에 작성하세요
    
    예: 약물명을 입력받아 기본 정보를 제공하는 도구
    """
    
    try:
        # 입력 검증
        if not input_data.strip():
            return "입력 데이터를 제공해주세요."
        
        # 여기에 실제 로직 구현
        result = f"입력된 '{input_data}'에 대한 처리 결과입니다."
        
        # 결과 반환
        return f"""
        **도구 실행 결과**

        입력: {input_data}
        결과: {result}

        참고: 실제 의학적 결정에는 전문가와 상담하세요.
        """.strip()
        
    except Exception as e:
        return f"오류 발생: {str(e)}"

# 테스트
if __name__ == "__main__":
    print("도구 테스트:")
    print(my_custom_tool("테스트 입력"))
