'''
Author: tansen
Date: 2023-02-09 23:46:35
LastEditors: tansen
LastEditTime: 2023-02-10 23:04:33
'''
import os
import numpy as np
import pandas as pd


class DataRecon:
    def __init__(
        self, 
        path_gl,  # gl path
        path_tb,  # tb path
        save_name,  # file save name
        save_path,  # file save path
        opening,  # opening balance
        closing,  # closing balance
        debit,  # debit amount
        credit,  # credit amount
        company_gl,  # gl company name
        company_tb,  # tb company name
        account_gl,  # gl account code
        account_tb,  # tb account code
        position,  # position
        is_direction=False,  # 是否有借贷方向,默认无
        is_lastAccount=False,  # 是否取末级科目,默认无
        is_openDebit=False,  # tb是否有借贷,默认无
        open_oth=None,  # opening credit
        close_oth=None,  # closing credit
        symbol=None,  # 借方符号,默认无
        direction=None  # 借贷方向column name,默认无
        ) -> None:
        self.path_gl = path_gl
        self.path_tb = path_tb
        self.save_name = save_name
        self.save_path = save_path
        self.opening = opening
        self.closing = closing
        self.debit = debit
        self.credit = credit
        self.company_gl = company_gl
        self.company_tb = company_tb
        self.position = position
        self.account_gl = account_gl
        self.account_tb = account_tb
        self.is_direction = is_direction
        self.is_lastAccount = is_lastAccount
        self.is_openDebit = is_openDebit
        self.open_oth = open_oth
        self.close_oth = close_oth
        self.symbol = symbol
        self.direction = direction

    def read_file(self, file_path):
        """ read file """
        try:
            data = pd.read_excel(file_path, dtype=object)
        except:
            data = pd.read_csv(file_path, dtype=object)
        return data

    def handle_gl(self):
        """ handle gl """
        try:
            data = self.read_file(self.path_gl)
            data = data.fillna(0)
            data[self.debit] = data[self.debit].astype(float)
            data[self.credit] = data[self.credit].astype(float)
            data["Account"] = data[self.company_gl] + "_" + data[self.account_gl]
            data["Opening"] = None
            data["Closing"] = None
            data["Amount"] = data[self.debit] - data[self.credit]
            print(f"\033[36mstep 1 -> read GL {os.path.basename(self.path_gl)} successfully.\033[0m")  
            return data.loc[:, ["Account", "Opening", "Closing", "Amount"]]
        except Exception as e:
            print(f"step 1 Error: {e}")
    
    def handle_tb(self):
        """ handle tb """
        try:
            data = self.read_file(self.path_tb)
            data["Account"] = data[self.company_tb] + "_" + data[self.account_tb]
            if self.is_lastAccount:
                data = data.loc[~data[self.account_tb].isnull()]
                data = self.get_value(data)
                data = data.fillna(0)
                data[self.opening] = data[self.opening].astype(float)
                data[self.closing] = data[self.closing].astype(float)
                if self.is_openDebit:
                    data[self.open_oth] = data[self.open_oth].astype(float)
                    data[self.close_oth] = data[self.close_oth].astype(float)
                    data["Opening"] = data[self.opening] - data[self.open_oth]
                    data["Closing"] = data[self.closing] - data[self.close_oth]
                if not self.is_openDebit:
                    data = self.get_direction(data)
            if not self.is_lastAccount:
                data[self.opening] = data[self.opening].astype(float)
                data[self.closing] = data[self.closing].astype(float)
                data = self.get_direction(data)
            data["Amount"] = None
            print(f"\033[36mstep 2 -> read TB {os.path.basename(self.path_tb)} successfully.\033[0m")
            return data.loc[:, ["Account", "Opening", "Closing", "Amount"]]
        except Exception as e:
            print(f"step 2 Error: {e}")

    def merge_data(self):
        """ merge gl and tb table"""
        gl = self.handle_gl()
        tb = self.handle_tb()
        try:
            rt = pd.concat([gl, tb], axis=0, ignore_index=False, sort=False)
            rt["Opening"] = rt["Opening"].astype(float)
            rt["Closing"] = rt["Closing"].astype(float)
            rt["Amount"] = rt["Amount"].astype(float)
            print(f"\033[36mstep 3 -> merge {os.path.basename(self.path_gl)} and {os.path.basename(self.path_tb)} completed.\033[0m")
            return rt
        except Exception as e:
            print(f"step 3 Error: {e}")

    def pivot_data(self):
        """ data pivot and recon """
        rt = self.merge_data()
        pt = pd.pivot_table(
            rt, index=['Account'], 
            values=['Opening', 'Closing', 'Amount'], 
            aggfunc=np.sum)
        print(f"\033[36msetp 4 -> pivot completed.\033[0m")
        pt.insert(loc=0, column="Account", value=pt.index)
        pt["Difference"] = pt["Opening"] - pt["Closing"] + pt["Amount"]
        try:
            pt.to_excel(f"{self.save_path}/{self.save_name}.xlsx", index=False, encoding="gbk")
            print(f"\033[36msave path -> '{self.save_path}\\{self.save_name}.xlsx'\033[0m")
        except Exception as e:
            print(f"step 4 Error: {e}")

    def df_screen(self, df, cd):
        df_cy = df.copy() 
        idx_z = [ True for i in df_cy.index]
        orcom  = lambda a, b: [ any([a[i],b[i]]) for i in range(len(a))]
        addcom  = lambda a, b: [ all([a[i],b[i]]) for i in range(len(a))]
        for z in cd:
            if isinstance(cd[z], list):
                for index,c in enumerate(cd[z]):
                    if index!=0:
                        idx_c = orcom(idx_c, list(df_cy[z] == c))
                    else:
                        idx_c = list(df_cy[z] == c)    
            else:
                idx_c = list(df_cy[z] == cd[z])
            idx_z = addcom(idx_z, idx_c)
        return df_cy.loc[idx_z, :]

    def get_value(self, data):
        cell = 0
        last_acc = []
        df_col = [col for col in data.columns]
        data_fr = pd.DataFrame(data, columns=df_col)
        while cell < len(data)-1:
            try:
                if data.iloc[cell, self.position-1] == data.iloc[cell+1, self.position-1][:len(data.iloc[cell, self.position-1])]:
                    pass
                else:
                    last_acc.append(data.iloc[cell, self.position-1])
                cell += 1
            except:
                break
        last_acc.append(data.iloc[len(data)-1, self.position-1])
        cd = {
            self.account_tb: last_acc
        }
        data = self.df_screen(data_fr, cd)
        return data
    
    def get_direction(self, data):
        if self.is_direction:
            data["Opening"] = data.apply(lambda x: x[self.opening] if x[self.direction] == self.symbol else x[self.direction] * -1, axis=1)
            data["Closing"] = data.apply(lambda x: x[self.closing] if x[self.direction] == self.symbol else x[self.direction] * -1, axis=1)
        if not self.is_direction:
            data["Opening"] = data[self.opening]
            data["Closing"] = data[self.closing]
        return data