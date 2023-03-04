'''
Author: XiaZeCheng
Date: 2023-03-02 20:01:08
LastEditors: tansen
LastEditTime: 2023-03-04 22:42:29
'''

import re
import warnings
from typing import Union

import numpy as np
import pandas as pd
from rich.progress import track
from pandas.core.frame import DataFrame


warnings.filterwarnings("ignore")


class JournalsTemplate():
    def __init__(self) -> None:
        pass
    
    '''
    @staticmethod
    def insert_column(
        df: DataFrame
    ) -> DataFrame:
        """ insert column """
        try:
            # read template column name
            with open("config/columnName.txt", "r", encoding="utf-8") as fp:
                column_names = fp.readlines()
            list_cs = [column_name.strip("\n") for column_name in column_names]
            # insert column
            for value in list_cs:
                df[value] = None
            print("\033[1;32minsert column successfully.\033[0m")
            return df
        except Exception:
            print("\033[31;1mError: columnName.txt not found.\033[0m")
    '''

    @staticmethod
    def reset_column(
        df: DataFrame,
        entity: str = "Entity",
        companyName: str = "Company Name",
        journalNumber: str = "Journal Number",
        spotlightType: str = "Spotlight Type",
        dateEntered: str = "Date Entered",
        timeEntered: str = "Time Entered",
        dateUpdated: str = "Date Updated",
        timeUpdated: str = "Time Updated",
        userIDEntered: str = "UserID Entered",
        nameOfUserEntered: str = "Name of User Entered",
        userIDUpdated: str = "UserID Updated",
        nameOfUserUpdated: str = "Name of User Updated",
        dateEffective: str = "Date Effective",
        dateOfJournal: str = "Date of Journal",
        financialPeriod: str = "Financial Period",
        journalType: str = "Journal Type",
        journalTypeDescription: str = "Journal Type Description",
        autoManualOrInterface: str = "Auto Manual or Interface",
        journalDescription: str = "Journal Description",
        lineNumber: str = "Line Number",
        lineDescription: str = "Line Description",
        currency: str = "Currency",
        entityCurrencyEC: str = "Entity Currency (EC)",
        exchangeRate: str = "Exchange Rate",
        dcIndicator: str = "DC Indicator",
        signedJournalAmount: str = "Signed Journal Amount",
        unsignedDebitAmount: str = "Unsigned Debit Amount",
        unsignedCreditAmount: str = "Unsigned Credit Amount",
        signedAmountEC: str = "Signed Amount EC",
        unsignedDebitAmountEC: str = "Unsigned Debit Amount EC",
        unsignedCreditAmountEC: str = "Unsigned Credit Amount EC",
        accountNumber: str = "Account Number",
        accountDescription: str = "Account Description",
        controllingAreaForCostAndProfitCentre: str = "Controlling Area for Cost and Profit Centre",
        costCentre: str = "Cost Centre",
        costCentreDescription: str = "Cost Centre Description",
        profitCentre: str = "Profit Centre",
        profitCentreDescription: str = "Profit Centre Description",
        sourceActivityOrTransactionCode: str = "Source Activity or Transaction Code"
    ) -> DataFrame:
        df["Entity"] = df[entity]
        df["Company Name"] = df[companyName]
        df["Journal Number"] = df[journalNumber]
        df["Spotlight Type"] = df[spotlightType]
        df["Date Entered"] = df[dateEntered]
        df["Time Entered"] = df[timeEntered]
        df["Date Updated"] = df[dateUpdated]
        df["Time Updated"] = df[timeUpdated]
        df["UserID Entered"] = df[userIDEntered]
        df["Name of User Entered"] = df[nameOfUserEntered]
        df["UserID Updated"] = df[userIDUpdated]
        df["Name of User Updated"] = df[nameOfUserUpdated]
        df["Date Effective"] = df[dateEffective]
        df["Date of Journal"] = df[dateOfJournal]
        df["Financial Period"] = df[financialPeriod]
        df["Journal Type"] = df[journalType]
        df["Journal Type Description"] = df[journalTypeDescription]
        df["Auto Manual or Interface"] = df[autoManualOrInterface]
        df["Journal Description"] = df[journalDescription]
        df["Line Number"] = df[lineNumber]
        df["Line Description"] = df[lineDescription]
        df["Currency"] = df[currency]
        df["Entity Currency (EC)"] = df[entityCurrencyEC]
        df["Exchange Rate"] = df[exchangeRate]
        df["DC Indicator"] = df[dcIndicator]
        df["Signed Journal Amount"] = df[signedJournalAmount]
        df["Unsigned Debit Amount"] = df[unsignedDebitAmount]
        df["Unsigned Credit Amount"] = df[unsignedCreditAmount]
        df["Signed Amount EC"] = df[signedAmountEC]
        df["Unsigned Debit Amount EC"] = df[unsignedDebitAmountEC]
        df["Unsigned Credit Amount EC"] = df[unsignedCreditAmountEC]
        df["Account Number"] = df[accountNumber]
        df["Account Description"] = df[accountDescription]
        df["Controlling Area for Cost and Profit Centre"] = df[controllingAreaForCostAndProfitCentre]
        df["Cost Centre"] = df[costCentre]
        df["Cost Centre Description"] = df[costCentreDescription]
        df["Profit Centre"] = df[profitCentre]
        df["Profit Centre Description"] = df[profitCentreDescription]
        df["Source Activity or Transaction Code"] = df[sourceActivityOrTransactionCode]
        return df
    
    @staticmethod
    def pivot(
        df: DataFrame,
        index: Union[str, list[str], None] = None,
        values: Union[str, list[str], None] = None,
        save_path: str = "saveFile",
        is_pivot: bool = False,  # export pivot table -> default(No)
        is_net2zero: bool = False  # export net 2 zero table -> default(No)
    ) -> None:
        """ get pivot table and net 2 zero table """
        pt = pd.pivot_table(df, index=index, values=values, aggfunc=np.sum)
        if is_pivot:
            pt.insert(loc=0, column="Account", value=pt.index)
            pt.to_excel(f"{save_path}/pivot.xlsx", index=False)
            print("\033[1;32mpivot save file path: {save_path}\\pivot.xlsx\033[0m")
        if is_net2zero:
            pt.to_excel(f"{save_path}/net2zero.xlsx")
            print("\033[1;32mnet2zero save file path: {save_path}\\net2zero.xlsx\033[0m")
    
    @staticmethod
    def convert_format(
        df: DataFrame,
        dateEffective: str = "Date Effective",
        dateEntered: str = "Date Entered",
        lineDescription: str = "Line Description",
        is_convertDate: bool = False,  # convert date format to dd/mm/yyyy
        is_retain2decimals: bool = False,  # retain 2 decimals
        is_processStrings: bool = False,  # clear special symbols, limit string length
    ) -> DataFrame:
        """ convert format """
        if is_convertDate:
            df[dateEffective] = pd.to_datetime(df[dateEffective])
            df[dateEffective] = pd.to_datetime(df[dateEffective]).dt.strftime("%d/%m/%Y")
            df[dateEntered] = pd.to_datetime(df[dateEntered])
            df[dateEntered] = pd.to_datetime(df[dateEntered]).dt.strftime("%d/%m/%Y")
            print("\033[1;32mconvert date format successfully.\033[0m")
        if is_retain2decimals:
            df = df.round({'Unsigned Debit Amount': 2, 'Unsigned Credit Amount': 2, "Signed Journal Amount":2, 
                 "Unsigned Debit Amount EC":2, "Unsigned Credit Amount EC":2, "Signed Amount EC":2})
            print("\033[1;32mretain 2 decimals successfully.\033[0m")
        if is_processStrings:
            df[lineDescription] = df[lineDescription].astype(str)
            df[lineDescription] = df[lineDescription].apply(lambda x: re.sub("\W", "", x))
            df[lineDescription] = df[lineDescription].apply(lambda x: x[: 200])
            print("\033[1;32mclear special symbols and limits string length successfully.\033[0m")
        return df
    
    @staticmethod
    def calculation_sum(
        df: DataFrame,
        debit: str = "Unsigned Debit Amount EC",
        credit: str = "Unsigned Credit Amount EC",
        amount: str = "Signed Amount EC"
    ) -> None:
        """ calculation of summation """
        df[debit] = df[debit].astype(float)
        df[credit] = df[credit].astype(float)
        df[amount] = df[amount].astype(float)
        print(f'\033[34mDebit -> {df[debit].sum()}\033[0m')
        print(f'\033[34mCredit -> {df[credit].sum()}\033[0m')
        print(f'\033[34mAmount -> {df[amount].sum()}\033[0m')
    
    @staticmethod
    def sort_add(
        df: DataFrame,
        journalNumber: str = "Journal Number",
        lineNumber: str = "Line Number",
        financialPeriod: str = "Financial Period",
        ascending: bool = True,
        is_sort: bool = False,  # sort values by Journal Number
        is_addLnumber: bool = False,  # add Line Number -> default(No)
        is_addFperiod: bool = False,  # add Financial Period
    ) -> DataFrame:
        if is_sort:
            df = df.sort_values(by=journalNumber, ascending=ascending, ignore_index=True)
            print("\033[1;32msort value successfully.\033[0m")
        if is_addLnumber:
            df[lineNumber] = int(1)
            for value in track(range(1, len(df))):
                if df[journalNumber][value] == df[journalNumber][value-1]:
                    df[lineNumber][value] = df[lineNumber][value-1] + 1
                else:
                    df[lineNumber][value] = 1
            print("\033[1;32madd Line Number successfully.\033[0m")
        if is_addFperiod:
            df[financialPeriod] = df["Date Effective"].str.split("/")[1]
            df[financialPeriod] = df[financialPeriod].astype("uint8")
            print("\033[1;32madd Financial Period successfully.\033[0m")
        return df
    
    @staticmethod
    def get_last_account(
        df: DataFrame,
        location: int = 2,  # entity_accountCode loaction
        entity_account: str = "enacc",  # entity_accountCode column
    ) -> list:
        """ get end-level account """
        cell = 0
        last_acc: list = []
        while cell < len(df)-1:
            try:
                if df.iloc[cell, location-1] == df.iloc[cell+1, location-1][:len(df.iloc[cell, location-1])]:
                    pass
                else:
                    last_acc.append(df.iloc[cell, df.columns.get_loc(entity_account)])
                cell += 1
            except:
                break
        last_acc.append(df.iloc[len(df)-1, location-1])
        print("\033[1;32mget end-level account successfully.\033[0m")
        return last_acc
    
    @staticmethod
    def screen(
        df: DataFrame,
        entity_account: str = "enacc",  # entity_accountCode column
        screen_condition: Union[str, list[str], None] = None  # screening conditions
    ) -> DataFrame:
        """ screen data """
        list_screen: list = []
        for condition in screen_condition:
            df_screen = df.loc[df[entity_account] == condition]
            list_screen.append(df_screen)
        df = pd.concat(list_screen, axis=0, ignore_index=True, sort=False)
        print("\033[1;32mscreen data successfully.\033[0m")
        return df
    
    @staticmethod
    def calculation_dc(
        df: DataFrame,
        amount: str = "Signed Amount EC",
        dcIndicator: str = "DC Indicator",
        debit: str = "Unsigned Debit Amount EC",
        credit: str = "Unsigned Credit Amount EC",
        is_calculationDC: bool = False,  # calculate the dc according to the dc direction
        is_direction: bool = False,  # calculate the dc direction according to the amount
    ) -> DataFrame:
        if is_direction:
            df[amount] = df[amount].astype(float)
            df[dcIndicator] = np.where(df[amount] >= 0, "D", "C")
            print("\033[1;32madjust dc direction successfully.\033[0m")
        if is_calculationDC:
            df[debit] = np.where(df[amount]>0, df[amount], 0)
            df[credit] = np.where(df[amount]<0, df[amount]*-1, 0)
            print("\033[1;32madjust dc values successfully.\033[0m")
        return df
    
    @staticmethod
    def get(
        df: DataFrame
    ) -> DataFrame:
        try:
            # read template column name
            with open("config/columnName.txt", "r", encoding="utf-8") as fp:
                column_names = fp.readlines()
            list_cs = [column_name.strip("\n") for column_name in column_names]
            # insert column
            print("\033[1;32mget columns successfully.\033[0m")
            return df.loc[:, list_cs]
        except Exception:
            print("\033[31;1mError: columnName.txt not found.\033[0m")
    
    @staticmethod
    def write(
        df: DataFrame,
        path: str = "saveFile/handleGL.txt"
    ) -> None:
        df.to_csv(path, index=False, encoding="utf-16le", sep="|")
        print(f"\033[1;32msave path -> {path}.\033[0m")
    
    @staticmethod
    def check(
        df: DataFrame,
        entity: str = "Entity",
        currency: str = "Currency",
        currencyEC: str = "Entity Currency (EC)",
        amount: str = "Signed Amount EC",
        debit: str = "Unsigned Debit Amount EC",
        credit: str = "Unsigned Credit Amount EC",
        mi: str = "Auto Manual or Interface",
        fp: str = "Financial Period",
        is_equal: bool = True,  # check debit credit and amount column
        is_mi: bool = True,  # check auto manual or interface column
        is_negative: bool = True,  # check negative number
        is_month: bool = True,  # check Financial Period
        is_entity: bool = True,  # check entity
        is_currency: bool = True,  # check currency
    ) -> DataFrame:
        if is_equal:
            debit_sum = df[debit].sum()
            credit_sum = df[credit].sum()
            amount_sum = df[amount].sum()
            if debit_sum == credit_sum and amount_sum == float(0):
                print("\033[1;32mdebit credit amount is correct.\033[0m")
            else:
                print("\033[1;31mError: please check debit credit and amount column.\033[0m")
        if is_mi:
            ami = df[mi].unique().tolist()
            if pd.isna(ami):
                print("\033[1;31mError: [Auto Manual or Interface] column is null.\033[0m")
            else:
                print(f"\033[1;34m[Auto Manual or Interface] -> {ami}\033[0m")
        if is_negative:
            uni_d = df[debit].unique().tolist()
            uni_c = df[credit].unique().tolist()
            neg_d = [value for value in uni_d if value < 0]
            neg_c = [value for value in uni_c if value < 0]
            if len(neg_d) == 0 and len(neg_c) == 0:
                print("\033[1;32mno negative number.\033[0m")
            else:
                print("\033[1;31mError: there are negative numbers.\033[0m")
        if is_month:
            month = df[fp].unique().tolist()
            if pd.isna(month):
                print("\033[1;31mError: [Financial Period] column is null.\033[0m")
            else:
                print(f"\033[1;34m[Financial Period] -> {month}\033[0m")
        if is_entity:
            ent = df[entity].unique().tolist()
            if pd.isna(ent):
                print("\033[1;31mError: [Entity] column is null.\033[0m")
            else:
                print(f"\033[1;34m[Entity] -> {ent}\033[0m")
        if is_currency:
            curr = df[currency].unique().tolist()
            curr_ec = df[currencyEC].unique().tolist()
            if pd.isna(curr) or pd.isna(curr_ec):
                print("\033[1;31mError: [Currency] or [Currency EC] column is null.\033[0m")
            else:
                print(f"\033[1;34m[currency] -> {curr}\n[Currency EC] -> {curr_ec}\033[0m")
