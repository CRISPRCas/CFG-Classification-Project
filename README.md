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
├── data/
│   ├── cfg_definitions/
│   │    ├── cfg_1.json       # 存储随机生成的CFG文法（独立的CFG定义）
│   │    ├── cfg_2.json       # 更多CFG文法定义
│   │    └── ...
│   ├── corresponding_strings/
│   │    ├── cfg_1.json       # 存储cfg_1对应的字符串和标签数据，每行一个字符串和其对应的标签
│   │    ├── cfg_2.json       # 存储cfg_2对应的字符串和标签数据
│   │    └── ...
│   └── results/
│        ├── llm_results.jsonl # 存储LLM的判断结果，按行存储每个测试字符串的结果
│        └── parsed_results.jsonl # 存储解析后的布尔值判断结果，按行存储
├── src/
│   ├── generate_cfg.py        # 生成随机CFG和测试字符串的数据集生成脚本
│   ├── llm_test.py           # 使用LLM API对数据集进行测试的脚本
│   └── analyze_results.py    # 分析LLM结果，生成统计报告和图表的脚本
├── reports/
│   └── analysis_report.md    # LLM测试的统计结果报告
├── notebooks/
│   └── data_visualization.ipynb # 交互式Jupyter Notebook用于结果可视化
├── README.md                   # 项目的README文件（即此文件）
├── requirements.txt            # 项目所需的依赖库
└── config.yaml                 # 配置文件，用于存储CFG参数及API密钥等
```

## 3. 文件详细说明

### 3.1 data/
- **cfg_definitions/**：存储生成的CFG文法，所有数据以`.json`格式单独存储。
  - 每个文件包含以下字段：
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

- **strings_labels_cfg_*.jsonl**：存储字符串和标签的数据，使用`.jsonl`格式，每个文件对应一个CFG定义。
  - 每行包含以下字段：
    - **cfg_id**：对应的CFG文件ID（例如`cfg_1`）。
    - **string**：需要测试的字符串。
    - **label**：布尔值，表示字符串是否应被CFG接受（true/false）。
  - 示例：
    ```jsonl
    { "cfg_id": "cfg_1", "string": "a a", "label": true }
    { "cfg_id": "cfg_1", "string": "b a", "label": false }
    ```

- **results/**：存储LLM测试的原始结果以及解析后的判断结果。
  - **llm_results.jsonl**：包含LLM对每个CFG和字符串组合的原始判断结果，使用`.jsonl`格式，每行表示一个测试结果。
    - 字段包括：
      - **cfg_id**：对应的CFG文件ID。
      - **string**：被测试的字符串。
      - **llm_response**：LLM的原始响应（如“接受”或“不接受”）。
      - **error**：如果LLM API在处理请求时发生错误，该字段存储错误信息（如`null`表示无错误）。
    - 示例：
      ```jsonl
      { "cfg_id": "cfg_1", "string": "a a", "llm_response": "接受", "error": null }
      { "cfg_id": "cfg_1", "string": "b a", "llm_response": "不接受", "error": "TimeoutError" }
      ```
  - **parsed_results.jsonl**：解析后的布尔值判断结果，使用`.jsonl`格式，每行包含以下字段：
    - **cfg_id**：对应的CFG文件ID。
    - **string**：被测试的字符串。
    - **expected_result**：布尔值，表示字符串是否应被该CFG接受（true/false）。
    - **llm_result**：布尔值，表示LLM是否认为该字符串被CFG接受（true/false）。
    - 示例：
      ```jsonl
      { "cfg_id": "cfg_1", "string": "a a", "expected_result": true, "llm_result": true }
      { "cfg_id": "cfg_1", "string": "b a", "expected_result": false, "llm_result": false }
      ```

### 3.2 src/
- **generate_cfg.py**：用于生成随机CFG文法及其对应的可接受和不可接受字符串，生成的数据会被保存到`data/cfg_definitions/`和`data/strings_labels_cfg_*.jsonl`中。
- **llm_test.py**：调用LLM API进行测试，判断每个字符串是否被对应的CFG接受，并将结果保存到`data/results/llm_results.jsonl`中。
- **analyze_results.py**：解析LLM的测试结果，生成解析后的判断结果并保存到`data/results/parsed_results.jsonl`中，随后统计正确率、召回率等指标，并生成可视化图表。

### 3.3 reports/
- **analysis_report.md**：统计报告，记录了测试结果的摘要以及关键的可视化分析。

### 3.4 notebooks/
- **data_visualization.ipynb**：用于交互式可视化数据，帮助用户更直观地理解LLM在CFG识别任务上的表现。

### 3.5 README.md
- 项目的描述文档，包括整体概述、文件结构、安装和运行步骤等内容。

### 3.6 requirements.txt
- 项目所需的依赖库列表，如`requests`（用于API调用）、`matplotlib`（用于生成图表）等。

### 3.7 config.yaml
- 配置文件，存储项目的相关配置参数，例如CFG生成时的参数范围、LLM API密钥等信息。

## 4. 安装与运行

### 4.1 安装依赖
在项目根目录下运行以下命令来安装必要的Python库：
```sh
pip install -r requirements.txt
```

### 4.2 运行项目

1. **生成数据集**：
   ```sh
   python src/generate_cfg.py
   ```
   该脚本会生成若干CFG及其对应的测试字符串，保存到`data/cfg_definitions/`和`data/strings_labels_cfg_*.jsonl`中。

2. **测试LLM区分能力**：
   ```sh
   python src/llm_test.py
   ```
   调用LLM API对数据集进行测试，结果保存到`data/results/llm_results.jsonl`。

3. **分析结果并生成图表**：
   ```sh
   python src/analyze_results.py
   ```
   该脚本会解析LLM的测试结果，并将解析后的判断结果保存到`data/results/parsed_results.jsonl`，同时生成统计报告和图表。

4. **可视化分析（可选）**：
   使用`notebooks/data_visualization.ipynb`文件可进行交互式可视化。

## 5. 项目报告
测试完成后，报告文件将在`reports/analysis_report.md`中生成。该报告将包含对LLM在CFG接受性测试中表现的详细分析，包括各类指标（如准确率、召回率）以及相应的图表。

## 6. 注意事项
- 运行LLM测试需要API密钥，请确保将密钥正确配置在`config.yaml`中。
- 数据集的生成过程可能较慢，特别是在生成较复杂的CFG文法时。

## 7. 未来工作
- 扩展CFG的生成策略，使其包含更多样化的结构。
- 使用更多的LLM来对比不同模型在该任务上的表现。
- 考虑加入不同类型的文法（如正则文法）以测试LLM的普遍文法识别能力。

感谢您的阅读，希望本项目对您有所帮助！
