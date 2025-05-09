import json

input_path = "test_possible_item_count_duplicates_removed.jsonl"
output_path = "test_possible_item_count_duplicates_removed_wrapped_scalar.jsonl"

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        data = json.loads(line)
        # assistant content는 JSON string이므로 파싱 필요
        assistant_content = data["messages"][-1]["content"]
        assistant_json = json.loads(assistant_content)
        # possible_item_count가 배열이 아니면 배열로 감싸기
        if "possible_item_count" in assistant_json and not isinstance(assistant_json["possible_item_count"], list):
            assistant_json["possible_item_count"] = [assistant_json["possible_item_count"]]
        # 다시 문자열로 변환
        data["messages"][-1]["content"] = json.dumps(assistant_json, ensure_ascii=False)
        outfile.write(json.dumps(data, ensure_ascii=False) + "\n")