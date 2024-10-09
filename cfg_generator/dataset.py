import os
import jsonlines
from .loader import load_cfg_from_json


class CFGDataset:
    def __init__(self, data_dir):
        self.data = []
        cfg_definitions_dir = os.path.join(data_dir, "cfg_definitions")
        corresponding_strings_dir = os.path.join(data_dir, "corresponding_strings")

        # 遍历cfg_definitions目录下的所有CFG定义文件
        for cfg_file_name in os.listdir(cfg_definitions_dir):
            if cfg_file_name.endswith(".json"):
                cfg_id = cfg_file_name.split("_")[1].split(".")[0]
                cfg_file_path = os.path.join(cfg_definitions_dir, cfg_file_name)
                strings_file_path = os.path.join(
                    corresponding_strings_dir, f"cfg_{cfg_id}.jsonl"
                )

                # 读取CFG定义
                cfg = load_cfg_from_json(cfg_file_path)

                # 读取对应的字符串和标签
                with jsonlines.open(strings_file_path, mode="r") as reader:
                    for string_data in reader:
                        self.data.append(
                            {
                                "cfg": str(cfg),
                                "string": string_data["string"],
                                "label": string_data["label"],
                            }
                        )

    def __iter__(self):
        for item in self.data:
            yield item

    def __len__(self):
        return len(self.data)


if __name__ == "__main__":
    data_dir = "data"
    cfg_dataset = CFGDataset(data_dir)
    print(len(cfg_dataset))
    cfg_dataset.data = cfg_dataset.data[:10]

    for data in cfg_dataset:
        print(data)
        