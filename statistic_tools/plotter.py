import os
import json
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import pprint
from collections import defaultdict
import numpy as np

class JSONLineAnalyzer:
    def __init__(self, directory, bucket_size=1):
        self.directory = directory
        self.bucket_size = bucket_size

    def analyze(self):
        results = {}
        for filename in os.listdir(self.directory):
            if filename.endswith('.jsonl'):
                filepath = os.path.join(self.directory, filename)
                result = self.analyze_file(filepath)
                results[filename[:-6]] = result
        return results

    def analyze_file(self, filepath):
        with open(filepath, 'r') as f:
            records = [json.loads(line) for line in f]

        # Group records into buckets based on cfg length
        buckets = defaultdict(list)
        for record in records:
            cfg_length = len(record.get('string', []))
            bucket_key = cfg_length // self.bucket_size
            buckets[bucket_key].append(record)

        bucket_results = {}
        for bucket_key, bucket_records in buckets.items():
            error_count = 0
            total_count = 0
            empty_llm_count = 0

            y_true = []
            y_pred = []

            for record in bucket_records:
                total_count += 1

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

            bucket_results[bucket_key] = {
                'cfg_length': bucket_key * self.bucket_size,
                'error_ratio': error_ratio,
                'empty_llm_ratio': empty_llm_ratio,
                'classification_report': report
            }

        return bucket_results

class PlotAnalyzerResults:
    def __init__(self, results, bucket_size=1):
        self.results = results
        self.bucket_size = bucket_size

    def plot_metric(self, metric='f1-score', average='weighted avg'):
        # Prepare data for plotting
        cfg_lengths = []
        metric_values = []
        metric_errors = []

        for key, bucket_results in self.results.items():
            for bucket_key, result in bucket_results.items():
                cfg_length = result['cfg_length']
                report = result['classification_report']
                value = report.get(average, {}).get(metric, 0)

                cfg_lengths.append(cfg_length)
                metric_values.append(value)
                # Assuming error as a standard deviation for illustrative purposes
                metric_errors.append(np.std(metric_values))

        # Sort data based on cfg lengths
        sorted_data = sorted(zip(cfg_lengths, metric_values, metric_errors))
        cfg_lengths, metric_values, metric_errors = zip(*sorted_data)

        # Plot the metric with error bars
        plt.figure(figsize=(10, 6))
        plt.errorbar(cfg_lengths, metric_values, yerr=metric_errors, fmt='-o', color='b', ecolor='r', capsize=5, elinewidth=2, markeredgewidth=2)
        plt.xlabel('String Length (Bucket Size {})'.format(self.bucket_size))
        plt.ylabel('{} ({})'.format(metric.capitalize(), average))
        plt.title('{} vs String Length'.format(metric.capitalize()))
        plt.grid(True)
        plt.show()

# Example usage:
if __name__ == "__main__":
    # Step 1: Analyze JSON lines
    analyzer = JSONLineAnalyzer('./result', bucket_size=10)
    analysis_results = analyzer.analyze()
    
    # Step 2: Plot the results
    plotter = PlotAnalyzerResults(analysis_results, bucket_size=10)
    plotter.plot_metric(metric='f1-score', average='weighted avg')