import pandas as pd
import glob
import os
import shutil
import re
from typing import List


def __main__():
    """
    This function reformats files from the float.com.au website to minimise file size
    ONLY EVER NEED BE RUN ONCE.
    :return:
    """
    main_dir: str = os.path.dirname(os.getcwd())
    equities_files_sub: List[str] = glob.glob(f"{main_dir}/prices/equities/*/*.*")
    equities_files: List[str] = glob.glob(f"{main_dir}/prices/equities/*.*")
    eto_files_sub: List[str] = glob.glob(f"{main_dir}/prices/etos/*/*.*")
    eto_files: List[str] = glob.glob(f"{main_dir}/prices/etos/*.*")
    all_files: List[str] = equities_files_sub + equities_files + eto_files + eto_files_sub
    for f in all_files:
        # determine the file type
        ext_file: str = os.path.splitext(f)[1]
        file_name: str = os.path.split(f)[1]  # get just the file name
        year_sub: str = file_name[:4]
        print(f"Working on file {file_name}")
        type_sub: str = 'equities' if 'equities' in f.lower() else 'etos'
        if '.txt' == ext_file:
            # remove all the non-numeric values from the file name as this is all we need
            file_name: str = re.sub(r"\D", "", file_name) + ".csv"
            # get sub folder destination renewed
            year_sub: str = file_name[:4]
        else:
            # original float.com.au files to be minimised
            df: pd.DataFrame = pd.read_csv(f, header=0, dtype='str', names=['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])
            # remove any leading zeroes
            df.replace(r"^0\.", ".", inplace=True, regex=True)
            df.to_csv(f, index=False, header=False)
        output_folder: str = f"{main_dir}/prices/{type_sub}/{year_sub}"
        # check if folder exists, if not create folder
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        # create full path for file
        output_file: str = f"{output_folder}/{file_name}"
        shutil.move(f, output_file)


__main__()
