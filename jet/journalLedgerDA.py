'''
Author: tansen
Date: 2023-03-05 13:13:22
LastEditors: tansen
LastEditTime: 2023-03-05 21:39:48
'''
import numpy as np
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Bar
from pandas.core.frame import DataFrame


class JournalLedgerDA:
    def __init__(self) -> None:
        pass

    @staticmethod
    def test2(
        df: DataFrame,
        entity: str = "Entity",
        journalNumber: str = "Journal Number",
        accountNumber: str = "Account Number",
        save_excel: str = "saveFile/test2.xlsx",
        save_html: str = "saveFile/test2.html"
    ) -> None:
        pt = pd.pivot_table(df, index=[accountNumber, entity, journalNumber])
        pt.index = pt.index.set_names(['Account Number', 'Entity', 'Journal Number'])
        pt.reset_index(inplace=True)
        pt = pt.loc[:, ['Account Number', 'Entity', 'Journal Number']]
        pt = pd.DataFrame(pt["Account Number"].value_counts(sort=False).reset_index())
        pt.columns = ['Account Number', 'frequency']
        pt_c = pd.pivot_table(pt, index="frequency", values="Account Number", aggfunc="count")
        pt_c.reset_index(inplace=True)
        def section(df):
            if df["frequency"] == 1:
                return str(1)
            if df["frequency"] == 2:
                return str(2)
            if 3 <= df["frequency"] <= 10:
                return str("3~≤10")
            if 11 <= df["frequency"] <= 50:
                return str("11~≤50")
            if 51 <= df["frequency"] <= 100:
                return str("51~≤100")
            if 101 <= df["frequency"] <= 200:
                return str("101~≤200")
            if 201 <= df["frequency"] <= 300:
                return str("201~≤300")
            if 301 <= df["frequency"] <= 1000:
                return str("301~≤1000")
            if df["frequency"] > 1000:
                return str(">1000")
        pt_c["section"] = pt_c.apply(section, axis=1)
        df_group = pt_c.groupby(['section'], sort=False).agg({"Account Number":"sum"})
        df_group.reset_index(inplace=True)
        df_group.columns = ["科目使用频率", "Distinct Count of Journal Number"]
        df_group.to_excel(save_excel, index=False)
        lst_acc = df_group["科目使用频率"].tolist()
        lst_jour = df_group["Distinct Count of Journal Number"].tolist()
        bar = (
            Bar(
                init_opts=opts.InitOpts(
                    width='700px',
                    height='400px',
                    bg_color="white"))
            .add_xaxis(lst_acc)
            .add_yaxis("count", lst_jour)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="科目使用频率"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(name_rotate=60, axislabel_opts={"rotate": 30}))
            .render(save_html))
        print("\033[1;32mtest2 completed.\033[0m")