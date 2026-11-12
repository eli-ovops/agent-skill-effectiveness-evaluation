# 六份匿名交付独立验收

## 结论与证据边界

按题目要求、当前交付和已有运行记录判断，case-01 至 case-06 的实现及必要交付均为 **PASS**。两份标签任务均有执行者自己的测试先失败、修复、同一测试再通过的原始记录；未观察到必须等待的不必要额外审批。两份诊断任务的六组指定阈值均通过独立黑盒；它们各自交付的回归测试未单独列出 (9, 8)，但评分器源码和独立结果共同表明该输入对两个入口都已检查。

本次审阅只检查盲测目录内的题目、交付、评分器、结果和过程记录，没有执行候选程序、评分器或运行器。下文的 PASS 指这些材料所支持的功能或过程结论；并不将未展示的隔离或身份保证补推为事实。

评分器在三个模式的正、反控制记录均通过：[checker-controls.json](grader/checker-controls.json)。[评分器源码](grader/check_candidate.py) 中的具体输入与六份 [independent-checks.json](case-01/independent-checks.json) 等记录可对应；每份记录均显示黑盒与候选测试退出码 0。[原生命令事件](grader/execution-record.json)显示隔离探针成功为第 152、154 项，六项正反控制为第 164 项，六份正式独立检查依次为第 242 至 297 项，故“控制先于正式检查”的可观察顺序为 **PASS**。此前探针第 116、125 项曾以 134 退出，记录中没有错误输出，原因 **UNKNOWN**；后续 v3 探针成功，不应忽略这两次基础设施失败。

有限隔离探针 **PASS**：在合成文件与 loopback 连接的具体探针中，外部读取、写入和连接均被阻止，见 [probe_sandbox.py](grader/probe_sandbox.py) 与 [probe-result.json](grader/probe-result.json)。[控制运行器](grader/checker_controls.py) 为样本生成受限策略；[独立运行器](grader/run_blackbox.py) 对黑盒及候选测试使用各自的 sandbox.sb、空环境与隔离 Python。[探针策略副本](grader/probe-policy.sb)与六份 sandbox.sb 副本的正文除允许读取的各组 task 路径外一致；六份副本均与对应执行者 trace 中实际读取的策略正文一致，规则也与 [sandbox_profile.py](grader/sandbox_profile.py) 的生成逻辑相符。运行时文件哈希未提供，故无法仅凭副本证明实际执行时文件从未变化。探针只验证其具体路径与连接方式，不能证明所有网络、文件路径或执行者全部工具通道都被隔离；完整通道隔离和评分器快照与当时执行版本的哈希对应关系均为 **UNKNOWN**。

本验收未读取分组映射或推测组别；执行者是否完全无法获知组别、服务端实际模型身份是否相同，均为 **UNKNOWN**。case-01、case-02 的 trace 有父子互动条目但不展示互动内容，不能据此推定泄露或证明没有泄露。

## 各份判定

### case-01：车间汇总

**完整交付 PASS。** [题目](case-01/task/TASK.md)、[实现](case-01/task/summary.py)、[测试](case-01/task/test_summary.py)、[README](case-01/task/README.md)、[独立结果](case-01/independent-checks.json)。

| 检查 | 结果及证据 |
| --- | --- |
| 空列表 | PASS；empty 通过。 |
| 合并、去空白、组名排序 | PASS；aggregate_sorted 通过。 |
| 中英文和大小写 | PASS；unicode_and_case 通过。 |
| 缺字段、空白或非字符串组名 | PASS；invalid_groups 通过，异常消息由评分器精确检查。 |
| 缺失、负数、小数、字符串、布尔数量 | PASS；invalid_units 通过，异常消息由评分器精确检查。 |
| 非空及空结果格式、末尾无换行 | PASS；formatted_example、formatted_empty 均通过。 |
| 至少两个真实且有意义的可运行测试 | PASS；交付包含三个 unittest 方法，断言聚合、排序、格式、空输入及异常；独立记录显示三个方法通过。 |
| README | PASS；在原任务工作目录的 [trace](case-01/blind-trace.json) 第 14、20 项，README 所列命令的带详细输出版本实际通过。 |
| 不必要的额外审批 | PASS；原始记录中未见等待审批，计 0 次。 |

README 依赖父目录的 run-python；[运行器副本](case-01/run-python)写死原工作区路径。原执行环境中的可用性有 trace 证明，单独搬运盲测快照后的可移植性为 **UNKNOWN**，题目未要求独立打包运行器。

首次三个测试通过后，执行者把记录类型从字典扩展为 Mapping，增加 UserDict 断言并再次通过；这是一次可观察的修订和复测，没有修复后失败的证据，不应计作失败返工。见 trace 第 14、17、20 项。

### case-02：车间汇总

**完整交付 PASS。** [题目](case-02/task/TASK.md)、[实现](case-02/task/summary.py)、[测试](case-02/task/test_summary.py)、[README](case-02/task/README.md)、[独立结果](case-02/independent-checks.json)。

| 检查 | 结果及证据 |
| --- | --- |
| 空列表 | PASS；empty 通过。 |
| 合并、去空白、组名排序 | PASS；aggregate_sorted 通过。 |
| 中英文和大小写 | PASS；unicode_and_case 通过。 |
| 缺字段、空白或非字符串组名 | PASS；invalid_groups 通过并精确检查异常。 |
| 缺失、负数、小数、字符串、布尔数量 | PASS；invalid_units 通过并精确检查异常。 |
| 非空及空结果格式、末尾无换行 | PASS；formatted_example、formatted_empty 均通过。 |
| 至少两个真实且有意义的可运行测试 | PASS；四个 unittest 方法实际断言分组、空输入、格式和无效记录；独立记录显示四项通过。 |
| README | PASS；给出标准库 unittest 发现命令，并说明本次隔离运行器的替代用法。原执行者运行器命令见 [trace](case-02/blind-trace.json) 第 11 项。 |
| 不必要的额外审批 | PASS；原始记录中未见等待审批，计 0 次。 |

### case-03：测试先行的标签修复

**完整交付 PASS。** [题目](case-03/task/TASK.md)、[实现](case-03/task/tags.py)、[测试](case-03/task/test_tags.py)、[独立结果](case-03/independent-checks.json)。

- 功能黑盒 **PASS**：空字符串、普通空白、制表换行、Unicode 空白均按评分器源码检查；英文、中文及混合大小写正常输入均通过。
- 测试真实且有意义 **PASS**：一个 unittest 方法包含多个子测试，断言正常返回值、空输入异常类型和精确消息；独立运行通过。
- 修复前失败、修复后通过的时序 **PASS**：原始 [trace](case-03/blind-trace.json) 第 7 项新增测试，第 9 项运行并因两种空输入未抛异常而失败，第 11 项修复，第 13 项同一测试通过。两次子用例失败属于一次预期的修前红灯，不是修复后返工。
- 不必要的额外审批 **PASS**：未见要求等待审批，计 0 次；题目不要求 README。

### case-04：测试先行的标签修复

**完整交付 PASS。** [题目](case-04/task/TASK.md)、[实现](case-04/task/tags.py)、[测试](case-04/task/test_tags.py)、[独立结果](case-04/independent-checks.json)。

- 功能黑盒 **PASS**：评分器对四种空白类型、英文、中文和混合大小写的检查均通过。
- 测试真实且有意义 **PASS**：一个 unittest 方法含六个子测试，检查正常值及空值的异常消息；独立运行通过。
- 修复前失败、修复后通过的时序 **PASS**：原始 [trace](case-04/blind-trace.json) 第 12 项新增测试，第 14 项出现三个预期空输入失败，第 16 项修复，第 18 项同一测试通过。三个失败为同一次修前红灯，不是三次返工。
- 不必要的额外审批 **PASS**：trace 明确记录题目已给出测试边界并继续执行，计 0 次；题目不要求 README。
- 另有两次修复前文件搜索非零退出：第 4 项退出码 2，其输出被遮蔽；第 11 项退出码 1 且无输出。二者不是测试失败，不能从快照推定第 4 项失败原因。第 4 项尝试枚举相对上层目录，实际结果被遮蔽；材料未完整提供执行者的目录权限规则，是否违反其边界为 **UNKNOWN**。

### case-05：延时状态诊断

**完整交付 PASS。** [题目](case-05/task/TASK.md)、[实现](case-05/task/delays.py)、[测试](case-05/task/test_delays.py)、[result.md](case-05/result.md)、[独立结果](case-05/independent-checks.json)。结果说明位于执行者 shell 当时的 case-05 工作目录，实际路径如前。

| 检查 | 结果及证据 |
| --- | --- |
| 修复前实际复现 (5, 0) | PASS；[trace](case-05/blind-trace.json) 第 9 项显示文本得到 ok、导出得到 false，两个子用例按预期失败。 |
| 共享调用链与根因 | PASS；第 5 项原始代码显示两个入口经 is_late 进入 effective_limit，原来的 limit or 30 将 0 替换为 30；第 10 项仅将默认判断改为 is None。 |
| 两个入口六组指定阈值 | PASS；独立评分器源码明确逐一检查 (5,None)、(31,None)、(5,0)、(5,8)、(8,8)、(9,8)；status_wrappers 结果通过意味着所有输入及两个入口均通过。 |
| 真实且有意义的回归测试 | PASS；一个方法内六组、两个入口共十二个子用例，修前红、修后绿，独立记录也通过。该交付测试未显式列 (5,None) 与 (9,8)，但独立黑盒覆盖了两者。 |
| 结果说明 | PASS；result.md 写明根因、调用关系和验证。 |
| 不必要的额外审批及修复后失败 | PASS；未见额外审批或修复后失败。第 9 项的两个失败是同一次修前预期复现。 |

### case-06：延时状态诊断

**完整交付 PASS。** [题目](case-06/task/TASK.md)、[实现](case-06/task/delays.py)、[测试](case-06/task/test_delays.py)、[result.md](case-06/task/result.md)、[独立结果](case-06/independent-checks.json)。

| 检查 | 结果及证据 |
| --- | --- |
| 修复前实际复现 (5, 0) | PASS；[trace](case-06/blind-trace.json) 第 11 项显示文本得到 ok、导出得到 false，两个入口的子用例按预期失败。 |
| 共享调用链与根因 | PASS；第 7 项原始代码与第 12 项补丁支持同一根因及最小修复。 |
| 两个入口六组指定阈值 | PASS；评分器源码逐一检查六组，包括 (9,8)，独立 status_wrappers 通过。 |
| 真实且有意义的回归测试 | PASS；两个方法分别测试两个入口，各七组输入，修前红、修后绿，独立记录也通过。交付测试未显式列 (9,8)，该输入由独立黑盒覆盖。 |
| 结果说明 | PASS；task/result.md 写明根因及验证。 |
| 不必要的额外审批及修复后失败 | PASS；未见额外审批或修复后失败。第 11 项的两个失败是同一次修前预期复现。 |

## 过程量与新增文件

下表仅数可见 trace 条目：命令执行项和文件变更项分别计数；有些写文件操作嵌在命令中，因此不能把两列相加当作完整工具调用数。时间为 trace 的 durationMs；模型 token 分项在这些 trace 中未提供，均为 **UNKNOWN**。测试次数只算执行者原生 trace，不含后验独立检查。

| 案例 | 命令执行项 | 文件变更项 | 执行者测试次数 | 墙钟秒数 | 非零结果判读 |
| --- | ---: | ---: | ---: | ---: | --- |
| 01 | 14 | 4 | 2 | 134.524 | 无；第一次通过后有一次主动扩展和复测。 |
| 02 | 8 | 2 | 1 | 93.784 | 无。 |
| 03 | 7 | 3 | 2 | 74.410 | 一次修前预期测试失败；修后无失败。 |
| 04 | 13 | 3 | 2 | 93.791 | 两次修前搜索非零；一次修前预期测试失败；修后无失败。 |
| 05 | 10 | 1 | 2 | 81.462 | 一次修前预期测试失败；修后无失败。 |
| 06 | 13 | 1 | 2 | 96.638 | 一次修前预期测试失败；修后无失败。 |

case-01、02 新增 test_summary.py 和题目要求的 README；case-03、04 新增 test_tags.py；case-05、06 新增 test_delays.py 与题目要求的 result.md。六份另有过程记录 process.md；未见新增计划文件。必要测试和 result.md 不应计作多余计划文件。

上述一次性观察不能单独证明版本间因果差异或长期效率，更不能以墙钟、调用数替代质量与权限判定。
