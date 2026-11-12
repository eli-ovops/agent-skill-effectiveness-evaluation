# 全目录 Skill 限制审查：结果

**确实有值得关注的限制，但目前没有证据说所有 Skill 都拖慢模型或让模型变笨。** 本次发现三种不同问题：本会话目录描述被截短，可能影响选用；少量 Skill 正文含与当前高优先规则冲突或过于固定的流程；同名不同内容和重复内容会增加选择歧义。只有被选中并读取的正文才会施加正文里的具体指令。静态文本不证明这些风险已经在真实任务中发生。

## 目录与入口

- 会话开始时注入 **475 个 Skill 路径、422 个不同显示名**。原生注入行逐条复核通过：475 条描述均只有 13–17 字符，部分截断在词中，例如 `graphify: Use for any qu`。原始 Skill frontmatter 描述更长。已证实当前会话可见路由信息不完整；误选/漏选是否发生、截断来自哪一层均 **UNKNOWN**。[核验](INJECTED_METADATA.md)
- 截至 2026-11-10 13:24:54 +08 的文件快照，六个发现根及可达技能软链接共 **532 个逻辑路径、532 个规范化真实路径、506 种字节内容**。其中 473 个路径与本会话初始目录完全对应，另 59 个未在初始目录列出，另有两个初始目录路径后来消失；这些状态不能直接等同启用、停用或实际使用。
- 缓存变动得到交叉核验：`windsor-ai/4.0.9` 的两个初始路径在首轮可读，后来不存在；`4.1.0` 的对应路径存在。该时点若依旧按旧路径读取会遇到缺失，但实际插件刷新或当前启用版本 **UNKNOWN**；没有改插件配置。[版本漂移](snapshot-03/version-drift.json)
- 初始目录显示名中，**27 组同名但内容不同，24 组同名且内容相同**；完整磁盘快照有 26 组跨真实路径的相同字节内容。例：两份 `tdd` 和两份 `planning-with-files` 同名不同内容，两份 `design-taste-frontend` 内容相同。兼容入口、插件来源和引用关系可能不同，不能仅凭同名或哈希删除。[组表](snapshot-03/injected-duplicate-groups.jsonl)

## 优先处理候选

| 候选 | 已确认的文本事实 | 应如何理解 |
|---|---|---|
| `graphify` | [描述:3](/Users/USER/.agents/skills/graphify/SKILL.md:3) 覆盖任何代码库问题；[170](/Users/USER/.agents/skills/graphify/SKILL.md:170) 指示存在 Gemini Key 时使用对应后端，[219](/Users/USER/.agents/skills/graphify/SKILL.md:219) 写必须使用 Agent | 与当前凭证红线、子代理授权边界存在明确文本冲突；本次没有运行该 Skill，实际越权 UNKNOWN。应把后端和代理限定为明确授权后的选项 |
| `tdd` 两版 | [项目版:49](/Users/USER/Documents/skills/.agents/skills/tdd/SKILL.md:49)–56 要求编码前确认接口、测试和计划；[另一版:22](/Users/USER/.agents/skills/tdd/SKILL.md:22) 要求测试接缝逐项预先确认 | 明确授权且条件已充分时会与自主执行规则冲突。受控样例中项目版读取后**没有**停下要批准；不能推广到另一版本或其他任务 |
| `finesse-ui` | [29](/Users/USER/.codex/skills/finesse-ui/SKILL.md:29)、[197–199](/Users/USER/.codex/skills/finesse-ui/SKILL.md:197) 对图片建议写出“询问并等待”；[43](/Users/USER/.codex/skills/finesse-ui/SKILL.md:43) 要求记录构建日志并打 CSS 标记 | 用户已明确要求或授权图片时，不应重复索取同一授权；未经授权的费用、外部素材和客户数据仍需保护。实际造成等待 UNKNOWN |
| `requesting-code-review` / `dispatching-parallel-agents` | 前者在[14–17](/Users/USER/.codex/skills/requesting-code-review/SKILL.md:14)、[32–34](/Users/USER/.codex/skills/requesting-code-review/SKILL.md:32) 将审查子代理设为必选；后者在[14](/Users/USER/.codex/skills/dispatching-parallel-agents/SKILL.md:14)、[66–74](/Users/USER/.codex/skills/dispatching-parallel-agents/SKILL.md:66) 将独立任务分派给代理 | 当前平台要求用户明确指派子代理；Skill 不能自行扩权或超过并发。保留必要审查和风险相称验证，可由合适 Owner 完成 |
| `onboarding-questionnaire` | [309–326](/Users/USER/.codex/skills/onboarding-questionnaire/SKILL.md:309) 要求确认蓝图，并逐屏确认后再继续 | 对已清楚授权的实现可能制造重复等待；价格、客户承诺和关键业务事实仍需要真实决策 |
| `ponytail` | [27–28](/Users/USER/.agents/skills/ponytail/SKILL.md:27) 跨回复持续；[60](/Users/USER/.agents/skills/ponytail/SKILL.md:60) 提议复杂需求先交简化版；[66](/Users/USER/.agents/skills/ponytail/SKILL.md:66) 限制一般输出长度 | 有泛化风险，但 [69–71](/Users/USER/.agents/skills/ponytail/SKILL.md:69)、[90–93](/Users/USER/.agents/skills/ponytail/SKILL.md:90) 又保护用户要求的说明、完整需求及安全。此前简单诊断试点未出现缩水；复杂任务是否受影响 UNKNOWN |
| `planning-with-files`、`agent-reach`、`design-taste-frontend`、`systematic-debugging` 等 | 分别存在固定频率写计划、宽泛工具路由和附带更新、根据风格推定安装依赖、任何故障执行完整阶段等条款 | 应按风险和任务裁剪，不把关键词命中当缺陷；各自已有适用范围或安全例外，具体见[逐项审查](STATIC_AUDIT.md) |

`brainstorming`、`using-superpowers` 的当前版本已写明清楚授权可继续、只选最少必要 Skill；`test-driven-development` 和 `verification-before-completion` 也包含按风险验证或复用现有证据的边界。不能根据旧版名声或“必须”关键词将这些安全/验证约束一概删除。

## 最小行为验证

针对最可能造成额外审批的项目版 `tdd`，在静态清单完成后，只做一对新鲜上下文、相同输入的本地合成试验。两组均被明确告知接口和验收已定、无需再问；B 实际读取 Skill。**B 没有请求额外批准，A/B 均完成，独立检查均 9/9。** 这说明该次模型遵守了更高优先级的明确授权，不证明其他任务、其他模型或同名另一版本也一定如此。[设计、原生记录与边界](BEHAVIOR_RESULT.md)

同例 A/B 原生墙钟分别为 105.746 / 119.112 秒；总输入 576,461 / 716,240，其中未缓存 32,589 / 32,464；输出 4,549 / 5,169。B 多做测试，不能把全部差额归因于 Skill；缓存比例不同也不能据此推断费用。此前 `prompt-videos` 与 `diagnose` 的两对试点仅适用于各自简单样例，不能外推几百个 Skill。

## 建议与未知

1. 优先排查**会话路由描述为何被截短**，在保留现有安全/权限的前提下让描述完整且有明确适用范围；先定位，不擅自改平台设置。
2. 由用户决定是否另行修改：优先审阅 `graphify` 的凭证/代理指令、两版 `tdd` 的审批、`finesse-ui` 的已授权后再问，以及强制审查/并行子代理。具体修改应保持必要安全门禁与用户真实业务决定。
3. 对 `ponytail`、调试和文件规划做风险相称的适用边界审阅；同名候选仅建立人工去重清单，不自动禁用、删除或卸载。

目录区块为 40,048 字符，只表示静态大小；实际目录注入 token、对误选的因果作用和费用 **UNKNOWN**。[开销记录](OVERHEAD.md)另列本阶段根会话及定向样例的可见原生用量，两者不能随意相加。已按用户要求保留全部原始清单、命中、软链接和过滤记录；未更改全局规则、已安装 Skill、插件配置或其他项目。[总控回传回执](return-receipt.md)只证明提交，不证明对方已审核或汇报。
