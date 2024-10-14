# CFG Classification Project

## 1. 项目概述

本项目旨在构造一个上下文无关文法（CFG）数据集，测试大型语言模型（LLM）在区分字符串是否能够被给定的CFG接受方面的能力。项目包括以下三个部分：

1. **构造数据集**：构造随机生成的CFG文法，并生成相应的可接受和不可接受的字符串。
2. **测试LLM区分能力**：调用LLM API来判断给定CFG和字符串是否匹配，并记录结果。
3. **统计报告**：对测试结果进行统计分析，并制成图表进行可视化。

## 2. 文件结构

项目文件组织为如下目录树：

```
CFG_Classification_Project/
├── cfg_generator/
│   ├── cfg.py                         # CFG 类
│   ├── dataset.py                     # 数据集类
│   └── loader.py                      # 数据加载方法
├── configs/
│   ├── config_1.json                  # 生成的配置文件
│   └── ...
├── data/
│   ├── cfg_definitions/
│   │    ├── cfg_1.json                # 存储随机生成的 CFG 文法（独立的 CFG 定义）
│   │    ├── cfg_2.json                # 更多 CFG 文法定义
│   │    └── ...
│   └── corresponding_strings/
│        ├── cfg_1.jsonl               # 存储 cfg_1 对应的字符串和标签数据，每行一个字符串和其对应的标签
│        ├── cfg_2.jsonl               # 存储 cfg_2 对应的字符串和标签数据
│        └── ...
├── llm_evaluator/
│   └── evaluator.py                   # API 调用测试方法
└── report/
│   └── report-1.md                    # 实验结果报告
└── results/
│   ├── gpt-xx.jsonl                   # 实验原始结果
├── scripts/
│   ├── generarun_generate_dataset.sh  # 生成随机 CFG 和测试字符串的数据集生成脚本
│   ├── run_generate_report.sh         # 使用 LLM API 对数据集进行测试的脚本
│   └── run_test_llm.sh                # 分析 LLM 结果
├── statistic_tools/
│   ├── analyzer.py                    # 实验结果指标分析
│   ├── plotter.py                     # 作图
│   └── sampler.py                     # 采样实验结果做 Case Study
├── environment.yml                    # 项目所需的 conda 环境
├── generate_dataset.py                # Step1: 构造数据集
├── generate_report.py                 # Step3: 数据分析
├── README.md                          # 项目的 README 文件（即此文件）
└── test_llm.py                        # Step2: 测试 LLM 在 CFG 上的判定能力
```

## 3. 文件详细说明

### 3.1 cfg_generator/
- **cfg.py**：定义了上下文无关文法（CFG）的类，用于表示CFG的产生式、非终结符、终结符等。
- **dataset.py**：数据集类，负责管理CFG与对应的测试字符串数据。
- **loader.py**：数据加载方法，用于加载生成的CFG数据集。

### 3.2 configs/
- **config_1.json**：项目配置文件，包括生成CFG的参数和LLM API相关设置。其他文件与之类似，存储不同的实验配置。

### 3.3 data/
- **cfg_definitions/**：存储生成的CFG文法，每个CFG以`.json`格式存储，文件包含以下字段：
  - **non_terminals**：非终结符的列表。
  - **terminals**：终结符的列表。
  - **start_symbol**：开始符号。
  - **productions**：产生式规则。
  - 示例：
    ```json
    {
      "non_terminals": ["S", "A"],
      "terminals": ["a", "b"],
      "start_symbol": "S",
      "productions": {
        "S": ["A A", "b"],
        "A": ["a", "S"]
      }
    }
    ```

- **corresponding_strings/**：存储与CFG定义对应的字符串和标签数据，每个CFG对应一个`.jsonl`文件，其文件名与`cfg_definitions`中的文件名一致。
  - 每行包含以下字段：
    - **string**：需要测试的字符串。
    - **label**：布尔值，表示字符串是否应被CFG接受（true/false）。
  - 示例：
    ```json
    { "string": "00(0", "label": true }
    { "string": "b a", "label": false }
    ```

### 3.4 llm_evaluator/
- **evaluator.py**：负责调用LLM API对CFG和字符串进行匹配判断，记录结果。

### 3.5 report/
- **report-1.md**：实验结果报告文件，包含测试结果的详细分析和图表可视化。

### 3.6 results/
- **gpt-xx.jsonl**：存储LLM测试的原始结果。每行表示一个测试结果，包含以下字段：
  - **cfg**：对应的CFG。
  - **string**：被测试的字符串。
  - **label**：布尔值，表示字符串是否应被CFG接受（true/false）。
  - **llm_response**：LLM的原始响应。
  - **llm_parsed_result**：布尔值，表示LLM是否认为该字符串被CFG接受（true/false）。
  - **error**：如果LLM API在处理请求时发生错误，该字段存储错误信息（如`null`表示无错误）。
  - 示例：
    ```json
    { "cfg": "cfg_1", "string": "a a", "label": true, "llm_response": "接受", "llm_parsed_result": true, "error": null }
    { "cfg": "cfg_1", "string": "b a", "label": false, "llm_response": "不接受", "llm_parsed_result": false, "error": "TimeoutError" }
    ```

### 3.7 scripts/
- **run_generate_dataset.sh**：生成随机CFG和测试字符串的数据集生成脚本。
- **run_generate_report.sh**：运行LLM API对数据集进行测试并生成报告的脚本。
- **run_test_llm.sh**：分析LLM的测试结果。

### 3.8 statistic_tools/
- **analyzer.py**：实验结果指标分析工具，用于计算准确率、召回率等。
- **plotter.py**：用于绘制实验结果的图表。
- **sampler.py**：用于采样实验结果进行案例研究（Case Study）。

### 3.9 generate_dataset.py
- **generate_dataset.py**：用于构造数据集，包括随机生成CFG及其对应的测试字符串，并保存到`data/`目录中。

### 3.10 test_llm.py
- **test_llm.py**：调用LLM API测试每个CFG对应的字符串，记录判断结果。

### 3.11 generate_report.py
- **generate_report.py**：解析LLM的测试结果，生成解析后的判断结果，并对数据进行统计分析，生成报告和图表。

### 3.12 environment.yml
- **environment.yml**：项目所需的Conda环境文件，列出了所需的Python库及其版本。

### 3.13 README.md
- **README.md**：项目描述文档，包括整体概述、文件结构、安装和运行步骤等内容。

## 4. 安装与运行

### 4.1 安装依赖
在项目根目录下运行以下命令来安装必要的Python库：
```sh
conda env create -f environment.yml
```

### 4.2 运行项目

1. **生成数据集**：
   ```sh
   bash scripts/run_generate_dataset.sh
   ```
   该脚本会生成若干CFG及其对应的测试字符串，保存到`data/cfg_definitions/`和`data/corresponding_strings*.jsonl`中。

2. **测试LLM区分能力**：
   ```sh
   bash scripts/run_test_llm.sh
   ```
   调用LLM API对数据集进行测试，结果保存到`data/results/`。

3. **分析结果并生成图表**：
   ```sh
   bash scripts/run_test_llm.sh
   ```
   该脚本会解析LLM的测试结果。


## 5. 项目报告
测试完成后，报告文件在`reports/`中。该报告将包含对LLM在CFG接受性测试中表现的详细分析，包括各类指标（如准确率、召回率）以及相应的图表。

## 6. 注意事项
- 运行LLM测试需要API密钥，请确保将密钥正确配置在`config.yaml`中。
- 数据集的生成过程可能较慢，特别是在生成较复杂的CFG文法时。

感谢您的阅读，希望本项目对您有所帮助！
