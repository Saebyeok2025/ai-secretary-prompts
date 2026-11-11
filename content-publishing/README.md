# 책 기반 콘텐츠 발행 에이전트

책 원문 → 블로그·SNS 원고와 이미지 → 실제 계정 발행 → 게시 검증을 관리하는 로컬 에이전트 프로젝트입니다. 기존 ai-secretary-prompts 저장소의 콘텐츠 발행 모듈로 추가합니다.

## 현재 구현된 기능과 실행 환경

| 기능 | 구현 상태 |
|---|---|
| 블로그 다음 장 묶음 선택·실행 프롬프트 출력 | agent.py |
| 블로그 로컬 발행 증빙 파일·체크 항목 검사 | agent.py verify; 실제 사이트는 조회하지 않음 |
| SNS 독립 진도·카드 수·계정 설정 검사·프롬프트 출력 | sns.py |
| 원문 판독·원고 작성·이미지 생성·브라우저 편집·발행 | 연결된 도구를 가진 에이전트가 지침에 따라 수행 |
| 자체 게시 API·브라우저 실행 엔진·스케줄러·진도 자동 갱신 | 미구현 |
| GitHub Actions | 단위 테스트만 실행; 실제 발행 없음 |

Python만 실행해서 글이 발행되는 독립 프로그램이 아닙니다. Codex 등의 실제 도구 실행 환경이 필요하며, 이 묶음은 해당 환경의 내부 도구를 일반 Python 라이브러리로 제공하지 않습니다. 계정 비밀번호나 세션을 GitHub로 옮기지 않습니다.

## 로컬 준비

Python 3.10 이상, 외부 패키지 없이 실행합니다. 이 폴더에서:

```powershell
Copy-Item config.example.json config.local.json
Copy-Item state.example.json state.local.json
Copy-Item sns.config.example.json sns.config.local.json
Copy-Item sns.state.example.json sns.state.local.json
```

로컬 설정에 실제 원본 폴더·블로그 주소·SNS 계정/연결 프로필을 입력합니다. 공개 예제에는 실제 계정이 없습니다. 실제 계정명 변경은 로컬 최신 파일과 게시 화면으로 확인합니다. books 배열 순서가 책 처리 순서이며 목차를 확인해 등록합니다.

state의 completed는 책별 발행 검증 완료 장 목록입니다. 블로그와 SNS를 별도로 입력합니다. 기존 진행기록.json은 형식이 다르므로 그대로 복사하지 않습니다. 완료가 불확실한 장은 임의로 완료 처리하지 않습니다. 보조 코드는 첫 미완료 묶음을 고르므로 누락된 과거 기록이 있으면 실제 게시물과 대조하여 정리한 후 실행해야 합니다. 사용자 지시로 건너뛴 범위는 별도 이력에 남기고 자동 계획을 그대로 발행하지 않습니다.

```powershell
python agent.py plan
python agent.py prompt
python sns.py plan
python sns.py prompt
python -m unittest discover -s tests -v
```

plan/prompt는 계산·출력만 하며 설정·진도를 변경하지 않습니다.

## 에이전트 실행 요청

블로그:

> AGENTS.md와 docs/OPERATIONS.md 및 최신 로컬 운영 파일을 읽고 python agent.py prompt로 대상을 제안해줘. 진행기록과 실제 게시물로 확정한 뒤 원문을 읽고 원고·이미지를 저장해줘. 지정 계정에 편집·발행하고 실제 게시물의 제목·카테고리·이미지·서식을 확인한 후 기록해줘.

SNS:

> AGENTS.md와 docs/OPERATIONS.md, 최신 로컬 SNS 운영·계정 파일을 읽고 python sns.py prompt로 대상을 제안해줘. 독립 SNS 기록과 실제 게시물을 대조하고 카드 6~10장을 제작·검수해줘. 승인된 Instagram 업로드와 Threads·Facebook 연결 공유로 공개하고 서비스별 실제 게시물과 URL을 확인해줘. 부분 성공은 구분해 기록하고 중복 게시하지 마.

로컬 blog manifest 예시는 manifest.example.json입니다. 증빙 파일과 함께 output 아래에 저장한 후:

```powershell
python agent.py verify --manifest output/DATE_BOOK_CHAPTERS/manifest.json
```

이 검사는 파일과 운영자가 입력한 체크 값을 확인합니다. 이미지 픽셀·웹 게시 상태·실제 글꼴의 자동 검증이 아니며 진도도 자동 갱신하지 않습니다. 실제 게시 확인은 에이전트/운영자가 수행합니다.

## 운영 규칙

- 최신 통합 기준: docs/OPERATIONS.md. 블로그 세부 참고: docs/source-instructions/.
- 블로그 07:30 작업 시작. SNS 18:30 제작, 20:00 공개 목표, Asia/Seoul.
- 사용자 저서 46장을 2장씩, 완료 후 도파미네이션 미발행 장, 이후 가나다순.
- SNS는 블로그와 독립 진도. 기존 초기 지침의 ‘그날 아침과 같은 범위’는 폐기.
- 계정·서비스별 실제 게시물을 확인한 뒤 완료 기록. 부분 성공·중단은 별도 보존.
- 블로그 썸네일 1장+소주제 이미지 4~5장. SNS 카드 기본 8장(6~10장).
- 출력물·실제 설정·진도·책 원문·인증 정보는 PC/OneDrive에 보관.

이 저장소의 지침과 PC의 운영 원본이 달라지면 최신 사용자 지시를 반영하여 함께 갱신합니다. 설정·진도 원본은 한 곳으로 정하고 예제 상태와 이중 관리하지 않습니다.

## 예약과 이전

GitHub 업로드는 예약 활성화를 뜻하지 않습니다. 기존 로컬 예약의 중복 여부를 확인한 뒤 실행 환경에서 지침 경로를 연결합니다. 기존 예약을 이 배포본이 변경하지 않습니다. PC 자료와 로그인 브라우저를 사용하면 PC·앱·연결이 필요합니다. GitHub Actions에서 이 PC의 Chrome 세션을 그대로 사용할 수 없습니다.

라이선스는 상위 저장소 정책과 소유자의 선택을 따릅니다. 실제 공개 전 git status로 민감 파일 포함 여부를 확인합니다. .gitignore는 이미 추적된 파일을 제거하지 않습니다.
