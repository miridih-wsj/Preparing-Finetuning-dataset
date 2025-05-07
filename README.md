# Preparing Finetuning dataset

csv는 https://docs.google.com/spreadsheets/d/1uZpM377RsVHEaZPj_iE25Q6sbVwVVJFd313TBx_-ugI/edit?gid=805221309#gid=805221309 
위 링크에서 다운

---

## 실행 방법 (Gradio+FastAPI JSONL 편집기)

### 1. 가상환경(venv) 생성 및 활성화 (권장)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 서버 실행 (기본: 8000, 이미 사용 중이면 8001 등으로 변경)
```bash
uvicorn app:app --reload --port 8001
```

### 4. 브라우저에서 접속
```
http://localhost:8001/
```

### 5. 자주 발생하는 문제/해결법
- **포트 충돌:**
  - `[Errno 48] Address already in use` → 이미 서버가 떠 있으면 다른 포트(예: 8001)로 실행
- **패키지 설치 에러:**
  - Homebrew Python 환경에서는 반드시 venv 사용 권장
  - `error: externally-managed-environment` → venv로 실행하거나, `pipx` 사용
- **uvicorn 명령어가 없을 때:**
  - venv 활성화 후 `pip install uvicorn` 또는 `python3 -m pip install uvicorn`
- **Gradio row 클릭시 에러:**
  - app.py의 select_row 함수가 최신 버전이면 자동 해결됨

---

### 기타
- dataset.jsonl 파일이 실시간으로 편집/저장됩니다.
- 추가 문의/에러 발생 시 에러 메시지와 함께 문의 바랍니다.