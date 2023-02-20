import pandas as pd
import warnings

warnings.filterwarnings("ignore")

class LowMemory:
    def __init__(
        self, 
        file_path: str, 
        sep=",",
        dtype=None,
        encoding=None
        ) -> None:
        self.file_path = file_path
        self.sep = sep
        self.dtype = dtype
        self.encoding = encoding     

    def read_file(self):
        try:
            df = pd.read_excel(self.file_path, dtype=self.dtype)
        except:
            df = pd.read_csv(self.file_path, dtype=self.dtype, encoding=self.encoding, sep=self.sep)
        return df

    def mem_usage(self, pandas_obj: str) -> str:
        if isinstance(pandas_obj, pd.DataFrame):
            usage_b = pandas_obj.memory_usage(deep=True).sum()
        else:  # 假设这不是一个df,而是一个Series
            usage_b = pandas_obj.memory_usage(deep=True)
        usage_mb = usage_b / 1024 ** 2  # 将bytes转化成megabytes
        return "{:03.2f} MB".format(usage_mb)

    def convert_dtypes(self) -> tuple:
        self.df = self.read_file()

        df_int = self.df.select_dtypes(include=['int'])  # 用DataFrame.select_dtypes来选中表中的int数据
        df_int = df_int.apply(pd.to_numeric, downcast='unsigned')  # 用 pd.to_numeric()来降低我们的数据类型

        df_float = self.df.select_dtypes(include=['float'])  # 用DataFrame.select_dtypes来选中表中的float数据
        df_float = df_float.apply(pd.to_numeric, downcast='float')  # 用pd.to_numeric()来降低我们的数据类型

        df_obj = self.df.select_dtypes(include=['object'])   # 用DataFrame.select_dtypes来选中表中的object数据
        for col in df_obj.columns:
            num_unique_values = len(df_obj[col].unique())
            num_total_values = len(df_obj[col])
            if num_unique_values / num_total_values < 0.5:
                df_obj.loc[:, col] = df_obj[col].astype('category')
            else:
                df_obj.loc[:, col] = df_obj[col]
        print(f"dtypes converted.")
        return df_int, df_float, df_obj
    
    def converted_df(self):
        tup_dtypes = self.convert_dtypes()
        self.df[tup_dtypes[0].columns] = tup_dtypes[0]
        self.df[tup_dtypes[1].columns] = tup_dtypes[1]
        self.df[tup_dtypes[2].columns] = tup_dtypes[2]
        return self.df
