from DataAnalysisPath.DataAnalysis import DataAnalysis, SortType
import time


c = time.time()

# todo add field evalator
# todo change unum (random random)
# todo optimize normalizer

analysis = DataAnalysis("../data/aref.csv",
                        "../data/aref.org.csv",
                        normalize=False,
                        sort_type=SortType.X)

print(time.time() - c)