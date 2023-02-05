'''
Author: tansen
Date: 2023-02-04 21:26:17
LastEditors: tansen
LastEditTime: 2023-02-05 11:13:15
'''

import os
import numpy as np
import pandas as pd


class DataRecon:
    def __init__(self, path_gl, path_tb, save_name, save_path) -> None:
        self.path_gl = path_gl
        self.path_tb = path_tb
        self.save_name = save_name
        self.save_path = save_path
        self.pivot_data()

    def read_file(self, file_path):
        """ 读取文件 """
        try:
            data = pd.read_excel(file_path, dtype=object)
        except:
            data = pd.read_csv(file_path, dtype=object)
        return data

    def handle_gl(self):
        try:
            # read GL
            data = self.read_file(self.path_gl)
            # 将dr与cr转为float
            data["借方发生额"] = data["借方发生额"].astype(float)
            data["贷方发生额"] = data["贷方发生额"].astype(float)
            # add column account, opeing, closing
            data["account"] = data["被审计单位"] + "_" + data["科目编号"]
            data["opening"] = None
            data["closing"] = None
            # get amount for gl
            data["amount"] = data["借方发生额"] - data["贷方发生额"]
            print(f"read GL -> {os.path.basename(self.path_gl)} successfully.")
            return data.loc[:, ["account", "opening", "closing", "amount"]]
        except Exception as e:
            print(e)

    def handle_tb(self):
        try:
            # read TB
            data = self.read_file(self.path_tb)
            # 将opening与closing转为float
            data["期初数"] = data["期初数"].astype(float)
            data["期末数"] = data["期末数"].astype(float)
            # get account, opening, closing, amount
            data["account"] = data["被审计单位"] + "_" + data["科目编号"]
            data["opening"] = data.apply(self.opening, axis=1)
            data["closing"] = data.apply(self.closing, axis=1)
            data["amount"] = None
            print(f"read TB -> {os.path.basename(self.path_tb)} successfully.")
            return data.loc[:, ["account", "opening", "closing", "amount"]]
        except Exception as e:
            print(e)

    def opening(self, row):
        if row["借贷方向"] == "借":
            return row["期初数"]
        if row["借贷方向"] == "贷":
            return row["期初数"]*-1

    def closing(self, row):
        if row["借贷方向"] == "借":
            return row["期末数"]
        if row["借贷方向"] == "贷":
            return row["期末数"]*-1

    def merge_data(self):
        """ 合并GL和TB """
        gl = self.handle_gl()
        tb = self.handle_tb()
        try:
            # merge gl and tb
            rt = pd.concat([gl, tb], axis=0, ignore_index=False, sort=False)
            rt["opening"] = rt["opening"].astype(float)
            rt["closing"] = rt["closing"].astype(float)
            rt["amount"] = rt["amount"].astype(float)
            print("merge completed.")
            return rt
        except Exception as e:
            print(e)

    def pivot_data(self) -> None:
        rt = self.merge_data()
        # pivot
        pt = pd.pivot_table(rt, index=['account'], values=['opening', 'closing', 'amount'], aggfunc=np.sum)
        print(f"pivot completed.")
        # insert column
        pt.insert(loc=0, column="account", value=pt.index)
        # reset index
        pt.reset_index(drop=True, inplace=True)
        # calculate diff
        pt["diff"] = pt["opening"] - pt["closing"] + pt["amount"]
        try:
            pt.to_excel(f"{self.save_path}/{self.save_name}.xlsx", index=False, encoding="gbk")
            print(f"save path -> '{self.save_path}\\{self.save_name}.xlsx'")
        except Exception as e:
            print(e)
