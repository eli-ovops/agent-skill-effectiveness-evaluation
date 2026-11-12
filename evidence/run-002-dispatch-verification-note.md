# 派发参数离线比对限制

本次从本会话原生日志定向读取 4 条 `spawn_agent` 调用，调用时间、call ID、任务名和 `fork_turns` 可见；但日志中的 message 字段是平台保护的密文，不能按明文比较组间任务单。首次试图当作明文做字符串相等断言，因此返回 AssertionError；不是子代理执行或测试失败。不得尝试解密或接触认证材料。

原始聊天工具调用中已直接提交共同任务及 B 专属 Skill 指令；样例文件和验收文件的实际字节一致性由独立 SHA-256 和 `cmp` 记录证明。系统最终向模型注入的全部上下文内容仍为 UNKNOWN，不能把 `fork_turns=none` 写成“完全无共享目录/知识”。

失败步骤新建的 `/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/evidence/run-002-dispatch-prompts.json` 只含不可比对的密文，属于本次一次性中间文件；先提取无密文的派发元数据后删除，保留本失败说明和本机会话原始日志。

处理回执：已保存 [非密文元数据](run-002-dispatch-metadata.json)（四个调用均 `fork_turns=none`，未覆盖模型或强度），并只删除上述新建、非符号链接的中间文件，文件大小 9,357 字节。同一文件系统 `df -k` 显示可用空间从 10,283,488 KiB 到 10,283,496 KiB；并发磁盘活动和粒度使实际释放量无法可靠归因，记 UNKNOWN。未删除任何其他文件。
