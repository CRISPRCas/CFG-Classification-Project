from statistics.analyzer import JSONLineAnalyzer

if __name__=="__main__":
    analyzer = JSONLineAnalyzer('./result')
    result = analyzer.analyze()
    print(result)