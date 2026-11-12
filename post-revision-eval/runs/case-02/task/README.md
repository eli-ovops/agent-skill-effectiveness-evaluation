# 车间汇总

`summary.py` 提供 `summarize(records)` 和 `format_summary(summary)`，仅使用 Python 标准库。
前者校验记录、去除组名两端空白并按区分大小写的组名汇总；后者将汇总结果格式化为文本。

在本目录运行测试：

```sh
python3 -m unittest discover -v
```

在本次隔离环境中，也可使用 `../run-python -m unittest discover -v`。
