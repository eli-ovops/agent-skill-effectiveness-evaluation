# run-002 派发与边界原始记录

- 2026-11-10 04:48 UTC 左右：用户通过主会话明确授权隔离子代理，每批最多两个；目标先前为 blocked，平台恢复状态尚未确认。派发前两组输入哈希与 `run-002-input-hashes.txt` 一致，两个目标 Skill 哈希分别为 `fa5553541b39a9d5d72d64472a29bcf0f31805b51c3433a47b0416eefdd6adac` 和 `28886402bbfa0470248086eab9106a103b964b76ae9496e63ff0c8a6761b6d13`。
- 第一批：`/root/video_a`、`/root/video_b`，均使用 `fork_turns=none`，未显式覆盖 model/effort，各自限定 `video-A/`、`video-B/`；除了目录及 B 明确读取目标 Skill 外，共同任务和禁止项相同。`collaboration.list_agents` 实际返回两者 `running`，不是仅记录派发。A 不额外读取/应用可选 Skill；B 读取并应用 `prompt-videos` 适用步骤。均禁联网、真实账户和凭证、付费、生成视频、服务、修改其他目录、继续派代理。
- 完成、模型和用量、诊断批次及失败另行追加实际回执；派发和 `running` 不代表结果已完成或验收通过。
