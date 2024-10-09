import os
import json
from sklearn.metrics import classification_report
import pprint

class JSONLineAnalyzer:
    def __init__(self, directory):
        self.directory = directory

    def analyze(self):
        results = {}
        for filename in os.listdir(self.directory):
            if filename.endswith('.jsonl'):
                filepath = os.path.join(self.directory, filename)
                result = self.analyze_file(filepath)
                results[filename[:-6]] = result
        return results

    def analyze_file(self, filepath):
        error_count = 0
        total_count = 0
        empty_llm_count = 0

        y_true = []
        y_pred = []

        with open(filepath, 'r') as f:
            for line in f:
                total_count += 1
                record = json.loads(line)

                # Check if 'error' field is non-empty
                if record.get('error'):
                    error_count += 1
                    continue

                # Only consider records with 'error' as empty
                label = record.get('label')
                llm_parsed_result = record.get('llm_parsed_result')

                if llm_parsed_result is None:
                    empty_llm_count += 1
                    llm_parsed_result = 'none'  # Consider 'none' for metrics calculation

                if label is not None and llm_parsed_result is not None:
                    # Convert label to string to ensure consistent data types
                    label_str = str(label).lower() if isinstance(label, bool) else label
                    llm_parsed_result_str = str(llm_parsed_result).lower() if isinstance(llm_parsed_result, bool) else llm_parsed_result
                    y_true.append(label_str)
                    y_pred.append(llm_parsed_result_str)

        error_ratio = error_count / total_count if total_count > 0 else 0
        empty_llm_ratio = empty_llm_count / (total_count - error_count) if (total_count - error_count) > 0 else 0

        # Generate classification report for the three-class problem (true, false, none)
        labels = ['true', 'false', 'none']
        report = classification_report(y_true, y_pred, labels=labels, zero_division=0, output_dict=True)

        return {
            'error_ratio': error_ratio,
            'empty_llm_ratio': empty_llm_ratio,
            'classification_report': report
        }

# Example usage:
if __name__=="__main__":
    analyzer = JSONLineAnalyzer('./result')
    result = analyzer.analyze()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)