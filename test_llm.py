import json
import argparse
from llm_evaluator.evaluator import CFGAcceptanceExperiment
from cfg_generator.dataset import CFGDataset

def main(model_name, data_dir, output_file):
    # 初始化实验
    experiment = CFGAcceptanceExperiment(model=model_name)

    # 加载数据集
    dataset = CFGDataset(data_dir)
    print(f"Loaded {len(dataset)} test cases from {data_dir}")

    # 实时写入实验结果
    with open(output_file, 'w') as f:
        for result in experiment.run_experiment(dataset):
            try:
                json_line = {
                    "cfg": result["cfg"],
                    "string": result["string"],
                    "label": result["label"],
                    "llm_response": result["raw_response"],
                    "llm_parsed_result": result["result"],
                    "error": result["error"]
                }
                f.write(json.dumps(json_line) + "\n")
            except Exception as e:
                # 如果有错误发生，跳过这个实验结果
                print(f"Error encountered in test case: {str(e)}")
                continue

# 解析命令行参数
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run CFG Acceptance Experiment with LLM")
    parser.add_argument('--model', type=str, required=True, help="Specify the LLM model to use (e.g., 'gpt-3.5-turbo')")
    parser.add_argument('--data_dir', type=str, default="data", help="Directory containing the dataset")
    parser.add_argument('--output_file', type=str, required=True, help="File path to save the results in JSONL format")
    args = parser.parse_args()

    # 运行实验
    main(args.model, args.data_dir, args.output_file)