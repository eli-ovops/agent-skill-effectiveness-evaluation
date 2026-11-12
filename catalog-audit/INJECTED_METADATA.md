# 本会话 Skill 目录元数据核验

来源是本会话启动时开发者注入的 `skills_instructions`，由本会话本机记录的第 5 行定向提取；只提取目录名、描述和文件路径，没有扫描其他聊天。475 条解析结果逐条与原生注入行完全匹配，不是本次正则或展示脚本截短了描述。

示例原生行：

```text
- imagegen: Generate or ed (file: r2/imagegen/SKILL.md)
- skill-creator: Create or update (file: r2/skill-creator/SKILL.md)
- ponytail: Forces the laz (file: r1/ponytail/SKILL.md)
- graphify: Use for any qu (file: r1/graphify/SKILL.md)
- using-superpowers: Use when selecti (file: r0/using-superpowers/SKILL.md)
```

475 条注入描述长度分布为 13 字符 2 条、14 字符 175 条、15 字符 33 条、16 字符 238 条、17 字符 27 条；中位数 16。对照 SKILL.md frontmatter 的简单提取，475 条原始描述均更长，所提取原始描述中位数 274 字符；这是文本静态统计，并非完整 YAML 解析或真实 token 测量。注入区块整体 40,048 字符、40,492 UTF-8 字节，也不是每次实际消耗 token 或费用。

**已证实的现象：**当前会话的可见路由描述被截至很短，部分截在句中。**待验证的风险：**选 Skill 时可能缺少适用对象、排除条件或关键区别；这不证明任何一次已误选、漏选，也不证明正文被截断或模型智力下降。截断发生在哪一层尚未定位，不能把原因归给某个 Skill 或擅自改平台配置。

完整结构化清单见 [injected-catalog.jsonl](injected-catalog.jsonl)，统计见 [catalog-comparison.json](snapshot-02/catalog-comparison.json)；475 个路径在第二文件快照中均找到，第三快照时其中两个旧版插件路径已消失，详见 [变化记录](snapshot-03/version-drift.json)。
