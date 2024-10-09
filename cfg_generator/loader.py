import json
from .cfg import CFG

def save_cfg_to_json(cfg, file_path):
    """
    将CFG类保存为JSON文件
    """
    cfg_data = {
        "non_terminals": cfg.non_terminals,
        "terminals": cfg.terminals,
        "productions": cfg.productions,
        "num_productions_range": cfg.num_productions_range,
        "production_length_range": cfg.production_length_range,
        "terminal_probability": cfg.terminal_probability
    }
    with open(file_path, 'w') as json_file:
        json.dump(cfg_data, json_file, indent=4)


def load_cfg_from_json(file_path):
    """
    从JSON文件加载CFG类
    """
    with open(file_path, 'r') as json_file:
        cfg_data = json.load(json_file)
    
    # 创建新的CFG对象并赋值
    cfg = CFG(
        non_terminals=cfg_data.get("non_terminals"),
        terminals=cfg_data.get("terminals"),
        num_productions_range=tuple(cfg_data.get("num_productions_range", (1, 3))),
        production_length_range=tuple(cfg_data.get("production_length_range", (1, 3))),
        terminal_probability=cfg_data.get("terminal_probability", 0.5)
    )
    
    # 设置产生式
    cfg.productions = cfg_data.get("productions", {})
    
    return cfg
