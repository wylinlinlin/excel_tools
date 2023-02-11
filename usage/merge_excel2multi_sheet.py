""" 将多个excel的单个sheet合并至一个excel多个sheet """
import os
import pandas as pd

dir = r'C:\Users\hanstan\Desktop\475929\init_data\new_sub\mer'
origin_file_list = os.listdir(dir)

with pd.ExcelWriter(r'C:\Users\hanstan\Desktop\475929\init_data\new_sub\v3.xlsx') as writer:
    # 循环遍历列表
    for file in range(len(origin_file_list)):
        # 拼接每个文件的路径
        # file_path = dir + '/' + origin_file_list[file]
        file_path = f"{dir}/{origin_file_list[file]}"
        # 把表名赋予给对应的sheet，去掉文件类型.xlsx  .split('_')[1][:-5]}
        sheet_name = f"{str(file+1)}{origin_file_list[file].split('_')[1][:-5]}"
        df = pd.read_excel(file_path)
        df.to_excel(writer, sheet_name, index=False)
        # 变相解决表格中第一行第一列为空的缺陷
        string = "".join(list(str(i) for i in df.index))
        print(f"{str(file+1)} {str(origin_file_list[file])} merged.")
        # 如果索引都为数字，则不保留索引
        if string.isdigit():
            df.to_excel(writer, sheet_name, index=False)
        else:
            df.to_excel(writer, sheet_name)

print("done.")

