'''
Author: tansen
Date: 2023-03-05 13:13:22
LastEditors: tansen
LastEditTime: 2023-03-10 22:11:52
'''
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Bar, Line
from pyecharts.commons.utils import JsCode
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
    
    @staticmethod
    def test5(
        df: DataFrame,
        entity: str = "Entity",
        journalNumber: str = "Journal Number",
        lineDescription: str = "Line Description",
    ) -> None:
        df["desc_len"] = df[lineDescription].str.len()
        pt = pd.pivot_table(df, index=["desc_len", entity, journalNumber], values=None)
        pt.index = pt.index.set_names(['desc_len', 'Entity', 'Journal Number'])
        pt.reset_index(inplace=True)
        pt = pt.loc[:, ['desc_len', 'Entity', 'Journal Number']]
        pt = pd.DataFrame(pt["desc_len"].value_counts(sort=False).reset_index())
        pt.columns = ['分录摘要字符长度', '凭证数量']
        def section(df):
            if df["分录摘要字符长度"] == 0:
                return str(0)
            if df["分录摘要字符长度"] == 1:
                return str(1)
            if df["分录摘要字符长度"] == 2:
                return str(2)
            if df["分录摘要字符长度"] == 3:
                return str(3)
            if df["分录摘要字符长度"] == 4:
                return str(4)
            if df["分录摘要字符长度"] == 5:
                return str(5)
            if df["分录摘要字符长度"] == 6:
                return str(6)
            if df["分录摘要字符长度"] == 7:
                return str(7)
            if df["分录摘要字符长度"] == 8:
                return str(8)
            if df["分录摘要字符长度"] == 9:
                return str(9)
            if df["分录摘要字符长度"] >= 10:
                return str("≥10")
        pt["section"] = pt.apply(section, axis=1)
        df_group = pt.groupby(['section'], sort=False).agg({"凭证数量":"sum"})
        df_group.reset_index(inplace=True)
        df_create = pd.DataFrame(
            {
                "section": [str(i) for i in range(11)]}
        )
        df_create = df_create.replace("10", "≥10")
        new_df = pd.merge(df_create, df_group, left_on="section", right_on="section", how="left")
        new_df["%"] = new_df["凭证数量"] / new_df["凭证数量"].sum()*100
        new_df = new_df.round({'%': 2})
        new_df.columns = ["分录摘要字符长度", "凭证数量", "%"]
        new_df = new_df.fillna(0)
        new_df["凭证数量"] = new_df["凭证数量"].astype(int)
        new_df["%"] = new_df["%"].astype(str)
        new_df["%"] = new_df["%"] + "%"
        x_axis = new_df["分录摘要字符长度"].tolist()
        y_axis_number = new_df["凭证数量"].tolist()
        y_axis_number = [int(i) for i in y_axis_number]
        y_axis_percent = new_df["%"].tolist()
        y_axis_percent = [float(x.strip('%'))*100 for x in y_axis_percent]
        def draw_triple_bar_plot():
            bar = (
                Bar(
                    init_opts=opts.InitOpts(width="700px", height="400px", bg_color="white"))
                    .add_xaxis(x_axis)
                    .add_yaxis(series_name='凭证数量',
                            y_axis=y_axis_number,
                            label_opts=opts.LabelOpts(is_show=True),)
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title="分录描述字符数量"),
                        tooltip_opts=opts.TooltipOpts(
                            is_show=True, trigger="axis"),
                        xaxis_opts=opts.AxisOpts(
                            axislabel_opts={"rotate": 16},
                            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow")
                        )
                    )
            )
            line = (
                Line()
                    .add_xaxis(x_axis)
                    .add_yaxis(
                        "%", 
                        y_axis_percent, 
                        label_opts=opts.LabelOpts(
                            formatter=JsCode("function (params) {return params.value[1]/100 + '%'}")))
                    .set_global_opts(
                        yaxis_opts=opts.AxisOpts(
                            axislabel_opts=opts.LabelOpts(formatter="{value} %")))
            )
            bar.overlap(line)
            bar.render("saveFile/test5.html")
        draw_triple_bar_plot()
        new_df.to_excel("saveFile/test5.xlsx", index=False)
        print("\033[1;32mtest5 completed.\033[0m")

    @staticmethod
    def test8_9(
        df: DataFrame
    ) -> None:
        df = df.loc[:, ["Entity", "Journal Number", "Signed Amount EC"]]
        df["Signed Amount EC"] = df["Signed Amount EC"].abs().astype(int)
        pt = pd.pivot_table(df, index=["Signed Amount EC", "Entity", "Journal Number"])
        pt.reset_index(inplace=True)
        pt["amount"] = pt["Signed Amount EC"]
        df_group = pt.groupby(['Signed Amount EC'], sort=False).agg({"amount":"count"})
        df_group.reset_index(inplace=True)
        df_group.columns = ["账套中所包含的金额（*不包含小数）", "Distinct Count of Journal Number"]
        df_group["账套中所包含的金额（*不包含小数）"] = df_group["账套中所包含的金额（*不包含小数）"].astype(str)
        df_group["金额长度"] = df_group["账套中所包含的金额（*不包含小数）"].str.len()
        df_group["账套中所包含的金额（*不包含小数）"] = df_group["账套中所包含的金额（*不包含小数）"].astype(int)
        df_group.to_excel("saveFile/test8_9.xlsx", index=False)
