'''
Author: tansen
Date: 2023-02-27 22:19:54
LastEditors: Please set LastEditors
LastEditTime: 2023-03-01 00:32:16
'''
import os
from typing import Union

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame


class JET:
    def __init__(self) -> None:
        pass

    @staticmethod
    def read(
        path: str,
        sep: str = ",",
        encoding: str = "utf-8",
        dtype: Union[dict, None] = None,
        skiprows: Union[int, None] = None,
        usecols: Union[str, list, None] = None
    ) -> DataFrame:
        """ read file """
        file_extension = os.path.splitext(path)[-1]
        if file_extension.lower() == ".xlsx":
            df = pd.read_excel(
                path,
                dtype=dtype,
                skiprows=skiprows,
                usecols=usecols)
        else:
            df = pd.read_csv(
                path,
                dtype=dtype,
                sep=sep,
                encoding=encoding)
        print("\033[1;32mread successfully.\033[0m")
        return df
    
    @staticmethod
    def write(
        df: DataFrame,
        rows: int = 70_0000,
        path: str = "saveFile"
    ) -> None:
        try:
            if len(df) <= rows:
                df.to_excel(f"{path}.xlsx", index=False, encoding="gbk")
                print(f"\033[36m'{os.path.basename(path)}.xlsx' is saved.\033[0m")
            else:
                df.to_csv(f"{path}.csv", index=False, encoding="utf-8")
                print(f"\033[36m'{os.path.basename(path)}.csv' is saved.\033[0m")
        except Exception as e:
            print(f"Save Error: {e}.")

    @staticmethod
    def pivot(
        df: DataFrame,
        index: Union[str, list[str]],
        values: Union[str, list[str]],
        path: str = "pt.xlsx",
    ) -> list:
        pt = pd.pivot_table(
            df,
            index=index,
            values=values,
            aggfunc=np.sum)
        pt.insert(loc=0, column="Account", value=pt.index)
        pt.to_excel(path, index=False, encoding="gbk")
        print(f"\033[36msave path -> '{path}'\033[0m")
        return pt.index.unique().tolist()

    @staticmethod
    def get_last_account(
        df: DataFrame,
        location: int = 1,  # entity_account of column
        en_acc: str = "enacc"  # entity_account
    ) -> list:
        """ get end-level account """
        cell = 0
        last_acc = []
        while cell < len(df)-1:
            try:
                if df.iloc[cell, location-1] == df.iloc[cell+1, location-1][:len(df.iloc[cell, location-1])]:
                    pass
                else:
                    last_acc.append(df.iloc[cell, df.columns.get_loc(en_acc)])
                cell += 1
            except:
                break
        last_acc.append(df.iloc[len(df)-1, location-1])  # append last account
        print("\033[1;32mget end-level account successfully.\033[0m")
        return last_acc

    @staticmethod
    def screen(df: DataFrame, cd: dict) -> DataFrame:
        """ data screen """
        df_cy = df.copy()
        idx_z = [True for i in df_cy.index]
        def orcom(a, b): return [any([a[i], b[i]]) for i in range(len(a))]
        def addcom(a, b): return [all([a[i], b[i]]) for i in range(len(a))]
        for z in cd:
            if isinstance(cd[z], list):
                for index, c in enumerate(cd[z]):
                    if index != 0:
                        idx_c = orcom(idx_c, list(df_cy[z] == c))
                    else:
                        idx_c = list(df_cy[z] == c)
            else:
                idx_c = list(df_cy[z] == cd[z])
            idx_z = addcom(idx_z, idx_c)
        print("\033[1;32mscreen successfully.\033[0m")
        return df_cy.loc[idx_z, :]


if __name__ == "__main__":
    jet = JET()
    df = jet.read(path=r"E:\Desktop\test_data\demo.xlsx", )
    d = jet.get_last_account(df)
    print(d)
    

    def gl():
        df["Account"] = df["entity"] + "_" + df["account"]
        pt = jet.pivot(dataframe=df, index=["Account"], values=[""], path=r"")
        cd = {
            "Account": pt
        }
        df_col = [col for col in df.columns]
        data_fr = pd.DataFrame(df, columns=df_col)
        df = jet.screen(df, cd)
        df.to_excel()

    def tb():
        df = jet.get_last_account(df)
        df.to_excel()

    print("\033[1;32mdone.\033[0m")
