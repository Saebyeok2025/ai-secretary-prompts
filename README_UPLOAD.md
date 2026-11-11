# 기존 저장소에 추가하기

대상: https://github.com/Saebyeok2025/ai-secretary-prompts

이 묶음은 기존 README·00_core.md·다른 모듈을 덮어쓰지 않습니다. 압축을 풀어 **안쪽의 `content-publishing/`, `modules/`, `.github/` 폴더와 이 안내 파일**을 기존 저장소 루트에 추가하세요. 동일 이름의 파일이 이미 있다면 변경 내용을 비교한 후 병합합니다.

## GitHub 웹에서 추가

1. 저장소에서 Add file → Upload files를 엽니다.
2. 압축 파일 자체가 아니라 압축을 푼 파일·폴더를 올립니다. `ai-secretary-content-upload` 바깥 폴더가 한 겹 더 들어가지 않게 합니다.
3. 변경 목록에 PDF, 실제 계정 설정, 진행기록, 로그인 파일이 없는지 확인하고 커밋합니다.
4. 기존 README의 모듈 목록에 아래 한 줄을 추가합니다.

```markdown
- [콘텐츠 발행 에이전트](modules/05-content-publishing.md): 책 원문 기반 블로그·인스타그램 제작, 발행, 검증 운영 지침과 보조 코드.
```

`.github/workflows/content-check.yml`은 코드 검사 전용입니다. 업로드가 누락돼도 발행 기능이 생기거나 사라지지 않습니다. 기존 workflow 파일은 유지합니다.

## Git으로 추가

기존 저장소의 로컬 복제본에 이 묶음의 내용을 복사한 뒤:

```powershell
git status --short
git add content-publishing modules/05-content-publishing.md .github/workflows/content-check.yml README_UPLOAD.md
git diff --cached --stat
git commit -m "Add book content publishing module and local planning tools"
git push
```

이 배포본은 아직 원격 저장소에 업로드하지 않았습니다. 업로드 전에 실제 변경 목록을 확인하세요. 기존 저장소의 라이선스 조건을 따르며 이 묶음은 별도 라이선스를 부여하지 않습니다.

## 구현 범위

실제 Python 코드: 블로그 다음 범위 계산·프롬프트 출력·로컬 증빙 검사, SNS 독립 진도 계산·카드 제작 명세·실행 프롬프트 출력.

실제 발행: 원문을 읽고 이미지를 생성하고 연결된 로그인 브라우저에서 조작하는 에이전트가 수행합니다. 이 코드는 게시 API, 브라우저 자동화 엔진, 자체 스케줄러를 포함하지 않습니다. GitHub 업로드만으로 예약이 활성화되지 않습니다.
