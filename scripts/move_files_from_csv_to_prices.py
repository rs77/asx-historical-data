import shutil
import re
import os
import glob
from typing import List


def __main__():
    main_dir: str = os.path.dirname(os.getcwd())
    # when the capture is done move the files from the `csv` location to their respective `prices` location
    csv_files: List[str] = glob.glob(f"{main_dir}/csv/*")
    for f in csv_files:
        file_name: str = os.path.split(f)[1]  # get just the file name
        # remove all the non-numeric values from the file name as this is all we need
        file_name: str = re.sub(r"\D", "", file_name) + ".csv"
        folder_sub: str = file_name[:4]
        if 'equities' in f.lower():
            shutil.move(f, f"{main_dir}/prices/equities/{folder_sub}/{file_name}")
        elif 'etos' in f.lower():
            shutil.move(f, f"{main_dir}/prices/etos/{folder_sub}/{file_name}")


__main__()
