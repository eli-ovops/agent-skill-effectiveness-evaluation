# 定向使用审计（截至 2026-11-10）

这里只审查了两条指定的近期任务和本评估会话；没有枚举全部聊天。`read_thread` 的回合/调用 ID 是可追溯来源，助手最终发言只能作为线索；路径、成功调用、产物和验收分别判断。

| Skill / 任务 | 在目录中 | 实际读取 | 可观察到的关键步骤 | 结果验收与边界 |
|---|---|---|---|---|
| `prompt-videos`，2026-11-04 长方形顶喷交接，thread `01a18a5f-a7dc-7371-b3e3-1329812e5e95`，turn `01a1a438-1738-7ff3-9b04-1efe2b8e5f64` | 当前会话 Skills 清单列出；历史该轮目录注入状态 **UNKNOWN** | `exec-30c34b9c-cc23-4cc1-9963-564fbd322782` 执行 `cat /Users/USER/.agents/skills/prompt-videos/SKILL.md`，completed，exit 0，且工具输出可回读；[历史读取原文](evidence/prompt-videos.historical-read.txt) SHA-256 与本次快照完全一致 | 该回合 `exec-e6c5b933-b090-4066-906f-d0eb4b019370` 制作 ZIP，原生输出记载 7 项、CRC 与 SHA256 核对。现存 ZIP 的提示词有 0–4/4–9/9–12/12–15 秒时序、景别/动作、场景光影、声音和参照边界，与读取内容中的部分方法一致；这证明产物具备这些要素，不能证明因果来源，也不能证明全部 Skill 步骤都执行 | 2026-11-10 只读复核现存 ZIP：7 项、`testzip()` 返回 `None`，有 5 个素材和 2 个文字文件，**没有视频**。交接说明明确后续需生成并完整回看。现存 ZIP SHA-256 `197fb28c8798258cd79ade7666a2d15fb5b459753711b7e73108e46aee8116b7`；历史回执未显示整包哈希，因此不能仅凭当前哈希断定和当时字节完全相同。用户验收、成片质量及效率效果 **UNKNOWN** |
| `diagnose`，本评估的独立试验 B，thread `01a1c3ca-b9d4-75e2-a091-c26599b99963` | 当前 Skills 清单列出 | 该组 `exec-a278fb5a-b216-43c6-9eb3-0d959d35d37e` 读取 `/Users/USER/Documents/skills/.agents/skills/diagnose/SKILL.md`，completed，exit 0；[快照](evidence/diagnose.SKILL.snapshot.md) SHA-256 `28886402bbfa0470248086eab9106a103b964b76ae9496e63ff0c8a6761b6d13` | 同组先两次复现；探针前的 commentary 列出三个可证伪假设，随后定点探针、一次补丁和固定测试均可在[工具记录](evidence/run-002-tool-traces.json)核对。对照组的可见命令没有读取该可选 Skill | 修复后本地固定检查 12/12；仅为一例简单合成任务。可比效果见[结果报告](RESULTS.md)，长期效果 UNKNOWN |
| `ponytail`，本评估会话及独立诊断 A/B | 当前 Skills 清单列出；编码任务属于共同硬约束 | 根会话及两组独立诊断都各有 `cat` 成功回执；A 为 `exec-a7923e84-cd34-4624-8a0f-47d275679499`，B 为 `exec-5d7d12fd-0047-4994-8600-3ff6fd4fe33c` | 两组均观察共享入口、使用一行修复和标准库，留有前后测试；这些行为和部分 Skill 内容一致，不能由此推出原因或效果 | 两组样例本地验收均为 12/12；它是共同约束，未进行有无对照 |

本次 `prompt-videos` 独立 B 组亦通过 `exec-51b8ce48-3a8d-4dce-ac29-c757a4b078ed` 成功读取；其提示词实际包含场景、时序、镜头和声音要素。独立 A 组的可见命令没有读取该可选 Skill。两组均没有生成视频，见[试点报告](RESULTS.md)。

另查 `01a14294-ab5b-7361-b999-bbfc17fbbe76`（「博众家具｜一期开发执行」）最近 10 个回合，未见 `SKILL.md` 读取命令；该聊天还有更早回合，因此**不能**推断它从未读取或未沿用任何 Skill。历史 `diagnose` 使用证据仍缺失，不用无关项目或搜索全库补数。

取证入口：Codex `read_thread` 对上述 thread 指定 `turnLimit:5`（博众为 10）、`includeOutputs:true`；以 turn/call ID 定位，返回内容可能随保留策略变化。历史读取原文和本次快照在本目录留存。交接包为只读验 CRC；未外发其内容，未改其他项目。
