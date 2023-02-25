'''
Author: tansen
Date: 2023-02-20 00:46:00
LastEditors: Please set LastEditors
LastEditTime: 2023-02-25 16:59:26
'''
import warnings
from typing import Union

import pandas as pd
from pandas.core.frame import DataFrame

warnings.filterwarnings("ignore")


class Optimization:
    def __init__(
            self,
            file_path: str,  # file path
            sep=",",  # separator
            sheet_name: Union[str, None] = None,  # sheet name
            skip_rows: Union[int, None] = None,  # skip row
            usecols: Union[str, int, None] = None,  # use column
            dtype: Union[str, dict[str], None] = None,  # type
            encoding: Union[str, None] = None  # encoding
    ) -> None:
        self.file_path = file_path
        self.sep = sep
        self.sheet_name = sheet_name
        self.skip_rows = skip_rows
        self.usecols = usecols
        self.dtype = dtype
        self.encoding = encoding

    def read_file(self) -> DataFrame:
        """ read file: xls, xlsx, csv, tsv, txt... """
        try:
            df = pd.read_excel(
                self.file_path,
                dtype=self.dtype,
                sheet_name=self.sheet_name,
                skip_rows=self.skip_rows,
                usecols=self.usecols)
        except:
            df = pd.read_csv(self.file_path, dtype=self.dtype,
                             encoding=self.encoding, sep=self.sep)
        return df

    def convert_dtypes(self) -> tuple:
        """ convert dtype of datafame """
        self.df = self.read_file()

        # select int type in dataframe
        df_int = self.df.select_dtypes(include=['int'])
        # reduce data type
        df_int = df_int.apply(pd.to_numeric, downcast='unsigned')

        # select float type in dataframe
        df_float = self.df.select_dtypes(include=['float'])
        # reduce data type
        df_float = df_float.apply(pd.to_numeric, downcast='float')

        # select object type in datafame
        df_obj = self.df.select_dtypes(include=['object'])
        for col in df_obj.columns:
            num_unique_values = len(df_obj[col].unique())
            num_total_values = len(df_obj[col])
            if num_unique_values / num_total_values < 0.5:
                df_obj.loc[:, col] = df_obj[col].astype('category')
            else:
                df_obj.loc[:, col] = df_obj[col]
        return df_int, df_float, df_obj

    def converted_df(self) -> DataFrame:
        tup_dtypes = self.convert_dtypes()
        self.df[tup_dtypes[0].columns] = tup_dtypes[0]
        self.df[tup_dtypes[1].columns] = tup_dtypes[1]
        self.df[tup_dtypes[2].columns] = tup_dtypes[2]
        print("\033[1;32mdtypes converted.\033[0m")
        return self.df

    @staticmethod
    def write(
            dataframe: DataFrame,
            pickle_path: str,
            pickle_name: str = "processed",
            fomat: str = "pkl"  # gzip, bz2, xz
        ) -> None:
        """ write dataframe to pickle """
        try:
            path = f"{pickle_path}/{pickle_name}.{fomat}"
            dataframe.to_pickle(path=path, compression="infer")
            print("\033[1;32mpickle file is saved.\033[0m")
        except Exception as e:
            print(f"Write pickle file Error: {e}.")
    
    @staticmethod
    def read(pickle_file: str) -> DataFrame:
        """ read pickle file to dataframe """
        try:
            df = pd.read_pickle(pickle_file, compression="infer")
        except Exception as e:
            print(f"Read pickle file Error: {e}.")
        else:
            return df
