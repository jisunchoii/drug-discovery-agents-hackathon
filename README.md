# 🧬 신약개발 어시스턴트 (해커톤 에디션)

Strands Agents를 활용한 위트있는 신약개발 관련 AI 어시스턴트

![UI Screenshot](data/images/ui.png)

## 목적
신약개발 해커톤 참가자들의 스트레스 해소와 창의적 영감을 위한 재미있는 도구들을 제공합니다!

## 프로젝트 구조

```
drug-discovery-agents/
├── agents/                     # AI 에이전트 모듈
│   ├── drug_development_agent.py    # 메인 신약개발 에이전트 (예시)
│   ├── meta_tooling_agent.py        # 메타툴링 에이전트 (도구 생성)
│   └── agent_skeleton.py            # 에이전트 템플릿 (starter file)
├── tools/                      # 도구 모듈
│   ├── molecular_calculator.py      # 분자량 계산기 (예시)
│   └── tool_skeleton.py             # 도구 템플릿 (starter file)
├── config/                     # 설정 파일
│   └── settings.py               
├── data/                       # 데이터 및 이미지
│   └── images/
│       ├── ui.png                   
│       └── peccy.jpg                
├── app.py                     # Streamlit 메인 애플리케이션
├── requirements.txt           # Python 패키지 의존성
├── .env.example               # 환경변수 예시 파일
└── README.md                  # 프로젝트 문서
```

## 설치 및 실행 

### 자동 실행 스크립트 사용
```bash
# 실행 권한 부여 (최초 1회)
chmod +x run.sh

# 애플리케이션 실행
./run.sh
```

`run.sh` 스크립트는 다음 작업을 자동으로 수행합니다:
- 가상환경 생성 (없는 경우)
- 가상환경 활성화
- 필요한 패키지 설치
- 환경변수 파일 생성 (없는 경우)
- Streamlit 애플리케이션 실행

## Q CLI 프로필 및 컨텍스트 설정
터미널 상에서 Q CLI를 설정하여 자연어 기반으로 에이전트 개발을 수행할 수 있습니다.

### 초기 설정
```bash
# Q CLI 접근
q chat

# 컨텍스트 파일 추가
/context add context/context.md

# 설정 확인
"현재 프로젝트 구조를 설명해주세요"
"어떤 것부터 시작하면 될까요?"
```

> **💡 참고**: 가상환경을 사용하면 시스템 Python 환경과 분리되어 패키지 충돌을 방지할 수 있습니다.

## Starter 기능

- **분자량 계산기**: 화학식 입력 시 분자량 계산
- **일반 대화**: 신약개발 관련 격려와 위트있는 대화

## 주의사항

이 도구들은 교육 목적입니다. 
실제 의학적 조언이나 신약개발 결정에는 전문가와 상담하세요!
