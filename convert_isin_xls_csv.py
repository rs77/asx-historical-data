import pandas as pd
import glob
from typing import List

# get all files in directory
files: List[str] = glob.glob("/Users/ryansheehy/PycharmProjects/OptionsHistory/contract_data/isin_xls/*.xls")

for file in files:
    read_csv = pd.read_excel(file)
    print(read_csv)

