#!/bin/bash

# 定义模型名称数组
models=(
  "gpt-4o-mini"
  "gpt-3.5-turbo"
  "gpt-4o"
)

# 遍历数组中的每个模型名称
for model in "${models[@]}"
do
  python test_llm.py \
         --model "$model" \
         --output_file "result/${model}.jsonl"
done