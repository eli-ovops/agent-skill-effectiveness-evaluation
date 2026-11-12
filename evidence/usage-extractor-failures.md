# 用量采集器测试失败记录

- 2026-11-10，第二版合成测试返回 exit 1：`KeyError: 'total_tokens'`，位置 `test_usage_extractor.py` 第 30 行。当合成事件把 `rate_limits` 放在 `info` 前，截断逻辑曾错误地解析出没有 `info` 的部分对象。
- 这是采集器的测试失败，不是模型用量、账户或业务失败。先前快照 02 的可见原生日志采用 `info` 在前的格式，仍保留原件，不能据此推断其他顺序安全。
- 已改为在不支持的字段顺序或缺少 `info` 时拒绝该行，不输出部分数据；随后保留复测回执。`LOCAL_BLOCKERS.md` 对 KeyError 的既有建议为核对实际 schema，而非假定字段位置。
