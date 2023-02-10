from data_recon import DataRecon


config_args_kingdee = {
    "path_gl": r"test_gl.xlsx",  # 序时账的路径
    "path_tb": r"test_tb.xlsx",  # 余额表的路径
    "save_name": "test_recon",  # 保存的文件名(不用写后缀名)
    "save_path": r"",  # 保存文件的路径
    "opening": "期初余额借方",  # 期初余额 column name
    "closing": "期末余额借方",  # 期末余额 colunm name
    "debit": "借方",  # 借方发生额 column name
    "credit": "贷方",  # 贷方发生额 column name
    "company_gl": "公司",  # gl公司 column name
    "company_tb": "company",  # tb公司 column name
    "account_gl": "科目编码",  # gl科目代码 column name
    "account_tb": "科目代码",  # tb科目代码 column name
    "position": 2,  # tb科目代码所在第n列
    "is_direction": False,  # 是否是否有借贷方向,有则True,无则False
    "is_lastAccount": True,  # 是否取末级科目,是则True,否则False
    "is_openDebit": True,  # 是否有期初借贷
    "open_oth": "期初余额贷方",  # opening credit
    "close_oth": "期末余额贷方",  # closing credit
    "symbol": "",  # 借方发生额符号
    "direction": "",  # 借贷方向 column name
}


if __name__ == "__main__":
    print("\033[35mstart running...\033[0m")
    recon = DataRecon(
        path_gl=config_args_kingdee["path_gl"],
        path_tb=config_args_kingdee["path_tb"],
        save_name=config_args_kingdee["save_name"],
        save_path=config_args_kingdee["save_path"],
        opening=config_args_kingdee["opening"],
        closing=config_args_kingdee["closing"],
        debit=config_args_kingdee["debit"],
        credit=config_args_kingdee["credit"],
        company_gl=config_args_kingdee["company_gl"],
        company_tb=config_args_kingdee["company_tb"],
        account_gl=config_args_kingdee["account_gl"],
        account_tb=config_args_kingdee["account_tb"],
        position=config_args_kingdee["position"],
        is_direction=config_args_kingdee["is_direction"],
        is_lastAccount=config_args_kingdee["is_lastAccount"],
        is_openDebit=config_args_kingdee["is_openDebit"],
        open_oth=config_args_kingdee["open_oth"],
        close_oth=config_args_kingdee["close_oth"],
        symbol=config_args_kingdee["symbol"],
        direction=config_args_kingdee["direction"]
    )
    recon.pivot_data()
    print("\033[35mend of run.\033[0m")
