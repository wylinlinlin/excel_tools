### JET template

> create JET template

Need pip

* `pip install rich`

Usage

```python
from journalsTemplate import JournalsTemplate

jet = journalsTemplate()
jet.check(df)
```

Function

* `reset_column`: 
  * 插入JET模板列
* `pivot`: 
  * 数据透视
  * Net 2 Zero
* `convert_format`: 
  * 转换日期格式为 *dd/mm/yyyy*
  * 保留2位小数
  * 去除特殊字符与保留前200 *Line Description*
  * 汉字转拼音

* `calculation_sum`:
  * 计算 *debit*、*credit*、*amount* 的加总

* `sort_add`:
  * 根据 *Journal Number* 排序
  * 计算 *Line Number*
  * 计算 *Financial Period*

* `get_last_account`:
  * 取末级科目

* `screen`:
  * 条件筛选(根据末级科目可筛选出需要的结果)

* `calculation_dc`:
  * 计算借贷方向
  * 调整借贷值的正负

* `get`:
  * 获得标准模板数据

* `write`:
  * 保存数据位txt,分隔符为|,且编码为utf-16le

* `check`:
  * 检查借贷是否相等,amount是否为0
  * 检查 *Auto Manual or Interface*
  * 检查借贷是否存在负数
  * 检查 *Financial Period*
  * 检查 *Entity*
  * 检查 *Currency*、 *Currency EC*
