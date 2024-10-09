import os
import json
import jsonlines
import uuid
import random
import argparse
from lark import Lark
from cfg_generator.cfg import CFG

def generate_cfg_and_strings(config):
    output_dir = "data"
    cfg_definitions_dir = os.path.join(output_dir, "cfg_definitions")
    corresponding_strings_dir = os.path.join(output_dir, "corresponding_strings")
    
    os.makedirs(cfg_definitions_dir, exist_ok=True)
    os.makedirs(corresponding_strings_dir, exist_ok=True)

    num_cfgs = config['num_cfgs']
    num_strings_per_cfg = config['num_strings_per_cfg']
    str_length_range = tuple(config['str_length_range'])
    non_terminals = config['non_terminals']
    terminals = config['terminals']
    num_productions_range = tuple(config['num_productions_range'])
    production_length_range = tuple(config['production_length_range'])
    terminal_probability = config['terminal_probability']

    for _ in range(num_cfgs):
        # 生成随机的UUID，用作文件名
        cfg_id = str(uuid.uuid4())[:8]
        cfg_file_path = os.path.join(cfg_definitions_dir, f"cfg_{cfg_id}.json")
        strings_file_path = os.path.join(corresponding_strings_dir, f"cfg_{cfg_id}.jsonl")

        # 生成随机的CFG配置
        cfg = CFG(
            non_terminals=non_terminals,
            terminals=terminals,
            num_productions_range=num_productions_range,
            production_length_range=production_length_range,
            terminal_probability=terminal_probability,
        )
        cfg.generate_terminating_cfg()

        # 保存CFG定义到JSON文件
        cfg_data = {
            "non_terminals": cfg.non_terminals,
            "terminals": cfg.terminals,
            "productions": cfg.productions,
            "num_productions_range": cfg.num_productions_range,
            "production_length_range": cfg.production_length_range,
            "terminal_probability": cfg.terminal_probability
        }
        with open(cfg_file_path, 'w') as json_file:
            json.dump(cfg_data, json_file, indent=4)

        # 将CFG转换为Lark格式
        lark_grammar = cfg.cfg_to_lark()
        parser = Lark(lark_grammar, start="s", parser="earley")

        # 生成字符串及其标签，确保字符串不重复
        existing_strings = set()
        strings_data = []
        while len(strings_data) < num_strings_per_cfg:
            # 70% 使用 generate_string_within_length 生成，30% 随机生成
            if random.random() < 0.7:
                random_string = cfg.generate_string_within_length(*str_length_range)
            else:
                random_string = ''.join(random.choices(cfg.terminals, k=random.randint(*str_length_range)))

            # 确保字符串不重复
            if random_string in existing_strings:
                continue

            # 使用 Lark parser 解析字符串，确定标签
            try:
                parser.parse(random_string)
                label = True  # 解析成功，标签为 True
            except Exception:
                label = False  # 解析失败，标签为 False

            existing_strings.add(random_string)
            strings_data.append({"string": random_string, "label": label})

        # 随机打乱生成的字符串数据
        random.shuffle(strings_data)

        # 将字符串数据保存到JSONL文件
        with jsonlines.open(strings_file_path, mode='w') as writer:
            writer.write_all(strings_data)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Generate CFG datasets.")
    parser.add_argument("--config", type=str, required=True, help="The path to the configuration JSON file.")
    args = parser.parse_args()

    # 读取配置文件
    with open(args.config, 'r') as config_file:
        config = json.load(config_file)

    # 调用生成方法
    generate_cfg_and_strings(config)


if __name__ == "__main__":
    main()