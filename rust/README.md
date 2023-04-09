# csv, excel toolkit written in Rust

**rsv** is a command line tool to deal with small and big CSV, TXT, EXCEL files (especially >10G). **rsv** has following features:

- written in Rust
- fast and parallel data processing (based on Rayon)
- real-time progress bar
- simple usage
- support command pipelines

## Usage

download **rsv.exe** from release tab, and append the file directory to system path.

## Available commands

- **head** - Show head n lines of CSV, TXT or EXCEL file.
- **tail** - Show tail n lines of CSV, TXT or EXCEL file.
- **header** - Show file headers.
- **count** - Count the number of lines of file :running:.
- **estimate** - Fast estimate the number of lines.
- **clean** - Clean file with escape char (e.g. ") or other strings :running:.
- **unique** - Drop duplicates of data.
- **frequency** - Show frequency table for column(s) :running: :star:.
- **split** - Split file into separate files sequentially or based on column value :running: :star:.
- **select** - Select rows and columns by filter :running:.
- **flatten** - Prints flattened records to view records one by one.
- **slice** - Prints a slice of rows from file.
- **search** - Search with regexes :running: :star:.
- **sort** - In-memory data sorting, support for at most two columns :star:.
- **sample** - Data sampling based on priority queue.
- **stats** - Statistics for column(s), including min, max, mean, unique, null :running: :star:.
- **excel2csv** - Convert excel to csv.
- **to** - Save command output data to disk, can be one of TXT, CSV, TSV, XLSX or XLS.
- **table** - Format data as an aligned table.

Tips 1:

- :running: means the command is supported with a real-time progress bar.
- :star: means the command is supported with parallel data processing.

Tips 2:

All commands, except "clean" and "excel2csv", are allowed to be chained.

Tips 3:

You can always check usage of each command by **rsv command --help** or **rsv command -h**,
for example, rsv frequency --help.

## Basic Usage

- **rsv head**

```shell
rsv head data.csv                   # default to show head 10 records
rsv head -n 5 data.csv              # show head 5 records
rsv head data.xlsx                  # EXCEL file, default to first sheet
rsv head --sheet 1 data.xlsx        # second sheet
rsv head --help                     # help info on all flags
```

- **rsv tail**

```shell
rsv tail data.csv                   # default to show tail 10 records
rsv tail -n 5 data.csv              # show tail 5 records
rsv tail data.xlsx                  # EXCEL file, default to first sheet
rsv tail --sheet 1 data.xlsx        # second sheet
rsv tail --help                     # help info on all flags
```

- **rsv header**

```shell
rsv headers data.csv                # separator "," (default)
rsv headers -s \t data.csv          # separator tab
rsv headers data.xlsx               # EXCEL file
rsv headers --help                  # help info on all flags
```

- **rsv count**

```shell
rsv count data.csv                  # plain-text file
rsv count data.xlsx                 # EXCEL file
rsv count --no-header data.csv
rsv count --help                    # help info on all flags
```

- **rsv estimate**

```shell
rsv estimate data.csv
rsv estimate data.xlsx
rsv estimate --help                 # help info on all flags
```

- **rsv clean**

```shell
rsv clean data.csv                               # default to clean escape char "
rsv clean -e "content-to-delete" data.csv        # escape is a str, clean str to empty
rsv clean -o new-file.csv data.csv               # save to new-file.csv, the default is data-cleaned.csv
rsv clean --help                                 # help info on all flags
```

- **rsv unique**

```shell
rsv unique data.csv               # default to drop duplicates on all columns,
                                    # default keep first record of duplicates
rsv unique -c 0 data.csv          # drop on first column
rsv unique -c 0,1 data.csv        # drop on first and second columns
rsv unique --keep-last data.csv   # keep the last record when dropping
rsv unique data.xlsx              # apply to EXCEL file
rsv unique data.txt               # apply to TXT file

column selection syntax:
-c 0,1,2,5   -->    cols [0,1,2,5]
-c 0-2,5     -->    same as cols [0,1,2,5]
-c -1        -->    last column
-c -2--1     -->    last two columns
```

- **rsv frequency**

```shell
rsv frequency -c 0 data.csv              # default to the first column, descending order
rsv frequency -c 0 data.xlsx             # EXCEL file
rsv frequency -c 0,1,2,5 data.csv        # columns 0, 1, 2, and 5
rsv frequency -c 0-2,5 data.csv          # same as above
rsv frequency -c 0-2 --export data.csv   # export result to data-frequency.csv
rsv frequency -n 10 data.csv             # keep top 10 frequent items
rsv frequency -a 10 data.csv             # in ascending order
rsv frequency --help                     # help info on all flags

column selection syntax:
-c 0,1,2,5   -->    cols [0,1,2,5]
-c 0-2,5     -->    same as cols [0,1,2,5]
-c -1        -->    last column
-c -2--1     -->    last two columns
```

- **rsv split**

```shell
rsv split data.csv                # default to first column and field separator of ,
rsv split data.xlsx               # EXCEL file
rsv split -s \t data.csv          # tab separator
rsv split -c 1 data.csv           # split based on second column
rsv split -c 0 -s \t data.csv     # first column, \t separator
rsv split --size 1000 data.xlsx   # Sequential split, 1000 records in a file.
rsv split --help                  # help info on all flags
```

- **rsv select**

```shell
rsv select -f 0=a,b,c data.csv          # first column has values of a, b, or c
rsv select -f 0=a,b,c data.xlsx         # EXCEL file, sheet can be specified with the --sheet flag
rsv select -f "0N>10&1=c" data.csv      # first column > 10 numerically, AND the second column equals c
rsv select -f 0!= --export data.csv     # export result, in which the first column is non-empty
rsv select --help                       # help info on other options

Filter syntax, support =, !=, >, >=, <, <= and &:
-f 0=a,b,c           -->  first column is a, b, or c
-f 0N=1,2            -->  first column numerically equals to 1 or 2
-f 0!=               -->  first column is not empty
-f "0>=2022-01-21"   -->  first column equal to or bigger than 2022-01-21, lexicographically
-f "0N>10"           -->  first column > 10 numerically
-f "0N>10&2=pattern" -->  first column > 10 numerically, AND the third column equals to <pattern>

NOTE: 1. only & (AND) operation is supported, | (OR) operation is not supported;
      2. quotes are needed when the filter contains special chars, e.g., &, > or <;
      3. The filter option can be omitted to select all rows.

column selection syntax:
-c 0,1,2,5   -->    cols [0,1,2,5]
-c 0-2,5     -->    same as cols [0,1,2,5]
-c -1        -->    last column
-c -2--1     -->    last two columns
```

- **rsv flatten**

```shell
rsv flatten data.csv                       # default to show first 5 records
rsv flatten -n 50 data.csv                 # show 50 records
rsv flatten data.xls                       # EXCEL file
rsv flatten --delimiter "--" data.csv      # change line delimiter to anything
rsv flatten --help                         # help info on all flags
```

- **rsv slice**

```shell
rsv slice -s 100 -e 150 data.csv           # set start and end index
rsv slice -s 100 -l 50 data.csv            # set start index and the length
rsv slice -s 100 -l 50 data.xlsx           # EXCEL FILE
rsv slice -s 100 -l 50 --export data.csv   # export to data-slice.csv
rsv slice -e 10 --export data.csv          # set end index and export data
rsv slice -i 9 data.csv                    # the 10th line sliced only
rsv slice --help                           # help info on all flags
```

- **rsv search**

```shell
rsv search PATTERN data.csv                # search PATTERN
rsv search "^\d{4}-\d{2}-\d{2}$" data.csv  # search dates
rsv search --export PATTERN data.csv       # export result
rsv search PATTERN data.xlsx               # search EXCEL file
rsv slice --help                           # help info on all flags
```

- **rsv sample**

```shell
rsv sample data.csv                 # default to sample 10 records
rsv sample --no-header data.csv     # no-header
rsv sample -n 20 data.csv           # pull more
rsv sample -n 20 data.xlsx          # EXCEL file
rsv sample --seed 100 data.xlsx     # set a seed
rsv sample --time-limit 2 data.xlsx # set time limit to 2 seconds for large file
rsv sample -n 20 --export data.xlsx # data export
```

- **rsv sort**

```shell
rsv sort -c 0 data.csv        # default to sort by first column in ascending
rsv sort -c 0D data.csv       # descending sort
rsv sort -c 0DN data.csv      # sort as numeric values
rsv sort -c 0DN,2N data.csv   # sort two columns
rsv sort -E data.csv          # export result
rsv sort data.xlsx            # sort EXCEL file
```

- **rsv stats**

```shell
rsv stats data.csv                       # all columns, statistics include: min, max, mean, unique, null
rsv stats data.xlsx                      # EXCEL FILE
rsv stats -c 0,1 data.csv                # first two columns
rsv stats -c 0,1 --export data.csv       # export to data-stats.csv
rsv slice --help                         # help info on all flags
```

- **rsv excel2csv**

```shell
rsv excel2csv data.xlsx                 # apply to xlsx file, default to first sheet (or sheet1)
rsv excel2csv data.xls                  # apply also to xls file
rsv excel2csv --sheet 1 data.xls        # second sheet, e.g., sheet 2
rsv excel2csv -S 1 data.xls             # same as above
```

- **rsv table**

```shell
rsv head data.csv | rsv table                   # convert result to an aligned table
rsv slice -s 10 -e 15 data.csv | rsv table      # convert result to an aligned table
```

## Command pipeline

- **two commands pipelined**

```shell
rsv search "^\d{4}-\d{2}-\d{2}$" data.csv | rsv table     # search date and print in an aligned table
rsv select -f 0=a,b data.csv | rsv frequency -c 0         # filter rows and get its frequency table
rsv select -f "0!=&2N>10" data.csv | rsv head -n 5        # filter rows, and show head 5 records
rsv select -f "2N=10,20" -c 0-4 data.csv | rsv stats      # filter rows, select columns and make statistics
rsv select -f "2N=10,20" -c 0-4 data.csv | rsv sort -c 2  # filter rows, select columns and sort data
```

- **more commands pipelined**

```shell
rsv search pattern1 data.csv | rsv sort -c 1ND | rsv table             # search, sort and print
rsv select -f 1=a,b data.csv | rsv search pattern | rsv stats          # select, search, and make statistics
rsv select -f "0N>=10&0N<20" data.csv | rsv search pattern | rsv table # select, search, and print in a table
```

## Data export

- **method 1: by the --export or -E flag, support exporting to csv file only**

```shell
rsv slice -s 1000 -e 2000 --export data.csv           # the data export flag
rsv slice -s 1000 -e 2000 -E data.csv                 # same as above
rsv search --export pattern data.xlsx                 # export search data
rsv select -f "0N>=10" --export pattern data.xlsx     # export select data
```

- **method 2: by "rsv to" subcommand, support csv, txt, tsv, excel**

```shell
rsv slice -s 1000 -e 2000 data.csv | rsv to out.csv          # export to CSV
rsv slice -s 1000 -e 2000 data.csv | rsv to out.xlsx         # export to EXCEL
rsv search pattern data.xlsx | rsv to out.tsv                # export to TSV
rsv select -f "0N>=10" pattern data.xlsx | rsv to out.txt    # export to TXT
```

## Author

[[ribbondz](https://github.com/ribbondz/rsv/commits?author=ribbondz)](https://github.com/ribbondz/rsv)


# Rust 编写的CSV，Excel 工具包

**rsv**是一个命令行工具，用于处理小型和大型CSV，TXT，EXCEL文件（尤其是>10G）。**RSV** 具有以下功能：

- 用 Rust 编写
- 快速和并行数据处理（基于Rayon）
- 实时进度条
- 用法简单
- 支持命令管道

## 用法

从release页面下载 **rsv.exe**，并将文件添加到目标路径。

## 可用命令

- **head** - 显示 CSV、TXT 或 EXCEL 文件的开头 n 行。
- **tail** - 显示 CSV、TXT 或 EXCEL 文件的尾部 n 行。
- **header** - 显示文件头。
- **count** - 计算文件行数:running:。
- **estimate** - 快速估计行数。
- **clean** - 使用转义字符（例如“）或其他字符串清理文件:running:。
- **unique** - 删除重复数据。
- **frequency** - 显示列的频率表:running::star:。
- **split** - 按顺序或基于列值将文件拆分为单独的文件:running::star:。
- **select** - 通过过滤器选择行和列:running:。
- **flatten** - 打印扁平化的记录以一条一条地查看记录。
- **slice** - 打印文件中的一部分行。
- **search** - 使用正则表达式搜索 :running: :star:。
- **sort** - 内存数据排序，最多支持两列 :star:。
- **sample** - 基于优先级队列的数据采样。
- **stats** - 列的统计信息，包括最小值、最大值、平均值、唯一值、null :running: :star:。
- **excel2csv** - 将 excel 转换为 csv。
- **to** - 将命令输出数据保存到磁盘，可以是 TXT、CSV、TSV、XLSX 或 XLS 之一。
- **table** - 将数据格式化为对齐的表格。

提示1：

- :running: 表示该命令支持实时进度条。
- :star: 表示该命令支持并行数据处理。

提示2：

除了“clean”和“excel2csv”之外的所有命令都允许链接。

提示3：

您可以随时通过 **rsv command --help** 或 **rsv command -h** 检查每个命令的使用情况，
例如，rsv 频率 --help。

## 基本用法

**rsv head**

```shell
rsv head data.csv                   # 默认显示前10条记录
rsv head -n 5 data.csv              # 显示前5条记录
rsv head data.xlsx                  # EXCEL文件，默认第一个sheet
rsv head --sheet 1 data.xlsx        # 第二个sheet
rsv head --help                     # 所有的帮助信息
```

- **rsv tail**

```shell
rsv tail data.csv                   #默认显示最后10条记录
rsv tail -n 5 data.csv 				#显示最后5条记录
rsv tail data.xlsx 					# EXCEL文件，默认为第一个sheet
rsv tail --sheet 1 data.xlsx 		# 第二个sheet
rsv tail --help 					# 所有的帮助信息
```

- **rsv header**

```shell
rsv headers data.csv 				# 分隔符（默认为“，”）
rsv headers -s \t data.csv 			# 分隔符标签
rsv headers data.xlsx 				# EXCEL 文件
rsv headers --help 					# 所有的帮助信息
```

- **rsv count**

```shell
rsv count data.csv                  # 文本文件
rsv count data.xlsx                 # EXCEL 文件
rsv count --no-header data.csv
rsv count --help                    # 所有的帮助信息
```

- **rsv estimate**

```shell
rsv estimate data.csv
rsv estimate data.xlsx
rsv estimate --help                 # 所有的帮助信息
```

- **rsv clean**

```shell
rsv clean data.csv                               # 默认清除转义字符“
rsv clean -e "content-to-delete" data.csv        # escape一个字符串，清空字符串
rsv clean -o new-file.csv data.csv               # 保存到new-file.csv，默认是data-cleaned.csv
rsv clean --help                                 # 所有的帮助信息
```

- **rsv unique**

```shell
rsv unique data.csv               # 默认删除所有列上的重复项，
                                  # 默认保留第一个重复记录
rsv unique -c 0 data.csv          # 删除第一列上的重复项
rsv unique -c 0,1 data.csv        # 删除第一列和第二列上的重复项
rsv unique --keep-last data.csv   # 删除时保留最后一条记录
rsv unique data.xlsx              # 应用于EXCEL文件
rsv unique data.txt               # 应用于TXT文件

列选择语法:
-c 0,1,2,5   -->    cols [0,1,2,5]
-c 0-2,5     -->    same as cols [0,1,2,5]
-c -1        -->    last column
-c -2--1     -->    last two columns
```

- **rsv frequency**

```shell
rsv frequency -c 0 data.csv              # 默认为第一列，降序排列
rsv frequency -c 0 data.xlsx             # EXCEL文件
rsv frequency -c 0,1,2,5 data.csv        # 列 0 ，1，2，5
rsv frequency -c 0-2,5 data.csv          # 同上
rsv frequency -c 0-2 --export data.csv   # 将结果导出到 data-frequency.csv
rsv frequency -n 10 data.csv             # 保留前 10 个高频项
rsv frequency -a 10 data.csv             # 按升序排列
rsv frequency --help                     # 所有的帮助信息

column selection syntax:
-c 0,1,2,5   -->    cols [0,1,2,5]
-c 0-2,5     -->    same as cols [0,1,2,5]
-c -1        -->    last column
-c -2--1     -->    last two columns
```

- **rsv split**

```shell
rsv split data.csv                # 默认为第一列和字段分隔符，
rsv split data.xlsx               # EXCEL文件
rsv split -s \t data.csv          # 制表符分隔符
rsv split -c 1 data.csv           # 根据第二列拆分
rsv split -c 0 -s \t data.csv     # 第一列，\t 分隔符
rsv split --size 1000 data.xlsx   # 顺序拆分，一个文件中有 1000 条记录。
rsv split --help                  # 所有的帮助信息
```

- **rsv select**

```shell
rsv select -f 0=a,b,c data.csv          # 第一列的值为 a、b 或 c
rsv select -f 0=a,b,c data.xlsx         # EXCEL文件，sheet可以用--sheet标志指定
rsv select -f "0N>10&1=c" data.csv      # 第一列 > 10 数值，并且第二列等于 c
rsv select -f 0!= --export data.csv     # 导出结果，其中第一列非空
rsv select --help                       # 其他选项的帮助信息

Filter syntax, support =, !=, >, >=, <, <= and &:
-f 0=a,b,c 								--> 第一列是 a、b 或 c
-f 0N=1,2 								--> 第一列在数值上等于 1 或 2
-f 0!= 									--> 第一列不为空
-f "0>=2022-01-21" 						--> 第一列等于或大于 2022-01-21，按字典顺序
-f "0N>10" 								--> 第一列 > 10
-f "0N>10&2=pattern" 					--> 第一列 > 10，第三列等于 <pattern>

NOTE: 1. 只支持&（AND）操作，| (OR) 操作不受支持；
       2. 当过滤器包含特殊字符时需要引号，例如 &、> 或 <；
       3. filter选项可以省略，选择所有行。

column selection syntax:
-c 0,1,2,5   -->    cols [0,1,2,5]
-c 0-2,5     -->    same as cols [0,1,2,5]
-c -1        -->    last column
-c -2--1     -->    last two columns
```

- **rsv flatten**

```shell
rsv flatten data.csv 						# 默认显示前 5 条记录
rsv flatten -n 50 data.csv 					# 显示 50 条记录
rsv flatten data.xls 						# EXCEL文件
rsv flatten --delimiter "--" data.csv 		# 将行分隔符更改为任何内容
rsv flatten --help                         	# 所有的帮助信息
```

- **rsv slice**

```shell
rsv slice -s 100 -e 150 data.csv 			# 设置开始和结束索引
rsv slice -s 100 -l 50 data.csv 			# 设置起始索引和长度
rsv slice -s 100 -l 50 data.xlsx 			# EXCEL 文件
rsv slice -s 100 -l 50 --export data.csv 	#导出到data-slice.csv
rsv slice -e 10 --export data.csv 			#设置结束索引并导出数据
rsv slice -i 9 data.csv 					# 只对第 10 行进行切片
rsv slice --help                           	# 所有的帮助信息
```

- **rsv search**

```shell
rsv search PATTERN data.csv                # 查询 PATTERN
rsv search "^\d{4}-\d{2}-\d{2}$" data.csv  # 查询日期
rsv search --export PATTERN data.csv       # 导出结果
rsv search PATTERN data.xlsx               # 在EXCEL文件这查询
rsv slice --help                           # 所有的帮助信息
```

- **rsv sample**

```shell
rsv sample data.csv                 # default to sample 10 records
rsv sample --no-header data.csv     # no-header
rsv sample -n 20 data.csv           # pull more
rsv sample -n 20 data.xlsx          # EXCEL file
rsv sample --seed 100 data.xlsx     # set a seed
rsv sample --time-limit 2 data.xlsx # set time limit to 2 seconds for large file
rsv sample -n 20 --export data.xlsx # data export
```

- **rsv sort**

```shell
rsv sort -c 0 data.csv 			# 默认按第一列升序排序
rsv sort -c 0D data.csv 		# 降序排序
rsv sort -c 0DN data.csv 		# 按数值排序
rsv sort -c 0DN,2N data.csv 	# 对两列进行排序
rsv sort -E data.csv 			# 导出结果
rsv sort data.xlsx 				# 排序EXCEL文件
```

- **rsv stats**

```shell
rsv stats data.csv                       # 所有列，统计包括：min, max, mean, unique, null
rsv stats data.xlsx                      # EXCEL 文件
rsv stats -c 0,1 data.csv                # 前两列
rsv stats -c 0,1 --export data.csv       # 导出到 data-stats.csv
rsv slice --help                         # 所有的帮助信息
```

- **rsv excel2csv**

```shell
rsv excel2csv data.xlsx                 # 适用于 xlsx 文件，默认为第一个sheet（或 sheet1）
rsv excel2csv data.xls                  # 也适用于 xls 文件
rsv excel2csv --sheet 1 data.xls        # 第二个sheet, e.g., sheet 2
rsv excel2csv -S 1 data.xls             # 同上
```

- **rsv table**

```shell
rsv head data.csv | rsv table                   # 将结果转换为对齐表
rsv slice -s 10 -e 15 data.csv | rsv table      # 同上
```

## 命令 pipeline

- **two commands pipelined**

```shell
rsv search "^\d{4}-\d{2}-\d{2}$" data.csv | rsv table     # 搜索日期并在对齐的表格中打印
rsv select -f 0=a,b data.csv | rsv frequency -c 0         # 过滤行并获取其频率表
rsv select -f "0!=&2N>10" data.csv | rsv head -n 5        # 过滤行，并显示前 5 条记录
rsv select -f "2N=10,20" -c 0-4 data.csv | rsv stats      # 筛选行，选择列并进行统计
rsv select -f "2N=10,20" -c 0-4 data.csv | rsv sort -c 2  # 筛选行、选择列和排序数据
```

- **more commands pipelined**

```shell
rsv search pattern1 data.csv | rsv sort -c 1ND | rsv table             # search, sort and print
rsv select -f 1=a,b data.csv | rsv search pattern | rsv stats          # select, search, and make statistics
rsv select -f "0N>=10&0N<20" data.csv | rsv search pattern | rsv table # select, search, and print in a table
```

## 数据导出

- **方法 1：通过 --export 或 -E ，仅支持导出到 csv 文件**

```shell
rsv slice -s 1000 -e 2000 --export data.csv           # 数据导出
rsv slice -s 1000 -e 2000 -E data.csv                 # 同上
rsv search --export pattern data.xlsx                 # 导出search数据
rsv select -f "0N>=10" --export pattern data.xlsx     # 导出search数据
```

- **方法二：通过“rsv to”子命令，支持csv, txt, tsv, excel**

```shell
rsv slice -s 1000 -e 2000 data.csv | rsv to out.csv          # 导出为 CSV
rsv slice -s 1000 -e 2000 data.csv | rsv to out.xlsx         # 导出为 EXCEL
rsv search pattern data.xlsx | rsv to out.tsv                # 导出为 TSV
rsv select -f "0N>=10" pattern data.xlsx | rsv to out.txt    # 导出为 TXT
```
