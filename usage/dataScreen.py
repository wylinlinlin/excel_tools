import pandas as pd
import os


target_args = {
    # 需要拆账的文件路径
    "file_path": r'C:/Users/hanstan/Desktop/434611/mer_save/8files/业务及管理费.csv',
    # 筛选条件的文件路径
    "txt_path": r'C:/Users/hanstan/Desktop/486615/2022-10/code.txt',
    # "sana_path": r"C:/Users/hanstan/Desktop/486615/2022-10/name.txt",
    # 保存文件的文件路径
    "out": r'C:/Users/hanstan/Desktop/486615/wyn_sa/by_account',
    # 待筛选的列名
    "col1": '机构',
    # "col2": ''
}


def df_screen(df, cd):
    df_cy = df.copy() 
    idx_z = [True for i in df_cy.index]
    orcom  = lambda a, b: [any([a[i], b[i]]) for i in range(len(a))]
    addcom  = lambda a, b: [all([a[i], b[i]]) for i in range(len(a))]
    for z in cd:
        if isinstance(cd[z], list):
            for index, c in enumerate(cd[z]):
                if index != 0:
                    idx_c = orcom(idx_c, list(df_cy[z] == c))
                else:
                    idx_c = list(df_cy[z] == c)            
        else:
            idx_c = list(df_cy[z] == cd[z])
        idx_z = addcom(idx_z ,idx_c)
    return df_cy.loc[idx_z, :]

def read_data(file_path):
    file_name = os.path.splitext(file_path)
    if file_name[1] == '.xlsx':
        df = pd.read_excel(file_path, dytype=object)
    else:
        df = pd.read_csv(file_path, dtype=object)
        # df['add_col'] = df['科目代码'].str[:4]
    return df

def read_target(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    target = [line.strip('\n') for line in lines]
    return target

def read_sana(sana_path):
    with open(sana_path, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    sana = [line.strip('\n') for line in lines]
    return sana

def main():
    print('开始读取数据...')
    df = read_data(target_args['file_path'])
    df_col = [df.columns[col] for col in range(len(df.columns))]
    data_fr = pd.DataFrame(df, columns=df_col)
    target = read_target(target_args['txt_path'])
    # target_code = read_sana(target_args["sana_path"])
    # sa_name = read_sana(target_args['sana_path'])
    for tar in range(len(target)):
        cd = {
            # target_args['col1']: target[tar],  # 第1个条件
            df["add_col"]: target[tar]
            # target_args['col2']: []  # 第2个条件
        }
        new_df = df_screen(data_fr, cd)
        del new_df["add_col"]
        try:
            new_df.to_excel(target_args['out'] + '/' + str(target[tar]) + '.xlsx', index=False, encoding='gbk')
            print(f"{str(tar+1)} {str(target[tar])}.xlsx is saved")
        except:
            new_df.to_csv(target_args['out'] + '/' + str(target[tar]) + '.csv', index=False, encoding='utf-8')
            print(str(tar+1) + ' ' + str(target[tar]) + '.csv is saved.')
        else:
            pass
    print('---------------ok---------------')


if __name__ == '__main__':
    main()
