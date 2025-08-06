"""
분자량 계산기 도구
"""

from strands import tool
import re


@tool
def molecular_weight_calculator(formula: str) -> str:
    """화학식을 입력받아 분자량을 계산합니다"""
    
    # 원소별 원자량 (g/mol)
    atomic_weights = {
        'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
        'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
        'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
        'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
        'Fe': 55.845, 'Cu': 63.546, 'Zn': 65.38, 'Br': 79.904, 'I': 126.904
    }
    
    try:
        # 화학식에서 원소와 개수 추출
        pattern = r'([A-Z][a-z]?)(\d*)'
        matches = re.findall(pattern, formula.replace(' ', ''))
        
        if not matches:
            return "올바른 화학식을 입력해주세요. 예: C8H10N4O2"
        
        total_weight = 0
        composition = []
        
        for element, count in matches:
            if element not in atomic_weights:
                return f"알 수 없는 원소입니다: {element}"
            
            count = int(count) if count else 1
            weight = atomic_weights[element] * count
            total_weight += weight
            composition.append(f"{element}: {count}개")
        
        # 유명한 화합물인지 확인
        famous_compounds = {
            'C8H10N4O2': '카페인 ☕ (연구자의 필수 연료!)',
            'C21H30O2': '테스토스테론 💪',
            'C43H66N12O12S2': '인슐린 (일부) 💉',
            'C2H6O': '에탄올 🍺 (실험 후 스트레스 해소용?)',
            'H2O': '물 💧 (생명의 근원)',
            'C6H12O6': '포도당 🍯 (뇌의 연료)',
            'C9H8O4': '아스피린 💊'
        }
        
        compound_info = famous_compounds.get(formula.replace(' ', ''), '')
        
        result = f"""🧪 분자량 계산 결과:
            화학식: {formula}
            구성: {', '.join(composition)}
            분자량: {total_weight:.2f} g/mol

            {compound_info}

            💡 팁: 카페인 없이는 신약개발도 불가능하죠!
            """
        
        return result
        
    except Exception as e:
        return f"계산 오류: {e}\n올바른 화학식을 입력해주세요. 예: C8H10N4O2 (카페인)"
