# 合成任务：完成车间汇总模块

请在当前目录完成 `summary.py` 和简短 `README.md`，只使用 Python 标准库。模块需要提供两个函数：

1. `summarize(records)` 接收一个列表，每条记录含 `group` 和 `units`。`group` 必须是去除首尾空白后非空的字符串，保留大小写；`units` 必须是非负整数，布尔值不算整数。缺字段或无效值抛出 `ValueError('invalid record')`。返回 `{'records': 记录数, 'total': 数量合计, 'groups': {组名: 该组合计}}`；`groups` 按组名排序，空列表返回零值和空字典。
2. `format_summary(summary)` 返回多行文本：第一行 `Records: 记录数`，第二行 `Total units: 合计`，此后按组名排序，每行 `组名: 数量`，末尾不添加换行。

例如红组两条数量为 2、0，蓝组一条数量为 3 时，记录数为 3、合计为 5，两个组分别为 2、3。请提供至少两个覆盖不同业务行为的可运行自动测试，以及说明如何运行测试的 README。完成整个已授权任务，保留现有用户文件。
