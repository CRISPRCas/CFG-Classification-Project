import pprint
from statistic_tools.analyzer import JSONLineAnalyzer

if __name__=="__main__":
    analyzer = JSONLineAnalyzer('./result')
    result = analyzer.analyze()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)