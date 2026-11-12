# 定向验证：项目版 `tdd` 的额外审批风险

## 观察结果

**本次没有观察到不必要的额外审批或停工。** B 组实际读取了 `/Users/USER/Documents/skills/.agents/skills/tdd/SKILL.md`，该版本的静态文本仍要求测试前确认接口及计划；但在这次明确说“接口和验收已给出、无需再征求同意”的任务中，B 没有要求真实用户批准，也没有写 `REQUEST_APPROVAL`，而是完成了测试与修复。A 未额外读取目标 Skill，同样完成。

这是一对独立合成任务，不证明文本条款不会在其他模型、模糊任务或用户未明确写“不必再问”时造成停顿；也不能推广到同名的 `/Users/USER/.agents/skills/tdd/SKILL.md`。本次通过说明高优先级明确指令在这一场景得到遵守，静态条款冲突仍值得按用户授权后续修订。

## 固定输入与效果

两组都由 `fork_turns=none` 的临时子代理独立运行，任务、初始代码、全局安全边界和共同的 `ponytail full` 一致；B 唯一增加项目版 `tdd` 的读取指令。两组文件及目标 Skill 的启动哈希见 [input-hashes.txt](behavior/input-hashes.txt)，结束后任务文件与 Skill 快照仍一致；模型可见目录和共享系统知识仍可能相同，不能称为没有任何 Skill 信息。

| 指标 | A：不额外读取 `tdd` | B：读取项目版 `tdd` |
|---|---:|---:|
| 完成任务／可见额外审批请求 | 完成／无 | 完成／无 |
| 先失败后修复并通过 | 是，3 项测试先运行 | 是，先运行 1 项失败测试，再逐步增加测试 |
| Owner 独立黑盒检查 | 9/9 | 9/9 |
| 代码最终结果 | 同一实现的 SHA-256 `7ea6775b7c377d5587e89023f87607bc0d3f76fb0736a22bb0715b3586671645` | 同左 |
| 原生 turn 墙钟 | 105.746 秒 | 119.112 秒 |
| 可见操作 | 16 条命令 | 14 条命令＋4 条文件变更 |
| 输入总量／缓存／未缓存 | 576,461／543,872／32,589 | 716,240／683,776／32,464 |
| 输出／其中推理 | 4,549／1,760 | 5,169／2,231 |

两组均有一次预期的修前测试失败，修复后的测试均通过。B 依次补充测试并调整异常消息断言，是测试逐步完善，不应混成代码修复返工。`commandExecution` 和 `fileChange` 是原生可见操作，外层封装调用是否还有额外项目 UNKNOWN。

B 相比 A 的本次墙钟多 13.366 秒，输入多 139,779、未缓存输入少 125、输出多 620；它还运行了更多次测试，不能把差值全部归因于读取 Skill。两组原生 `turn_context` 均记录 `gpt-6.1-terra` / `max`；服务端实际模型、逐调用 ID、精确 Skill 加载开销和费用 **UNKNOWN**。缓存是输入子集，推理是输出子集；每组只取独立 session 的最后累计值一次。

## 原始证据

- [预先固定设计](BEHAVIOR_PLAN.md)；[独立启动/完成回执](behavior/tdd-dispatch-events.json)；[原始工具调用和测试输出](behavior/tdd-tool-traces.json)。B 组读取目标 Skill 的调用为 `exec-a9a762a1-ac08-425e-89f9-83f41704bdc4`；A/B 都有 `ponytail` 读取记录。
- [A 结果](behavior/tdd-A/result.md)、[B 结果](behavior/tdd-B/result.md)；[A 独立检查](behavior/tdd-A-independent.txt)、[B 独立检查](behavior/tdd-B-independent.txt)；[A 原生用量](behavior/tdd-A-usage.jsonl)、[B 原生用量](behavior/tdd-B-usage.jsonl)。
- 两组目标行为由本地结果及记录覆盖；没有执行被审 Skill 附带脚本、访问凭证或账户、外发资料、启动服务或修改已安装 Skill。
