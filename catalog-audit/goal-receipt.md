# 目标完成回执

本阶段目标在目录审查、定向行为验证和向总控回传之后，`update_goal` 返回 `complete`；回执中的 `tokensUsed=242733`、`timeUsedSeconds=1497`，未设置 token 预算。

这是目标工具的自身统计口径，不等于或可与 [原生会话输入/缓存/输出分项](OVERHEAD.md) 相加；真实费用、各条目录描述造成的 token 增量以及子代理用量是否包含于根会话口径仍为 UNKNOWN。
