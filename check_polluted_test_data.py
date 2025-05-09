train_path = "train_possible_item_count_duplicates_removed_wrapped_scalar.jsonl"
test_path = "test_possible_item_count_duplicates_removed_wrapped_scalar.jsonl"

with open(train_path, "r", encoding="utf-8") as f:
    train_lines = set(line.strip() for line in f if line.strip())

with open(test_path, "r", encoding="utf-8") as f:
    test_lines = set(line.strip() for line in f if line.strip())

shared_lines = train_lines & test_lines

print(f"중복 라인 개수: {len(shared_lines)}")
if shared_lines:
    print("중복 라인 예시:")
    for i, line in enumerate(list(shared_lines)[:5]):
        print(f"{i+1}: {line}")
else:
    print("중복 라인이 없습니다.")