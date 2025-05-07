import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import gradio as gr
import os

DATASET_PATH = "dataset.jsonl"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class Message(BaseModel):
    role: str
    content: str

class Entry(BaseModel):
    messages: List[Message]

# --- File I/O helpers ---
def read_jsonl(path=DATASET_PATH):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def write_jsonl(entries, path=DATASET_PATH):
    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# --- FastAPI Endpoints ---
@app.get("/entries", response_model=List[Entry])
def get_entries():
    return read_jsonl()

@app.get("/entry/{idx}", response_model=Entry)
def get_entry(idx: int):
    entries = read_jsonl()
    if idx < 0 or idx >= len(entries):
        raise HTTPException(404)
    return entries[idx]

@app.post("/entry", response_model=Entry)
def add_entry(entry: Entry):
    entries = read_jsonl()
    entries.append(entry.dict())
    write_jsonl(entries)
    return entry

@app.put("/entry/{idx}", response_model=Entry)
def update_entry(idx: int, entry: Entry):
    entries = read_jsonl()
    if idx < 0 or idx >= len(entries):
        raise HTTPException(404)
    entries[idx] = entry.dict()
    write_jsonl(entries)
    return entry

@app.delete("/entry/{idx}")
def delete_entry(idx: int):
    entries = read_jsonl()
    if idx < 0 or idx >= len(entries):
        raise HTTPException(404)
    entries.pop(idx)
    write_jsonl(entries)
    return {"ok": True}

# --- Gradio UI ---
def load_entries():
    entries = read_jsonl()
    # For display: flatten to user/assistant text for table
    table = []
    for i, entry in enumerate(entries):
        system = next((m["content"] for m in entry["messages"] if m["role"] == "system"), "")
        user = next((m["content"] for m in entry["messages"] if m["role"] == "user"), "")
        assistant = next((m["content"] for m in entry["messages"] if m["role"] == "assistant"), "")
        table.append([i, system, user, assistant])
    return table

def refresh_table():
    return gr.update(value=load_entries())

def add_entry_gr(system, user, assistant):
    entry = {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ]
    }
    entries = read_jsonl()
    entries.append(entry)
    write_jsonl(entries)
    return load_entries(), "추가 완료"

def edit_entry_gr(idx, system, user, assistant):
    entries = read_jsonl()
    idx = int(idx)
    if idx < 0 or idx >= len(entries):
        return gr.update(), "잘못된 인덱스"
    entries[idx] = {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ]
    }
    write_jsonl(entries)
    return load_entries(), "수정 완료"

def delete_entry_gr(idx):
    entries = read_jsonl()
    idx = int(idx)
    if idx < 0 or idx >= len(entries):
        return gr.update(), "잘못된 인덱스"
    entries.pop(idx)
    write_jsonl(entries)
    return load_entries(), "삭제 완료"

def search_entries_gr(query):
    entries = read_jsonl()
    query = query.strip().lower()
    filtered = []
    for i, entry in enumerate(entries):
        user = next((m["content"] for m in entry["messages"] if m["role"] == "user"), "")
        assistant = next((m["content"] for m in entry["messages"] if m["role"] == "assistant"), "")
        if query in user.lower() or query in assistant.lower():
            system = next((m["content"] for m in entry["messages"] if m["role"] == "system"), "")
            filtered.append([i, system, user, assistant])
    return filtered

def select_row(evt: gr.SelectData):
    idx = evt.index
    # idx가 리스트([row, col])일 경우 row만 사용
    if isinstance(idx, list):
        idx = idx[0]
    entries = read_jsonl()
    if idx < 0 or idx >= len(entries):
        return "", "", "", ""
    entry = entries[idx]
    system = next((m["content"] for m in entry["messages"] if m["role"] == "system"), "")
    user = next((m["content"] for m in entry["messages"] if m["role"] == "user"), "")
    assistant = next((m["content"] for m in entry["messages"] if m["role"] == "assistant"), "")
    return str(idx), system, user, assistant

with gr.Blocks(title="JSONL Editor") as demo:
    gr.Markdown("""# JSONL Dataset Editor\n- 실시간 편집/추가/삭제/검색 지원\n- dataset.jsonl 파일을 직접 관리합니다.""")
    with gr.Row():
        search_box = gr.Textbox(label="검색 (user/assistant)")
        search_btn = gr.Button("검색")
        refresh_btn = gr.Button("새로고침")
    table = gr.Dataframe(
        headers=["Index", "System", "User", "Assistant"],
        datatype=["number", "str", "str", "str"],
        value=load_entries(),
        interactive=True,
        row_count=10,
        col_count=(4, "fixed"),
        label="데이터셋"
    )
    with gr.Row():
        idx_in = gr.Textbox(label="Index (수정/삭제용)")
        system_in = gr.Textbox(label="System")
        user_in = gr.Textbox(label="User")
        assistant_in = gr.Textbox(label="Assistant")
    with gr.Row():
        add_btn = gr.Button("추가")
        edit_btn = gr.Button("수정")
        del_btn = gr.Button("삭제")
    status = gr.Textbox(label="상태", interactive=False)

    # Actions
    add_btn.click(add_entry_gr, [system_in, user_in, assistant_in], [table, status])
    edit_btn.click(edit_entry_gr, [idx_in, system_in, user_in, assistant_in], [table, status])
    del_btn.click(delete_entry_gr, [idx_in], [table, status])
    search_btn.click(search_entries_gr, [search_box], table)
    refresh_btn.click(refresh_table, None, table)
    table.select(select_row, None, [idx_in, system_in, user_in, assistant_in])

# Mount Gradio app to FastAPI
app = gr.mount_gradio_app(app, demo, path="/") 