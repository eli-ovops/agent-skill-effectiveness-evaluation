# Skill 全目录：静态限制与冲突审查

## 结论和证据边界

**有些 Skill 的正文确实包含可能限制执行的硬流程或与当前高优先级规则冲突的文本。** 这不意味着它们每次都被选中、正文每次都进入上下文，或这些条款已经实际使任务缩水。高优先级用户与平台规则仍然控制实际行为；以下把“文本事实”“可能风险”和“已观察到的行为”分开。

本次比对的高优先依据包括 [全局凭证与账户红线](/Users/USER/.codex/AGENTS.md:14)、[既有常规授权不得反复确认](/Users/USER/.codex/AGENTS.md:31)、[编码默认 ponytail 但不得削弱验收](/Users/USER/.codex/AGENTS.md:75)，以及本会话平台对临时子代理须有用户明确指派、优先复用合适 checkout 的指令。文件和平台指令的优先级高于被审 Skill。

当前会话开发者实际注入 **475 个路径条目、422 个不同显示名**；描述全部只有 13–17 字符，短到有些在句中截断。这是[对原始注入行逐条核验](INJECTED_METADATA.md)的静态事实，并非本次提取错误；它可能妨碍区分适用条件，但没有证据证明已经导致误选。不能从字符长度估算 token 或费用，也不能据此断言模型能力下降。

## 清点范围与可复核数据

扫描六个本机发现根及可达的技能软链接，只读取 `SKILL.md` 和相关 `agents/openai.yaml` 元数据；不执行被审脚本。第三快照为 **532 个逻辑路径、532 个不同规范化真实路径、506 种字节内容**，其中本会话初始注入的 475 个路径有 473 个当时仍可读取；另 59 条不在初始注入列表中，不能称其启用或已加载。共记录 19 个可解析目录软链接，13 个 `.git`/依赖缓存目录被排除；另外两项为注入路径后来消失的记录，见下段。软链接落到其他真实路径并不意味着多个启用项。

第一次快照为 515 条；期间插件缓存出现 `visualize/1.0.89`，第二快照为 516 且当时全部 475 个注入路径可读。之后 `windsor-ai/4.1.0` 出现 18 个路径，原注入的 `windsor-ai/4.0.9` 下两个路径消失；第三快照因此为 532，原有共同路径内容哈希无变化。[变化清单](snapshot-03/version-drift.json)保留新增/消失路径；不能据此断言新旧插件启用或停用。13:24:54 +08 六个根经独立 `rg --files` 只对文件名交叉核对，第三快照对当时可见结果缺失 0；它不覆盖未列根、跳过的依赖目录或之后新变化。

按本会话**显示名**分组，有 27 组同名但内容 SHA-256 不同、24 组同名且内容相同；第三快照已消失的两个注入路径使用第二快照哈希保留历史。例：两个 `tdd`、两个 `planning-with-files` 内容不同；两份 `design-taste-frontend` 字节相同。全量第三快照另有 26 组不同真实路径的同内容副本。前者可能造成入口含义/行为不同，后者可能造成重复发现；文件同哈希不证明插件依赖、维护者或删除安全，暂不自动去重。部分兼容入口（例如 `evidence-gated-project-workflow`）是有意转向权威版本，不能当成错误。

第二快照的注入目录中 405 个路径未见相邻 `agents/openai.yaml`，54 个存在但未匹配到 `allow_implicit_invocation` 文本，16 个匹配 `true`；这是静态文本扫描、不是完整 YAML 语义或当前启用状态。`SKILL.md` 正文被读取时才可能发挥正文约束；本次静态审计把它们当数据，不执行其指令。

- [全部注入条目](injected-catalog.jsonl) · [第三快照文件元数据](snapshot-03/inventory.jsonl) · [全部关键词命中](snapshot-03/hits.jsonl) · [同名组](snapshot-03/injected-duplicate-groups.jsonl) · [同内容组](snapshot-03/duplicate-contents.jsonl) · [软链接](snapshot-03/symlinks.jsonl) · [排除项](snapshot-03/scan-skips.jsonl) · [统计](snapshot-03/summary.json) · [覆盖核验](snapshot-03/coverage-check.json) · [开销边界](OVERHEAD.md)
- 3,236 条关键词命中只是**导航线索**，不是 3,236 个问题。扫描器对 10 条疑似敏感或高熵片段未保存原文；这不证明它们是实际凭证。下列候选已经查看上下文；其余正文没有逐条人工判定安全或有害。

## 优先候选：文本事实、冲突与实际使用

| 优先级与候选 | 可定位文本及触发范围 | 高优先级边界与判断 | 实际使用证据 |
|---|---|---|---|
| P1 `graphify` | [SKILL.md:3](/Users/USER/.agents/skills/graphify/SKILL.md:3) 对任何代码库问题给出宽触发；[165–170](/Users/USER/.agents/skills/graphify/SKILL.md:165) 指示有 Gemini Key 时调用 Gemini 提取；[219](/Users/USER/.agents/skills/graphify/SKILL.md:219) 对语义提取写明必须使用 Agent 工具 | **已证实文本冲突**：当前全局 §0 禁止未经特定例外读取/使用凭证，平台禁止未获明确指派的子代理；Skill 不能用“Key 已存在”或工具可用取代授权。外部传输、成本及环境可用性要另核。推荐缩窄为明确需要图谱的任务，改为授权后才可选后端/代理 | 本次仅作为数据审查，未读取 Key、运行图谱或外传；历史实际使用和影响 UNKNOWN |
| P1 `tdd` 两版本 | [项目版:49](/Users/USER/Documents/skills/.agents/skills/tdd/SKILL.md:49)–56 要求写代码前确认接口、测试行为并取得计划批准；[另一版:22](/Users/USER/.agents/skills/tdd/SKILL.md:22) 要求每个测试接缝先由用户确认 | **已证实文本冲突**：适用范围是 TDD/测试先行，不是所有任务；但用户已经授权实现且接口和验收明确时，这些一律确认与当前自主执行、避免重复审批规则冲突。保留行为测试和必要业务决定，建议将确认限定于真正有重大缺口或用户要求审批 | [定向行为试验](BEHAVIOR_RESULT.md)：在一个明确写出无需二次确认的合成任务中，项目版实际读取后没有停下请求审批，两组均完成并独立通过 9/9；不代表其他场景或另一版本 |
| P1 `finesse-ui` | [SKILL.md:22](/Users/USER/.codex/skills/finesse-ui/SKILL.md:22) 说明规则有上下文；但 [29](/Users/USER/.codex/skills/finesse-ui/SKILL.md:29)、[197–199](/Users/USER/.codex/skills/finesse-ui/SKILL.md:197) 对图像建议要求先提议并等待用户答应；[43](/Users/USER/.codex/skills/finesse-ui/SKILL.md:43) 要求记录构建日志并给 CSS 打标 | **条件性文本冲突**：在用户已明确要求图像或已有同范围授权时，不应再次把回复当作唯一授权；额外日志/标记也须符合项目范围。未经授权付费、外部素材或客户资产仍需相应许可。建议按当前明确授权和实际成本/来源判断，不做全局先问门禁 | 当前仅静态读取；未证实该 Skill 已导致用户等待或改动项目 |
| P1 `requesting-code-review` | [SKILL.md:3](/Users/USER/.codex/skills/requesting-code-review/SKILL.md:3) 覆盖完成任务、重大功能和合并；[14–17](/Users/USER/.codex/skills/requesting-code-review/SKILL.md:14)、[32–34](/Users/USER/.codex/skills/requesting-code-review/SKILL.md:32) 将对应场景的审查子代理写为必选 | **条件性文本冲突**：当前平台需要用户明确指派才可启动子代理；不能凭 Skill 自行派发。应保留与风险匹配的代码审查和证据，允许合格的当前 Owner 审查或报告独立审查缺口 | 真实派发/停工证据 UNKNOWN |
| P1 `dispatching-parallel-agents` | [SKILL.md:3](/Users/USER/.codex/skills/dispatching-parallel-agents/SKILL.md:3)、[14](/Users/USER/.codex/skills/dispatching-parallel-agents/SKILL.md:14)、[66–74](/Users/USER/.codex/skills/dispatching-parallel-agents/SKILL.md:66) 将独立问题分别派给代理；[79–85](/Users/USER/.codex/skills/dispatching-parallel-agents/SKILL.md:79) 要求完整测试套件 | **条件性文本冲突**：不能覆盖当前子代理授权与并发上限，也不能对无关低风险改动机械扩大测试。应在获授权且确有收益时并行，并按风险选验证范围 | 真实超额派发或过度测试 UNKNOWN |
| P1 `onboarding-questionnaire` | 面向 iOS 订阅式问卷入门；[110](/Users/USER/.codex/skills/onboarding-questionnaire/SKILL.md:110)、[309–326](/Users/USER/.codex/skills/onboarding-questionnaire/SKILL.md:309) 要求确认转变、屏幕顺序和每个页面内容后再进入下一页 | **条件性文本冲突**：若用户已授权完整实现且业务事实清楚，逐屏强制确认会增加未要求的审批；真正影响定价、承诺和业务真实性的选择仍需确认。建议只对实质未知或用户明确要求评审的部分停住 | 当前只有文本，实际等待/返工 UNKNOWN |
| P2 `ponytail` | 全局对编码任务默认 full；[27–28](/Users/USER/.agents/skills/ponytail/SKILL.md:27) 持续激活，[60](/Users/USER/.agents/skills/ponytail/SKILL.md:60) 复杂需求先交简化版，[66](/Users/USER/.agents/skills/ponytail/SKILL.md:66) 一般输出最多三行 | **泛化与内部张力风险**，不是已证实缩水：同时 [69–71](/Users/USER/.agents/skills/ponytail/SKILL.md:69) 保留用户要求的报告，[90–93](/Users/USER/.agents/skills/ponytail/SKILL.md:90) 禁止省略明确需求、安全和无障碍。应保留最小充分实现，明确复杂需求必须交完整已授权范围、解释按用户需求 | 此前两组独立诊断均实际读取并完整通过简单样例；不足以证明复杂任务缩水或无风险，见[试点](../RESULTS.md) |
| P2 `planning-with-files` 两版本 | [r0:3](/Users/USER/.codex/skills/planning-with-files/SKILL.md:3)、[40–42](/Users/USER/.codex/skills/planning-with-files/SKILL.md:40) 限定只读/输出受限不得建文件；但 [111–117](/Users/USER/.codex/skills/planning-with-files/SKILL.md:111) 要求每两次查看就写入、重大决定前重读。r0 [6–29](/Users/USER/.codex/skills/planning-with-files/SKILL.md:6) 还声明多个 hook；[r1:16–24](/Users/USER/.agents/skills/planning-with-files/SKILL.md:16) 是另一套轻量文件方案 | **执行开销及同名歧义风险**：只在确需跨阶段持久化且获授权时保留必要文件；读写节奏可按任务调整。frontmatter 中存在 hook 文本不证明当前 Codex 已注册或执行，脚本运行和权限必须另核 | 两个版本的实际选择、hook 是否启用、成本均 UNKNOWN |
| P2 `agent-reach` | [SKILL.md:4–11](/Users/USER/.agents/skills/agent-reach/SKILL.md:4) 对互联网问题及任意 URL 写 `MUST USE`；[45–55](/Users/USER/.agents/skills/agent-reach/SKILL.md:45) 要求指定后端、体检及较大任务后查更新；[17–18](/Users/USER/.agents/skills/agent-reach/SKILL.md:17) 又排除已有专用 Skill 的平台 | **宽触发与额外调用风险**：与优先使用适合的已连接工具、外部访问需符合本任务目的的规则存在张力；体检的登录态访问/更新 API 的实际副作用未核。建议限定于其确有优势且获授权的平台研究，不把版本检查变成通用收尾 | 未运行 doctor、外部服务或登录态；实际影响 UNKNOWN |
| P2 `design-taste-frontend` | 仅适用于落地页/作品集/改版，[8–9](/Users/USER/.agents/skills/design-taste-frontend/SKILL.md:8) 写规则要结合 brief；但 [84–102](/Users/USER/.agents/skills/design-taste-frontend/SKILL.md:84) 在匹配某种风格时要求安装官方包 | **依赖与风格约束风险**：用户禁增依赖、现有组件已足够或安装副作用未核时，上级规则优先；真实官方设计系统要求与无障碍价值应保留。建议把“风格相似”与“必须安装某套系统”分开 | 两份注入副本 SHA-256 相同，实际选用/安装 UNKNOWN；单份正文约 87,126 字符，不代表本会话已读入或 token 成本 |
| P2 `systematic-debugging` | [SKILL.md:28–50](/Users/USER/.codex/skills/systematic-debugging/SKILL.md:28) 覆盖任何技术问题并要求每次完整四阶段 | **固定流程开销风险**：先找证据和根因有价值，简单可复现问题可按复杂度缩放；不能从文本推断模型实际一定变慢 | 实际使用与影响 UNKNOWN；此前 A/B 只测 `diagnose`，不能代替本 Skill 的行为证据 |
| P2 `executing-plans` / `using-git-worktrees` | [executing-plans:14–23](/Users/USER/.codex/skills/executing-plans/SKILL.md:14) 已明确不自动派代理或创建 worktree，但 [62](/Users/USER/.codex/skills/executing-plans/SKILL.md:62) 对 main/master 本地实现一律要求额外同意；[using-git-worktrees:3](/Users/USER/.codex/skills/using-git-worktrees/SKILL.md:3) 把“执行实现计划前”列为触发，[41–48](/Users/USER/.codex/skills/using-git-worktrees/SKILL.md:41) 则要求尊重已知偏好 | **条件性范围冲突**：当前规则偏好复用安全的现有 checkout，明确禁止直接 push/merge 主分支，并未一律禁止已授权的本地实现。应保留真实并发隔离和 Git 发布安全，不自动把分支名转成重复审批或新 worktree | 当前任务未使用这两个 Skill；实际新增 worktree/等待 UNKNOWN |

## 已核对且不应误判为问题的边界

- [brainstorming:12–24](/Users/USER/.codex/skills/brainstorming/SKILL.md:12)、[60](/Users/USER/.codex/skills/brainstorming/SKILL.md:60) 已明确：清楚授权的实现不强制单独设计审批或每次 TDD；只读和用户要求先审方案仍要尊重。
- [using-superpowers:11–21](/Users/USER/.codex/skills/using-superpowers/SKILL.md:11) 要求最小必要 Skill 集、不自动重复流程；[53–57](/Users/USER/.codex/skills/using-superpowers/SKILL.md:53) 保留用户与高优先规则。不能把旧版名声当作当前硬门禁。
- [test-driven-development:3–15](/Users/USER/.codex/skills/test-driven-development/SKILL.md:3) 将测试与风险相称、低影响变更可选更小验证；[verification-before-completion:20](/Users/USER/.codex/skills/verification-before-completion/SKILL.md:20) 允许复用当前版本证据、不要求无理由重复跑。它们体现必要验证边界，不应因含“必须”就停用。

## 建议顺序

1. **先定位目录描述截断的来源**，在不更改配置前确认注入链；保留短而完整、区分触发/排除条件的描述。此项为平台/路由元数据问题，不贸然归责具体 Skill。
2. **优先审阅条件性硬冲突**：`graphify` 的凭证/外部后端与子代理、两版 `tdd` 的逐项确认、`finesse-ui` 的已有授权后再问、强制审查/并行子代理。安全、费用、真实数据和必要验收不得被消融。
3. **按风险调整而非一律关掉**：`ponytail` 保留边界但明确完整交付；复杂诊断与长任务保留证据要求，按实际复杂度调整固定阶段和重复读写。
4. **候选去重先核用途和依赖**：尤其同名不同内容的 `tdd`、`planning-with-files`、`diagnose`，以及同内容的两份 `design-taste-frontend`。仅作为人工评估清单，不改注册、配置、软链接或文件。

## 当前未知

其他会话实际被哪些 Skill 读取、其他场景下指令是否改变行为、是否产生额外等待/返工、当前插件缓存中未注入版本是否启用、所有 hook 是否被 Codex 解释、实际 token/价格与哪一层截断描述，均为 **UNKNOWN**。仅对 `tdd` 的一个关键场景做过[小规模隔离验证](BEHAVIOR_RESULT.md)，不把它包装成整个库的 A/B 结果。
