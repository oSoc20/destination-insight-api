import pandas as pd
from misc import count_repetitions
import sys

data = pd.read_csv('data.csv')
result = count_repetitions(data, 'origin', 'top', 10, return_json=True)
print(result)
sys.stdout.flush()