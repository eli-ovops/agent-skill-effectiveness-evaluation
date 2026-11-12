# graphify 冻结文本的定向静态复核

本次只读核对被冻结的入口及相关引用，没有运行 graphify、子代理权限测试、数据库、凭证、网络、服务或监控。静态文本一致性不代表实际行为已验证。

## 第一轮后的问题及第二轮

首轮后版本 [入口](../optimization/frozen/after/user-graphify/SKILL.md) 第 14、167 行把子代理限定为可选且须获准，但第 261–264 行仍指示一次并行派出全部子代理，存在分支及并发歧义。该发现已回传总控；原冻结文件保留。

[第二轮入口](../optimization/revision-2/after/user-graphify/SKILL.md) 第 261–265、281、285–291 行区分内联与获授权子代理、约束批量并发、规定相同输出结构及权限内恢复；[GitHub 与合并引用](../optimization/revision-2/after/user-graphify/references/github-and-merge.md) 第 5、38–39、49 行明确后端权限及图谱可选性。第二轮 22 份资源与清单 SHA-256 一致，目标入口和相关引用的第二轮 before 与首轮 after 一致。

第二轮 [exports 引用](../optimization/revision-2/after/user-graphify/references/exports.md) 第 31、43 行仍推荐密码环境变量；[transcribe 引用](../optimization/revision-2/after/user-graphify/references/transcribe.md) 第 48 行只提子代理路径。已把前者的凭证红线和后者的路径歧义回传总控。

## 第三轮定向复核

第三轮 25 份资源与 [指纹清单](../optimization/revision-3/frozen-manifest.json) 一致；入口、GitHub 引用、exports 和 transcribe 的第三轮 before 均与第二轮 after 一致。

- [exports](../optimization/revision-3/after/user-graphify/references/exports.md) 第 5、27、33、45、51、67 行区分文件、数据库、服务与配置权限，明确当前高优先级规则禁止所需凭证使用时停止 push；默认目标和 MERGE 均不自动授权。
- [transcribe](../optimization/revision-3/after/user-graphify/references/transcribe.md) 第 5、50 行不把模型缺失当下载授权，并允许内联或获授权 worker。
- [watch](../optimization/revision-3/after/user-graphify/references/add-watch.md) 第 5 行、[hooks](../optimization/revision-3/after/user-graphify/references/hooks.md) 第 5 行和 [query](../optimization/revision-3/after/user-graphify/references/query.md) 第 5、23、176、190 行对相关持久操作、权限与只读默认作出说明。

上述定向条款未再发现需要升级的同类实质冲突；这不是对全部引用、其他 Skill 或权限行为的全面验收。所有外部系统、凭证与子代理边界的行为结果仍为 UNKNOWN。
