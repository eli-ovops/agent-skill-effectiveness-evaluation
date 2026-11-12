# 车间汇总

`summarize(records)` 去除组名首尾空白，按区分大小写的组名汇总非负整数数量。记录缺字段或包含无效值时抛出 `ValueError('invalid record')`。`format_summary(summary)` 将汇总结果格式化为按组名排序的多行文本。

在本目录运行标准库自动测试：

```sh
../run-python -m unittest discover -v
```
