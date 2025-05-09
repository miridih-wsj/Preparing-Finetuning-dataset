input_path = "train_possible_item_count.jsonl"
output_path = "train_possible_item_count_duplicates_removed.jsonl"

seen = set()
with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        if line not in seen:
            outfile.write(line)
            seen.add(line)