import glob
from typing import List
import pandas as pd
import numpy as np
from datetime import datetime, date
import os


def get_date(el: str):
    return datetime.strptime(el, '%Y%m%d').date()

start_date: date = date(2020, 1, 1)
main_dir: str = os.path.dirname(os.getcwd())
data_dir: str = os.path.join(main_dir, 'prices', 'etos', str(start_date.year))
data_files: List[str] = glob.glob(f"{data_dir}/*.csv")
data_file_col: List[str] = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']
data_type_col: List[str] = {'symbol': "string", 'date': "string", 'open': float, 'high': float, 'low': float,
                            'close': float, 'volume': np.uint64}
df: pd.DataFrame = pd.DataFrame(columns=data_file_col)


# concatenate the data
for f in data_files:
    temp_df: pd.DataFrame = pd.read_csv(f, header=0, dtype=data_type_col, names=data_file_col, parse_dates=['date'],
                                        infer_datetime_format=True, index_col=None, date_parser=get_date)
    df = df.append(temp_df, ignore_index=True)

# sort dataframe by symbol then date
df.sort_values(by=['symbol', 'date'], ascending=[True, True], inplace=True)
df.reset_index(drop=True, inplace=True)
df1 = df.loc[df.groupby('symbol')['volume'].idxmax()]

# detect if there has been an increase in volume over the last X periods
1