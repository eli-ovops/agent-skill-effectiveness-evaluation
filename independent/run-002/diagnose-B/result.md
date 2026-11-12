# 诊断结果

- 开始时间：2026-11-10 04:50:19 UTC（时钟工具）
- 结束时间：2026-11-10 04:52:14 UTC（本报告生成时，本机 UTC 时钟）
- 可核实模型：UNKNOWN；推理强度：UNKNOWN（本次没有可安全核实的实际运行信息）。
- 修改：仅修改 orders.py 的 total_due 一行；仅在 shipping 为 None 时计算默认运费，显式 0 直接参与合计。购物车和账单均调用该共享函数。
- TASK.md、check.py 未修改。result.md 为本任务报告，没有新建临时文件。
- 失败次数：修复前固定检查失败 2 次，每次均有相同的 2 条用例失败；修复后测试失败 0 次。代码返工 0 次，一次修改。
- 任务所需验证已完成；无需服务、网络或真实数据。

## 实际过程与假设

1. 阅读任务、orders.py 和固定检查，确认两个入口通过 total_due 汇合。
2. 连续两次运行固定检查，准确复现两个入口小计 45、显式运费 0 多算 10 的问题。check.py 已在正确的共享调用路径覆盖该回归，无需新增重复测试文件。
3. 排列并区分三个假设：共享函数将 0 当作未提供（预测默认值变化会改变显式 0 的合计）；入口丢失 0（预测共享函数直接调用正常）；合计加法额外加价（预测其他运费也会受影响）。定点探针发现直接调用已错误，替换默认运费后显式 0 结果随之改变，而运费 8 的结果不变，支持第一个假设。
4. 将真值回退改为显式 None 判断。重跑原始固定检查，并补查真正省略参数、99 和 100 的门槛、Decimal 运费。未加入调试日志或临时探针文件。

## 每次测试与探针输出

### 修复前固定检查，第 1 次

命令：PYTHONDONTWRITEBYTECODE=1 python3 check.py；退出码 1。

~~~text
10/12 checks passed
cart_total(45, 0) = 55; expected 45
invoice_total(45, 0) = 55; expected 45
~~~

### 修复前固定检查，第 2 次

命令：PYTHONDONTWRITEBYTECODE=1 python3 check.py；退出码 1。

~~~text
10/12 checks passed
cart_total(45, 0) = 55; expected 45
invoice_total(45, 0) = 55; expected 45
~~~

### 定点探针

在独立 Python 进程中分别直接调用 total_due(45, 0)、total_due(45, 8)，再仅在内存中将 default_shipping 替换成返回 91 的函数，测试显式 0、实际省略参数与显式 8。退出码 0。

~~~text
direct zero: 55
direct nonzero: 53
direct zero with default=91: 136
direct omitted with default=91: 136
direct nonzero with default=91: 53
~~~

### 修复后固定检查

命令：PYTHONDONTWRITEBYTECODE=1 python3 check.py；退出码 0。

~~~text
12/12 checks passed
~~~

### 修复后补充检查

在独立 Python 进程中对 cart_total、invoice_total 各执行 8 个断言：小计 99 和 100 时真正省略运费、显式 0、显式 8，以及小计 Decimal('99.00') 时 Decimal('0.00')、Decimal('8.50')。退出码 0。

~~~text
16/16 boundary, omitted-argument and decimal checks passed
~~~
