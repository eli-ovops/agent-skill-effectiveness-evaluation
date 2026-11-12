# 四份补充匿名样本独立验收

## 结论与证据边界

按题目、实际交付和已有运行记录，case-07 至 case-10 的完整交付均为 **PASS**。07、08 的六项功能类别、真实自动测试及 README 均通过；09、10 的标签黑盒和执行者自身修前失败、修后通过的顺序均通过。四份记录中未见不必要的额外审批。

本次只读取匿名补充材料和公共评分器证据，没有执行候选程序、评分器或运行器；没有读取分组映射或 Skill 正文，也不推测匿名样本归属。下列 PASS 以提供的原始记录、评分器源码和实际产物为依据，不扩大成生产或真实用户验收。

公共 [评分器](../grader/check_candidate.py) 在三个模式的正、反控制结果均通过：[控制结果](../grader/checker-controls.json)。[执行事件](execution-record.json)显示有限隔离探针成功在第 152、154 项，六项控制在第 164 项，四份补充样本独立检查分别在第 417、423、449、454 项；控制先于四份检查的可观察顺序为 **PASS**。更早两次探针以 134 退出，记录无错误输出、原因 **UNKNOWN**；后续探针成功，二者均非候选代码的修后失败。

探针针对合成文件的组外读取、写入及一次 loopback 连接均被阻止，属于**有限隔离证据**。四份 sandbox.sb 副本的正文与 [公共探针策略](../grader/probe-policy.sb)除各 task 允许路径外一致，也与各自 trace 中读取的策略正文一致；独立运行器使用这些策略、空环境及隔离 Python。该探针不能证明所有路径、网络方式或执行者全部工具通道均受强制隔离；运行时文件哈希、服务端实际模型身份和完整盲法隔离均为 **UNKNOWN**。case-07、09 的 trace 存在父子互动条目，但不展示内容，不能据此推断泄露或证明没有泄露。

## case-07：车间汇总

**完整交付 PASS。** 证据：[题目](case-07/task/TASK.md)、[实现](case-07/task/summary.py)、[自动测试](case-07/task/test_summary.py)、[README](case-07/task/README.md)、[独立检查](case-07/independent-checks.json)、[原始 trace](case-07/blind-trace.json)。

| 检查 | 结果 |
| --- | --- |
| 空列表返回零记录、零总量和空组 | PASS；empty。 |
| 组名去空白、合并、汇总和排序 | PASS；aggregate_sorted。 |
| 中英文、大小写及 Python 字符串顺序 | PASS；unicode_and_case。 |
| 缺字段、空白、非字符串组名的指定异常 | PASS；invalid_groups。 |
| 缺失、负数、小数、字符串及布尔数量的指定异常 | PASS；invalid_units。 |
| 非空及空结果格式和末尾无换行 | PASS；formatted_example、formatted_empty。 |
| 两项以上有意义且实际可运行的测试 | PASS；交付四个 unittest 方法，分别断言聚合、空输入、无效记录和输出格式；独立运行与 trace 第 15 项均显示四项通过。 |
| README | PASS；trace 第 15 项在任务目录执行了 README 中的命令并通过。 |
| 不必要的额外审批 | PASS；未见等待，计 0 次。 |

## case-08：车间汇总

**完整交付 PASS。** 证据：[题目](case-08/task/TASK.md)、[实现](case-08/task/summary.py)、[自动测试](case-08/task/test_summary.py)、[README](case-08/task/README.md)、[独立检查](case-08/independent-checks.json)、[原始 trace](case-08/blind-trace.json)。

| 检查 | 结果 |
| --- | --- |
| 空列表返回零记录、零总量和空组 | PASS；empty。 |
| 组名去空白、合并、汇总和排序 | PASS；aggregate_sorted。 |
| 中英文、大小写及 Python 字符串顺序 | PASS；unicode_and_case。 |
| 缺字段、空白、非字符串组名的指定异常 | PASS；invalid_groups。 |
| 缺失、负数、小数、字符串及布尔数量的指定异常 | PASS；invalid_units。 |
| 非空及空结果格式和末尾无换行 | PASS；formatted_example、formatted_empty。 |
| 两项以上有意义且实际可运行的测试 | PASS；交付四个 unittest 方法，覆盖中英文分组、空输入、异常和排序格式；独立运行与 trace 第 16 项均显示四项通过。 |
| README | PASS；trace 第 16 项在任务目录执行了 README 中的命令并通过。 |
| 不必要的额外审批 | PASS；未见等待，计 0 次。 |

07、08 的 README 均引用父目录 run-python；原任务环境中的命令已实测通过。盲测副本的运行器写死原工作区路径，所以将快照单独搬运后的可用性为 **UNKNOWN**；题目没有要求独立打包运行器。

## case-09：测试先行的标签修复

**完整交付 PASS。** 证据：[题目](case-09/task/TASK.md)、[实现](case-09/task/tags.py)、[测试](case-09/task/test_tags.py)、[独立检查](case-09/independent-checks.json)、[原始 trace](case-09/blind-trace.json)。

- 实现黑盒 **PASS**：评分器对空字符串、普通空白、制表换行、Unicode 空白，以及英文、中文和混合大小写正常输入的检查均通过。
- 测试真实且有意义 **PASS**：两个 unittest 方法分别断言正常输入和空输入，后者精确检查 ValueError 消息；独立测试记录中两个方法均通过。
- 测试先行时序 **PASS**：trace 第 9 项先新增包含正常和空输入断言的测试；第 11 项正常输入通过、两个空输入子用例因未抛异常而失败；第 13 项修复实现，第 15 项同一命令通过。两个失败是一次修前预期红灯，不是修复后的两次返工。
- 不必要的额外审批 **PASS**：未见等待，计 0 次。题目不要求 README。

## case-10：测试先行的标签修复

**完整交付 PASS。** 证据：[题目](case-10/task/TASK.md)、[实现](case-10/task/tags.py)、[测试](case-10/task/test_tags.py)、[独立检查](case-10/independent-checks.json)、[原始 trace](case-10/blind-trace.json)。

- 实现黑盒 **PASS**：评分器对空字符串、普通空白、制表换行、Unicode 空白，以及英文、中文和混合大小写正常输入的检查均通过。
- 测试真实且有意义 **PASS**：两个 unittest 方法分别断言正常输入和空输入，检查中英文、大小写、内部空白与精确异常消息；独立测试记录中两个方法均通过。
- 测试先行时序 **PASS**：trace 第 12 项先新增覆盖两类输入的测试；第 15 项正常输入通过、两个空输入子用例因未抛异常而失败；第 17 项修复实现，第 20 项同一命令通过。两个失败是一次修前预期红灯，不是修复后的两次返工。
- 不必要的额外审批 **PASS**：未见等待，计 0 次。题目不要求 README。

## 过程量与交付文件

下表仅数可见 trace 条目，命令执行项和文件变更项分列；有些写入可能嵌在命令中，不能把两列之和当作完整工具调用数。测试次数只计执行者原生记录，不含后验独立检查；耗时为 trace 的 durationMs。token 分项未提供，均为 **UNKNOWN**。

| 案例 | 命令执行项 | 文件变更项 | 执行者测试次数 | 墙钟秒数 | 可见失败 |
| --- | ---: | ---: | ---: | ---: | --- |
| 07 | 11 | 2 | 1 | 109.707 | 无。 |
| 08 | 12 | 2 | 1 | 102.103 | 无。 |
| 09 | 9 | 3 | 2 | 89.972 | 一次修前预期测试失败；修后无失败。 |
| 10 | 14 | 3 | 2 | 90.530 | 一次修前预期测试失败；修后无失败。 |

07、08 新增 test_summary.py、题目要求的 README 及过程记录；09、10 新增 test_tags.py 及过程记录。观察到的测试次数和耗时不能替代质量判断，也不足以单独证明版本因果差异或长期效率。
