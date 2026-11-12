# 实际执行者任务单

十份执行任务均使用 `fork_turns=none`、同一模型和推理强度，不向执行者提供前后映射或修改预期。以下是实际文本，`<CASE>` 只替换为对应匿名目录名；编码对象是 ponytail 时采用版本 A，其余采用版本 B。版本 A/B 是任务单类型，不是 Skill 新旧标签。

版本 A 前段：

> 你负责独立完成本地合成工作目录 `/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/post-revision-eval/runs/<CASE>` 的任务。先读取该目录 `skill/SKILL.md` 并应用适用步骤，再阅读 `task/TASK.md` 与所需素材；本次编码规则只从该冻结 skill 读取，不读取当前安装位置的 Skill、其他组、父会话、历史结果或评分文件。

版本 B 前段：

> 你负责独立完成本地合成工作目录 `/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/post-revision-eval/runs/<CASE>` 的任务。先读取该目录 `skill/SKILL.md` 和共同编码规则 `common/ponytail/SKILL.md` 并应用适用步骤，再阅读 `task/TASK.md` 与所需素材；这些编码规则只从本组冻结文件读取，不读取当前安装位置的 Skill、其他组、父会话、历史结果或评分文件。

两种后段相同：

> 尊重用户任务及更高优先级安全和授权规则。你不是工作区唯一执行者，只写本组目录，不回退他人改动。不得访问真实账户、余额、订单、仓位或权益，不读任何认证材料、凭证、.env 或环境秘密；不联网、不安装、不启动服务或调度、不对外发送、不调用子代理、不改组外文件或配置。执行代码前先以文本检查将运行的模块和测试，确保只有本地合成任务所需行为；执行 Python 只能经本组 `/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/post-revision-eval/runs/<CASE>/run-python`，例如用其运行标准库 unittest。若认为确有必须由用户作出的决定，在本组文件写 REQUEST_INPUT 和原因并暂停受影响部分，不向用户发送模拟问题。完成交付并写 process.md，简述真实行动、失败、决定点和验证，不虚构实际运行或模型配置。

任务单文字内的 Markdown 排版只用于本文易读，未对执行者增加新授权。运行器只覆盖经它执行的进程，执行者全部工具通道并未强制隔离。
