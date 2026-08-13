"""
从 SkillsMP API 抓取的开源 Skill 数据 + prompts.chat + anthropics/skills
整合导入到 AI Skill 库数据库
"""
import sqlite3
import json
from datetime import datetime

DB_PATH = "suqianqian.db"

# ==================== 来自真实开源仓库的高质量 Skill ====================
# 数据来源: SkillsMP API (skillsmp.com), prompts.chat, anthropics/skills
# 均为开源项目 (MIT/Apache 2.0/CC0)

SKILLS = [
    # ==================== 1. 通用AI能力 ====================
    {
        "title": "Karpathy 编码准则 Skill",
        "desc": "源自 Andrej Karpathy 的 LLM 编码行为准则，减少 AI 编码常见错误：过度复杂化、隐藏假设、缺乏验证",
        "content": """# Karpathy 编码准则

> 来源: [prompts.chat](https://prompts.chat) - Karpathy Guidelines
> 许可证: MIT

行为准则，减少 LLM 编码中的常见错误。在编写、审查或重构代码时使用。

## 1. 先思考再编码

**不要假设。不要隐藏困惑。暴露权衡。**

实现之前：
- 明确陈述你的假设。如果不确定，就问。
- 如果存在多种解读，列出来——不要默默选一个。
- 如果存在更简单的方案，说出来。必要时推回。
- 如果有不清楚的地方，停下来。指出困惑之处。提问。

## 2. 简洁优先

**解决问题的最少代码。不做投机性开发。**

- 不添加超出要求的功能。
- 单次使用的代码不做抽象。
- 不添加未被请求的"灵活性"或"可配置性"。
- 不为不可能的场景做错误处理。
- 如果你写了 200 行但 50 行就能搞定，重写。

自问："一个高级工程师会说这过于复杂吗？"如果是，简化。

## 3. 精准修改

**只改必须改的。只清理你自己造成的混乱。**

编辑现有代码时：
- 不要"改进"相邻的代码、注释或格式。
- 不要重构没坏的东西。
- 匹配现有风格，即使你会用不同方式。
- 如果发现无关的死代码，提一下——不要删。

## 4. 目标驱动执行

**定义成功标准。循环直到验证通过。**

将任务转化为可验证目标：
- "添加验证" → "为无效输入写测试，然后让测试通过"
- "修复 Bug" → "写一个复现 Bug 的测试，然后让测试通过"
- "重构 X" → "确保重构前后测试都通过"

## 适配说明
- 适用于所有代码生成/审查场景
- Ollama: 推荐 qwen2.5-coder / deepseek-coder
- Dify: 可作为代码助手的 System Prompt
""",
        "category": "通用AI能力",
        "sub_category": "自我校验Skill",
        "tags": ["编码准则", "Karpathy", "代码质量", "最佳实践"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "yazz4444 (via prompts.chat)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "自适应思考框架 Skill",
        "desc": "让 AI 根据问题复杂度动态调整思考深度，嵌入'标准-借智-审查'三级质量控制",
        "content": """# 自适应思考框架 (Adaptive Thinking Framework)

> 来源: [prompts.chat](https://prompts.chat) - Adaptive Thinking Framework
> 许可证: CC0

目标：让每次回复更准确、全面、公正——如同站在巨人肩膀上思考。

## 核心结构：三层质量控制

### 第零层：自适应感知引擎

根据以下因素动态调整后续每个环节的执行深度：
- 问题的复杂度
- 事项的利害和权重
- 时间紧迫性
- 可用有效信息
- 用户的显式需求
- 上下文特征（技术vs非技术、情感vs理性等）

### 第一层：初始对接 + 向上追问（定标准）

**执行动作：**
1. 用自己的话清晰复述用户输入
2. 形成初步理解
3. 考虑宏观背景和语境
4. 梳理已知信息和未知要素
5. 反思用户潜在的真实动机
6. 关联相关知识库内容
7. 识别潜在歧义点

**元思考（必须完成）：**
> "对于这个用户输入，一个'好回答'应该满足什么标准？"

### 第二层：借智展开（多维度分析）

从多个视角/框架/学科交叉审视问题：
- 该领域的经典理论怎么说？
- 有没有反直觉的发现？
- 历史上类似问题的解决路径？

### 第三层：审查回溯

- 推理链是否完整？
- 是否有未检验的假设？
- 结论是否经得起反驳？

## 适配说明
- 适合复杂分析、决策支持场景
- Ollama: 推荐 7B+ 模型使用
- 可作为 System Prompt 全局生效
""",
        "category": "通用AI能力",
        "sub_category": "思维链CoT",
        "tags": ["自适应思考", "质量控制", "深度分析", "框架"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "prompts.chat 社区",
        "source_type": "开源改编",
        "license": "CC0",
    },
    {
        "title": "提示词优化器 Skill",
        "desc": "分析原始提示词，识别意图和差距，输出可直接粘贴的优化后提示词",
        "content": """# 提示词优化器 (Prompt Optimizer)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - prompt-optimizer
> 许可证: MIT | Stars: 239K+

## 功能
分析原始提示词，识别意图和差距，匹配最佳组件，输出优化后的可直接使用的提示词。

## 角色定义
```
你是一个提示词优化顾问。你的职责是：
- 分析用户提供的原始提示词
- 识别意图、缺失信息和改进空间
- 输出优化后的提示词

重要：你只提供咨询角色——绝不自行执行任务。
```

## 优化流程

### 1. 意图识别
- 用户想要什么类型的输出？
- 目标受众是谁？
- 期望的格式和风格？

### 2. 差距分析
- 缺少哪些关键上下文？
- 约束条件是否明确？
- 输出格式是否指定？

### 3. 优化策略
- 添加角色设定（如适用）
- 明确输出格式要求
- 增加示例（few-shot）
- 添加约束和边界条件
- 结构化指令（分步骤）

### 4. 输出格式
```
## 原始提示词分析
- 意图：[识别的意图]
- 优势：[做得好的地方]
- 差距：[需要改进的地方]

## 优化后提示词
[优化后的完整提示词]

## 优化说明
- 改动1：[原因]
- 改动2：[原因]
```

## 触发条件
当用户说"优化提示词"、"改进我的提示词"、"如何编写更好的提示词"时激活。
""",
        "category": "通用AI能力",
        "sub_category": "RAG问答优化",
        "tags": ["提示词优化", "Prompt Engineering", "优化器"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Skill 创建指南 Skill",
        "desc": "教用户如何创建、审查、验证 AgentSkill，包含 SKILL.md 规范模板",
        "content": """# Skill 创建指南

> 来源: [anthropics/skills](https://github.com/anthropics/skills) - skill-creator
> 许可证: Apache 2.0

## 什么是 Skill？

Skill 是指令、脚本和资源的文件夹，AI 可以动态加载来提升特定任务的表现。

## SKILL.md 文件结构

```yaml
---
name: my-skill-name
description: 清晰描述这个 Skill 做什么以及何时使用它
---

# Skill 名称

[在这里添加 AI 激活此 Skill 时要遵循的指令]

## 示例
- 使用示例 1
- 使用示例 2

## 指南
- 指南 1
- 指南 2
```

## Frontmatter 必填字段
- **name**: 唯一标识符（小写，连字符分隔）
- **description**: 完整描述 Skill 做什么、何时使用

## 最佳实践
1. **描述要具体**：说明触发条件和预期输出
2. **指令要结构化**：使用标题、列表、代码块
3. **包含示例**：至少 2-3 个使用示例
4. **设定边界**：明确 Skill 不做的事情
5. **可测试**：能验证 Skill 是否被正确执行

## 创建步骤
1. 创建文件夹，放入 SKILL.md
2. 添加必要的资源文件（模板、示例等）
3. 测试 Skill 的触发和执行
4. 验证输出质量
""",
        "category": "通用AI能力",
        "sub_category": "角色设定Skill",
        "tags": ["Skill创建", "SKILL.md", "规范", "模板"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "Anthropic (官方)",
        "source_type": "开源改编",
        "license": "Apache2.0",
    },

    # ==================== 2. 文案内容创作 ====================
    {
        "title": "内部沟通写作 Skill",
        "desc": "来自 Anthropic 官方 Skill，覆盖 3P 更新、公司通讯、FAQ、状态报告等所有内部沟通场景",
        "content": """# 内部沟通写作 Skill

> 来源: [anthropics/skills](https://github.com/anthropics/skills) - internal-comms
> 许可证: Source-available

## 适用场景
- 3P 更新（Progress 进展 / Plans 计划 / Problems 问题）
- 公司通讯/Newsletter
- FAQ 回答
- 状态报告
- 领导力更新
- 项目更新
- 事件报告

## 使用方法

### 1. 识别沟通类型
根据请求确定沟通类型。

### 2. 3P 更新模板
```markdown
## Progress 本周进展
- [项目A] 完成了XX，达成XX效果
- [项目B] 推进至XX阶段

## Plans 下周计划
- [项目A] 目标：完成XX
- [项目B] 启动XX

## Problems 遇到的问题
- 问题1：[描述] → 需要：[支持/决策]
- 问题2：[描述] → 建议：[方案]
```

### 3. 状态报告模板
```markdown
# [项目名] 状态报告
**日期：** YYYY-MM-DD
**状态：** 🟢 正常 / 🟡 有风险 / 🔴 阻塞

## 摘要
一段话概括当前状态。

## 关键指标
| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|

## 风险与缓解
- 风险1 → 缓解措施
- 风险2 → 缓解措施

## 需要的决策/支持
- [ ] 决策1
- [ ] 支持2
```

### 4. 写作原则
- 先说结论，再展开细节
- 量化成果，避免模糊表述
- 每个问题附带解决方案或需要的支持
- 语气专业但不生硬
""",
        "category": "文案内容创作",
        "sub_category": "公文写作",
        "tags": ["内部沟通", "3P更新", "状态报告", "Anthropic"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "Anthropic (官方)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "技术文档写作 Skill",
        "desc": "构建和审查高质量技术文档及 Agent 指令文件，来自高星开源项目",
        "content": """# 技术文档写作 Skill

> 来源: SkillsMP API (386K⭐ 仓库)
> 许可证: MIT

## 适用场景
- API 文档编写
- README / 贡献指南
- 技术设计文档
- Agent 指令文件（SKILL.md 等）
- 用户手册

## System Prompt

```
你是一个资深技术文档工程师。请遵循以下原则编写文档：

### 文档结构原则
1. 先写"是什么"和"为什么"，再写"怎么做"
2. 每个章节独立可读
3. 使用渐进式披露：概述 → 快速开始 → 详细指南 → API 参考
4. 代码示例必须完整可运行

### 写作规范
- 使用主动语态
- 一个句子只表达一个意思
- 技术术语首次出现时给出定义
- 避免歧义代词（"它"、"这个"）
- 列表项保持平行结构

### 代码示例规范
- 包含必要的 import
- 添加注释说明关键步骤
- 展示输入和输出
- 标注版本要求

### 审查清单
- [ ] 标题层级是否合理？
- [ ] 是否有遗漏的前提条件？
- [ ] 代码示例是否可运行？
- [ ] 链接是否有效？
- [ ] 是否考虑了不同水平的读者？
```

## 文档模板
```markdown
# [项目名称]

[一句话描述]

## 功能特性
- 特性1
- 特性2

## 快速开始

### 安装
\`\`\`bash
[安装命令]
\`\`\`

### 基本用法
\`\`\`[lang]
[最简示例代码]
\`\`\`

## 详细指南
## API 参考
## 贡献指南
## 许可证
```
""",
        "category": "文案内容创作",
        "sub_category": "公众号文案",
        "tags": ["技术文档", "README", "API文档", "写作规范"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "SkillsMP 社区",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 3. 网文小说专用 ====================
    {
        "title": "创意写作头脑风暴 Skill",
        "desc": "来自高星开源项目的创意工作前置 Skill，在任何创意工作之前必须使用",
        "content": """# 创意写作头脑风暴 Skill

> 来源: [github.com/obra/superpowers](https://github.com/obra/superpowers) - brainstorming
> Stars: 271K+ | 许可证: MIT

## 触发条件
在任何创意工作之前必须使用——创建功能、构建组件、添加新内容。

## 流程

### 第一步：理解需求
```
请帮我分析以下创意需求：
- 需求描述：[填写]
- 目标受众：[填写]
- 约束条件：[预算/字数/风格/时间]
```

### 第二步：发散探索
生成至少 5 个不同方向：
1. **保守方案**：最安全、最成熟的做法
2. **激进方案**：打破常规的创新做法
3. **用户视角**：从最终用户体验出发
4. **极简方案**：砍到最少的核心版本
5. **混合方案**：组合以上方案的元素

### 第三步：评估筛选
对每个方案评估：
| 维度 | 评分(1-5) | 说明 |
|------|-----------|------|
| 可行性 | | |
| 创新性 | | |
| 用户价值 | | |
| 实施成本 | | |

### 第四步：深化方案
选择 1-2 个最佳方案，深化为：
- 详细大纲/骨架
- 关键节点/转折点
- 预期效果和风险

## 适配说明
- 适用于小说大纲、文案创意、产品策划
- Ollama: 推荐创意类任务用 temperature 0.8+
""",
        "category": "网文小说专用",
        "sub_category": "剧情逻辑自检",
        "tags": ["头脑风暴", "创意", "发散思维", "评估"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "obra (via superpowers)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 4. 程序/测试/运维 ====================
    {
        "title": "测试驱动开发 Skill",
        "desc": "来自 271K⭐ 开源项目，实现任何功能或修复 Bug 前必须先写测试",
        "content": """# 测试驱动开发 (TDD) Skill

> 来源: [github.com/obra/superpowers](https://github.com/obra/superpowers) - test-driven-development
> Stars: 271K+ | 许可证: MIT

## 核心规则
实现任何功能或修复 Bug 时，在写实现代码之前必须先使用此 Skill。

## TDD 循环：红-绿-重构

### 1. 红（Red）- 写一个失败的测试
```
在写任何实现代码之前：
1. 明确要测试的行为
2. 写一个最小化的测试用例
3. 运行测试，确认它失败
4. 测试失败的原因必须是"功能未实现"（而非语法错误）
```

### 2. 绿（Green）- 写最少的代码让测试通过
```
只写让测试通过的最少代码：
- 不做过度设计
- 不添加未要求的功能
- 不重构现有代码
- 目标：让红灯变绿灯
```

### 3. 重构（Refactor）- 在测试保护下改善代码
```
测试全部通过后：
- 消除重复
- 改善命名
- 提取公共逻辑
- 确保每次重构后测试仍然通过
```

## 测试编写规范
- 测试名称描述行为，不是实现：`test_用户密码错误时返回401`
- 一个测试只验证一件事
- 测试独立，不依赖执行顺序
- 使用 Given-When-Then 结构

## 审查代码 Review 反馈时
收到代码审查反馈时，在实现建议之前：
1. 先写一个测试覆盖反馈指出的问题
2. 确认测试失败
3. 再实现修复
4. 确认所有测试通过
""",
        "category": "程序/测试/运维",
        "sub_category": "测试用例",
        "tags": ["TDD", "测试驱动", "红绿重构", "obra"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "obra (via superpowers)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "编写实施计划 Skill",
        "desc": "来自 271K⭐ 项目，在动手编码前先生成详细的多步骤实施计划",
        "content": """# 编写实施计划 Skill (Writing Plans)

> 来源: [github.com/obra/superpowers](https://github.com/obra/superpowers) - writing-plans
> Stars: 271K+ | 许可证: MIT

## 触发条件
当你有一个多步骤任务的规格或需求时，在动手写代码之前使用。

## 计划模板

```markdown
# [项目/功能名称] 实施计划

## 概述
一段话描述要做什么和为什么。

## 前置条件
- [ ] 条件1
- [ ] 条件2

## 步骤

### Step 1: [步骤名称]
- **目标：** 这一步要达成什么
- **输入：** 需要什么
- **操作：**
  1. 具体操作1
  2. 具体操作2
- **输出/验证：** 如何确认这一步完成
- **预计耗时：** X 分钟

### Step 2: [步骤名称]
...

## 风险
| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|

## 成功标准
- [ ] 标准1（可验证）
- [ ] 标准2（可验证）

## 回滚方案
如果出问题，如何回退。
```

## 计划原则
1. **每个步骤独立可验证**：完成一步后能确认是否正确
2. **粒度适中**：一步不要太大（>2小时），也不要太小（<5分钟）
3. **包含回退路径**：每步出错时怎么办
4. **标注依赖关系**：哪些步骤可以并行，哪些必须串行
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["实施计划", "项目管理", "TDD", "obra"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "obra (via superpowers)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "MySQL 模式与优化 Skill",
        "desc": "MySQL/MariaDB 的 Schema 设计、查询优化、索引策略、事务和连接池模式",
        "content": """# MySQL Patterns Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - mysql-patterns
> Stars: 239K+ | 许可证: MIT

## 覆盖领域
MySQL 和 MariaDB 的 Schema、查询、索引、事务、复制和连接池模式。

## 核心模式

### Schema 设计
```sql
-- 用户表最佳实践
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_email (email),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 查询优化
- 只 SELECT 需要的列，不要 `SELECT *`
- 大表 JOIN 时，先过滤小表
- 使用 `EXPLAIN` 分析慢查询
- 避免在 WHERE 中对列使用函数

### 索引策略
- 高频查询字段建索引
- 复合索引遵循最左前缀原则
- 区分度低的字段（如 gender）不单独建索引
- 定期清理无用索引

### 事务注意
- 事务尽量短
- 避免在事务中做 IO 操作
- 合理选择隔离级别（默认 REPEATABLE READ）
- 注意死锁检测和重试

### 连接池
- 设置合理的 `max_connections`
- 使用连接池（如 HikariCP）
- 监控 `Threads_connected` 和 `Threads_running`
""",
        "category": "程序/测试/运维",
        "sub_category": "代码解释",
        "tags": ["MySQL", "数据库", "优化", "Schema"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "前端开发模式 Skill",
        "desc": "React、Next.js、状态管理、性能优化和 UI 组件的前端开发模式集合",
        "content": """# Frontend Patterns Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - frontend-patterns
> Stars: 239K+ | 许可证: MIT

## 覆盖领域
React、Next.js、状态管理、性能优化和 UI 组件开发模式。

## React 核心模式

### 组件设计
```tsx
// ✅ 组合优于继承
function Card({ children }: { children: React.ReactNode }) {
  return <div className="card">{children}</div>;
}

function CardHeader({ title }: { title: string }) {
  return <div className="card-header">{title}</div>;
}

// 使用
<Card>
  <CardHeader title="标题" />
  <CardBody>内容</CardBody>
</Card>
```

### 状态管理选择
| 场景 | 推荐方案 |
|------|----------|
| 组件内部状态 | useState |
| 跨组件共享 | Context + useReducer |
| 服务端状态 | TanStack Query |
| 复杂全局状态 | Zustand / Jotai |
| URL 状态 | Next.js searchParams |

### 性能优化
- `React.memo` 包裹纯展示组件
- `useMemo` 缓存昂贵计算
- `useCallback` 稳定回调引用
- 虚拟列表处理大数据集
- 图片懒加载 + 适当格式（WebP/AVIF）

### Next.js 最佳实践
- App Router 优先使用 Server Components
- 数据获取在 Server Component 中完成
- 客户端交互用 `"use client"` 组件
- 合理使用 `loading.tsx` 和 `error.tsx`
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["React", "Next.js", "前端", "组件"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 5. 办公自动化SOP ====================
    {
        "title": "收件箱分类处理 Skill",
        "desc": "TaskFlow 模式的收件箱分类：意图路由、等待回复、后续摘要的自动化工作流",
        "content": """# 收件箱分类处理 Skill (TaskFlow: Inbox Triage)

> 来源: SkillsMP API (386K⭐ 仓库)
> 许可证: MIT

## 适用场景
邮件/消息/任务的自动分类、路由和跟进。

## 工作流

### 1. 收件扫描
```
请对以下收件箱内容进行分类：

[粘贴邮件/消息列表]

对每条消息分类为：
- 🔴 需要立即回复（紧急+重要）
- 🟡 需要回复（重要但不紧急）
- 🟢 仅供了解（无需回复）
- 🗑️ 可以忽略
```

### 2. 意图识别
对每条需要处理的消息：
- **请求类型**：信息请求 / 决策请求 / 行动请求
- **截止日期**：有明确期限 / 无明确期限
- **涉及人员**：需要谁参与

### 3. 优先级排序
```
按以下矩阵排序：
| | 紧急 | 不紧急 |
|---|---|---|
| 重要 | 立即处理 | 计划处理 |
| 不重要 | 委托他人 | 批量处理/忽略 |
```

### 4. 草拟回复
为 🔴 和 🟡 类消息草拟回复：
- 简洁专业
- 直接回应核心问题
- 包含明确的下一步

### 5. 跟进清单
生成待跟进事项：
- [ ] 事项 → 负责人 → 截止日期
""",
        "category": "办公自动化SOP",
        "sub_category": "会议纪要",
        "tags": ["收件箱", "分类", "TaskFlow", "邮件管理"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "SkillsMP 社区",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "电子表格处理 Skill",
        "desc": "使用自然语言编辑 PDF/Excel/Word/PPT 文档，来自高星开源项目",
        "content": """# 文档处理 Skill (Nutrient / nano-pdf)

> 来源: SkillsMP API - nano-pdf & nutrient-document-processing
> Stars: 239K-386K | 许可证: MIT

## 功能
使用自然语言指令处理多种文档格式。

## 支持的格式
- PDF：编辑、提取、OCR、签名、填写
- DOCX：读取、编辑、格式转换
- XLSX：数据分析、公式生成、图表建议
- PPTX：幻灯片创建和编辑
- HTML：转换和处理
- 图像：OCR 识别

## Excel 处理提示词
```
请帮我处理以下 Excel 数据：

### 数据描述
- 列：[列出列名]
- 行数：[约X行]
- 样本数据：[前3-5行]

### 需求
- [分析/清洗/转换/生成公式]

### 请提供：
1. 数据质量评估
2. 推荐的处理方法
3. 具体的 Excel 公式或 Python 代码
4. 结果预览
```

## PDF 处理提示词
```
请从以下 PDF 内容中提取信息：

### 提取需求
- 目标字段：[列出需要提取的字段]
- 输出格式：[JSON / CSV / 表格]

### 处理规则
- 如果字段不存在，标记为 N/A
- 数字统一格式
- 日期统一为 YYYY-MM-DD
```

## 适配说明
- 配合代码执行能力效果更佳
- Dify: 可配合代码节点使用
- Ollama: 需要配合代码解释器工具
""",
        "category": "办公自动化SOP",
        "sub_category": "Excel分析",
        "tags": ["PDF", "Excel", "文档处理", "OCR"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "SkillsMP 社区",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 6. 学习科研助手 ====================
    {
        "title": "系统性文献综述 Skill",
        "desc": "系统化学术文献综述工作流，适用于学术、生物医学、技术和科学研究",
        "content": """# 系统性文献综述 Skill (Literature Review)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - literature-review
> Stars: 239K+ | 许可证: MIT

## 适用场景
系统性文献综述工作流，适用于学术、生物医学、技术和科学研究。

## 工作流

### 阶段一：定义综述范围
```
请帮我规划一篇系统性文献综述：
- 研究问题：[PICO格式 或 具体问题]
- 时间范围：[如 2020-2025]
- 数据库：[PubMed / Google Scholar / arXiv / ...]
- 纳入标准：[列出]
- 排除标准：[列出]
```

### 阶段二：检索策略
```
请为以下研究问题设计检索策略：
- 核心概念：[概念A] AND [概念B] AND [概念C]
- 同义词/近义词扩展
- Boolean 检索式
- 数据库特定的语法（PubMed MeSH / IEEE Thesaurus）
```

### 阶段三：筛选与提取
```
对每篇文献提取：
| 字段 | 内容 |
|------|------|
| 标题 | |
| 作者/年份 | |
| 研究设计 | |
| 样本量 | |
| 主要发现 | |
| 局限性 | |
| 与本研究的关系 | |
```

### 阶段四：综合分析
```
请对以下文献进行综合分析：
1. 按主题/方法/发现分组
2. 识别共识和分歧
3. 指出研究空白
4. 绘制时间线展示演进
5. 生成综述 narrative
```

### 输出格式
```markdown
## 文献综述

### 研究背景
### 方法论概述
### 主要发现
#### 主题1
#### 主题2
### 研究空白与未来方向
### 参考文献
```
""",
        "category": "学习科研助手",
        "sub_category": "文献总结",
        "tags": ["文献综述", "系统性回顾", "学术", "PRISMA"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "签证文档翻译 Skill",
        "desc": "翻译签证申请材料为英文并生成双语PDF，来自开源项目",
        "content": """# 签证文档翻译 Skill (Visa Doc Translate)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - visa-doc-translate
> Stars: 239K+ | 许可证: MIT

## 功能
翻译签证申请材料（图片/文档）为英文，创建双语对照版本。

## 使用流程

### 1. 文档识别
```
请识别以下签证文档的内容：
- 文档类型：[身份证/户口本/银行流水/在职证明/营业执照/...]
- 原始语言：[中文/日文/韩文/...]
- 目标语言：英文

### 输出要求：
1. 原文逐段翻译
2. 保留原始格式和编号
3. 专有名词使用官方英文译法
4. 标注不确定的翻译
```

### 2. 翻译规范
- 人名：使用拼音或护照上的英文名
- 地址：从小到大排列（英文习惯）
- 日期：统一为 YYYY-MM-DD
- 金额：保留原始货币，附注约合美元
- 机构名称：使用官方英文译名

### 3. 双语对照格式
```
| 原文 | English Translation |
|------|-------------------|
| [原文内容] | [翻译内容] |
```

### 4. 注意事项
- 翻译必须忠实原文，不添加不删减
- 不确定的翻译用 [?] 标注
- 公章/签名位置用 [Seal] / [Signature] 标注
- 每页标注页码
""",
        "category": "学习科研助手",
        "sub_category": "论文润色",
        "tags": ["翻译", "签证", "双语", "文档"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 7. 行业垂直Skill ====================
    {
        "title": "SEO 审计与优化 Skill",
        "desc": "技术 SEO、页面优化、结构化数据、Core Web Vitals 和内容策略的全流程 SEO 改善",
        "content": """# SEO 审计与优化 Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - seo
> Stars: 239K+ | 许可证: MIT

## 覆盖领域
技术 SEO、页面优化、结构化数据、Core Web Vitals 和内容策略。

## SEO 审计模板

### 1. 技术 SEO 检查
```
请对以下网站进行技术 SEO 审计：
- 网站：[URL]
- 重点关注：[全站/特定页面]

检查项：
- [ ] robots.txt 配置
- [ ] sitemap.xml 完整性
- [ ] 页面加载速度（Core Web Vitals）
- [ ] 移动端适配
- [ ] HTTPS 状态
- [ ] 规范化 URL (canonical)
- [ ] 重定向链
- [ ] 404 页面
```

### 2. 页面优化
```
对目标页面优化：
- 标题标签（Title Tag）：50-60字符，含核心关键词
- 元描述（Meta Description）：150-160字符
- H1-H6 标题层级
- 图片 ALT 文本
- 内部链接结构
- URL 结构优化
```

### 3. 内容策略
```
请为以下主题规划内容：
- 核心关键词：[填写]
- 长尾关键词：[列出3-5个]
- 搜索意图：[信息型/导航型/交易型]

内容建议：
1. 文章标题（含关键词，吸引点击）
2. 内容大纲（H2/H3 结构）
3. 字数建议
4. 内链建议
```

### 4. 结构化数据
```
为以下页面生成 Schema.org 标记：
- 页面类型：[文章/产品/FAQ/本地商家/...]
- 关键信息：[列出]

输出 JSON-LD 格式
```
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["SEO", "技术SEO", "关键词", "Schema"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "品牌发现与识别 Skill",
        "desc": "帮助品牌通过结构化多轮会谈发现和提炼品牌身份，来自开源项目",
        "content": """# 品牌发现 Skill (Brand Discovery)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - brand-discovery
> Stars: 239K+ | 许可证: MIT

## 适用场景
品牌需要发现或表达其身份特征时，通过结构化的多轮会谈完成。

## 会谈流程

### Session 1: 品牌核心
```
请引导我完成品牌核心发现：

1. **使命**：我们为什么存在？
2. **愿景**：我们要去哪里？
3. **价值观**：我们相信什么？
4. **独特卖点**：我们和别人有什么不同？

请用引导式提问帮助我逐一探索。
```

### Session 2: 品牌个性
```
如果品牌是一个人：
- TA 的性格是？（5个形容词）
- TA 说话方式是？（正式/随意/幽默/权威）
- TA 穿什么？（视觉风格联想）
- TA 的朋友怎么描述 TA？

### 品牌声音指南
| 维度 | 我们是 | 我们不是 |
|------|--------|----------|
| 语气 | | |
| 用词 | | |
| 句式 | | |
```

### Session 3: 视觉方向
```
基于以上品牌核心和个性：
- 推荐色彩方向（主色+辅色+强调色）
- 字体风格建议
- 视觉风格关键词（3-5个）
- 参考品牌/设计（用于 mood board）
```

### 输出物
最终生成品牌识别文档：
1. 品牌使命/愿景/价值观
2. 品牌个性描述
3. 品牌声音指南
4. 视觉方向建议
5. 品牌故事（100字版本 + 300字版本）
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["品牌", "视觉识别", "品牌策略", "设计"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 8. Agent 工作流模板 ====================
    {
        "title": "Tavily 搜索研究 Skill",
        "desc": "Tavily 网页搜索、内容提取和研究工具，来自高星开源项目",
        "content": """# Tavily 搜索研究 Skill

> 来源: SkillsMP API (386K⭐ 仓库) - tavily
> 许可证: MIT

## 功能
使用 Tavily 进行网页搜索、内容提取和深度研究。

## 搜索模式

### 1. 快速搜索
```
搜索主题：[填写]
要求：
- 返回 5-10 个最相关的结果
- 包含标题、摘要、URL
- 按相关性排序
```

### 2. 深度研究
```
研究问题：[填写]
流程：
1. 生成 3-5 个搜索查询覆盖不同角度
2. 对每个查询执行搜索
3. 提取关键信息
4. 交叉验证多个来源
5. 综合为结构化报告

输出格式：
## 研究报告
### 摘要
### 关键发现
### 详细分析
### 来源列表
```

### 3. 内容提取
```
从以下 URL 提取内容：
- URL列表：[填写]
- 提取目标：[全文/摘要/特定信息]
- 输出格式：[Markdown/JSON]
```

## Dify 集成
```
在 Dify 中配置 Tavily 工具：
1. 获取 API Key: app.tavily.com
2. 在 Dify 工具市场添加 Tavily
3. 在 Chatflow 中连接搜索节点
4. 配置搜索参数（深度、数量、域名过滤）
```

## 适配说明
- 需要 Tavily API Key（有免费额度）
- Ollama: 需要配合工具调用能力
- Dify: 原生支持 Tavily 工具节点
""",
        "category": "Agent工作流模板",
        "sub_category": "Dify工作流",
        "tags": ["Tavily", "搜索", "研究", "内容提取"],
        "fit_tools": ["Dify", "Ollama"],
        "author": "SkillsMP 社区",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Notion 文档管理 Skill",
        "desc": "Notion CLI/API 操作：页面管理、Markdown 内容、数据源、文件、评论和搜索",
        "content": """# Notion 文档管理 Skill

> 来源: SkillsMP API (386K⭐ 仓库) - notion
> 许可证: MIT

## 功能
通过 Notion API 进行页面、数据库、评论的自动化管理。

## 核心操作

### 1. 搜索
```
在 Notion 中搜索：
- 关键词：[填写]
- 过滤类型：[page/database/all]
- 排序：[最后编辑时间/创建时间]
```

### 2. 创建页面
```
在 Notion 创建页面：
- 标题：[填写]
- 父页面/数据库：[填写]
- 内容（Markdown）：
[粘贴 Markdown 内容]

自动转换为 Notion Block 格式
```

### 3. 数据库操作
```
查询数据库：
- 数据库ID：[填写]
- 过滤条件：[属性] [操作符] [值]
- 排序：[属性] [asc/desc]
- 分页：[page_size]
```

### 4. 评论管理
```
为页面添加评论：
- 页面ID：[填写]
- 评论内容：[填写]
- @提及：[用户列表]
```

## Dify 集成
```
在 Dify 中集成 Notion：
1. 创建 Notion Integration: notion.so/my-integrations
2. 获取 Internal Integration Token
3. 在 Dify 中配置自定义工具
4. 设置 API 端点和认证
```

## 自动化场景
- 会议纪要自动同步到 Notion
- 知识库内容定期更新
- 项目状态自动汇报
- 周报自动写入 Notion 数据库
""",
        "category": "Agent工作流模板",
        "sub_category": "Dify工作流",
        "tags": ["Notion", "文档管理", "API", "自动化"],
        "fit_tools": ["Dify", "Ollama"],
        "author": "SkillsMP 社区",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Manim 技术视频生成 Skill",
        "desc": "构建可复用的 Manim 技术概念讲解视频、图表、系统图和产品演示",
        "content": """# Manim 技术视频生成 Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - manim-video
> Stars: 239K+ | 许可证: MIT

## 功能
使用 Manim 库创建技术概念讲解视频、图表动画和系统演示。

## 视频类型

### 1. 概念讲解
```python
# 示例：解释神经网络的反向传播
from manim import *

class BackpropExplanation(Scene):
    def construct(self):
        title = Text("反向传播").scale(1.2)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        # 网络结构
        layers = VGroup(*[
            self._create_layer(n, x)
            for n, x in [(3, -4), (4, 0), (2, 4)]
        ])
        self.play(FadeIn(layers, shift=RIGHT))
        # ... 动画展示前向传播和反向传播

    def _create_layer(self, n_neurons, x_pos):
        neurons = VGroup(*[
            Dot(point=[x_pos, y, 0], radius=0.2)
            for y in np.linspace(-2, 2, n_neurons)
        ])
        return neurons
```

### 2. 数据图表
```python
class DataChart(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 10],
            y_range=[0, 100],
            axis_config={"include_tip": True},
        )
        graph = axes.plot(lambda x: 10 * x, color=BLUE)
        self.play(Create(axes), Create(graph))
```

### 3. 系统架构图
```python
class SystemArchitecture(Scene):
    def construct(self):
        # 组件方框
        frontend = RoundedRectangle(...).shift(LEFT * 4)
        backend = RoundedRectangle(...).shift(ORIGIN)
        database = RoundedRectangle(...).shift(RIGHT * 4)

        # 连接箭头
        arrow1 = Arrow(frontend, backend)
        arrow2 = Arrow(backend, database)

        self.play(
            FadeIn(frontend), FadeIn(backend), FadeIn(database),
            GrowArrow(arrow1), GrowArrow(arrow2)
        )
```

## 使用建议
- 先写脚本（旁白文本 + 对应画面）
- 从简单场景开始，逐步添加复杂度
- 使用 `self.wait()` 控制节奏
- 渲染命令：`manim -pql scene.py ClassName`
""",
        "category": "Agent工作流模板",
        "sub_category": "OpenWebUI Pipeline",
        "tags": ["Manim", "视频", "动画", "技术讲解"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "持续学习 Skill",
        "desc": "自动从 AI 会话中提取可复用模式并保存为学习到的 Skill，持续进化",
        "content": """# 持续学习 Skill (Continuous Learning)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - continuous-learning
> Stars: 239K+ | 许可证: MIT

## 功能
自动从 AI 会话中提取可复用的模式和最佳实践，保存为持久化的 Skill。

## 工作流程

### 1. 会话分析
```
请分析以下 AI 会话记录，提取可复用的模式：

[粘贴会话记录]

### 提取维度
1. **用户偏好模式**：用户反复要求什么格式/风格？
2. **成功解决模式**：哪些回答获得了用户认可？
3. **错误修正模式**：AI 犯了什么错？如何修正的？
4. **工作流程模式**：用户习惯的工作步骤是什么？
```

### 2. 模式提炼
```
对每个识别到的模式：
- 名称：[简洁描述]
- 触发条件：[什么时候适用]
- 模式内容：[具体规则/步骤]
- 验证方式：[如何确认模式有效]
```

### 3. Skill 生成
```
将提炼的模式转化为 Skill 格式：

---
name: [auto-learned-pattern-name]
description: [自动学习到的模式描述]
---

# [模式名称]

## 何时使用
[触发条件]

## 规则
1. [规则1]
2. [规则2]

## 示例
[从会话中提取的成功示例]
```

### 4. 模式管理
- 定期回顾已学习的模式
- 合并重复模式
- 删除过时模式
- 验证模式在新场景中的有效性

## 适配说明
- 需要会话历史记录功能
- Dify: 可通过对话日志实现
- Ollama: 需要外部脚本配合
""",
        "category": "Agent工作流模板",
        "sub_category": "Ollama角色Skill",
        "tags": ["持续学习", "模式提取", "自我进化", "Skill生成"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 新增：来自 SkillsMP API 的高星通用 Skill ====================
    # 数据来源: skillsmp.com API (openclaw 386K⭐, ECC 239K⭐, obra 271K⭐, mattpocock 214K⭐)

    # ==================== 1. 通用AI能力（补充） ====================
    {
        "title": "代码审查接收与验证 Skill",
        "desc": "收到代码审查反馈时，用技术严谨性验证而非盲目接受，来自 271K⭐ 开源项目",
        "content": """# 代码审查接收与验证 Skill (Receiving Code Review)

> 来源: [github.com/obra/superpowers](https://github.com/obra/superpowers) - receiving-code-review
> Stars: 271K+ | 许可证: MIT

## 触发条件
收到代码审查反馈后，在实现建议之前使用。尤其是反馈看起来不清晰或技术上可疑时。

## 核心原则
**技术严谨性和验证，而非表演性同意或盲目执行。**

## 处理流程

### 1. 评估反馈
```
对每条审查反馈：
1. 反馈是否解决了实际问题？
2. 建议的修改是否技术上正确？
3. 是否引入了新问题？
4. 是否有更简单的方案？
```

### 2. 验证而非盲从
- 不要仅仅因为审查者说了就照做
- 验证建议是否真的改善了代码
- 如果不同意，用技术论据回应
- 对于不确定的建议，先写测试验证

### 3. 实现前检查
```
在实现每条建议之前：
- [ ] 理解建议解决的问题
- [ ] 确认方案不会引入新问题
- [ ] 考虑是否有更简洁的实现
- [ ] 确保不偏离原始需求
```

### 4. 回应规范
- 同意的：说明为什么同意，直接实施
- 不同意的：给出技术理由，提出替代方案
- 不确定的：先做实验/写测试验证
""",
        "category": "通用AI能力",
        "sub_category": "自我校验Skill",
        "tags": ["代码审查", "Code Review", "验证", "obra"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "obra (via superpowers)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "意图驱动开发 Skill",
        "desc": "将模糊的产品需求转化为可验证的验收标准，降低安全/数据/迁移风险，来自 239K⭐ 项目",
        "content": """# 意图驱动开发 Skill (Intent-Driven Development)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - intent-driven-development
> Stars: 239K+ | 许可证: MIT

## 触发条件
当需要澄清功能需求、定义验收标准、降低安全/数据/迁移/集成变更风险时。

## 核心流程

### 1. 意图澄清
```
对每个需求回答：
- 用户/业务的真实目标是什么？
- 成功的具体表现是什么？
- 什么情况下算失败？
- 有哪些隐含假设需要验证？
```

### 2. 验收标准生成
```markdown
## 功能验收标准
- [ ] AC-1: Given [前置条件], When [操作], Then [预期结果]
- [ ] AC-2: Given [前置条件], When [操作], Then [预期结果]

## 非功能验收标准
- [ ] 性能: 响应时间 < Xms (P95)
- [ ] 安全: 输入验证/授权检查
- [ ] 数据: 迁移回滚方案
- [ ] 可观测: 日志/指标/告警
```

### 3. 风险评估
| 风险类型 | 检查项 |
|----------|--------|
| 安全风险 | 认证/授权/输入验证/密钥管理 |
| 数据风险 | 迁移/回滚/一致性/备份 |
| 集成风险 | API 契约/版本兼容/超时重试 |
| 性能风险 | 数据量/并发/缓存/降级 |

### 4. 输出物
- 清晰的验收标准列表
- 风险缓解措施
- 可测试的实现目标
""",
        "category": "通用AI能力",
        "sub_category": "思维链CoT",
        "tags": ["意图驱动", "验收标准", "需求分析", "ECC"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "编码规范基线 Skill",
        "desc": "跨项目通用编码规范：命名、可读性、不可变性、代码质量审查，来自 239K⭐ 项目",
        "content": """# 编码规范基线 Skill (Coding Standards)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - coding-standards
> Stars: 239K+ | 许可证: MIT

## 适用范围
跨项目通用的编码规范基线。当没有框架特定 Skill 适用时使用。

## 命名规范
- **变量/函数**: 描述用途而非类型（`userCount` 而非 `num`）
- **布尔值**: 用 is/has/should/can 前缀（`isActive`, `hasPermission`）
- **常量**: UPPER_SNAKE_CASE
- **避免缩写**: 除非是广泛认可的（如 `id`, `url`, `http`）
- **一致性**: 同一概念全局使用同一名称

## 可读性
- 函数不超过 20 行（理想情况）
- 嵌套不超过 3 层
- 一个函数只做一件事
- 提前返回减少 else 嵌套
- 用有意义的变量名替代注释

## 不可变性优先
- 默认使用 const/final
- 避免修改函数参数
- 返回新对象而非修改原对象
- 使用不可变数据结构

## 代码质量审查清单
- [ ] 命名是否清晰表达意图？
- [ ] 是否有不必要的复杂度？
- [ ] 错误处理是否充分？
- [ ] 是否有重复代码可提取？
- [ ] 边界条件是否处理？
- [ ] 是否有安全隐患？
""",
        "category": "通用AI能力",
        "sub_category": "角色设定Skill",
        "tags": ["编码规范", "代码质量", "命名", "最佳实践"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 2. 文案内容创作（补充） ====================
    {
        "title": "文章写作 Skill",
        "desc": "撰写文章、指南、博客、教程、Newsletter，保持独特语气和品牌一致性，来自 239K⭐ 项目",
        "content": """# 文章写作 Skill (Article Writing)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - article-writing
> Stars: 239K+ | 许可证: MIT

## 触发条件
需要撰写超过一段的精致书面内容时，尤其是语气一致性、结构和可信度至关重要时。

## 写作流程

### 1. 语气分析
```
从提供的示例或品牌指南中提取：
- 正式度（1-10）
- 技术深度（入门/中级/专家）
- 情感色彩（理性/感性/混合）
- 人称（第一/第二/第三）
- 句式偏好（短句/长句/混合）
```

### 2. 结构模板
```markdown
# [吸引人的标题]

## 开头（钩子）
- 故事/数据/反直觉观点
- 建立与读者的连接
- 预告文章价值

## 正文
### 小节1：问题/背景
### 小节2：核心内容
### 小节3：实践/案例
### 小节4：进阶/延伸

## 结尾
- 核心要点回顾
- 行动号召 (CTA)
- 开放性问题引发讨论
```

### 3. 写作原则
- 每段只讲一个核心观点
- 用具体例子替代抽象描述
- 避免 AI 写作通病（过度使用"此外"、"值得注意的是"等）
- 数据支撑论点
- 主动语态优先
""",
        "category": "文案内容创作",
        "sub_category": "公众号文案",
        "tags": ["文章写作", "品牌语气", "内容创作", "ECC"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "品牌声音画像 Skill",
        "desc": "从真实内容中提炼品牌写作风格画像，确保跨渠道语气一致，来自 239K⭐ 项目",
        "content": """# 品牌声音画像 Skill (Brand Voice)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - brand-voice
> Stars: 239K+ | 许可证: MIT

## 功能
从真实帖子、文章、发布说明、文档或网站文案中构建写作风格画像，然后在内容、推广和社交工作流中复用。

## 分析流程

### 1. 样本收集
```
请提供以下品牌内容样本（至少 5-10 篇）：
- 博客文章 / 公众号文章
- 社交媒体帖子
- 产品描述
- 邮件/Newsletter
- 帮助文档
```

### 2. 风格画像输出
```markdown
## [品牌名] 声音画像

### 核心特质（3-5 个形容词）
- 特质1：[描述 + 示例]
- 特质2：[描述 + 示例]

### 语气光谱
| 维度 | 倾向 |
|------|------|
| 正式 ← → 随意 | [位置] |
| 严肃 ← → 幽默 | [位置] |
| 技术 ← → 通俗 | [位置] |
| 克制 ← → 热情 | [位置] |

### 常用表达
- ✅ 会说：[列出典型表达]
- ❌ 不会说：[列出典型表达]

### 句式特征
- 平均句长
- 段落长度偏好
- 标点使用习惯
```

### 3. 应用指南
- 新内容创作时参照画像
- 定期校准（每季度回顾）
- 不同渠道可微调但核心不变
""",
        "category": "文案内容创作",
        "sub_category": "海报文案",
        "tags": ["品牌声音", "写作风格", "语气一致", "ECC"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 4. 程序/测试/运维（补充） ====================
    {
        "title": "测试审计 Skill",
        "desc": "测试质量审计：识别低价值测试、实现耦合测试、重复测试，来自 386K⭐ 项目",
        "content": """# 测试审计 Skill (Test Audit)

> 来源: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) - test-audit
> Stars: 386K+ | 许可证: MIT

## 触发条件
编写、修改、审查或扫描测试时使用。

## 审计维度

### 1. 测试价值评估
```
对每个测试评估：
- 是否验证了用户可见的行为？
- 失败时是否提供了有用的诊断信息？
- 是否覆盖了真实的业务场景？
- 修改实现代码时，测试是否不需要改？
```

### 2. 问题分类
| 问题类型 | 特征 | 处理方式 |
|----------|------|----------|
| 低价值测试 | 只测试实现细节 | 重写为行为测试 |
| 耦合测试 | 依赖内部实现 | 解耦到公共接口 |
| 重复测试 | 多个测试验证同一行为 | 合并或删除 |
| 脆弱测试 | 频繁误报 | 修复或移除 |

### 3. 审计清单
- [ ] 测试名称是否描述了行为而非实现？
- [ ] 一个测试是否只验证一件事？
- [ ] 测试是否独立于执行顺序？
- [ ] 断言是否精确（不过度也不不足）？
- [ ] 测试数据是否 realistic？
- [ ] 是否有测试只验证实现细节？

### 4. 改进建议模板
```markdown
## 测试审计结果
- 总测试数：X
- 高价值：X (X%)
- 需改进：X (X%)
- 建议删除：X (X%)

### 改进建议
1. [测试名] → [建议]
2. [测试名] → [建议]
```
""",
        "category": "程序/测试/运维",
        "sub_category": "测试用例",
        "tags": ["测试审计", "测试质量", "openclaw"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "openclaw",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "安全审查 Skill",
        "desc": "添加认证、处理用户输入、管理密钥、创建 API 端点时的全面安全检查清单",
        "content": """# 安全审查 Skill (Security Review)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - security-review
> Stars: 239K+ | 许可证: MIT

## 触发条件
添加认证、处理用户输入、处理密钥、创建 API 端点或实现支付/敏感功能时。

## 安全检查清单

### 1. 认证与授权
- [ ] 所有端点是否有认证保护？
- [ ] 是否使用了强密码策略？
- [ ] JWT token 是否正确验证和过期？
- [ ] 是否有权限检查（RBAC/ABAC）？
- [ ] Session 是否正确管理？

### 2. 输入验证
- [ ] 所有用户输入是否经过验证？
- [ ] 是否使用白名单而非黑名单？
- [ ] 文件上传是否限制类型和大小？
- [ ] SQL 查询是否使用参数化？
- [ ] 是否防止了 XSS（输出编码）？

### 3. 密钥管理
- [ ] 密钥是否从环境变量读取（非硬编码）？
- [ ] 密钥是否在日志中脱敏？
- [ ] 是否使用了密钥轮换？
- [ ] API Key 是否有最小权限？

### 4. 数据传输
- [ ] 是否强制 HTTPS？
- [ ] 敏感数据是否加密存储？
- [ ] CORS 配置是否正确？
- [ ] CSP 头是否配置？

### 5. 日志与监控
- [ ] 是否记录了安全事件？
- [ ] 日志中是否避免了敏感信息？
- [ ] 是否有异常检测/告警？
""",
        "category": "程序/测试/运维",
        "sub_category": "运维巡检SOP",
        "tags": ["安全审查", "认证", "输入验证", "密钥管理"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Redis 模式 Skill",
        "desc": "Redis 数据结构模式、缓存策略、分布式锁、限流、Pub/Sub 和连接管理",
        "content": """# Redis Patterns Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - redis-patterns
> Stars: 239K+ | 许可证: MIT

## 覆盖领域
Redis 数据结构模式、缓存策略、分布式锁、限流、Pub/Sub 和生产连接管理。

## 核心模式

### 缓存策略
```
# Cache-Aside 模式
async def get_user(user_id):
    # 1. 先查缓存
    cached = await redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    # 2. 查数据库
    user = await db.get_user(user_id)
    # 3. 写入缓存（带过期时间）
    await redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

### 分布式锁
```
# Redis 分布式锁（Redlock 简化版）
async def acquire_lock(key, ttl=10):
    token = str(uuid4())
    acquired = await redis.set(f"lock:{key}", token, nx=True, ex=ttl)
    return token if acquired else None

async def release_lock(key, token):
    # 只释放自己持有的锁
    lua = "if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end"
    await redis.eval(lua, 1, f"lock:{key}", token)
```

### 限流（滑动窗口）
```
# 滑动窗口限流
async def rate_limit(user_id, limit=100, window=60):
    key = f"rate:{user_id}"
    now = time.time()
    pipe = redis.pipeline()
    pipe.zremrangebyscore(key, 0, now - window)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, window)
    _, _, count, _ = await pipe.execute()
    return count <= limit
```

### 连接管理
- 使用连接池（`redis.ConnectionPool`）
- 设置合理的 `socket_timeout` 和 `socket_connect_timeout`
- 监控 `INFO memory` 和 `INFO clients`
- 大 key 检测和清理
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["Redis", "缓存", "分布式锁", "限流"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "数据库迁移最佳实践 Skill",
        "desc": "Schema 变更、数据迁移、回滚和零停机部署，支持 PostgreSQL/MySQL 和主流 ORM",
        "content": """# 数据库迁移最佳实践 Skill (Database Migrations)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - database-migrations
> Stars: 239K+ | 许可证: MIT

## 适用范围
PostgreSQL、MySQL 和常见 ORM（Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate）的迁移实践。

## 核心原则

### 1. 安全变更
```
✅ 安全操作：
- 添加可选列（有默认值或允许 NULL）
- 添加新表
- 添加索引（CONCURRENTLY）
- 扩展列长度（VARCHAR 50→100）

❌ 危险操作：
- 删除列/表（先标记废弃，下个版本再删）
- 重命名列（用新列+数据迁移+逐步切换）
- 修改列类型（用新列+迁移+切换）
- 添加 NOT NULL 无默认值的列
```

### 2. 零停机迁移模式
```markdown
## 重命名列的安全方式
### 迁移1：添加新列
ALTER TABLE users ADD COLUMN full_name TEXT;

### 迁移2：双写（代码同时写新旧列）
### 迁移3：回填数据
UPDATE users SET full_name = name WHERE full_name IS NULL;

### 迁移4：切换读取到新列
### 迁移5：删除旧列（确认稳定后）
```

### 3. 回滚策略
- 每个迁移必须有对应的回滚脚本
- 数据迁移前做备份
- 大表迁移分批执行
- 测试环境先验证

### 4. ORM 特定
| ORM | 迁移命令 | 注意 |
|-----|----------|------|
| Prisma | `prisma migrate dev` | 开发环境用，生产用 `deploy` |
| Drizzle | `drizzle-kit push` | 支持 `drizzle-kit generate` |
| Django | `python manage.py makemigrations` | 注意 `--check` CI 集成 |
| TypeORM | `typeorm migration:generate` | 同步前 review SQL |
""",
        "category": "程序/测试/运维",
        "sub_category": "运维巡检SOP",
        "tags": ["数据库迁移", "Schema", "零停机", "PostgreSQL"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Python 调试 Skill",
        "desc": "Python 调试技巧：pdb、breakpoint()、事后检验、debugpy 远程附加，来自 386K⭐ 项目",
        "content": """# Python 调试 Skill (Python debugpy)

> 来源: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) - python-debugpy
> Stars: 386K+ | 许可证: MIT

## 功能
使用 pdb、breakpoint()、事后检验和 debugpy 远程附加来调试 Python 程序。

## 调试方法

### 1. breakpoint() 基础
```python
def process_data(data):
    # 在此处暂停执行
    breakpoint()
    # 检查变量
    result = transform(data)
    return result

# 条件断点
for item in items:
    if item.id == problematic_id:
        breakpoint()  # 只在特定条件下暂停
    process(item)
```

### 2. pdb 常用命令
```
(Pdb) help           # 显示所有命令
(Pdb) n (next)       # 执行下一行
(Pdb) s (step)       # 步入函数
(Pdb) c (continue)   # 继续执行
(Pdb) p variable     # 打印变量
(Pdb) pp variable    # 美化打印
(Pdb) l (list)       # 列出上下文代码
(Pdb) w (where)      # 显示调用栈
(Pdb) u (up)         # 上移一帧
(Pdb) d (down)       # 下移一帧
(Pdb) b line_number  # 设置断点
(Pdb) a (args)       # 打印函数参数
```

### 3. 事后检验
```python
import pdb
import sys

# 异常时自动进入调试
sys.excepthook = pdb.post_mortem

# 或在代码中手动触发
def buggy_function():
    try:
        result = 1 / 0
    except Exception:
        import traceback
        traceback.print_exc()
        pdb.post_mortem()
```

### 4. debugpy 远程调试
```python
# 服务端：启动 debugpy 监听
import debugpy
debugpy.listen(('0.0.0.0', 5678))
debugpy.wait_for_client()  # 等待调试器附加

# VS Code launch.json 配置：
# { "type": "python", "request": "attach",
#   "connect": { "host": "localhost", "port": 5678 } }
```
""",
        "category": "程序/测试/运维",
        "sub_category": "代码解释",
        "tags": ["Python", "调试", "pdb", "debugpy"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "openclaw",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 5. 办公自动化SOP（补充） ====================
    {
        "title": "GitHub 运维自动化 Skill",
        "desc": "GitHub 仓库运维：Issue 分类、PR 管理、CI/CD、Release 管理、安全监控",
        "content": """# GitHub 运维自动化 Skill (GitHub Ops)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - github-ops
> Stars: 239K+ | 许可证: MIT

## 功能
使用 gh CLI 进行 GitHub 仓库运维：Issue 分类、PR 管理、CI/CD 操作、Release 管理和安全监控。

## 核心操作

### 1. Issue 管理
```bash
# 列出所有 open issues
gh issue list --state open

# 创建 Issue（带标签和指派）
gh issue create --title "Bug: ..." --body "..." \\
  --label "bug,high-priority" --assignee "@me"

# Issue 分类脚本
gh issue list --label "needs-triage" --json number,title,labels \\
  --jq '.[] | "\\(.number): \\(.title)"'
```

### 2. PR 管理
```bash
# 创建 PR
gh pr create --title "feat: ..." --body "..." --base main

# 审查 PR
gh pr review --approve
gh pr review --request-changes --body "..."

# 检查 CI 状态
gh pr checks
```

### 3. Release 管理
```bash
# 创建 Release
gh release create v1.0.0 --title "v1.0.0" --notes "..."

# 自动生成 Release Notes
gh release create v1.0.0 --generate-notes
```

### 4. 自动化场景
- 每日检查 stale issues 并标记
- 自动给新 PR 分配 reviewer
- 监控 CI 失败并通知
- 定期安全依赖检查
""",
        "category": "办公自动化SOP",
        "sub_category": "周报月报",
        "tags": ["GitHub", "DevOps", "自动化", "CI/CD"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "自动化数据采集 Agent Skill",
        "desc": "全自动 AI 数据采集代理：定时抓取公共数据源，LLM 增强，存储到 Notion/Sheets",
        "content": """# 自动化数据采集 Agent Skill (Data Scraper Agent)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - data-scraper-agent
> Stars: 239K+ | 许可证: MIT

## 功能
构建全自动 AI 驱动的数据采集代理，适用于任何公共来源——招聘网站、价格信息、新闻、GitHub、体育赛事等。

## 架构

### 1. 采集配置
```yaml
scraper:
  name: "价格监控"
  schedule: "0 */6 * * *"  # 每6小时
  sources:
    - url: "https://example.com/products"
      selector: ".product-card"
      fields:
        name: ".product-name"
        price: ".price"
        date: "auto"
  enrichment:
    enabled: true
    model: "gemini-flash"  # 免费
    prompt: "提取产品类别和情感倾向"
  storage:
    type: "notion"  # 或 sheets/supabase
    database_id: "xxx"
```

### 2. 数据丰富
```
对每条采集数据：
1. 基础字段提取（名称、价格、日期）
2. LLM 增强：
   - 分类标注
   - 趋势分析
   - 异常检测
3. 去重和更新
```

### 3. 存储选项
| 存储 | 适用场景 | 优势 |
|------|----------|------|
| Notion | 团队协作查看 | 可视化好 |
| Google Sheets | 数据分析 | 公式支持 |
| Supabase | 大规模数据 | 查询性能 |
| CSV/JSON | 本地备份 | 简单直接 |

### 4. 运行方式
- GitHub Actions（免费）
- 定时触发 + 手动触发
- 结果通知（Slack/邮件）
""",
        "category": "办公自动化SOP",
        "sub_category": "Excel分析",
        "tags": ["数据采集", "爬虫", "自动化", "AI Agent"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 6. 学习科研助手（补充） ====================
    {
        "title": "文档查询 Skill",
        "desc": "通过 MCP 获取最新的库和框架文档，而非依赖训练数据，来自 239K⭐ 项目",
        "content": """# 文档查询 Skill (Documentation Lookup)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - documentation-lookup
> Stars: 239K+ | 许可证: MIT

## 功能
使用 Context7 MCP 获取最新的库和框架文档，而非依赖可能过时的训练数据。

## 触发条件
- 设置问题（"如何配置 XX？"）
- API 参考查询
- 代码示例请求
- 用户提到具体框架（React, Next.js, Prisma 等）

## 工作流程

### 1. 识别框架
```
用户提到以下框架时自动激活：
- React / Next.js / Vue / Svelte
- Prisma / Drizzle / TypeORM
- FastAPI / Django / Flask
- Tailwind / shadcn/ui
- 任何有文档的库
```

### 2. 查询文档
```
查询流程：
1. 识别用户提到的框架和版本
2. 通过 MCP 获取最新文档
3. 定位相关章节
4. 提取准确信息
5. 附上文档链接
```

### 3. 回答格式
```markdown
## [框架名] - [主题]

> 📖 来源: [官方文档](链接)

### 解答
[基于最新文档的回答]

### 代码示例
[来自文档的示例]

### 注意事项
- 版本要求
- 常见陷阱
```

## 适配说明
- 需要 Context7 MCP 服务器
- Ollama: 需要配合 MCP 工具调用
- Dify: 可通过 HTTP 节点集成
""",
        "category": "学习科研助手",
        "sub_category": "思维导图生成",
        "tags": ["文档查询", "MCP", "最新API", "Context7"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 7. 行业垂直Skill（补充） ====================
    {
        "title": "Bug 诊断循环 Skill",
        "desc": "系统性诊断困难 Bug 和性能回归的循环流程，来自 214K⭐ 项目",
        "content": """# Bug 诊断循环 Skill (Diagnosing Bugs)

> 来源: [github.com/mattpocock/skills](https://github.com/mattpocock/skills) - diagnosing-bugs
> Stars: 214K+ | 许可证: MIT

## 触发条件
用户说"诊断"/"调试这个"，或报告某些东西坏了/抛出异常/失败/变慢。

## 诊断循环

### Phase 1: 复现
```
1. 精确描述问题行为
2. 找到最小复现步骤
3. 确认复现环境
4. 记录：
   - 预期行为：[应该发生什么]
   - 实际行为：[实际发生了什么]
   - 环境：[OS/运行时/版本]
```

### Phase 2: 缩小范围
```
1. 二分法：哪次提交引入了问题？
2. 隔离：能否在最小环境中复现？
3. 依赖：是否是第三方库的问题？
4. 数据：是否特定数据才触发？
```

### Phase 3: 假设-验证
```markdown
对每个假设：
1. **假设**：[描述]
2. **预测**：如果假设正确，那么 [预期观察]
3. **测试**：[如何验证]
4. **结果**：✅ 证实 / ❌ 证伪
5. **下一步**：[基于结果]
```

### Phase 4: 修复与验证
```
1. 写一个复现 Bug 的测试
2. 确认测试失败
3. 实施修复
4. 确认测试通过
5. 确认没有引入新问题
6. 检查是否有类似 Bug
```

### 性能回归专项
- 对比前后版本的关键指标
- Profiling 找出热点
- 检查数据量变化
- 检查依赖版本变化
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["Bug诊断", "调试", "性能回归", "mattpocock"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "mattpocock",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 8. Agent 工作流模板（补充） ====================
    {
        "title": "MCP Server 构建模式 Skill",
        "desc": "使用 Node/TypeScript SDK 构建 MCP 服务器：工具、资源、提示词、验证和传输",
        "content": """# MCP Server 构建模式 Skill (MCP Server Patterns)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - mcp-server-patterns
> Stars: 239K+ | 许可证: MIT

## 功能
使用 Node/TypeScript SDK 构建 MCP 服务器——工具、资源、提示词、Zod 验证、stdio vs Streamable HTTP。

## 基础结构
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

// 注册工具
server.tool(
  "search",
  "Search for items",
  { query: z.string(), limit: z.number().optional() },
  async ({ query, limit = 10 }) => {
    const results = await searchItems(query, limit);
    return { content: [{ type: "text", text: JSON.stringify(results) }] };
  }
);

// 启动
const transport = new StdioServerTransport();
await server.connect(transport);
```

## 传输方式选择
| 方式 | 适用场景 |
|------|----------|
| stdio | 本地进程通信，最简单 |
| Streamable HTTP | 远程服务，支持 SSE |

## 最佳实践
- 工具描述要清晰（AI 根据描述决定何时调用）
- 使用 Zod 严格验证输入
- 错误返回有用的信息
- 资源用于提供上下文
- 提示词用于预设工作流
""",
        "category": "Agent工作流模板",
        "sub_category": "Dify工作流",
        "tags": ["MCP", "TypeScript", "服务器", "工具协议"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "LLM 成本优化 Skill",
        "desc": "LLM API 成本优化：按任务复杂度路由模型、预算跟踪、重试逻辑和提示缓存",
        "content": """# LLM 成本优化 Skill (Cost-Aware LLM Pipeline)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - cost-aware-llm-pipeline
> Stars: 239K+ | 许可证: MIT

## 功能
LLM API 使用的成本优化模式——按任务复杂度路由模型、预算跟踪、重试逻辑和提示缓存。

## 核心模式

### 1. 模型路由
```python
# 按任务复杂度选择模型
def route_model(task_type: str) -> str:
    routing = {
        "simple_classification": "gpt-4o-mini",      # $0.15/1M
        "summarization": "gpt-4o-mini",               # $0.15/1M
        "complex_reasoning": "gpt-4o",                # $2.50/1M
        "code_generation": "claude-3.5-sonnet",       # $3.00/1M
        "creative_writing": "claude-3.5-sonnet",      # $3.00/1M
        "data_extraction": "gpt-4o-mini",             # $0.15/1M
    }
    return routing.get(task_type, "gpt-4o-mini")
```

### 2. 预算控制
```python
class BudgetTracker:
    def __init__(self, daily_limit_usd=10.0):
        self.daily_limit = daily_limit_usd
        self.spent_today = 0.0

    def check_budget(self, estimated_cost: float) -> bool:
        return (self.spent_today + estimated_cost) <= self.daily_limit

    def record_usage(self, tokens_in: int, tokens_out: int, price_per_1m_in: float, price_per_1m_out: float):
        cost = (tokens_in / 1_000_000 * price_per_1m_in) + (tokens_out / 1_000_000 * price_per_1m_out)
        self.spent_today += cost
```

### 3. 提示缓存
- 将不变的指令放在提示词开头（利用缓存）
- 使用 prefix caching 减少重复计算
- 缓存常见问答对

### 4. 重试策略
- 指数退避 + 抖动
- 429 (rate limit): 等待后重试
- 500 (server error): 最多重试 3 次
- 考虑降级到更便宜的模型

### 5. 成本对比
| 策略 | 节省幅度 | 复杂度 |
|------|----------|--------|
| 模型路由 | 60-80% | 低 |
| 提示缓存 | 20-50% | 低 |
| 批量处理 | 50% (API折扣) | 中 |
| 本地模型 | 100% (边际) | 高 |
""",
        "category": "Agent工作流模板",
        "sub_category": "Ollama角色Skill",
        "tags": ["LLM成本", "模型路由", "预算控制", "优化"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "多 Agent 操作系统 Skill",
        "desc": "构建持久化多 Agent 系统：内核架构、专家 Agent、命令、文件记忆和调度自动化",
        "content": """# 多 Agent 操作系统 Skill (Agentic OS)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - agentic-os
> Stars: 239K+ | 许可证: MIT

## 功能
构建持久化多 Agent 操作系统，涵盖内核架构、专家 Agent、斜杠命令、文件记忆、调度自动化和状态管理。

## 架构

### 1. 内核设计
```
┌─────────────────────────────────┐
│           用户接口层             │
├─────────────────────────────────┤
│         命令路由器              │
├─────┬─────┬─────┬──────────────┤
│Agent│Agent│Agent│ Agent...     │
│  A  │  B  │  C  │              │
├─────┴─────┴─────┴──────────────┤
│         共享记忆层              │
│    (文件系统 + 索引)            │
└─────────────────────────────────┘
```

### 2. Agent 定义
```yaml
# agents/researcher.md
name: researcher
role: 信息搜集与分析
trigger:
  - "搜索" / "查找" / "调研"
tools:
  - web_search
  - document_reader
memory:
  - findings/
  - sources/
```

### 3. 文件记忆
```
memory/
├── facts/           # 已知事实
├── decisions/       # 决策记录
├── learnings/       # 学习到的模式
├── context/         # 当前上下文
└── archive/         # 归档
```

### 4. 调度自动化
- 定时任务（每日汇总、周报）
- 事件触发（新数据到达时通知）
- Agent 间协作（研究 → 分析 → 报告）

## 适配说明
- 无需外部数据库
- 基于文件系统实现
- 适合 Claude Code / Cursor 等环境
""",
        "category": "Agent工作流模板",
        "sub_category": "Dify工作流",
        "tags": ["多Agent", "操作系统", "文件记忆", "调度"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 第二批新增：来自 SkillsMP API 更多高星通用 Skill ====================

    # ==================== 4. 程序/测试/运维（第二批） ====================
    {
        "title": "Python 惯用法模式 Skill",
        "desc": "Pythonic 惯用法、PEP 8 标准、类型提示以及构建稳健 Python 应用的最佳实践，来自 239K 星项目",
        "content": """# Python Patterns Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - python-patterns
> Stars: 239K+ | 许可证: MIT

## 核心模式

### 1. Pythonic 惯用法
```python
# 列表推导优于 map/filter
squares = [x**2 for x in range(10)]

# 解包交换
a, b = b, a

# with 语句管理资源
with open('file.txt') as f:
    content = f.read()

# 字典 get 避免 KeyError
count = my_dict.get(key, 0)

# enumerate 替代 range(len())
for i, item in enumerate(items):
    print(f"{i}: {item}")

# 生成器表达式节省内存
total = sum(x * x for x in range(1000000))
```

### 2. 类型提示
```python
from typing import Protocol, TypeAlias
from dataclasses import dataclass

# dataclass 替代冗长 __init__
@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False

# Protocol 实现鸭子类型
class Renderable(Protocol):
    def render(self) -> str: ...

# TypeAlias 提高可读性
UserId: TypeAlias = int | str
```

### 3. 异步模式
```python
import asyncio

# 并发执行
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        return await asyncio.gather(*tasks)

# 信号量控制并发数
async def bounded_fetch(urls, limit=10):
    sem = asyncio.Semaphore(limit)
    async def fetch(url):
        async with sem:
            async with session.get(url) as resp:
                return await resp.text()
    return await asyncio.gather(*[fetch(u) for u in urls])
```

### 4. 项目组织
- 使用 `pyproject.toml` 管理依赖
- `src/` 布局防止导入问题
- 用 `__init__.py` 控制公共 API
- 用 `conftest.py` 共享 fixtures
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["Python", "PEP8", "类型提示", "惯用法"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "React 性能优化 Skill",
        "desc": "来自 Vercel 工程实践的 70+ 条 React/Next.js 性能规则，覆盖 8 个优先级分类",
        "content": """# React Performance Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - react-performance
> 基于 Vercel Engineering React Best Practices | Stars: 239K+ | 许可证: MIT

## 8 个优先级分类

### P0: 消除瀑布流（最高优先级）
- 使用 Server Components 避免客户端数据获取瀑布
- 并行化数据获取（`Promise.all`）
- 避免串行 API 调用

### P1: 减小 Bundle 体积
- 动态导入非首屏组件（`next/dynamic`）
- 使用 `tree-shaking` 友好的导入
- 分析 bundle：`@next/bundle-analyzer`

### P2: 服务端优化
- Server Components 优先
- 流式渲染（`Suspense`）
- ISR/SSG 适当使用

### P3: 客户端数据获取
- 使用 TanStack Query / SWR
- 避免 useEffect 中的 fetch
- 乐观更新改善感知性能

### P4: 减少重渲染
- `React.memo` 包裹纯展示组件
- `useMemo` / `useCallback` 缓存昂贵计算和回调
- 状态下移到需要的组件
- 使用 `key` 强制重挂载替代复杂状态逻辑

### P5: 渲染优化
- 虚拟列表处理大数据集
- 避免内联对象/函数导致的不必要渲染
- 使用 `useTransition` 处理非紧急更新

### P6: JS 微优化
- 防抖/节流高频事件
- Web Worker 处理 CPU 密集任务
- 避免不必要的正则表达式

### P7: 高级模式
- React Compiler（自动记忆化）
- Partial Prerendering
- 选择性 hydration
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["React", "Next.js", "性能优化", "Vercel"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC / Vercel)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "REST API 设计模式 Skill",
        "desc": "REST API 设计模式：资源命名、状态码、分页、过滤、错误响应、版本控制和速率限制",
        "content": """# API Design Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - api-design
> Stars: 239K+ | 许可证: MIT

## 核心模式

### 1. 资源命名
```
✅ 复数名词: /users, /orders, /products
✅ 嵌套不超过2层: /users/{id}/orders
✅ 用连字符: /order-items (非 /orderItems)
❌ 不用动词: /users (非 /getUsers)
❌ 不用缩写: /applications (非 /apps)
```

### 2. 状态码规范
| 场景 | 状态码 |
|------|--------|
| 创建成功 | 201 Created |
| 更新成功 | 200 OK |
| 删除成功 | 204 No Content |
| 参数错误 | 400 Bad Request |
| 未认证 | 401 Unauthorized |
| 无权限 | 403 Forbidden |
| 未找到 | 404 Not Found |
| 冲突 | 409 Conflict |
| 服务器错误 | 500 Internal Server Error |

### 3. 分页
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### 4. 错误响应
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "邮箱格式不正确",
    "details": [
      {"field": "email", "message": "必须是有效的邮箱地址"}
    ]
  }
}
```

### 5. 版本控制
- URL 路径: `/api/v1/users`（推荐）
- Header: `Accept: application/vnd.api+json;version=1`

### 6. 速率限制
```
响应头:
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1625097600
```
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["API设计", "REST", "状态码", "分页"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "后端架构模式 Skill",
        "desc": "Node.js/Express/Next.js 后端架构模式、API 设计、数据库优化和服务端最佳实践",
        "content": """# Backend Patterns Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - backend-patterns
> Stars: 239K+ | 许可证: MIT

## 核心模式

### 1. 项目结构
```
src/
├── routes/          # 路由定义
├── controllers/     # 请求处理
├── services/        # 业务逻辑
├── models/          # 数据模型
├── middleware/       # 中间件
├── utils/           # 工具函数
├── config/          # 配置
└── types/           # TypeScript 类型
```

### 2. 错误处理中间件
```typescript
// 统一错误处理
app.use((err, req, res, next) => {
  const status = err.status || 500;
  const code = err.code || 'INTERNAL_ERROR';
  res.status(status).json({
    error: { code, message: err.message }
  });
});
```

### 3. 验证层
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50),
  age: z.number().int().min(0).max(150).optional(),
});

// 在路由中使用
app.post('/users', validate(CreateUserSchema), createUser);
```

### 4. 数据库模式
- 使用连接池
- 查询参数化防注入
- 事务处理关键操作
- 索引优化高频查询

### 5. 安全清单
- CORS 正确配置
- Helmet 安全头
- 请求体大小限制
- 认证中间件
- 速率限制
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["后端架构", "Node.js", "Express", "最佳实践"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Docker 模式 Skill",
        "desc": "Docker/Docker Compose 模式：镜像构建、容器安全、网络、卷策略和多服务编排",
        "content": """# Docker Patterns Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - docker-patterns
> Stars: 239K+ | 许可证: MIT

## 核心模式

### 1. 多阶段构建
```dockerfile
# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 运行阶段（最小镜像）
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### 2. Docker Compose 开发环境
```yaml
version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app:cached
      - /app/node_modules
    ports:
      - "3000:3000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: pass

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

### 3. 安全最佳实践
- 不以 root 运行（`USER node`）
- 使用 `.dockerignore`
- 固定基础镜像版本
- 扫描漏洞（`docker scout`）
- 最小化层数

### 4. 健康检查
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \\
  CMD curl -f http://localhost:3000/health || exit 1
```
""",
        "category": "程序/测试/运维",
        "sub_category": "运维巡检SOP",
        "tags": ["Docker", "Compose", "容器化", "多阶段构建"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "部署模式 Skill",
        "desc": "部署工作流、CI/CD 流水线、健康检查、回滚策略和生产就绪检查清单",
        "content": """# Deployment Patterns Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - deployment-patterns
> Stars: 239K+ | 许可证: MIT

## 部署策略

### 1. 蓝绿部署
```
环境A (Blue)  ← 当前生产
环境B (Green) ← 部署新版本

1. 部署到 Green
2. 健康检查通过
3. 切换流量到 Green
4. 保留 Blue 作为回滚
```

### 2. 金丝雀发布
```
1. 部署新版本到 5% 流量
2. 监控错误率和延迟
3. 逐步扩大到 25% → 50% → 100%
4. 异常时自动回滚
```

### 3. CI/CD 流水线
```yaml
# GitHub Actions 示例
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: npm run build
      - name: Test
        run: npm test
      - name: Deploy
        run: |
          # 部署脚本
          kubectl set image deployment/app app=$IMAGE_TAG
          kubectl rollout status deployment/app
```

### 4. 生产就绪检查清单
- [ ] 健康检查端点
- [ ] 日志结构化（JSON）
- [ ] 监控和告警
- [ ] 环境变量管理
- [ ] 数据库备份策略
- [ ] 回滚方案
- [ ] HTTPS 配置
- [ ] 速率限制
- [ ] 错误追踪（Sentry等）
""",
        "category": "程序/测试/运维",
        "sub_category": "运维巡检SOP",
        "tags": ["部署", "CI/CD", "蓝绿部署", "金丝雀"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "跨语言错误处理 Skill",
        "desc": "TypeScript/Python/Go 的健壮错误处理模式：类型化错误、错误边界、重试和熔断器",
        "content": """# Error Handling Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - error-handling
> Stars: 239K+ | 许可证: MIT

## 覆盖语言
TypeScript、Python、Go 的通用错误处理模式。

## 核心模式

### 1. 类型化错误（TypeScript）
```typescript
class AppError extends Error {
  constructor(
    public code: string,
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', 404, `${resource} not found`);
  }
}

// 使用
try {
  const user = await findUser(id);
  if (!user) throw new NotFoundError('User');
} catch (e) {
  if (e instanceof AppError) {
    res.status(e.status).json({ error: { code: e.code, message: e.message } });
  }
}
```

### 2. 重试策略
```python
import tenacity

@tenacity.retry(
    retry=tenacity.retry_if_exception_type(ConnectionError),
    wait=tenacity.wait_exponential(multiplier=1, max=60),
    stop=tenacity.stop_after_attempt(3),
)
def fetch_data(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

### 3. 熔断器
```
状态转换：
CLOSED (正常) → OPEN (熔断) → HALF_OPEN (探测) → CLOSED

触发条件：连续失败 N 次
恢复策略：定期探测，成功后恢复
```

### 4. 用户友好的错误消息
- 不说技术细节（"数据库连接失败"）
- 说用户可以做什么（"请稍后重试"）
- 提供替代方案
- 记录详细日志供调试
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["错误处理", "TypeScript", "Python", "重试"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 2. 文案内容创作 / 设计（补充） ====================
    {
        "title": "设计系统构建 Skill",
        "desc": "构建或审计设计系统：无障碍、响应式、主题、组件库、Token，检查视觉一致性",
        "content": """# Design System Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - design-system
> Stars: 239K+ | 许可证: MIT

## 功能
生成或审计设计系统，检查视觉一致性，审查涉及样式的 PR。

## 设计 Token
```json
{
  "color": {
    "primary": { "50": "#eff6ff", "500": "#3b82f6", "900": "#1e3a5f" },
    "neutral": { "50": "#fafafa", "500": "#737373", "900": "#171717" },
    "semantic": { "success": "#22c55e", "warning": "#eab308", "error": "#ef4444" }
  },
  "spacing": { "xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px" },
  "radius": { "sm": "4px", "md": "8px", "lg": "12px", "full": "9999px" },
  "shadow": {
    "sm": "0 1px 2px rgba(0,0,0,0.05)",
    "md": "0 4px 6px rgba(0,0,0,0.07)",
    "lg": "0 10px 15px rgba(0,0,0,0.1)"
  },
  "typography": {
    "fontFamily": { "sans": "Inter, system-ui", "mono": "JetBrains Mono" },
    "fontSize": { "xs": "12px", "sm": "14px", "base": "16px", "lg": "18px", "xl": "24px" }
  }
}
```

## 审计清单
- [ ] 颜色对比度是否满足 WCAG AA？
- [ ] 间距是否使用 Token（非硬编码）？
- [ ] 组件是否支持主题切换？
- [ ] 响应式断点是否一致？
- [ ] 组件 API 是否统一可预测？

## 组件设计原则
- 组合优于配置
- 支持 `asChild` / `as` 属性
- 转发 ref
- 支持 `className` 覆盖
- 文档和 Storybook 故事
""",
        "category": "文案内容创作",
        "sub_category": "海报文案",
        "tags": ["设计系统", "Token", "组件库", "WCAG"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "UI 细节打磨 Skill",
        "desc": "让界面感觉精致的设计工程细节：间距、排版、边框、阴影、动效、点击区域、交互状态",
        "content": """# UI 细节打磨 Skill (Make Interfaces Feel Better)

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - make-interfaces-feel-better
> Stars: 239K+ | 许可证: MIT

## 触发条件
审查或改善 UI 的间距、排版、边框、阴影、动效、点击区域、图标、文本换行和交互状态。

## 打磨清单

### 间距
- 相关元素间距 8-12px，不相关元素 16-24px
- 使用 4px 基准网格
- 列表项之间保持一致间距

### 排版
- 行高 1.5（正文）、1.2（标题）
- 段落最大宽度 65ch（最佳阅读）
- 标题和正文至少 3 级对比

### 边框和阴影
- 边框用浅灰（`#e5e7eb`）而非深灰
- 阴影层级一致（最多 3-4 级）
- 避免同时使用边框和阴影

### 交互状态
- 所有可点击元素有 hover/active/focus 状态
- 按钮点击有即时反馈（< 100ms）
- 加载状态使用骨架屏而非 spinner

### 动效
- 持续时间 150-300ms
- 使用 `ease-out` 进入、`ease-in` 离开
- 减少动效（`prefers-reduced-motion`）

### 点击区域
- 最小点击区域 44x44px
- 按钮之间至少 8px 间距
- 图标按钮加大点击区域

### 文本
- 避免单字换行（`text-wrap: pretty`）
- 长文本提供截断或展开
- 数字使用等宽字体
""",
        "category": "文案内容创作",
        "sub_category": "海报文案",
        "tags": ["UI优化", "设计细节", "交互", "打磨"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 6. 学习科研助手（补充） ====================
    {
        "title": "PaddleOCR 文字识别 Skill",
        "desc": "从图片/扫描件/截图中提取文字，支持中日韩、小字体和手写体，来自 87K 星项目",
        "content": """# PaddleOCR 文字识别 Skill

> 来源: [github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
> Stars: 87K+ | 许可证: Apache 2.0

## 功能
从图片、照片、扫描件、截图或扫描 PDF 中提取文字，返回精确的可机器读取字符串和行级文本及可选的坐标。

## 适用场景
- 图片转文字
- 截图识字
- 扫描件 OCR
- 手写体识别
- 表格文字提取
- 证件信息提取

## 使用方式

### Python API
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')
result = ocr.ocr('image.jpg', cls=True)

for line in result[0]:
    box, (text, confidence) = line
    print(f'{text} ({confidence:.2f})')
```

### 命令行
```bash
# 单张图片
paddleocr --image_dir test.jpg --lang ch

# 目录批量
paddleocr --image_dir ./images/ --lang ch

# 输出为 JSON
paddleocr --image_dir test.jpg --lang ch --output ./result/
```

## 优势
- 中日韩识别精度极高
- 支持小字体和手写体
- 提供检测框坐标
- 支持 GPU 加速
- 开源免费

## 适配说明
- Ollama: 需要配合视觉模型使用
- Dify: 可通过代码节点集成
- 作为 OCR 工具层配合 LLM 使用效果最佳
""",
        "category": "学习科研助手",
        "sub_category": "文献总结",
        "tags": ["OCR", "文字识别", "PaddleOCR", "图片转文字"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "PaddlePaddle",
        "source_type": "开源改编",
        "license": "Apache2.0",
    },

    # ==================== 7. 行业垂直Skill（补充） ====================
    {
        "title": "ML 工程工作流 Skill",
        "desc": "生产级机器学习工程工作流：数据契约、可复现训练、模型评估、部署、监控和回滚",
        "content": """# ML Engineering Workflow Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - mle-workflow
> Stars: 239K+ | 许可证: MIT

## 功能
生产级 ML 工程工作流，超越一次性 notebook。

## 工作流阶段

### 1. 数据契约
```yaml
# data_contract.yaml
features:
  - name: user_age
    type: float
    range: [0, 150]
    nullable: false
  - name: purchase_amount
    type: float
    range: [0, inf]
    nullable: true
    default: 0
```

### 2. 可复现训练
- 固定随机种子
- 版本化数据集（DVC）
- 记录超参数（MLflow）
- 容器化训练环境

### 3. 模型评估
```python
# 评估指标门槛
EVAL_THRESHOLDS = {
    'accuracy': 0.95,
    'precision': 0.90,
    'recall': 0.90,
    'fairness_gap': 0.05,  # 不同群体间差异
}
```

### 4. 部署
- 模型注册表（MLflow / Vertex AI）
- A/B 测试框架
- 渐进式发布
- 回滚机制

### 5. 监控
- 数据漂移检测
- 模型性能衰减告警
- 预测延迟监控
- 定期再训练触发器
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["ML工程", "MLOps", "模型部署", "监控"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "本地 AI Agent 构建 Skill",
        "desc": "构建完全本地运行的 AI Agent：Small Language Model、本地工具、本地 RAG、隐私保护，来自 Microsoft",
        "content": """# 本地 AI Agent 构建 Skill (Local AI Agents)

> 来源: [github.com/microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners)
> Stars: 72K+ | 许可证: MIT

## 功能
构建完全在开发者工作站本地运行的 AI Agent，使用 Microsoft Foundry Local 和 Qwen 函数调用模型。

## 核心组件

### 1. Small Language Model (SLM)
- 使用 Qwen2.5 等小型模型
- 本地推理，无需云端
- OpenAI 兼容端点

### 2. 本地工具
```python
# 沙盒化工具定义
def search_docs(query: str) -> list[dict]:
    \"\"\"搜索本地文档库\"\"\"
    # 只在本地文件系统搜索
    results = local_index.search(query)
    return [{"title": r.title, "snippet": r.text} for r in results]

def run_code(code: str) -> str:
    \"\"\"在沙盒中执行代码\"\"\"
    # 受限环境执行
    return sandbox.execute(code, timeout=5)
```

### 3. 本地 RAG
```python
# 使用 Chroma 本地向量数据库
from chromadb import Client

client = Client()
collection = client.get_or_create_collection("docs")

# 嵌入和查询
results = collection.query(
    query_texts=["如何配置 Docker？"],
    n_results=5
)
```

### 4. 本地 MCP 服务器
- 工具定义在本地
- 数据不出本机
- 隐私保护

### 5. 混合路由
```
简单任务 → 本地 SLM（免费、快速、隐私）
复杂任务 → 云端大模型（高质量）
```

## 权衡
| 维度 | 本地 | 云端 |
|------|------|------|
| 隐私 | 完全保护 | 需信任提供商 |
| 成本 | 硬件投入 | 按量付费 |
| 质量 | 中等 | 最高 |
| 延迟 | 取决于硬件 | 网络延迟 |
""",
        "category": "行业垂直Skill",
        "sub_category": "教育",
        "tags": ["本地AI", "Agent", "隐私", "Microsoft"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "Microsoft",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 8. Agent 工作流模板（补充） ====================
    {
        "title": "Python 测试策略 Skill",
        "desc": "使用 pytest 的 Python 测试策略：TDD 方法、fixtures、mocking、参数化和覆盖率要求",
        "content": """# Python Testing Skill

> 来源: [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) - python-testing
> Stars: 239K+ | 许可证: MIT

## 核心策略

### 1. pytest Fixtures
```python
import pytest

@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.close()

@pytest.fixture
def client(db_session):
    with TestClient(app, db=db_session) as c:
        yield c

# 使用
def test_create_user(client):
    resp = client.post('/users', json={'name': 'Alice'})
    assert resp.status_code == 201
    assert resp.json()['name'] == 'Alice'
```

### 2. 参数化测试
```python
@pytest.mark.parametrize('input,expected', [
    ('hello', 'HELLO'),
    ('World', 'WORLD'),
    ('', ''),
])
def test_uppercase(input, expected):
    assert to_uppercase(input) == expected
```

### 3. Mocking
```python
from unittest.mock import patch, MagicMock

@patch('services.payment_gateway.charge')
def test_order_payment(mock_charge):
    mock_charge.return_value = {'status': 'success'}
    result = process_order(order_id=123)
    assert result['paid'] is True
    mock_charge.assert_called_once_with(123, amount=99.99)
```

### 4. 覆盖率要求
- 新代码最低 80%
- 核心业务逻辑 95%+
- 使用 `pytest-cov`
- CI 中强制覆盖率门槛
""",
        "category": "Agent工作流模板",
        "sub_category": "Ollama角色Skill",
        "tags": ["Python测试", "pytest", "TDD", "Mock"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 第四批新增 (Testing/DevOps/Frontend/ML/CS) ====================
    {
        "title": "E2E测试 Playwright模式 Skill",
        "desc": "来自 ECC 项目的 Playwright E2E 测试完整模式：Page Object Model、配置管理、CI/CD 集成、产物管理、不稳定测试策略",
        "content": """# E2E 测试 Playwright 模式

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/e2e-testing
> 许可证: MIT

Playwright E2E 测试的完整模式与最佳实践。

## 1. Page Object Model (POM)

```
tests/
  pages/
    base.page.ts       # 公共方法
    login.page.ts      # 登录页面对象
    dashboard.page.ts  # 仪表板页面对象
  fixtures/
    test-fixtures.ts   # 自定义 fixtures
```

### POM 核心原则
- 每个页面一个类，封装该页面的元素和操作
- 页面方法返回新的页面对象（导航时）
- 断言放在测试中，不在页面对象中
- 使用 `data-testid` 定位元素，而非 CSS 类名

## 2. 配置管理

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [['html', { open: 'never' }]],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } },
  ],
});
```

## 3. CI/CD 集成

### GitHub Actions 示例
```yaml
- name: Run E2E tests
  run: npx playwright test
- uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: playwright-report
    path: playwright-report/
```

### 关键 CI 实践
- CI 中启用重试（retries: 2）
- 并行执行（workers: 4+）
- 失败时自动上传截图/视频/trace
- 使用 Docker 确保浏览器依赖一致

## 4. 不稳定测试策略

### 常见原因与修复
| 原因 | 修复 |
|------|------|
| 竞态条件 | 使用 `waitFor` 而非固定延时 |
| 动画干扰 | 禁用动画或等待动画完成 |
| 网络波动 | 使用 `page.route()` mock API |
| 数据依赖 | 每个测试独立创建/清理数据 |

### 反模式
```typescript
// 错误：固定等待
await page.waitForTimeout(5000);

// 正确：等待条件
await expect(locator).toBeVisible({ timeout: 10000 });
```

## 5. 测试金字塔

```
        /  E2E  \          ← 少量关键流程
       / 集成测试 \         ← 模块间交互
      /  单元测试   \       ← 大量、快速
```

E2E 只覆盖核心用户旅程（登录、核心操作、支付），不替代单元测试。
""",
        "category": "程序/测试/运维",
        "sub_category": "测试框架",
        "tags": ["Playwright", "E2E测试", "POM", "CI/CD", "自动化测试"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "DevOps发布计划 Skill",
        "desc": "来自 GitHub awesome-copilot 的发布计划生成器：预检清单、分步部署、验证信号、回滚流程、沟通模板",
        "content": """# DevOps 发布计划

> 来源: [awesome-copilot](https://github.com/github/awesome-copilot) (37K+ stars) - skills/devops-rollout-plan
> 许可证: MIT

生成全面的发布计划，覆盖预检、部署、验证、回滚和沟通。

## 1. 预检清单 (Preflight Checks)

### 部署前必须确认
- [ ] 所有测试通过（单元、集成、E2E）
- [ ] 代码审查已完成并合并
- [ ] 数据库迁移脚本已 review 并在 staging 验证
- [ ] 环境变量/配置已更新（所有目标环境）
- [ ] 依赖版本锁定，无意外升级
- [ ] 回滚方案已准备并测试
- [ ] 监控告警规则已就位
- [ ] 相关团队已通知（时间窗口确认）

## 2. 分步部署

### 阶段化发布
```
1. Canary 发布 (5% 流量) → 观察 15min
2. 灰度扩展 (25% 流量) → 观察 30min
3. 半量发布 (50% 流量) → 观察 1h
4. 全量发布 (100% 流量) → 持续监控 24h
```

### 每步检查点
- 错误率 < 0.1%
- P99 延迟无显著退化（<10% 偏差）
- 无新增告警
- 用户反馈无异常

## 3. 验证信号

### 自动化验证
```bash
# 健康检查
curl -f https://api.example.com/health

# 冒烟测试
npm run smoke-test -- --env=production

# 指标对比
compare_metrics --baseline=staging --current=prod
```

### 关键指标
- 请求成功率 (should be ≥ 99.9%)
- 响应时间 P50/P95/P99
- 错误日志频率
- 资源使用率（CPU/Memory/Disk）

## 4. 回滚流程

### 回滚决策标准
- 错误率 > 1% 持续 5 分钟
- P99 延迟 > 2x 基线
- 核心功能不可用
- 数据一致性问题

### 回滚步骤模板
```
1. 宣布事件（严重级别 + 影响范围）
2. 执行回滚命令
3. 验证回滚成功（健康检查 + 冒烟测试）
4. 通知相关方
5. 安排事后复盘（24h 内）
```

## 5. 沟通模板

### 发布通知
```
📦 发布: [项目名] v[版本号]
🕐 时间: [开始时间] - [预计结束]
👤 负责人: [姓名]
📋 变更摘要: [3-5 条关键变更]
🔍 验证状态: [预检完成/灰度中/全量]
📞 紧急联系: [电话/Slack频道]
```
""",
        "category": "程序/测试/运维",
        "sub_category": "运维模式",
        "tags": ["DevOps", "发布计划", "灰度发布", "回滚", "CI/CD"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "github (via awesome-copilot)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "高级DevOps工程 Skill",
        "desc": "全面的 DevOps 工程实践：CI/CD 流水线、基础设施即代码、容器化、云平台（AWS/GCP/Azure）、监控体系",
        "content": """# 高级 DevOps 工程

> 来源: [claude-code-templates](https://github.com/davila7/claude-code-templates) (30K+ stars) - senior-devops
> 许可证: MIT

全面的 DevOps 技能覆盖 CI/CD、基础设施自动化、容器化和云平台。

## 1. CI/CD 流水线设计

### 核心原则
- **快速反馈**: 失败在 <10 分钟内反馈
- **幂等性**: 相同输入产生相同结果
- **增量构建**: 只构建/测试变更的部分
- **环境一致性**: dev/staging/prod 使用相同基础镜像

### 流水线阶段
```
代码提交 → lint + format → 单元测试 → 构建 → 集成测试
→ 安全扫描 → 构建镜像 → 部署 staging → E2E 测试
→ 审批(可选) → 部署 production
```

## 2. 基础设施即代码 (IaC)

### Terraform 最佳实践
```hcl
# 模块化设计
module "vpc" {
  source = "./modules/vpc"
  cidr   = var.vpc_cidr
}

module "eks" {
  source     = "./modules/eks"
  vpc_id     = module.vpc.vpc_id
  node_count = var.eks_nodes
}

# 状态管理
terraform {
  backend "s3" {
    bucket         = "tf-state-prod"
    key            = "infra/terraform.tfstate"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
```

### IaC 原则
- 所有环境通过变量区分，不复制代码
- State 文件远程存储 + 锁定
- 变更必须通过 PR + plan review
- 使用 `terraform fmt` 和 `tflint` 强制规范

## 3. 容器化模式

### Dockerfile 优化
```dockerfile
# 多阶段构建
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine AS runtime
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER app
EXPOSE 3000
HEALTHCHECK CMD wget -q --spider http://localhost:3000/health || exit 1
```

### 容器安全
- 非 root 用户运行
- 最小基础镜像（alpine/distroless）
- 扫描漏洞（trivy/snyk）
- 不存储密钥在镜像中

## 4. 监控与可观测性

### 三大支柱
| 支柱 | 工具 | 用途 |
|------|------|------|
| Metrics | Prometheus + Grafana | 系统指标、告警 |
| Logs | ELK / Loki | 集中日志 |
| Traces | Jaeger / Tempo | 分布式追踪 |

### 告警规则
- 基于 SLO 告警（错误预算），而非简单阈值
- 分级：P1 立即响应 / P2 1h 内 / P3 下个工作日
- 每个告警必须有 runbook
""",
        "category": "程序/测试/运维",
        "sub_category": "运维模式",
        "tags": ["DevOps", "CI/CD", "Terraform", "Docker", "Kubernetes", "监控"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "davila7",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "事件响应指挥官 Skill",
        "desc": "来自 alirezarezvani/claude-skills 的完整事件响应框架：严重级别分类、时间线重建、结构化事后分析，SRE 实战经验",
        "content": """# 事件响应指挥官

> 来源: [claude-skills](https://github.com/alirezarezvani/claude-skills) (24K+ stars) - incident-commander
> 许可证: MIT

从检测到解决再到事后复盘的完整事件响应框架。

## 1. 严重级别分类

| 级别 | 定义 | 响应时间 | 示例 |
|------|------|----------|------|
| SEV-1 | 核心业务完全不可用 | 立即 | 支付系统宕机、数据泄露 |
| SEV-2 | 核心功能严重降级 | 15 分钟 | 50% 用户无法登录 |
| SEV-3 | 非核心功能异常 | 1 小时 | 报表导出失败 |
| SEV-4 | 轻微问题 | 下个工作日 | UI 显示异常 |

## 2. 事件响应流程

### Phase 1: 检测与宣布 (0-5 min)
```
1. 确认事件（告警验证，排除误报）
2. 分配严重级别
3. 创建事件频道（Slack/Teams）
4. 指定事件指挥官 (IC)
5. 通知相关干系人
```

### Phase 2: 调查与缓解 (5-30 min)
```
1. 收集证据（日志、指标、最近变更）
2. 确定影响范围
3. 优先缓解（恢复服务 > 定位根因）
4. 执行缓解操作（回滚/扩容/切换）
5. 验证缓解效果
```

### Phase 3: 根因分析 (30 min - 24h)
```
1. 重建时间线
2. 5-Why 分析
3. 确认根因
4. 制定永久修复方案
```

### Phase 4: 事后复盘 (24-72h)
```
1. 编写事后报告 (Postmortem)
2. 召开复盘会议（无责文化）
3. 产出 Action Items
4. 跟踪完成进度
```

## 3. 事后报告模板

```markdown
# 事件事后报告

## 概要
- 日期: YYYY-MM-DD
- 持续时间: Xh Ym
- 严重级别: SEV-N
- 影响: [用户数/收入/功能]
- IC: [姓名]

## 时间线
| 时间 | 事件 |
|------|------|
| HH:MM | 告警触发 |
| HH:MM | 开始调查 |
| HH:MM | 执行回滚 |
| HH:MM | 服务恢复 |

## 根因
[5-Why 分析结果]

## 做得好的
- [列出]

## 需要改进的
- [列出]

## Action Items
| 任务 | 负责人 | 截止日期 | 状态 |
|------|--------|----------|------|
| [具体任务] | [姓名] | [日期] | TODO |
```

## 4. On-Call 最佳实践
- 轮班不超过 1 周
- 明确的升级路径（L1 → L2 → L3）
- 每个告警必须有 runbook
- 定期演练（Game Day）
""",
        "category": "程序/测试/运维",
        "sub_category": "运维模式",
        "tags": ["事件响应", "SRE", "Postmortem", "On-Call", "告警"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "alirezarezvani",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "前端无障碍设计 Skill",
        "desc": "来自 ECC 项目的 React/Next.js 无障碍设计模式：语义化 HTML、ARIA 属性、表单标注、键盘导航、焦点管理、屏幕阅读器支持",
        "content": """# 前端无障碍设计 (A11y)

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/frontend-a11y
> 许可证: MIT

React 和 Next.js 的无障碍设计模式。

## 1. 语义化 HTML

### 原则
- 用对元素比加 ARIA 更重要
- `<button>` 优于 `<div onClick>`
- `<nav>`, `<main>`, `<article>`, `<aside>` 优于全用 `<div>`
- 标题层级 h1→h2→h3 不跳级

### 反模式
```jsx
// 错误
<div onClick={handleClick} className="btn">提交</div>

// 正确
<button type="button" onClick={handleClick}>提交</button>
```

## 2. ARIA 属性

### 常用 ARIA
```jsx
// 加载状态
<div role="status" aria-live="polite">
  {loading ? '加载中...' : content}
</div>

// 模态框
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">确认删除</h2>
</div>

// 错误提示
<input aria-invalid={!!error} aria-describedby="error-msg" />
<span id="error-msg" role="alert">{error}</span>
```

### ARIA 规则
1. 能用原生语义就不用 ARIA
2. `aria-label` 给无文字的可交互元素
3. `aria-live` 给动态更新区域
4. 不要 `role="button"` 在真正的 `<button>` 上

## 3. 键盘导航

### 必须支持
- `Tab` / `Shift+Tab` - 在可交互元素间移动
- `Enter` / `Space` - 激活按钮/链接
- `Escape` - 关闭弹窗/模态
- `Arrow keys` - 在列表/菜单中移动

### 焦点管理
```jsx
// 模态框打开时锁定焦点
useEffect(() => {
  const previousFocus = document.activeElement;
  modalRef.current?.focus();
  return () => previousFocus?.focus();
}, []);

// 焦点陷阱（模态框内循环）
function trapFocus(container) {
  const focusable = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  // Tab 到最后一个 → 回到第一个
}
```

## 4. 表单无障碍

```jsx
<form>
  <label htmlFor="email">邮箱地址</label>
  <input
    id="email"
    type="email"
    required
    aria-required="true"
    aria-describedby="email-hint"
    autoComplete="email"
  />
  <span id="email-hint">我们不会分享您的邮箱</span>
</form>
```

## 5. 测试工具
- **axe-core**: 自动化 a11y 测试
- **Lighthouse**: Chrome DevTools 内置审计
- **VoiceOver / NVDA**: 屏幕阅读器手动测试
- **键盘测试**: 拔掉鼠标，只用键盘操作
""",
        "category": "程序/测试/运维",
        "sub_category": "前端开发",
        "tags": ["无障碍", "A11y", "ARIA", "键盘导航", "React", "语义化HTML"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "前端设计方向 Skill",
        "desc": "来自 ECC 项目的前端设计判断力：美学原则、设计语言一致性、产品级 UI 决策，帮非设计师做出专业级界面",
        "content": """# 前端设计方向

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/frontend-design-direction
> 许可证: MIT

为生产级 UI 工作设定前端设计方向，帮助开发者做出专业的产品级设计判断。

## 1. 设计系统基础

### 间距系统
```css
/* 使用 4px 基准的间距比例 */
--space-1: 4px;   /* 紧凑元素内间距 */
--space-2: 8px;   /* 相关元素间 */
--space-3: 12px;  /* 小组件内间距 */
--space-4: 16px;  /* 标准间距 */
--space-6: 24px;  /* 区块内间距 */
--space-8: 32px;  /* 区块间间距 */
--space-12: 48px; /* 段落间距 */
--space-16: 64px; /* 页面区域间距 */
```

### 排版比例
```css
--text-xs: 0.75rem;   /* 12px - 辅助文字 */
--text-sm: 0.875rem;  /* 14px - 次要文字 */
--text-base: 1rem;    /* 16px - 正文 */
--text-lg: 1.125rem;  /* 18px - 小标题 */
--text-xl: 1.25rem;   /* 20px - 标题 */
--text-2xl: 1.5rem;   /* 24px - 页标题 */
--text-3xl: 1.875rem; /* 30px - 大标题 */
```

## 2. 颜色使用原则

### 60-30-10 法则
- **60%** 主色调（通常是中性色：白/灰/深色背景）
- **30%** 辅助色（品牌色的淡色版本）
- **10%** 强调色（CTA 按钮、重要操作）

### 语义色
- 成功: 绿色系 (#10B981)
- 警告: 橙色系 (#F59E0B)
- 错误: 红色系 (#EF4444)
- 信息: 蓝色系 (#3B82F6)

## 3. 组件设计决策

### 按钮层级
1. **Primary**: 实心填充，每屏最多 1 个
2. **Secondary**: 描边/浅色底，辅助操作
3. **Ghost**: 无边框，低优先级操作
4. **Danger**: 红色，破坏性操作

### 卡片设计
- 圆角统一（8px 或 12px）
- 阴影层级：static < raised < overlay
- 内间距 ≥ 16px
- 内容层级清晰（标题→描述→操作）

## 4. 动效原则

### 时间参考
- 微交互（hover/focus）: 100-200ms
- 展开/折叠: 200-300ms
- 页面过渡: 300-500ms
- 复杂动画: 500-1000ms

### 缓动函数
- 进入: `ease-out`（快入慢出）
- 离开: `ease-in`（慢入快出）
- 移动: `ease-in-out`（两端慢中间快）

## 5. 响应式设计

### 断点策略
```css
/* Mobile First */
@media (min-width: 640px)  { /* sm: 平板竖屏 */ }
@media (min-width: 768px)  { /* md: 平板横屏 */ }
@media (min-width: 1024px) { /* lg: 笔记本 */ }
@media (min-width: 1280px) { /* xl: 桌面 */ }
```

### 关键原则
- 内容优先，装饰其次
- 触摸目标 ≥ 44x44px
- 文字最小 14px（移动端）
- 不要隐藏关键信息在 hover 中
""",
        "category": "程序/测试/运维",
        "sub_category": "前端开发",
        "tags": ["设计系统", "UI设计", "CSS", "响应式", "排版", "色彩"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "ML落地实战手册 Skill",
        "desc": "来自 ECC 的 AI/ML 落地方法论：给现有非 ML 代码库添加机器学习能力的完整路径，从问题定义到基线模型集成",
        "content": """# ML 落地实战手册

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/ml-adoption-playbook
> 许可证: MIT

给现有非 ML 代码库添加机器学习能力的端到端方法论。

## 1. 问题定义

### 从业务问题到 ML 问题
```
业务问题: "用户流失率太高"
  ↓
ML 问题: "预测哪些用户未来 30 天可能流失"
  ↓
任务类型: 二分类 (流失/留存)
  ↓
评估指标: Recall@80% precision (宁可多挽留，不要漏掉)
```

### 可行性检查清单
- [ ] 有足够的标注数据吗？（最低 1000+ 样本）
- [ ] 特征能从现有系统获取吗？
- [ ] ML 真的比规则引擎好吗？（先试规则）
- [ ] 预测结果能集成到业务流程吗？
- [ ] 能接受多大的错误率？

## 2. 数据准备

### 数据质量 > 数据数量
```python
# 数据质量检查
import pandas as pd

df = pd.read_csv('data.csv')

# 1. 缺失值分析
missing = df.isnull().sum() / len(df) * 100
print(missing[missing > 0].sort_values(ascending=False))

# 2. 类别不平衡检查
print(df['target'].value_counts(normalize=True))
# 如果 < 10% 或 > 90%，需要特殊处理

# 3. 数据泄露检查
# 确保特征不包含未来信息！
```

### 特征工程原则
1. 从领域知识出发，不要盲目挖掘
2. 先做简单特征，再逐步复杂
3. 每个特征都要能解释其业务含义
4. 记录所有特征变换（可复现）

## 3. 架构解耦

### ML 服务与业务代码分离
```
业务代码 (Python/Node/Go)
    ↓ HTTP API / gRPC
ML 服务 (Python + FastAPI)
    ↓
模型文件 (model.pkl / ONNX)
    ↓
特征存储 (Redis / Feature Store)
```

### 集成模式
```python
# 推荐：通过 API 调用
async def get_churn_prediction(user_id: str) -> float:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://ml-service:8001/predict",
            json={"user_id": user_id, "features": await get_features(user_id)}
        )
        return resp.json()["probability"]

# 不推荐：直接在业务代码中加载模型
```

## 4. 基线模型

### 先跑最简单的模型
```python
# Step 1: 规则基线
def predict_by_rules(features):
    return 1 if features['days_since_login'] > 30 else 0

# Step 2: 逻辑回归基线
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 3: 才考虑复杂模型（XGBoost/LightGBM）
```

### 模型选择决策树
```
数据量 < 10K → 逻辑回归 / SVM
数据量 10K-100K → XGBoost / LightGBM
数据量 > 100K + 非结构化 → 深度学习
表格数据 → 永远先试 XGBoost
```

## 5. 上线检查

- [ ] 离线指标达标（AUC / F1 / RMSE）
- [ ] 推理延迟满足要求（<100ms?）
- [ ] 有 fallback（模型挂了用规则兜底）
- [ ] 有监控（预测分布漂移检测）
- [ ] A/B 测试方案就绪
""",
        "category": "学习科研助手",
        "sub_category": "AI/ML工具",
        "tags": ["机器学习", "ML落地", "特征工程", "模型集成", "FastAPI"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "推荐系统流水线 Skill",
        "desc": "来自 ECC 的推荐系统架构：六阶段 Source-Hydrator-Filter-Scorer-Selector-SideEffect 框架，适用于任何'为用户选 Top-K'的场景",
        "content": """# 推荐系统流水线架构

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/recsys-pipeline-architect
> 许可证: MIT

使用六阶段框架设计可组合的推荐、排序和 Feed 流水线。

## 1. 六阶段框架

```
Source → Hydrator → Filter → Scorer → Selector → SideEffect
  来源      数据注入     过滤      打分      选择       副作用
```

适用于任何"为 (用户, 场景) 选出 Top-K 项"的系统：社交 Feed、内容推荐、搜索重排、任务优先级、通知分拣。

## 2. 各阶段详解

### Stage 1: Source（来源）
从哪获取候选集？
```python
# 多来源合并
sources = {
    "following": get_following_feed(user_id),      # 关注的人
    "trending": get_trending_content(),             # 热门
    "similar": get_similar_to_recent(user_id),     # 相似推荐
    "saved": get_related_to_saved(user_id),        # 收藏关联
}
```

### Stage 2: Hydrator（数据注入）
补充打分所需的特征数据
```python
def hydrate(items, user_id):
    for item in items:
        item.user_interaction = get_interaction(user_id, item.id)
        item.freshness_score = calc_freshness(item.created_at)
        item.social_proof = get_social_proof(user_id, item.id)
    return items
```

### Stage 3: Filter（过滤）
硬性规则过滤
```python
def hard_filter(items, user_id):
    return [
        item for item in items
        if not is_blocked(user_id, item.author_id)  # 屏蔽
        and not is_already_seen(user_id, item.id)    # 已看
        and item.status == 'published'               # 状态
        and not is_nsfw(item) or user.allow_nsfw     # 内容策略
    ]
```

### Stage 4: Scorer（打分）
多信号加权打分
```python
def score(item, user):
    scores = {
        'relevance': model_predict(user, item),     # 相关性模型
        'freshness': freshness_score(item),          # 新鲜度
        'quality': quality_score(item),              # 内容质量
        'social': social_score(user, item),          # 社交信号
        'diversity': diversity_score(user, item),    # 多样性
    }
    return sum(w * s for w, s in zip(weights, scores.values()))
```

### Stage 5: Selector（选择）
最终选择 + 排序约束
```python
def select(scored_items, k=20):
    # 多样性约束：同类别最多 30%
    selected = []
    category_count = {}
    for item in sorted(scored_items, key=lambda x: -x.score):
        cat = item.category
        if category_count.get(cat, 0) < k * 0.3:
            selected.append(item)
            category_count[cat] = category_count.get(cat, 0) + 1
        if len(selected) >= k:
            break
    return selected
```

### Stage 6: SideEffect（副作用）
推荐结果的后续处理
```python
async def side_effects(selected, user_id):
    await log_recommendations(selected, user_id)     # 日志
    await update_impressions(selected)               # 曝光记录
    await trigger_analytics(selected)                # 数据分析
```

## 3. 应用场景

| 场景 | Source | Scorer 重点 |
|------|--------|-------------|
| 社交 Feed | 关注 + 热门 | 社交信号 + 新鲜度 |
| 电商推荐 | 浏览 + 相似 | 协同过滤 + 转化概率 |
| 搜索重排 | 搜索结果 | 相关性 + 点击率 |
| 通知排序 | 待推送列表 | 紧急度 + 用户偏好 |
""",
        "category": "学习科研助手",
        "sub_category": "AI/ML工具",
        "tags": ["推荐系统", "Feed流", "排序算法", "架构设计", "机器学习"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "NetworkX图网络分析 Skill",
        "desc": "来自 K-Dense-AI 科学计算 Skill 库：用 Python NetworkX 创建、分析和可视化复杂网络与图结构，覆盖图算法、社区检测、合成网络生成",
        "content": """# NetworkX 图网络分析

> 来源: [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) (33K+ stars)
> 许可证: BSD-3-Clause

用 Python NetworkX 创建、分析和可视化复杂网络与图。

## 1. 基础操作

```python
import networkx as nx

# 创建图
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])

# 基本属性
print(f"节点数: {G.number_of_nodes()}")
print(f"边数: {G.number_of_edges()}")
print(f"密度: {nx.density(G):.3f}")
print(f"是否连通: {nx.is_connected(G)}")
```

## 2. 图算法

### 最短路径
```python
# 单源最短路径
paths = nx.single_source_shortest_path(G, 1)
lengths = nx.single_source_shortest_path_length(G, 1)

# 所有节点对
all_paths = dict(nx.all_pairs_shortest_path(G))

# 带权重
G_weighted = G.copy()
for u, v in G.edges():
    G_weighted[u][v]['weight'] = 1.0 / G.degree(u)
paths_w = nx.dijkstra_path(G_weighted, 1, 5)
```

### 中心性分析
```python
# 度中心性
degree_cent = nx.degree_centrality(G)

# 介数中心性（关键枢纽节点）
betweenness = nx.betweenness_centrality(G)

# 接近中心性
closeness = nx.closeness_centrality(G)

# PageRank
pagerank = nx.pagerank(G, alpha=0.85)

# 找到最重要的节点
top_node = max(pagerank, key=pagerank.get)
```

### 社区检测
```python
# Girvan-Newman 算法
communities = nx.community.girvan_newman(G)
top_level_communities = next(communities)

# Louvain 方法（需要 networkx 3.x+）
communities = nx.community.louvain_communities(G, seed=42)

# 可视化社区
import matplotlib.pyplot as plt
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=[list(communities).index(
    next(c for c in communities if n in c)) for n in G.nodes()],
    cmap=plt.cm.Set2, with_labels=True)
plt.show()
```

## 3. 合成网络生成

```python
# 随机图 (Erdos-Renyi)
G_random = nx.erdos_renyi_graph(100, 0.1, seed=42)

# 无标度网络 (Barabasi-Albert)
G_scale_free = nx.barabasi_albert_graph(100, 3, seed=42)

# 小世界网络 (Watts-Strogatz)
G_small_world = nx.watts_strogatz_graph(100, 6, 0.1, seed=42)

# 比较属性
for name, G_test in [("Random", G_random), ("Scale-free", G_scale_free), ("Small-world", G_small_world)]:
    print(f"{name}: 平均度={sum(dict(G_test.degree()).values())/G_test.number_of_nodes():.1f}, "
          f"聚类系数={nx.average_clustering(G_test):.3f}")
```

## 4. 实际应用场景

| 场景 | 节点 | 边 | 分析目标 |
|------|------|-----|----------|
| 社交网络 | 用户 | 关注/好友 | 社区检测、KOL 识别 |
| 知识图谱 | 概念 | 关系 | 路径推理、影响力传播 |
| 生物网络 | 蛋白质/基因 | 相互作用 | 关键靶点发现 |
| 交通网络 | 站点 | 线路 | 最短路径、瓶颈分析 |
""",
        "category": "学习科研助手",
        "sub_category": "科学计算",
        "tags": ["NetworkX", "图算法", "社区检测", "社交网络", "Python"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "K-Dense-AI",
        "source_type": "开源改编",
        "license": "BSD-3-Clause",
    },
    {
        "title": "Scikit-learn机器学习 Skill",
        "desc": "来自 K-Dense-AI 科学计算 Skill 库：scikit-learn 全面参考，监督学习、无监督学习、模型评估、超参调优、ML 流水线最佳实践",
        "content": """# Scikit-learn 机器学习

> 来源: [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) (33K+ stars)
> 许可证: BSD-3-Clause

Python scikit-learn 机器学习全面参考。

## 1. 监督学习

### 分类
```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 构建流水线
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 交叉验证
scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring='f1')
print(f"F1: {scores.mean():.3f} (+/- {scores.std():.3f})")

# 超参调优
param_grid = {
    'clf__n_estimators': [100, 200, 500],
    'clf__max_depth': [3, 5, 7, None],
    'clf__min_samples_split': [2, 5, 10],
}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='f1', n_jobs=-1)
grid.fit(X_train, y_train)
print(f"最佳参数: {grid.best_params_}")
```

### 回归
```python
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

model = HistGradientBoostingRegressor(max_iter=200)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.3f}")
print(f"R2: {r2_score(y_test, y_pred):.3f}")
```

## 2. 无监督学习

### 聚类
```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 肘部法确定 K
inertias = []
sil_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
    sil_scores.append(silhouette_score(X, kmeans.labels_))

best_k = range(2, 11)[sil_scores.index(max(sil_scores))]
```

### 降维
```python
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# PCA (快速，全局结构)
pca = PCA(n_components=0.95)  # 保留 95% 方差
X_pca = pca.fit_transform(X_scaled)
print(f"降维到 {pca.n_components_} 维")

# t-SNE (慢，局部结构/可视化)
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)
```

## 3. 模型评估

### 分类指标
```python
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, precision_recall_curve
)

print(classification_report(y_test, y_pred))
print(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.3f}")
```

### 防止数据泄露
```python
# 正确：先分割再预处理
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# 用 Pipeline 确保预处理只在训练集上 fit
pipe = Pipeline([
    ('scaler', StandardScaler()),  # 只在 X_train 上 fit
    ('clf', LogisticRegression())
])
pipe.fit(X_train, y_train)  # scaler 只 fit 训练集
score = pipe.score(X_test, y_test)  # transform 测试集
```

## 4. 模型选择指南

| 数据类型 | 首选 | 备选 |
|----------|------|------|
| 表格/结构化 | XGBoost/LightGBM | RandomForest, LogisticRegression |
| 小样本 (<1K) | SVM + RBF | LogisticRegression + L2 |
| 高维稀疏 | LogisticRegression | LinearSVM |
| 需要可解释 | LogisticRegression | DecisionTree, Rule-based |
| 快速原型 | HistGradientBoosting | RandomForest |
""",
        "category": "学习科研助手",
        "sub_category": "AI/ML工具",
        "tags": ["scikit-learn", "机器学习", "分类", "聚类", "Pipeline", "Python"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "K-Dense-AI",
        "source_type": "开源改编",
        "license": "BSD-3-Clause",
    },
    {
        "title": "跨项目编码规范 Skill",
        "desc": "来自 ECC 项目的跨项目通用编码约定：命名规范、可读性原则、不可变性、代码质量审查基线，适用于任何语言和框架",
        "content": """# 跨项目编码规范

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/coding-standards
> 许可证: MIT

跨项目通用的编码约定基线，关注命名、可读性和代码质量。

## 1. 命名规范

### 核心原则
- **名字要揭示意图**：`calculateMonthlyRevenue` 而非 `calc`
- **避免缩写**：`repository` 而非 `repo`（除非是团队共识）
- **布尔值用 is/has/can 开头**：`isActive`, `hasPermission`, `canEdit`
- **函数用动词开头**：`get`, `set`, `create`, `update`, `delete`, `validate`

### 命名模式
```
变量/属性: 名词 (user, orderCount, maxRetries)
函数/方法: 动词+名词 (getUserById, calculateTotal)
布尔值: is/has/can + 形容词 (isValid, hasActiveSession)
常量: UPPER_SNAKE_CASE (MAX_RETRY_COUNT, API_BASE_URL)
枚举值: PascalCase (OrderStatus.Pending, Color.Red)
```

## 2. 可读性原则

### 函数设计
- **单一职责**: 一个函数只做一件事
- **最多 3 个参数**: 超过就用对象/结构体
- **函数体不超过 20 行**: 超过就拆分
- **提前返回减少嵌套**

```python
# 错误：深层嵌套
def process(user):
    if user:
        if user.is_active:
            if user.has_permission:
                return do_something(user)
    return None

# 正确：提前返回
def process(user):
    if not user or not user.is_active or not user.has_permission:
        return None
    return do_something(user)
```

### 注释原则
- 注释解释 **为什么**，不是 **是什么**
- 好的命名胜过注释
- 公共 API 必须有文档注释
- TODO 必须附带负责人和日期

## 3. 不可变性优先

```python
# 错误：修改输入参数
def sort_items(items):
    items.sort()  # 修改了原始列表
    return items

# 正确：返回新对象
def sorted_items(items):
    return sorted(items)  # 不修改原始列表

# JavaScript
// 错误
function updateConfig(config, key, value) {
    config[key] = value;
    return config;
}

// 正确
function updateConfig(config, key, value) {
    return { ...config, [key]: value };
}
```

## 4. 代码审查清单

### 每次 PR 检查
- [ ] 命名清晰且一致
- [ ] 无重复代码（DRY）
- [ ] 错误处理完整
- [ ] 无硬编码的魔法数字/字符串
- [ ] 新增公共函数有文档
- [ ] 无不必要的注释（代码本身应该够清晰）
- [ ] 测试覆盖新增逻辑
- [ ] 无安全隐患（SQL 注入、XSS 等）

## 5. 错误处理

### 原则
- 只捕获你能处理的异常
- 用自定义错误类型区分业务错误
- 永远不要吞掉错误（空 catch）
- 提供有意义的错误信息

```python
# 错误
try:
    process(data)
except:
    pass

# 正确
try:
    process(data)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    return ErrorResponse(code=400, message=str(e))
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="服务暂时不可用")
```
""",
        "category": "程序/测试/运维",
        "sub_category": "编码规范",
        "tags": ["编码规范", "命名", "可读性", "代码审查", "最佳实践"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "浏览器视觉QA Skill",
        "desc": "来自 ECC 项目的浏览器自动化视觉测试：部署后自动进行 UI 交互验证和视觉回归检测",
        "content": """# 浏览器视觉 QA

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/browser-qa
> 许可证: MIT

部署后使用浏览器自动化进行视觉测试和 UI 交互验证。

## 1. 视觉测试策略

### 三层视觉验证
```
1. 像素级对比 (Pixel Diff)
   - 截图与基线对比
   - 检测意外 UI 变化
   - 工具: Playwright screenshot + pixelmatch

2. 组件级验证 (Component Snapshot)
   - 单个组件的截图
   - 不同状态（默认/hover/disabled/loading）
   - 不同视口尺寸

3. 交互验证 (Interaction Flow)
   - 点击、输入、导航的视觉反馈
   - 动画/过渡效果
   - 响应式布局
```

## 2. Playwright 视觉测试

```python
from playwright.sync_api import sync_playwright

def visual_regression_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        # 全页截图对比
        page.goto("https://staging.example.com")
        page.screenshot(path="screenshots/current.png")

        # 元素级截图
        header = page.locator("header")
        header.screenshot(path="screenshots/header-current.png")

        browser.close()

    # 像素对比
    # 使用 pixelmatch 或 resemble.js
    # 差异 > 阈值 → 测试失败
```

## 3. 交互验证

```python
def verify_interactions(page):
    # 按钮点击反馈
    btn = page.locator("button.submit")
    btn.click()
    expect(page.locator(".success-message")).to_be_visible()

    # 表单验证提示
    page.fill("input[email]", "invalid")
    page.click("button[type=submit]")
    expect(page.locator(".error-text")).to_contain_text("请输入有效邮箱")

    # 导航菜单
    page.hover("nav .menu-item")
    expect(page.locator(".dropdown")).to_be_visible()

    # 加载状态
    page.click("button.load-more")
    expect(page.locator(".spinner")).to_be_visible()
    expect(page.locator(".new-items")).to_be_visible(timeout=10000)
```

## 4. 响应式视觉检查

```python
VIEWPORTS = {
    "mobile": {"width": 375, "height": 667},
    "tablet": {"width": 768, "height": 1024},
    "desktop": {"width": 1440, "height": 900},
}

for name, viewport in VIEWPORTS.items():
    page.set_viewport_size(viewport)
    page.goto(url)
    page.screenshot(path=f"screenshots/{name}-full.png", full_page=True)
```

## 5. CI 集成

### 自动化视觉回归
```yaml
# GitHub Actions
- name: Visual Regression Tests
  run: |
    npm run build
    npx playwright test --config=visual.config.ts
  
- name: Upload Diffs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: visual-diffs
    path: test-results/**/*-diff.png
```

### 基线管理
- 基线截图存在 Git LFS 或专用存储
- 每次 UI 变更需更新基线（PR 中附带新基线）
- 允许 1-2% 像素差异（抗锯齿/字体渲染）
""",
        "category": "程序/测试/运维",
        "sub_category": "测试框架",
        "tags": ["视觉测试", "Playwright", "UI测试", "回归测试", "浏览器自动化"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 第五批新增 (Architecture/Decision-Motion/Verification/Industry) ====================
    {
        "title": "六边形架构模式 Skill",
        "desc": "来自 ECC 的 Ports & Adapters 架构设计：领域边界、依赖反转、可测试用例编排，支持 TypeScript/Java/Kotlin/Go",
        "content": """# 六边形架构模式 (Ports & Adapters)

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/hexagonal-architecture
> 许可证: MIT

设计、实现和重构 Ports & Adapters 系统，保持清晰的领域边界和依赖反转。

## 1. 核心结构

```
         ┌─────────────────────────────┐
         │        Adapters (外)        │
         │  ┌───────────────────────┐  │
         │  │    Ports (接口层)     │  │
         │  │  ┌─────────────────┐  │  │
  HTTP   │  │  │                 │  │  │  DB
  REST ──────→ │  │   Domain Core   │  │ ←──── Repository
  API   │  │  │   (业务逻辑)    │  │  │  │
         │  │  └─────────────────┘  │  │
         │  └───────────────────────┘  │
         └─────────────────────────────┘
```

## 2. 层级定义

### Domain Core (领域核心)
- 纯业务逻辑，无框架依赖
- 不 import 任何外部库
- 包含：实体、值对象、用例、领域事件

```python
# domain/entities.py
class Order:
    def __init__(self, id, items, customer_id):
        self.id = id
        self.items = items
        self.customer_id = customer_id
        self.status = 'pending'

    def total(self):
        return sum(item.price * item.quantity for item in self.items)

    def confirm(self):
        if self.status != 'pending':
            raise OrderStateError(f'Cannot confirm order in {self.status} state')
        self.status = 'confirmed'

# domain/use_cases.py
class CreateOrder:
    def __init__(self, order_repo: OrderRepository, notifier: OrderNotifier):
        self.order_repo = order_repo
        self.notifier = notifier

    def execute(self, customer_id, items):
        order = Order(id=new_id(), items=items, customer_id=customer_id)
        self.order_repo.save(order)
        self.notifier.notify_created(order)
        return order
```

### Ports (端口/接口)
```python
# domain/ports.py
from typing import Protocol

class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def find_by_id(self, id: str) -> Order | None: ...

class OrderNotifier(Protocol):
    def notify_created(self, order: Order) -> None: ...

class PaymentGateway(Protocol):
    def charge(self, amount: float, token: str) -> PaymentResult: ...
```

### Adapters (适配器)
```python
# adapters/http_controller.py (Driving Adapter)
from fastapi import APIRouter

class OrderController:
    def __init__(self, create_order: CreateOrder):
        self.create_order = create_order

    def setup_routes(self, router: APIRouter):
        @router.post('/orders')
        async def create(req: CreateOrderRequest):
            order = self.create_order.execute(req.customer_id, req.items)
            return {"order_id": order.id}

# adapters/postgres_repo.py (Driven Adapter)
class PostgresOrderRepository:
    def __init__(self, pool):
        self.pool = pool

    async def save(self, order):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO orders (id, customer_id, status) VALUES ($1, $2, $3)",
                order.id, order.customer_id, order.status
            )
```

## 3. 依赖规则

```
Domain Core ← 不依赖任何外部层
Ports ← 定义在 Domain，由 Adapters 实现
Driving Adapters → 调用 Use Cases → 通过 Ports 操作 Domain
Driven Adapters ← 实现 Ports ← 被 Use Cases 调用
```

## 4. 何时使用

| 场景 | 适合? |
|------|--------|
| 业务逻辑复杂且频繁变化 | 非常适合 |
| 需要多种数据源/外部服务 | 非常适合 |
| 需要高测试覆盖率 | 非常适合 |
| 简单 CRUD 应用 | 过度设计 |
| 原型/一次性脚本 | 不需要 |
""",
        "category": "程序/测试/运维",
        "sub_category": "架构设计",
        "tags": ["六边形架构", "Ports-Adapters", "DDD", "依赖反转", "Clean Architecture"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "正则 vs LLM 决策框架 Skill",
        "desc": "来自 ECC 的文本解析决策框架：何时用正则、何时用 LLM，从简单到复杂的渐进式策略",
        "content": """# 正则 vs LLM 结构化文本解析

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/regex-vs-llm-structured-text
> 许可证: MIT

解析结构化文本时的技术选择决策框架。

## 1. 决策树

```
文本格式是否固定？
├── 是 → 用正则表达式
│   示例: 日志行、日期、邮箱、URL
│
└── 否 → 文本是否有明确的模式但格式多变？
    ├── 是 → 正则 + 后处理
    │   示例: 地址解析、电话号码
    │
    └── 否 → 能否用规则/语法解析？
        ├── 是 → 用解析器 (JSON/YAML/CSV)
        │
        └── 否 → 用 LLM
            示例: 自然语言提取、模糊信息抽取
```

## 2. 正则优先原则

**始终从正则开始**，只在以下情况升级到 LLM：
1. 正则超过 5 个捕获组且难以维护
2. 输入格式变化太大，正则覆盖率 < 80%
3. 需要语义理解（如区分"苹果"是公司还是水果）

## 3. 混合策略

```python
import re
from openai import OpenAI

def parse_text(text: str) -> dict:
    # Step 1: 尝试正则
    pattern = r'(\d{4}-\d{2}-\d{2})\s+(\w+)\s+(.+)'
    match = re.match(pattern, text)
    if match:
        return {
            'date': match.group(1),
            'type': match.group(2),
            'content': match.group(3),
            'confidence': 'high'
        }

    # Step 2: 正则失败，用 LLM 兜底
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": "Extract date, type, content as JSON"
        }, {"role": "user", "content": text}],
        response_format={"type": "json_object"}
    )
    result = json.loads(response.choices[0].message.content)
    result['confidence'] = 'low'
    return result
```

## 4. 性能对比

| 方法 | 延迟 | 成本 | 准确率 | 维护性 |
|------|------|------|--------|--------|
| 正则 | <1ms | 0 | 高(固定格式) | 中 |
| 解析器 | <5ms | 0 | 很高 | 高 |
| LLM | 500-2000ms | $ | 中高 | 高 |

## 5. 实战建议

- **日志解析**: 永远用正则
- **表单数据提取**: 先正则，LLM 兜底
- **简历解析**: 直接 LLM（格式太多变）
- **API 响应**: 用 JSON 解析器
- **用户输入分类**: 规则 + LLM 混合
""",
        "category": "通用AI能力",
        "sub_category": "提示工程",
        "tags": ["正则表达式", "LLM", "文本解析", "决策框架", "性能优化"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "数据可视化报告 Skill",
        "desc": "来自 nexu-io/open-design 的数据报告生成器：将 CSV/Excel/JSON 数据转化为精美的可视化报告页面",
        "content": """# 数据可视化报告生成

> 来源: [nexu-io/open-design](https://github.com/nexu-io/open-design) (85K+ stars) - skills/data-report
> 许可证: MIT

将 CSV、Excel 或 JSON 数据转化为精美的可视化报告页面。

## 1. 报告结构

```
┌─────────────────────────────────┐
│  报告标题 + 摘要                │
├─────────────────────────────────┤
│  KPI 卡片 (3-4 个核心指标)      │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│  │128 │ │ 23%│ │ ¥4M│ │ 4.8 │   │
│  │用户│ │增长│ │营收│ │评分│   │
│  └────┘ └────┘ └────┘ └────┘   │
├─────────────────────────────────┤
│  主图表 (趋势/对比/分布)        │
│  ┌─────────────────────────┐    │
│  │  📈 折线图 / 柱状图     │    │
│  └─────────────────────────┘    │
├─────────────────────────────────┤
│  辅助图表 + 数据表格            │
├─────────────────────────────────┤
│  结论 + 建议                    │
└─────────────────────────────────┘
```

## 2. 图表选择指南

| 数据关系 | 推荐图表 | 场景 |
|----------|----------|------|
| 时间趋势 | 折线图 | 月度销售、DAU 变化 |
| 分类对比 | 柱状图 | 各部门业绩、产品评分 |
| 占比分布 | 饼图/环形图 | 市场份额、预算分配 |
| 相关性 | 散点图 | 价格vs销量 |
| 排名 | 水平柱状图 | Top 10 排行 |
| 地理分布 | 地图 | 区域销售 |
| 数据分布 | 直方图/箱线图 | 年龄分布、收入区间 |

## 3. 数据处理流程

```python
import pandas as pd
import json

def process_data(source):
    # 1. 读取数据
    if source.endswith('.csv'):
        df = pd.read_csv(source)
    elif source.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(source)
    elif source.endswith('.json'):
        df = pd.read_json(source)

    # 2. 基础分析
    summary = {
        'total_rows': len(df),
        'columns': list(df.columns),
        'numeric_cols': df.select_dtypes(include='number').columns.tolist(),
    }

    # 3. 自动检测 KPI
    kpis = []
    for col in df.select_dtypes(include='number').columns:
        kpis.append({
            'label': col,
            'value': df[col].sum(),
            'change': None  # 需要时间序列才能计算
        })

    return df, summary, kpis
```

## 4. 视觉设计规范

### 颜色系统
- 主色: 品牌色（最多 1 个）
- 辅助色: 主色的不同明度/饱和度
- 语义色: 红=下降/危险，绿=增长/安全，蓝=中性

### 排版
- 标题: 24-30px, 加粗
- KPI 数字: 36-48px, 加粗
- 正文: 14-16px
- 注释: 12px, 灰色

### 留白
- 卡片间距: 16-24px
- 图表内边距: 16px
- 页面边距: 24-32px
""",
        "category": "办公自动化SOP",
        "sub_category": "数据处理",
        "tags": ["数据可视化", "报告生成", "CSV", "Excel", "图表"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "nexu-io",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "UI动效系统 Skill",
        "desc": "来自 ECC 的 React/Next.js 生产级动效系统：动画模式、过渡效果、性能优化、Framer Motion 最佳实践",
        "content": """# UI 动效系统

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/motion-ui
> 许可证: MIT

React/Next.js 的生产级动效系统。

## 1. 动效原则

### 有意义的动效
- **引导注意力**: 新元素出现时吸引视线
- **建立关系**: 元素间的进入/退出暗示导航关系
- **提供反馈**: 交互后的即时视觉响应
- **状态变化**: 平滑过渡避免突兀跳变

### 反模式
- 纯装饰性动画（分散注意力）
- 超过 500ms 的动画（用户等待）
- 同时动画超过 3 个元素（视觉混乱）

## 2. 时间参考

| 类型 | 时长 | 缓动 |
|------|------|------|
| 微交互 (hover/click) | 100-200ms | ease-out |
| 展开/折叠 | 200-300ms | ease-in-out |
| 页面切换 | 300-500ms | ease-in-out |
| 进入视口 | 400-600ms | ease-out |
| 复杂编排动画 | 500-800ms | spring |

## 3. Framer Motion 模式

```jsx
import { motion, AnimatePresence } from 'framer-motion';

// 页面切换
const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

function PageTransition({ children }) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}

// 列表编排
function AnimatedList({ items }) {
  return (
    <AnimatePresence>
      {items.map(item => (
        <motion.div
          key={item.id}
          layout
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ type: 'spring', stiffness: 300, damping: 25 }}
        >
          {item.content}
        </motion.div>
      ))}
    </AnimatePresence>
  );
}

// 手势交互
function SwipeableCard({ onDismiss }) {
  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={(e, { offset }) => {
        if (Math.abs(offset.x) > 100) onDismiss();
      }}
      animate={{ x: 0 }}
    >
      Card Content
    </motion.div>
  );
}
```

## 4. 性能优化

### 只动画合成属性
```css
/* 好 - GPU 加速 */
transform: translateX(100px);
opacity: 0.5;

/* 差 - 触发重排 */
width: 200px;
margin-left: 100px;
top: 50px;
```

### will-change 使用
```css
.animate-on-hover:hover {
  will-change: transform;
  transform: scale(1.05);
}
/* 动画结束后移除 */
.animate-on-hover {
  will-change: auto;
}
```

### 减少动画偏好
```jsx
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

<motion.div
  animate={prefersReducedMotion ? {} : { x: 100 }}
  transition={prefersReducedMotion ? { duration: 0 } : undefined}
/>
```

## 5. 加载动画

```jsx
// 骨架屏（推荐）
function Skeleton({ width, height }) {
  return (
    <motion.div
      style={{ width, height, borderRadius: 8, background: '#e5e7eb' }}
      animate={{ opacity: [0.5, 1, 0.5] }}
      transition={{ duration: 1.5, repeat: Infinity }}
    />
  );
}

// 进度条
function ProgressBar({ progress }) {
  return (
    <motion.div
      style={{ height: 4, background: '#3b82f6' }}
      initial={{ width: 0 }}
      animate={{ width: `${progress}%` }}
      transition={{ duration: 0.3 }}
    />
  );
}
```
""",
        "category": "程序/测试/运维",
        "sub_category": "前端开发",
        "tags": ["动效", "Framer Motion", "React", "CSS动画", "UI交互"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "验证循环 Skill",
        "desc": "来自 ECC 的 AI 会话工作验证系统：在声称完成前全面验证 AI 编码会话的输出质量",
        "content": """# 验证循环

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/verification-loop
> 许可证: MIT

在声称工作完成前，全面验证 AI 编码会话的输出。

## 1. 验证流程

```
完成编码 → 静态检查 → 构建验证 → 测试运行 → 功能验证 → 质量审查
    ↓           ↓          ↓          ↓          ↓          ↓
  修改代码   lint/type   compile   unit/integ  manual     review
```

## 2. 检查清单

### Phase 1: 静态验证
- [ ] 代码无 lint 错误
- [ ] 类型检查通过（TypeScript/mypy）
- [ ] 无未使用的 import
- [ ] 命名规范一致

### Phase 2: 构建验证
- [ ] 项目能成功构建
- [ ] 无新增构建警告
- [ ] 依赖版本正确

### Phase 3: 测试验证
- [ ] 所有现有测试通过
- [ ] 新功能有对应测试
- [ ] 边界情况有测试
- [ ] 测试覆盖关键路径

### Phase 4: 功能验证
- [ ] 实现了用户要求的所有功能
- [ ] 没有引入副作用
- [ ] 错误处理完整
- [ ] 边界情况已处理

### Phase 5: 质量审查
- [ ] 代码可读性好
- [ ] 无重复代码
- [ ] 注释充分（复杂逻辑）
- [ ] 性能可接受

## 3. 自动化验证脚本

```bash
#!/bin/bash
# verify.sh - 一键验证

set -e

echo "🔍 Phase 1: Static Analysis"
npm run lint
npm run type-check

echo "🔨 Phase 2: Build"
npm run build

echo "🧪 Phase 3: Tests"
npm test -- --coverage

echo "✅ All checks passed!"
```

## 4. 常见遗漏

| 容易遗漏 | 后果 | 检查方法 |
|----------|------|----------|
| 错误处理 | 用户看到白屏 | 故意触发错误 |
| 空状态 | UI 崩溃 | 传入空数组 |
| 并发 | 竞态条件 | 快速连续操作 |
| 大数据 | 性能问题 | 1000+ 条数据测试 |
| 特殊字符 | 注入/崩溃 | 输入 emoji/unicode |

## 5. 验证心态

- **不要假设它工作了** - 验证它
- **不要只测 happy path** - 测 edge cases
- **不要跳过构建步骤** - 从头完整验证
- **不要相信自己的记忆** - 重新读代码确认
""",
        "category": "Agent工作流模板",
        "sub_category": "通用工作流",
        "tags": ["验证", "QA", "代码审查", "自动化测试", "质量保障"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "医疗临床决策支持 Skill",
        "desc": "来自 ECC 的 CDSS 开发模式：药物相互作用检查、剂量验证、临床评分（NEWS2/qSOFA）、告警分级、EMR 工作流集成",
        "content": """# 医疗临床决策支持系统 (CDSS)

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/healthcare-cdss-patterns
> 许可证: MIT

临床决策支持系统的开发模式与最佳实践。

## 1. CDSS 核心功能

### 药物相互作用检查 (DDI)
```python
class DrugInteractionChecker:
    # 严重级别
    SEVERITY = {
        'contraindicated': '禁忌 - 禁止联用',
        'major': '严重 - 需要密切监测',
        'moderate': '中等 - 可能需要调整',
        'minor': '轻微 - 通常无临床意义',
    }

    def check(self, drug_list: list[str]) -> list[dict]:
        interactions = []
        for i, drug_a in enumerate(drug_list):
            for drug_b in drug_list[i+1:]:
                result = self._lookup(drug_a, drug_b)
                if result and result.severity in ['contraindicated', 'major']:
                    interactions.append({
                        'drugs': [drug_a, drug_b],
                        'severity': result.severity,
                        'description': result.description,
                        'recommendation': result.recommendation,
                    })
        return sorted(interactions, key=lambda x: self._severity_rank(x['severity']))
```

### 剂量验证
```python
class DoseValidator:
    def validate(self, drug: str, dose: float, unit: str, route: str, patient: Patient) -> list[Alert]:
        alerts = []

        # 1. 范围检查
        max_dose = self.get_max_daily_dose(drug)
        if dose > max_dose:
            alerts.append(Alert('MAJOR', f'{drug} 单次剂量超过最大推荐量 {max_dose}{unit}'))

        # 2. 肾功能调整
        if patient.creatinine_clearance < 30:
            adjusted = self.renal_adjustment(drug, dose)
            if adjusted < dose:
                alerts.append(Alert('MODERATE', f'肾功能不全建议调整剂量至 {adjusted}{unit}'))

        # 3. 过敏检查
        if drug in patient.allergies:
            alerts.append(Alert('CONTRAINDICATED', f'患者对 {drug} 过敏！'))

        return alerts
```

## 2. 临床评分系统

### NEWS2 (国家早期预警评分)
```python
def calculate_news2(patient_vitals: dict) -> dict:
    scores = {
        'respiratory_rate': score_rr(patient_vitals['rr']),
        'oxygen_saturation': score_spo2(patient_vitals['spo2']),
        'temperature': score_temp(patient_vitals['temp']),
        'systolic_bp': score_sbp(patient_vitals['sbp']),
        'heart_rate': score_hr(patient_vitals['hr']),
        'consciousness': 3 if patient_vitals['avpu'] != 'A' else 0,
    }
    total = sum(scores.values())

    # 临床响应
    if total >= 7:
        response = '紧急 - 危重症团队'
    elif total >= 5:
        response = ' urgent - 紧急医疗评估'
    elif total >= 3:
        response = 'urgent - 医疗评估'
    else:
        response = '常规监测'

    return {'total': total, 'scores': scores, 'response': response}
```

### qSOFA (快速序贯器官衰竭评估)
```python
def calculate_qsofa(sbp: float, rr: float, gcs: int) -> dict:
    score = 0
    if sbp <= 100: score += 1   # 低血压
    if rr >= 22: score += 1     # 呼吸急促
    if gcs < 15: score += 1     # 意识改变

    risk = 'high' if score >= 2 else 'low'
    return {'score': score, 'mortality_risk': risk}
```

## 3. 告警分级

| 级别 | 触发条件 | 行为 | UI |
|------|----------|------|----|
| 禁忌 | 过敏/禁忌联用 | 阻止提交，红色 | 必须修改才能继续 |
| 严重 | 重大 DDI/超量 | 强提醒，橙色 | 需要确认才能继续 |
| 中等 | 需监测/调整 | 提醒，黄色 | 显示建议 |
| 信息 | 注意事项 | 弱提示，蓝色 | 可忽略 |

## 4. EMR 集成要点
- 遵循 HL7 FHIR 标准
- 不中断临床工作流
- 告警疲劳是最大风险（控制告警数量）
- 所有决策需可追溯（审计日志）
""",
        "category": "行业垂直Skill",
        "sub_category": "医疗健康",
        "tags": ["CDSS", "临床决策", "药物相互作用", "NEWS2", "FHIR"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "TailwindCSS开发模式 Skill",
        "desc": "来自 Coolify 项目的 Tailwind CSS 开发模式：响应式网格布局、UI 组件样式、暗色模式、间距排版最佳实践",
        "content": """# TailwindCSS 开发模式

> 来源: [Coolify](https://github.com/coollabsio/coolify) (60K+ stars) - skills/tailwindcss-development
> 许可证: Apache-2.0

Tailwind CSS v3/v4 的开发模式与最佳实践。

## 1. 响应式布局

### 网格系统
```html
<!-- 产品卡片网格 -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
  <div class="rounded-lg border border-gray-200 p-4 shadow-sm hover:shadow-md transition-shadow">
    <!-- Card content -->
  </div>
</div>

<!-- Dashboard 布局 -->
<div class="grid grid-cols-1 md:grid-cols-[240px_1fr] lg:grid-cols-[280px_1fr_320px]">
  <aside class="hidden md:block">Sidebar</aside>
  <main class="p-4 sm:p-6">Content</main>
  <aside class="hidden lg:block">Right Panel</aside>
</div>
```

### Flex 布局
```html
<!-- 导航栏 -->
<nav class="flex items-center justify-between px-4 sm:px-6 h-16 border-b">
  <div class="flex items-center gap-3">
    <img class="h-8 w-8" />
    <span class="text-lg font-semibold">Brand</span>
  </div>
  <div class="flex items-center gap-2 sm:gap-4">
    <button class="btn-ghost">Menu</button>
    <button class="btn-primary">Action</button>
  </div>
</nav>
```

## 2. 组件样式模式

### 按钮变体
```html
<!-- Primary -->
<button class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium
  text-white bg-blue-600 rounded-lg hover:bg-blue-700
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors duration-200">
  Primary Button
</button>

<!-- Secondary -->
<button class="... text-blue-600 bg-blue-50 hover:bg-blue-100 border border-blue-200 ...">
  Secondary
</button>

<!-- Ghost -->
<button class="... text-gray-700 hover:bg-gray-100 ...">
  Ghost
</button>
```

### 卡片
```html
<div class="rounded-xl border border-gray-200 bg-white shadow-sm">
  <div class="p-4 sm:p-6">
    <h3 class="text-lg font-semibold text-gray-900">Title</h3>
    <p class="mt-2 text-sm text-gray-600">Description text</p>
    <div class="mt-4 flex items-center gap-2">
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Active
      </span>
    </div>
  </div>
</div>
```

## 3. 暗色模式

```html
<!-- 自动跟随系统 -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">

<!-- 边框 -->
<div class="border-gray-200 dark:border-gray-700">

<!-- 输入框 -->
<input class="bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600
  text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500" />
```

### 暗色模式检查清单
- [ ] 所有背景色有 dark: 对应
- [ ] 文字颜色对比度 ≥ 4.5:1
- [ ] 图片/图标在暗色下可见
- [ ] 阴影在暗色下适当减弱

## 4. 排版系统

```html
<!-- 页面标题层级 -->
<h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-gray-900">Page Title</h1>
<h2 class="text-xl sm:text-2xl font-semibold text-gray-900">Section</h2>
<h3 class="text-lg font-semibold text-gray-900">Subsection</h3>

<!-- 正文 -->
<p class="text-base text-gray-600 leading-relaxed">Body text</p>
<p class="text-sm text-gray-500">Secondary text</p>
<p class="text-xs text-gray-400">Caption / Helper</p>
```

## 5. 性能优化

- 使用 `@apply` 谨慎（仅用于重复组件）
- 启用 JIT 模式减少 CSS 体积
- 避免任意值 `w-[347px]`（用设计系统值）
- 使用 `content-visibility: auto` 优化长列表
""",
        "category": "程序/测试/运维",
        "sub_category": "前端开发",
        "tags": ["TailwindCSS", "CSS", "响应式", "暗色模式", "组件库"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coollabsio (via Coolify)",
        "source_type": "开源改编",
        "license": "Apache-2.0",
    },

    # ==================== 第六批新增 (FastAPI/Go/Spring/Security/Research/Agent) ====================
    {
        "title": "FastAPI最佳实践 Skill",
        "desc": "来自 ECC 的 FastAPI 完整最佳实践：项目结构、Pydantic v2、依赖注入、异步处理、认证授权、事务服务层、测试",
        "content": """# FastAPI 最佳实践

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/fastapi-patterns
> 许可证: MIT

FastAPI 应用的完整最佳实践指南。

## 1. 项目结构

```
app/
├── main.py              # FastAPI 实例 + 生命周期
├── config.py            # Settings (pydantic-settings)
├── dependencies.py      # 公共依赖
├── routers/
│   ├── users.py
│   └── items.py
├── schemas/
│   ├── user.py          # Pydantic v2 模型
│   └── item.py
├── services/
│   ├── user_service.py  # 业务逻辑
│   └── item_service.py
├── repositories/
│   ├── user_repo.py     # 数据访问
│   └── item_repo.py
├── models/
│   └── database.py      # SQLAlchemy 模型
└── tests/
    ├── conftest.py
    ├── test_users.py
    └── test_items.py
```

## 2. Pydantic v2 Schema

```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# 创建请求
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r'^[\w.-]+@[\w.-]+\.\w+$')
    age: int = Field(ge=0, le=150)

# 响应模型
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    created_at: datetime

# 分页
class PaginatedResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
```

## 3. 依赖注入

```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# 数据库会话
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# 当前用户
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    user = await verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# 权限检查
def require_role(role: str):
    async def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
```

## 4. 路由示例

```python
from fastapi import APIRouter, status

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(),
):
    return await service.create(data)

@router.get("/", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: UserService = Depends(),
):
    return await service.list(page, page_size)
```

## 5. 测试

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_create_user(client):
    resp = await client.post("/users/", json={
        "name": "Test", "email": "test@example.com", "age": 25
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test"
```
""",
        "category": "程序/测试/运维",
        "sub_category": "后端开发",
        "tags": ["FastAPI", "Python", "Pydantic", "异步", "REST API"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Go惯用法模式 Skill",
        "desc": "来自 ECC 的 Go 语言惯用模式：函数选项、小接口、依赖注入、并发模式、错误处理、包组织",
        "content": """# Go 惯用法模式

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/golang-patterns
> 许可证: MIT

Go 语言的惯用模式、最佳实践和约定。

## 1. 函数选项模式

```go
// 用选项配置，而非多参数
 type Server struct {
    host string
    port int
    timeout time.Duration
}

type Option func(*Server)

func WithHost(host string) Option    { return func(s *Server) { s.host = host } }
func WithPort(port int) Option       { return func(s *Server) { s.port = port } }
func WithTimeout(d time.Duration) Option { return func(s *Server) { s.timeout = d } }

func NewServer(opts ...Option) *Server {
    s := &Server{host: "localhost", port: 8080, timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// 使用
srv := NewServer(WithPort(9090), WithTimeout(10*time.Second))
```

## 2. 小接口

```go
// 好：接口只做一件事
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Closer interface { Close() error }

// 组合小接口
type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}

// 接受接口，返回结构体
func Process(r io.Reader) (*Result, error) { ... }
```

## 3. 并发模式

```go
// Worker Pool
func workerPool(jobs <-chan Job, results chan<- Result, numWorkers int) {
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }
    wg.Wait()
    close(results)
}

// Context 取消
func doWork(ctx context.Context) error {
    select {
    case result := <-doSomething():
        return handle(result)
    case <-ctx.Done():
        return ctx.Err()
    }
}

// errgroup 并行任务
func fetchAll(ctx context.Context) ([]Data, error) {
    g, ctx := errgroup.WithContext(ctx)
    var mu sync.Mutex
    var results []Data

    for _, url := range urls {
        g.Go(func() error {
            data, err := fetch(ctx, url)
            if err != nil { return err }
            mu.Lock()
            results = append(results, data)
            mu.Unlock()
            return nil
        })
    }
    return results, g.Wait()
}
```

## 4. 错误处理

```go
// 自定义错误类型
type NotFoundError struct {
    Resource string
    ID       string
}
func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}

// 错误包装 (Go 1.13+)
func (s *Service) GetUser(id string) (*User, error) {
    user, err := s.repo.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}

// 错误判断
if errors.Is(err, ErrNotFound) { ... }
var nfe *NotFoundError
if errors.As(err, &nfe) { ... }
```

## 5. 包组织

```
myproject/
├── cmd/
│   └── server/
│       └── main.go        # 入口，最小化
├── internal/              # 私有包
│   ├── handler/           # HTTP 处理
│   ├── service/           # 业务逻辑
│   ├── repository/        # 数据访问
│   └── model/             # 领域模型
├── pkg/                   # 可导出的公共包
│   └── httputil/
└── go.mod
```
""",
        "category": "程序/测试/运维",
        "sub_category": "编码规范",
        "tags": ["Go", "Golang", "并发", "函数选项", "错误处理", "设计模式"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Spring Boot架构模式 Skill",
        "desc": "来自 ECC 的 Spring Boot 架构模式：REST API 设计、分层服务、数据访问、缓存、异步处理、日志记录",
        "content": """# Spring Boot 架构模式

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/springboot-patterns
> 许可证: MIT

Java Spring Boot 后端架构模式与最佳实践。

## 1. 分层架构

```
Controller (HTTP) → Service (业务) → Repository (数据)
     ↓                    ↓                  ↓
   DTO/Request      Domain Entity       JPA Entity
```

### Controller 层
```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping
    public Page<UserResponse> list(@RequestParam(defaultValue = "0") int page) {
        return userService.findAll(PageRequest.of(page, 20));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse create(@Valid @RequestBody CreateUserRequest request) {
        return userService.create(request);
    }
}
```

### Service 层
```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;

    public Page<UserResponse> findAll(Pageable pageable) {
        return userRepository.findAll(pageable).map(userMapper::toResponse);
    }

    @Transactional
    public UserResponse create(CreateUserRequest request) {
        User user = userMapper.toEntity(request);
        user = userRepository.save(user);
        return userMapper.toResponse(user);
    }
}
```

## 2. 异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.notFound().build();
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult().getFieldErrors()
            .stream().map(e -> e.getField() + ": " + e.getDefaultMessage()).toList();
        return ResponseEntity.badRequest().body(new ErrorResponse(errors));
    }
}
```

## 3. 缓存策略

```java
@Service
public class ProductService {
    @Cacheable(value = "products", key = "#id")
    public Product findById(Long id) {
        return productRepository.findById(id).orElseThrow();
    }

    @CacheEvict(value = "products", key = "#product.id")
    public Product update(Product product) {
        return productRepository.save(product);
    }

    @CacheEvict(value = "products", allEntries = true)
    @Scheduled(fixedRate = 3600000) // 每小时清理
    public void clearProductCache() {}
}
```

## 4. 异步处理

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(8);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
}

@Service
public class NotificationService {
    @Async
    public CompletableFuture<Void> sendEmail(String to, String subject) {
        // 异步发送邮件
        return CompletableFuture.runAsync(() -> emailClient.send(to, subject));
    }
}
```

## 5. 日志规范

```java
@Slf4j
@Service
public class OrderService {
    public Order createOrder(OrderRequest request) {
        log.info("Creating order for customer: {}", request.customerId());
        try {
            Order order = orderRepository.save(mapToEntity(request));
            log.info("Order created: id={}, total={}", order.getId(), order.getTotal());
            return order;
        } catch (Exception e) {
            log.error("Failed to create order for customer: {}", request.customerId(), e);
            throw e;
        }
    }
}
```
""",
        "category": "程序/测试/运维",
        "sub_category": "后端开发",
        "tags": ["Spring Boot", "Java", "REST API", "缓存", "异步", "分层架构"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "安全审查清单 Skill",
        "desc": "来自 ECC 的全面安全审查清单：认证、用户输入处理、密钥管理、API 安全、支付功能安全模式",
        "content": """# 安全审查清单

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/security-review
> 许可证: MIT

添加认证、处理用户输入、处理密钥、创建 API 端点或实现支付/敏感功能时的全面安全检查。

## 1. 认证与授权

- [ ] 密码使用 bcrypt/argon2 哈希（永远不要 MD5/SHA）
- [ ] JWT token 有过期时间
- [ ] JWT 密钥足够长（≥256 bit）且安全存储
- [ ] 每个端点都有权限检查
- [ ] 使用 RBAC 或 ABAC 而非硬编码角色检查
- [ ] Session 有超时和刷新机制
- [ ] 登录失败有速率限制

## 2. 输入验证

- [ ] 所有用户输入在服务端验证
- [ ] SQL 查询使用参数化/预编译语句
- [ ] HTML 输出转义（防 XSS）
- [ ] 文件上传验证类型、大小、文件名
- [ ] URL 参数验证（防开放重定向）
- [ ] JSON 解析有深度限制（防 billion laughs）
- [ ] 数字输入有范围限制

## 3. 密钥管理

- [ ] 密钥不在代码中硬编码
- [ ] 使用环境变量或密钥管理服务
- [ ] .env 文件在 .gitignore 中
- [ ] API 密钥有权限范围限制
- [ ] 定期轮换密钥
- [ ] 日志中不打印密钥/token

## 4. API 安全

- [ ] HTTPS 强制
- [ ] CORS 配置明确（不是 *）
- [ ] 速率限制实施
- [ ] 请求体大小限制
- [ ] 响应中不暴露内部信息（堆栈跟踪、SQL）
- [ ] 安全响应头（CSP, X-Frame-Options, HSTS）

## 5. 支付安全

- [ ] 支付金额在服务端计算（不是客户端）
- [ ] 幂等性键防止重复扣款
- [ ] Webhook 签名验证
- [ ] 支付状态机完整（pending → processing → completed/failed）
- [ ] 退款有权限控制和审计日志

## 6. 常见漏洞检查

| 漏洞 | 检查方法 |
|------|----------|
| SQL 注入 | 所有查询参数化？ |
| XSS | 输出转义？CSP 配置？ |
| CSRF | Token 验证？SameSite cookie？ |
| IDOR | 资源访问检查所有权？ |
| SSRF | URL 白名单？内网地址过滤？ |
| 路径遍历 | 文件名清理？沙箱目录？ |
""",
        "category": "程序/测试/运维",
        "sub_category": "安全",
        "tags": ["安全审查", "XSS", "CSRF", "JWT", "认证", "输入验证"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "深度研究 Skill",
        "desc": "来自 ECC 的多源深度研究 Skill：使用 firecrawl 和 exa 搜索网络、综合发现、生成带来源引用的研究报告",
        "content": """# 深度研究

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/deep-research
> 许可证: MIT

多源深度研究：搜索网络、综合发现、生成带引用的报告。

## 1. 研究流程

```
1. 理解研究问题
   ↓ 拆解子问题
2. 多源搜索
   ↓ 网络搜索 + 学术搜索 + 代码搜索
3. 信息筛选与验证
   ↓ 交叉验证、来源可信度评估
4. 综合与分析
   ↓ 提取关键发现、识别模式
5. 生成报告
   ↓ 结构化输出 + 来源引用
```

## 2. 搜索策略

### 多源搜索
```
- 通用搜索: 广泛了解主题
- 学术搜索: 论文、研究、权威来源
- 代码搜索: 实现示例、最佳实践
- 新闻搜索: 最新动态、行业趋势
```

### 查询优化
- 从宽泛到具体逐步缩小
- 使用专业术语和同义词
- 检查高结果来源的其他相关内容
- 每个子问题至少 3 个独立来源交叉验证

## 3. 来源评估

| 可信度 | 来源类型 | 权重 |
|--------|----------|------|
| 高 | 官方文档、学术论文、RFC | 直接引用 |
| 中 | 知名博客、Stack Overflow 高票答案 | 参考引用 |
| 低 | 个人博客、论坛帖子 | 仅做线索 |

## 4. 报告结构

```markdown
# [研究主题]

## 摘要
[3-5 句话总结核心发现]

## 关键发现
1. [发现 1] [1]
2. [发现 2] [2]
3. [发现 3] [3]

## 详细分析
### [子主题 1]
[内容] [引用]

### [子主题 2]
[内容] [引用]

## 结论与建议
[基于证据的建议]

## 来源
[1] URL - 标题 - 访问日期
[2] URL - 标题 - 访问日期
```

## 5. 质量标准

- 每个事实性声明都有来源
- 区分事实和观点
- 标注信息的时效性
- 承认知识空白和不确定性
- 提供反面观点（如果有）
""",
        "category": "通用AI能力",
        "sub_category": "提示工程",
        "tags": ["深度研究", "信息检索", "报告生成", "多源搜索", "引用"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Agent Loop设计检查 Skill",
        "desc": "来自 ECC 的 Agent 循环设计审查：防止循环失控、目标验证、五种失败模式分析、可判定目标设计",
        "content": """# Agent Loop 设计检查

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/loop-design-check
> 许可证: MIT

设计和审查目标导向的 Agent 循环，防止失控运行。

## 1. 循环骨架

```
┌─────────────────────────────────────┐
│          Agent Loop                 │
│                                     │
│  1. PLAN: 分析当前状态 → 下一步    │
│  2. BUILD: 执行动作                │
│  3. JUDGE: 验证结果是否满足目标    │
│  4. 如果未满足 → 回到 1           │
│  5. 如果满足/超时 → 退出           │
└─────────────────────────────────────┘
```

## 2. 可判定目标

**每个 Agent 循环必须有一个机器可判定的目标。**

```python
# 好：可判定
goal = "所有测试通过"  # 可以检查 exit code
goal = "文件存在且包含 'SUCCESS'"  # 可以检查
goal = "API 返回 200"  # 可以检查

# 差：不可判定
goal = "代码质量好"  # 什么是好？
goal = "用户满意"  # 无法机器判定
```

## 3. 五种失败模式

| 失败模式 | 描述 | 防护 |
|----------|------|------|
| 无限循环 | 永远达不到目标 | 最大迭代次数 + 超时 |
| Goodhart 作弊 | 优化了错误指标 | 独立验证器，非自我评估 |
| 错误答案跑到底 | 完成但结果错误 | 外部验证，不只是自我检查 |
| Token 燃烧 | 无意义重复消耗资源 | 重复检测 + 预算限制 |
| 范围蔓延 | 超出原始目标 | 目标边界严格定义 |

## 4. 检查清单

### 设计阶段
- [ ] 目标是否机器可判定？
- [ ] 边界条件是否定义？（什么算完成/失败）
- [ ] 最大迭代次数是否设置？
- [ ] 预算限制是否设置？（token/时间/成本）
- [ ] 回退策略是否定义？（达到上限时做什么）

### 验证器独立性
- [ ] 验证器是否独立于执行器？
- [ ] 验证器是否使用不同的方法？
- [ ] 判断是否保留给人？（高风险场景）

### 红线检查
- [ ] 循环能否删除生产数据？
- [ ] 循环能否发送外部通信？
- [ ] 循环能否修改自身代码？
- [ ] 以上操作是否有人工审批？

## 5. 实现模板

```python
class AgentLoop:
    def __init__(self, max_iterations=10, budget_tokens=50000):
        self.max_iterations = max_iterations
        self.budget_tokens = budget_tokens
        self.used_tokens = 0

    def run(self, goal, context):
        for i in range(self.max_iterations):
            if self.used_tokens >= self.budget_tokens:
                return LoopResult(status='budget_exhausted', partial=context)

            plan = self.plan(goal, context)
            action = self.build(plan)
            result = self.execute(action)
            context = self.update(context, result)

            if self.judge(goal, context):
                return LoopResult(status='success', result=context)

            if self.detect_looping(context):
                return LoopResult(status='stuck', partial=context)

        return LoopResult(status='max_iterations', partial=context)
```
""",
        "category": "Agent工作流模板",
        "sub_category": "通用工作流",
        "tags": ["Agent Loop", "循环设计", "目标验证", "失控防护", "自主Agent"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Kotlin Ktor服务器模式 Skill",
        "desc": "来自 ECC 的 Ktor 服务器完整模式：路由 DSL、插件、认证、Koin DI、序列化、WebSocket、测试",
        "content": """# Kotlin Ktor 服务器模式

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/kotlin-ktor-patterns
> 许可证: MIT

Ktor 服务器的完整开发模式。

## 1. 路由 DSL

```kotlin
fun Application.configureRouting() {
    routing {
        route("/api") {
            route("/users") {
                get {
                    val page = call.request.queryParameters["page"]?.toIntOrNull() ?: 1
                    val users = userService.findAll(page)
                    call.respond(users)
                }
                post {
                    val request = call.receive<CreateUserRequest>()
                    val user = userService.create(request)
                    call.respond(HttpStatusCode.Created, user)
                }
                get("/{id}") {
                    val id = call.parameters["id"]?.toLongOrNull()
                        ?: throw BadRequestException("Invalid id")
                    val user = userService.findById(id)
                        ?: throw NotFoundException("User not found")
                    call.respond(user)
                }
            }
        }
    }
}
```

## 2. 插件配置

```kotlin
fun Application.configurePlugins() {
    // 内容协商 (JSON 序列化)
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = false
            ignoreUnknownKeys = true
            encodeDefaults = true
        })
    }

    // 认证
    install(Authentication) {
        jwt("auth-jwt") {
            verifier(JWT.require(Algorithm.HMAC256(config.jwtSecret)).build())
            validate { credential ->
                JWTPrincipal(credential.payload)
            }
        }
    }

    // CORS
    install(CORS) {
        allowHost("localhost:3000")
        allowHeader(HttpHeaders.ContentType)
        allowHeader(HttpHeaders.Authorization)
        allowMethod(HttpMethod.Options)
    }

    // 状态码页面
    install(StatusPages) {
        exception<NotFoundException> { call, _ ->
            call.respond(HttpStatusCode.NotFound)
        }
        exception<BadRequestException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest, mapOf("error" to cause.message))
        }
    }
}
```

## 3. Koin 依赖注入

```kotlin
val appModule = module {
    single { UserRepository(get()) }
    single { UserService(get(), get()) }
    single { DatabaseFactory(get()) }
}

fun Application.configureDI() {
    KoinApplication {
        application {
            modules(appModule)
        }
    }
}
```

## 4. WebSocket

```kotlin
fun Application.configureWebSocket() {
    routing {
        webSocket("/ws/chat") {
            val session = ChatSession(this)
            chatManager.add(session)
            try {
                for (frame in incoming) {
                    when (frame) {
                        is Frame.Text -> {
                            val text = frame.readText()
                            chatManager.broadcast(session, text)
                        }
                        is Frame.Close -> break
                        else -> {}
                    }
                }
            } finally {
                chatManager.remove(session)
            }
        }
    }
}
```

## 5. 测试

```kotlin
class UserApiTest {
    @Test
    fun `create user returns 201`() = testApplication {
        application { configureTestApp() }
        val response = client.post("/api/users") {
            contentType(ContentType.Application.Json)
            setBody("{\"name\":\"Test\",\"email\":\"test@example.com\"}")
        }
        assertEquals(HttpStatusCode.Created, response.status)
    }
}
```
""",
        "category": "程序/测试/运维",
        "sub_category": "后端开发",
        "tags": ["Kotlin", "Ktor", "WebSocket", "Koin", "认证", "服务器"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "Laravel安全实践 Skill",
        "desc": "来自 ECC 的 Laravel 安全最佳实践：认证授权、Eloquent 安全、CSRF/XSS 防护、API 安全、部署配置",
        "content": """# Laravel 安全实践

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/laravel-security
> 许可证: MIT

Laravel 应用的安全最佳实践。

## 1. 认证与授权

```php
// 使用 Laravel 内置认证
// config/auth.php - 使用 bcrypt
'bcrypt' => [
    'driver' => 'bcrypt',
    'rounds' => 12,
],

// Gate 授权
Gate::define('update-post', function (User $user, Post $post) {
    return $user->id === $post->user_id;
});

// Policy
public function update(User $user, Post $post): bool
{
    return $user->id === $post->user_id;
}

// Controller 中使用
$this->authorize('update', $post);
```

## 2. Eloquent 安全

```php
// 参数化查询（自动防 SQL 注入）
User::where('email', $request->email)->first();

// 批量赋值保护
// Model 中定义
protected $fillable = ['name', 'email']; // 只允许这些字段
// 或使用
protected $guarded = ['id', 'role'];     // 保护这些字段

// 永远不要
User::create($request->all()); // 危险！
```

## 3. CSRF 防护

```blade
<!-- 表单中自动添加 CSRF token -->
<form method="POST" action="/update">
    @csrf
    <!-- ... -->
</form>

<!-- API 路由排除 CSRF（使用 token 认证） -->
<!-- app/Http/Middleware/VerifyCsrfToken.php -->
protected $except = [
    'api/*',
];
```

## 4. XSS 防护

```blade
<!-- Blade 自动转义 -->
{{ $user->name }}  <!-- 安全：自动 htmlspecialchars -->

<!-- 危险：不转义 -->
{!! $user->bio !!}  <!-- 只在信任内容时使用 -->

<!-- 富文本用 HTML Purifier -->
{!! clean($user->bio) !!}
```

## 5. 安全响应头

```php
// app/Http/Middleware/SecurityHeaders.php
public function handle($request, Closure $next)
{
    $response = $next($request);
    $response->headers->set('X-Content-Type-Options', 'nosniff');
    $response->headers->set('X-Frame-Options', 'SAMEORIGIN');
    $response->headers->set('X-XSS-Protection', '1; mode=block');
    $response->headers->set('Strict-Transport-Security', 'max-age=31536000');
    $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');
    return $response;
}
```

## 6. 部署安全

```env
# .env 生产环境
APP_ENV=production
APP_DEBUG=false
APP_KEY=base64:...  # php artisan key:generate
DB_PASSWORD=strong_password

# 速率限制
# app/Providers/RouteServiceProvider.php
RateLimiter::for('api', function (Request $request) {
    return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
});
```
""",
        "category": "程序/测试/运维",
        "sub_category": "安全",
        "tags": ["Laravel", "PHP", "安全", "CSRF", "XSS", "认证"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },

    # ==================== 第七批新增 (网文小说/营销/办公/财务/学习) ====================
    {
        "title": "故事创作脚手架 Skill",
        "desc": "来自 LifeOS 的故事创作脚手架：帮作者构建已有故事的结构、隐藏伤口、主题、散文，覆盖七个叙事层",
        "content": """# 故事创作脚手架

> 来源: [LifeOS](https://github.com/danielmiessler/LifeOS) (18K+ stars) - skills/WriteStory
> 许可证: MIT

帮助作者构建已有故事，从作者素材中提取结构、主题和散文。

## 1. 七层叙事结构

```
第1层: 脊柱 (Spine) - 故事的核心驱动力
第2层: 隐藏伤口 (Hidden Wound) - 主角的内在创伤
第3层: 错误信念 (Misbelief) - 因伤口产生的错误认知
第4层: 主题论证 (Thematic Argument) - 故事要证明的真理
第5层: 角色弧线 (Character Arc) - 从错误信念到真理
第6层: 情节结构 (Plot Structure) - 支撑弧线的事件
第7层: 散文风格 (Prose) - 语言、节奏、视角
```

## 2. 创作流程

### Step 1: 素材收集
- 作者提供笔记、想法、片段
- 不要求完整大纲，碎片即可

### Step 2: 脊柱提取
- 从素材中识别核心冲突
- 提出 3 个候选脊柱，作者选择
- 脊柱必须是作者认可的（不是 AI 强加）

### Step 3: 伤口与信念
- 基于脊柱反推主角的内在缺陷
- 伤口 → 错误信念 → 主题论证
- 形成完整的内在逻辑链

### Step 4: 结构搭建
- 三幕/五幕/英雄之旅（根据故事类型）
- 每个转折点与角色弧线对齐
- 确保外在冲突反映内在冲突

### Step 5: 散文风格
- 根据故事类型建议视角（第一/第三人称）
- 节奏建议（快节奏 vs 沉思式）
- 语言风格参考

## 3. 禁止事项

- 禁止通用 AI 模式（"在一个遥远的王国..."）
- 禁止代替作者做创意决定（只提供选项）
- 禁止跳过作者素材直接生成
- 禁止使用陈词滥调的情节装置

## 4. 规模适配

| 规模 | 结构复杂度 | 建议章节 |
|------|------------|----------|
| 短篇 | 单一弧线 | 1-3 章 |
| 中篇 | 主弧线+副线 | 5-10 章 |
| 长篇 | 多视角+多副线 | 15-30 章 |
| 系列 | 系列弧线+单本弧线 | 多本规划 |
""",
        "category": "网文小说专用",
        "sub_category": "创作框架",
        "tags": ["故事创作", "叙事结构", "角色弧线", "小说", "写作"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "danielmiessler (via LifeOS)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "故事创作与翻译 Agent Skill",
        "desc": "来自 InkOS 的故事创作与翻译 AI：支持长篇小说、短篇、剧本、互动叙事、风格模仿、多语言翻译",
        "content": """# 故事创作与翻译 Agent

> 来源: [InkOS](https://github.com/Narcooo/inkos) (9K+ stars)
> 许可证: MIT

故事创作与翻译 AI Agent，支持多种叙事形式和多语言翻译。

## 1. 支持的叙事形式

| 形式 | 描述 | 典型长度 |
|------|------|----------|
| 长篇小说 | 多章节连续叙事 | 10万字+ |
| 短篇小说 | 独立完整故事 | 1千-3万字 |
| 剧本 | 对白+场景描述 | 按幕分 |
| 互动叙事 | 分支剧情 | 多路线 |
| 同人创作 | 基于已有IP | 灵活 |
| 风格模仿 | 模仿特定作家风格 | 灵活 |

## 2. 创作工作流

### Phase 1: 世界观构建
- 时代背景、地理位置、社会结构
- 魔法/科技体系（如适用）
- 文化习俗、语言特点

### Phase 2: 角色设计
- 主角：目标、动机、缺陷、弧线
- 配角：与主角的关系、独立动机
- 反派：合理动机（不是纯粹的恶）

### Phase 3: 情节编织
- 主线：核心冲突的推进
- 副线：丰富世界观和角色深度
- 伏笔：前后呼应的细节

### Phase 4: 散文打磨
- 视角一致性
- 对话自然度
- 节奏控制（张弛有度）

## 3. 翻译能力

### 多语言支持
- 中↔英、日↔中、韩↔中
- 保留原文风格和文化内涵
- 注释文化特定概念

### 翻译原则
1. 信达雅：忠实原文、通顺流畅、文学美感
2. 文化适配：不是直译，是等效传达
3. 术语一致：建立术语表，全文统一
4. 格式保留：章节、对话、特殊格式

## 4. 上下文管理

- 持久化故事状态（角色位置、时间线）
- 可追溯的研究来源
- 多模型路由（创作/翻译/编辑用不同模型）
""",
        "category": "网文小说专用",
        "sub_category": "创作工具",
        "tags": ["小说创作", "翻译", "多语言", "世界观", "角色设计"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "Narcooo (via InkOS)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "营销活动策划 Skill",
        "desc": "来自 ECC 的端到端营销活动策划：受众研究、定位、着陆页文案、邮件序列、社交帖子、广告文案、内容日历",
        "content": """# 营销活动策划

> 来源: [ECC](https://github.com/affaan-m/ECC) (239K+ stars) - skills/marketing-campaign
> 许可证: MIT

端到端营销活动策划与执行。

## 1. 策划流程

```
受众研究 → 定位 → 活动角度 → 内容生产 → 渠道分发 → 效果追踪
```

## 2. 受众研究

### 用户画像模板
```
姓名: [虚拟名字]
年龄: [范围]
职业: [类型]
痛点: [核心问题]
目标: [想要达成什么]
渠道: [在哪里获取信息]
决策因素: [价格/质量/速度/品牌]
```

## 3. 定位声明

```
对于 [目标受众]
谁需要 [核心需求]
[产品名] 是一个 [品类]
它能 [核心价值]
不同于 [竞品] 的 [差异点]
```

## 4. 内容矩阵

| 渠道 | 内容类型 | 频率 | 目标 |
|------|----------|------|------|
| 博客 | 长文教程 | 2次/周 | SEO + 信任 |
| 邮件 | 序列邮件 | 发布前5封 | 转化 |
| 社交 | 短内容 | 每日 | 曝光 + 互动 |
| 广告 | 精准投放 | 持续 | 转化 |
| 视频 | 产品演示 | 1次/周 | 信任 + 转化 |

## 5. 着陆页文案结构

```
1. 标题: 一句话价值主张
2. 副标题: 展开说明
3. 社会证明: 客户数量/评分/知名客户
4. 痛点共鸣: 描述用户当前困境
5. 解决方案: 产品如何解决
6. 功能展示: 3-5 个核心功能
7. 客户证言: 2-3 条真实评价
8. CTA: 明确的行动号召
9. FAQ: 常见疑虑解答
10. 最终 CTA: 重复行动号召
```

## 6. 邮件序列

```
邮件1: 欢迎 + 价值承诺
邮件2: 痛点深化 + 故事
邮件3: 解决方案介绍
邮件4: 社会证明 + 案例
邮件5: 紧迫性 + 最终 CTA
```
""",
        "category": "文案内容创作",
        "sub_category": "营销策划",
        "tags": ["营销", "文案", "着陆页", "邮件序列", "内容日历"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m (via ECC)",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "PPT演示文稿 Skill",
        "desc": "来自 Anthropic 官方 Skill 库：PowerPoint (.pptx) 创建、读取、编辑，覆盖幻灯片设计、布局、模板、演讲备注",
        "content": """# PPT 演示文稿

> 来源: [anthropics/skills](https://github.com/anthropics/skills) (168K+ stars)
> 许可证: MIT

创建、读取和编辑 PowerPoint (.pptx) 演示文稿。

## 1. 使用 python-pptx

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

prs = Presentation()

# 标题幻灯片
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "项目汇报"
slide.placeholders[1].text = "2024 Q4 总结"

# 内容幻灯片
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "核心成果"
body = slide.placeholders[1]
tf = body.text_frame
tf.text = "用户增长 50%"
p = tf.add_paragraph()
p.text = "营收突破 1000 万"
p = tf.add_paragraph()
p.text = "NPS 评分达到 72"

prs.save('report.pptx')
```

## 2. 幻灯片设计原则

### 10/20/30 法则 (Guy Kawasaki)
- 最多 10 张幻灯片
- 不超过 20 分钟
- 字体不小于 30pt

### 每张幻灯片只传达一个信息
- 标题就是结论（不是"销售数据"，而是"Q4 销售增长 30%"）
- 图表支持结论，不是装饰
- 留白 > 填满

## 3. 常用布局

| 用途 | 布局 | 内容 |
|------|------|------|
| 开场 | 标题幻灯片 | 主题 + 副标题 |
| 问题 | 大图+文字 | 痛点描述 |
| 方案 | 三栏对比 | 解决方案 |
| 数据 | 图表 | 关键指标 |
| 团队 | 头像+名字 | 核心成员 |
| 结尾 | CTA | 下一步行动 |

## 4. 配色建议

- 商务: 深蓝(#1E3A5F) + 白 + 灰
- 科技: 黑 + 蓝紫(#6C5CE7) + 白
- 清新: 绿(#00B894) + 白 + 浅灰
- 活力: 橙(#E17055) + 深蓝 + 白

## 5. 触发场景

当用户提到 "deck"、"slides"、"presentation"、"演示文稿"、"幻灯片"、"PPT"，或涉及 .pptx/.potx 文件时使用。
""",
        "category": "办公自动化SOP",
        "sub_category": "文档处理",
        "tags": ["PPT", "PowerPoint", "演示文稿", "幻灯片", "python-pptx"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "anthropics",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "财务规划 Skill",
        "desc": "来自 Anthropic 金融服务的综合财务规划：退休预测、教育资金、遗产规划、现金流分析、场景建模",
        "content": """# 财务规划

> 来源: [anthropics/financial-services](https://github.com/anthropics/financial-services) (34K+ stars)
> 许可证: MIT

综合财务规划覆盖退休预测、教育资金、遗产规划、现金流分析。

## 1. 财务规划框架

### 信息收集
```
基本信息: 年龄、家庭、职业、收入
资产负债: 现金、投资、房产、贷款
收支情况: 月收入、固定支出、变动支出
目标: 退休、教育、购房、旅行
风险偏好: 保守/稳健/积极
```

### 分析维度
| 维度 | 关键指标 | 健康标准 |
|------|----------|----------|
| 流动性 | 紧急储备 | 3-6 个月支出 |
| 负债 | 负债收入比 | < 36% |
| 储蓄 | 储蓄率 | > 20% |
| 投资 | 资产配置 | 与风险匹配 |
| 保障 | 保险覆盖 | 覆盖重大风险 |

## 2. 退休规划

```python
def retirement_projection(current_age, retire_age, savings, monthly_contrib,
                          annual_return, inflation_rate, monthly_expense):
    years = retire_age - current_age
    # 未来价值
    fv_savings = savings * (1 + annual_return) ** years
    fv_contribs = monthly_contrib * 12 * (
        ((1 + annual_return) ** years - 1) / annual_return
    )
    total = fv_savings + fv_contribs
    # 退休后可支撑年数
    real_return = annual_return - inflation_rate
    if real_return <= 0:
        return total, total / (monthly_expense * 12)
    years_supported = total / (monthly_expense * 12)
    return total, years_supported
```

## 3. 现金流分析

### 月度现金流表
```
收入:
  工资收入        ¥XX,XXX
  投资收益        ¥X,XXX
  其他收入        ¥X,XXX
  ────────────────────────
  总收入          ¥XX,XXX

支出:
  固定支出 (房贷/保险)  ¥X,XXX
  变动支出 (餐饮/交通)  ¥X,XXX
  可选支出 (娱乐/购物)  ¥X,XXX
  ────────────────────────
  总支出            ¥XX,XXX

净现金流            ¥X,XXX
储蓄率              XX%
```

## 4. 场景分析

- 基准场景: 当前轨迹
- 乐观场景: 收入增长+10%，投资收益+5%
- 悲观场景: 收入不变，通胀+3%，医疗支出增加
- 压力测试: 失业 6 个月 / 重大医疗
""",
        "category": "行业垂直Skill",
        "sub_category": "金融服务",
        "tags": ["财务规划", "退休", "现金流", "投资", "场景分析"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "anthropics",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "学以致用框架 Skill",
        "desc": "来自 davila7 的 Ship-Learn-Next 框架：将学习内容（视频、文章、教程）转化为可执行的实施计划",
        "content": """# 学以致用框架 (Ship-Learn-Next)

> 来源: [claude-code-templates](https://github.com/davila7/claude-code-templates) (30K+ stars)
> 许可证: MIT

将学习内容转化为可执行的实施计划。

## 1. 框架核心

```
SHIP (交付) → LEARN (学习) → NEXT (下一步)
```

### SHIP: 你已经知道了什么？
- 列出你已经可以立即行动的事项
- 不需要更多学习就能做的事
- 最小可行行动是什么？

### LEARN: 还需要学什么？
- 识别知识缺口
- 找到最高效的学习资源
- 设定学习时间预算

### NEXT: 下一步具体做什么？
- 定义 3 个具体行动步骤
- 每个步骤有明确的完成标准
- 设定时间期限

## 2. 内容转化流程

### 输入: 学习内容
- YouTube 视频文字稿
- 博客文章
- 在线课程笔记
- 播客摘要

### 输出: 行动计划
```markdown
# [内容标题] 行动计划

## 核心要点 (3-5 条)
1. [要点]
2. [要点]
3. [要点]

## 立即行动 (SHIP)
- [ ] [今天就能做的事]
- [ ] [本周能完成的事]

## 深入学习 (LEARN)
- [ ] [需要学的概念] → [推荐资源]
- [ ] [需要学的技能] → [练习方法]

## 下一步 (NEXT)
1. [具体行动] - 截止 [日期]
2. [具体行动] - 截止 [日期]
3. [具体行动] - 截止 [日期]

## 检验标准
- [ ] 能向别人解释清楚核心概念
- [ ] 完成了一个小项目/作品
- [ ] 形成了自己的方法论
```

## 3. 学习原则

- **80/20 法则**: 聚焦 20% 的核心内容
- **费曼技巧**: 能用简单语言解释就是真懂了
- **刻意练习**: 在弱点上多花时间
- **间隔重复**: 定期回顾已学内容
""",
        "category": "学习科研助手",
        "sub_category": "学习方法",
        "tags": ["学习方法", "行动计划", "知识转化", "Ship-Learn-Next"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "davila7",
        "source_type": "开源改编",
        "license": "MIT",
    },
    # ==================== 第8批: 专业实用类 Skill ====================
    # 来源: affaan-m/ECC (239K⭐), coreyhaines31/marketingskills (44K⭐),
    #        amruthpillai/reactive-resume (40K⭐), github/awesome-copilot (37K⭐),
    #        LeoYeAI/openclaw-master-skills, AgriciDaniel/claude-ads, alibaba/spring-ai-alibaba
    {
        "title": "AI视频剪辑工作流 Skill",
        "desc": "AI辅助的视频编辑全流程工作流，涵盖从原始素材到FFmpeg、Remotion、ElevenLabs、fal.ai，再到Descript/CapCut最终润色的完整管线",
        "content": """# AI视频剪辑工作流

> 来源: [affaan-m/ECC](https://github.com/affaan-m/ECC) - video-editing
> 许可证: MIT | 239K+ Stars

AI辅助的视频编辑工作流程，用于剪辑、构建和增强实拍素材。

## 完整视频制作管线

### 1. 素材采集与整理
- 原始素材导入（视频、音频、图片）
- 素材分类与标记（按场景、镜头、质量）
- 转录与字幕生成（自动语音识别）
- 素材质量评估（分辨率、帧率、色彩）

### 2. 粗剪阶段
- 按脚本/大纲组织素材时间线
- 选取最佳镜头（take selection）
- 建立叙事节奏（pacing）
- 确定转场节点

### 3. 精剪与增强
- **FFmpeg 命令行处理**: 转码、裁剪、合并、滤镜
- **Remotion 程序化视频**: React代码生成动态图形
- **AI配音**: ElevenLabs 语音合成
- **AI图像/视频生成**: fal.ai 补充B-roll

### 4. 后期润色
- 调色与色彩校正
- 音频混合与降噪
- 字幕与图形叠加
- 多平台输出适配（横屏/竖屏/方形）

### 5. 工具链集成
| 环节 | 推荐工具 |
|------|----------|
| 粗剪 | Descript, CapCut |
| 特效 | Remotion, After Effects |
| 转码 | FFmpeg |
| 配音 | ElevenLabs |
| AI素材 | fal.ai (Seedance, Kling, Veo 3) |
| 字幕 | Whisper + 手动校正 |

## 适用场景
- 短视频/Vlog 制作
- 产品演示视频
- 音乐视频/创意剪辑
- 教程/课程内容录制
""",
        "category": "文案内容创作",
        "sub_category": "短视频脚本",
        "tags": ["视频剪辑", "FFmpeg", "Remotion", "ElevenLabs", "CapCut", "Descript", "视频制作"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "React视频创作Remotion Skill",
        "desc": "Remotion最佳实践，用React代码创建程序化视频，29条领域规则涵盖3D动画、音频同步、字幕、图表、转场等",
        "content": """# React视频创作 Remotion 最佳实践

> 来源: [affaan-m/ECC](https://github.com/affaan-m/ECC) - remotion-video-creation
> 许可证: MIT | 239K+ Stars

用 React 代码创建视频的 29 条领域特定规则。

## 核心规则

### 基础架构
1. **Composition 结构**: 每个视频场景一个 Composition
2. **帧驱动动画**: 使用 useCurrentFrame() + useVideoConfig()
3. **序列编排**: <Sequence> 控制时间线片段
4. **响应式尺寸**: 根据平台选择分辨率
   - 横屏 16:9 → 1920x1080
   - 竖屏 9:16 → 1080x1920
   - 方形 1:1 → 1080x1080

### 动画系统
5. **spring() 弹性动画**: 自然的物理运动
6. **interpolate() 插值**: 帧到属性的映射
7. **Easing 缓动函数**: 控制运动曲线
8. **分层动画**: 透明度 + 位移 + 缩放叠加

### 音频处理
9. **音频同步**: useAudioData() 获取音频频谱
10. **节拍检测**: 基于音频能量触发视觉
11. **音量控制**: 淡入淡出避免爆音

### 字幕与文本
12. **动态字幕**: 基于时间码的字幕组件
13. **文字动画**: 逐字/逐行出现效果
14. **字体加载**: @font-face 确保一致性

### 数据可视化
15. **图表组件**: 支持 D3/Recharts 集成
16. **动态数据**: 从 API/JSON 驱动图表
17. **过渡动画**: 数据切换时的平滑过渡

### 3D 与高级效果
18. **React Three Fiber**: 3D 场景集成
19. **着色器效果**: 自定义 GLSL 效果
20. **粒子系统**: 基于帧的粒子动画

### 输出与部署
21. **渲染命令**: npx remotion render
22. **编解码器选择**: H.264 通用 / ProRes 高质量
23. **并行渲染**: 多核加速渲染
24. **Lambda 云渲染**: AWS 分布式渲染

## 适用场景
- 数据可视化动画
- 产品功能演示
- 社交媒体动态内容
- 自动化报告视频
""",
        "category": "文案内容创作",
        "sub_category": "短视频脚本",
        "tags": ["Remotion", "React", "程序化视频", "动画", "3D", "数据可视化"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "SEO智能诊断 Skill",
        "desc": "全面的SEO审计诊断工具，诊断技术SEO、页面优化、Core Web Vitals等问题，提供可执行的修复方案",
        "content": """# SEO智能诊断

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - seo-audit
> 许可证: MIT | 44K+ Stars

系统化的 SEO 审计框架，诊断网站搜索可见性问题。

## 审计流程

### 1. 技术 SEO 审计
- **爬取分析**: robots.txt、sitemap.xml、爬取预算
- **索引状态**: Google Search Console 覆盖率报告
- **页面速度**: Core Web Vitals (LCP, FID, CLS)
- **移动友好**: 移动端可用性检查
- **HTTPS**: SSL 证书与安全状态
- **结构化数据**: Schema.org 标记验证

### 2. 页面 SEO 审计
- **Title Tag**: 长度、关键词包含、唯一性
- **Meta Description**: 吸引力、长度、CTA
- **H1-H6 层级**: 标题结构合理性
- **URL 结构**: 简洁、含关键词、无冗余参数
- **内链布局**: 锚文本多样性、链接深度
- **图片优化**: alt 文本、文件大小、WebP 格式

### 3. 内容 SEO 审计
- **关键词覆盖**: 目标关键词的内容深度
- **搜索意图匹配**: 信息型/导航型/交易型
- **内容新鲜度**: 更新时间、过时内容识别
- **E-E-A-T**: 经验、专业、权威、可信
- **内容差距**: 竞品有而你没有的关键词

### 4. 外链与权威
- **反向链接质量**: 域名权重、相关性
- **锚文本分布**: 自然 vs 过度优化
- **有害链接**: 识别并准备 disavow

### 5. 本地 SEO（如适用）
- **NAP 一致性**: 名称、地址、电话
- **Google Business Profile**: 完善度
- **本地引用**: 行业目录覆盖

## 输出格式
- 问题严重度分级（Critical / Warning / Info）
- 每个问题的具体修复步骤
- 优先级排序（影响 × 难度）
- 预期效果时间线
""",
        "category": "文案内容创作",
        "sub_category": "公众号文案",
        "tags": ["SEO", "技术SEO", "网站优化", "搜索引擎排名", "审计"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "AI搜索优化 Skill",
        "desc": "优化内容以被ChatGPT、Perplexity等AI搜索引擎引用和展示，覆盖AEO/GEO/LLMO等前沿策略",
        "content": """# AI搜索优化 (AEO/GEO/LLMO)

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - ai-seo
> 许可证: MIT | 44K+ Stars

让内容被 AI 助手和 AI 搜索引擎引用、推荐和展示。

## 核心策略

### 1. 理解 AI 搜索
- **AI Overviews**: Google AI 摘要引用
- **ChatGPT Search**: OpenAI 搜索结果
- **Perplexity**: 带引用的 AI 回答
- **Claude/Gemini**: 大模型知识引用

### 2. 内容优化
- **直接回答格式**: 用简洁段落回答常见问题
- **FAQ 结构**: 问题-答案对便于 AI 提取
- **数据与统计**: 具体数字增加可信度
- **引用权威来源**: 链接到可信来源
- **避免模糊表述**: 用具体、可验证的陈述

### 3. 技术实施
- **llms.txt 规范**: 在网站根目录提供 AI 友好的站点说明
- **OKF (Open Knowledge Format)**: 结构化知识格式
- **Schema Markup**: 结构化数据帮助 AI 理解
- **语义 HTML**: 清晰的标题层级和内容结构

### 4. 监控与衡量
- **AI 引用追踪**: 监控被 AI 引用的频率
- **零点击搜索**: 关注直接回答的曝光
- **品牌提及**: AI 回答中的品牌出现率

## 与传统 SEO 的区别
| 维度 | 传统 SEO | AI 搜索优化 |
|------|---------|------------|
| 目标 | 搜索排名 | 被 AI 引用 |
| 格式 | 长文+关键词 | 简洁+结构化 |
| 技术 | meta标签 | llms.txt + Schema |
| 衡量 | 排名/流量 | 引用率/提及率 |
""",
        "category": "文案内容创作",
        "sub_category": "公众号文案",
        "tags": ["AI搜索", "AEO", "GEO", "LLMO", "ChatGPT", "Perplexity", "llms.txt"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "营销心理学 Skill",
        "desc": "将行为科学和认知偏差应用于营销，涵盖社会认同、稀缺性、锚定效应、损失厌恶等核心心理模型",
        "content": """# 营销心理学

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - marketing-psychology
> 许可证: MIT | 44K+ Stars

应用心理学原理和行为科学到营销实践中。

## 核心心理模型

### 1. 认知偏差
- **锚定效应**: 先展示高价产品，让后续价格显得合理
- **损失厌恶**: 「你将失去」比「你将获得」更有效
- **框架效应**: 同一信息的不同呈现方式影响决策
- **确认偏差**: 人们倾向于寻找支持已有观点的信息

### 2. 社会影响力
- **社会认同**: 「已有10,000人选择」的从众效应
- **权威效应**: 专家背书和资质展示
- **互惠原则**: 先给予价值再请求行动
- **承诺一致**: 小承诺引导大决策

### 3. 决策模型
- **稀缺性**: 限时/限量创造紧迫感
- **选择悖论**: 选项过多导致决策瘫痪
- **峰终定律**: 体验的高峰和结尾决定记忆
- **心理账户**: 不同来源的钱被不同对待

### 4. 实战应用

#### 落地页优化
- Hero 区域：一句话说清价值 + 社会认同
- CTA 按钮：行动导向文案 + 降低风险感知
- 定价展示：锚定价格 + 推荐方案高亮

#### 邮件营销
- 主题行：好奇心 + 紧迫感
- 正文：故事 + 数据 + 社会认同
- CTA：单一明确行动 + 损失规避

#### 产品定价
- 三档定价策略（诱饵效应）
- 年付 vs 月付的心理账户
- 免费试用 → 沉没成本 → 转化

## 使用原则
- 道德使用：帮助而非操纵
- A/B 测试验证假设
- 数据驱动迭代优化
""",
        "category": "文案内容创作",
        "sub_category": "海报文案",
        "tags": ["营销心理学", "认知偏差", "行为科学", "转化率优化", "消费者行为"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "电商产品图生成 Skill",
        "desc": "为电商平台生成专业产品图片，支持8种视觉风格和6种场景类型，适配Amazon、Shopify、淘宝等",
        "content": """# 电商产品图生成

> 来源: [LeoYeAI/openclaw-master-skills](https://github.com/LeoYeAI/openclaw-master-skills) - product-image-generator
> 许可证: MIT

为电商平台生成专业的产品图片。

## 8种视觉风格

1. **纯白背景**: 产品主体突出，适合主图
2. **生活场景**: 产品在真实使用场景中
3. **极简美学**: 高级感留白 + 产品
4. **科技感**: 暗色调 + 光效 + 产品
5. **自然清新**: 植物/自然元素搭配
6. **节日主题**: 节日氛围装饰
7. **对比展示**: 使用前/后对比
8. **信息图式**: 产品 + 卖点标注

## 6种场景类型

| 场景 | 适用类目 | 说明 |
|------|---------|------|
| 棚拍 | 全品类 | 专业灯光、纯背景 |
| 家居 | 家居/家电 | 真实家居环境 |
| 户外 | 运动/旅行 | 自然光线户外场景 |
| 办公 | 3C/文具 | 现代办公桌面 |
| 美食 | 食品/厨具 | 美食摆盘场景 |
| 美妆 | 护肤/彩妆 | 梳妆台/浴室场景 |

## 平台适配规范
- **淘宝/天猫**: 800x800 主图，白底优先
- **京东**: 800x800，白底要求严格
- **Amazon**: 2000x2000，纯白背景(RGB 255,255,255)
- **Shopify**: 推荐 2048x2048 正方形
- **拼多多**: 750x352 轮播图

## 使用流程
1. 提供产品照片（至少1张清晰产品图）
2. 选择目标平台和风格
3. 指定场景类型
4. AI 生成多张候选图
5. 选择最佳方案微调
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["电商", "产品图", "淘宝", "Amazon", "Shopify", "AI生图"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "LeoYeAI",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "产品虚拟摄影 Skill",
        "desc": "从一张产品照片生成多角度营销级产品摄影，涵盖生活场景、微距细节、比例展示、营销排版四个方向",
        "content": """# 产品虚拟摄影

> 来源: [jau123/MeiGen-AI-Design-MCP](https://github.com/jau123/MeiGen-AI-Design-MCP) - product-photoshoot
> 许可证: MIT

从一张产品照片生成多方向营销级产品摄影。

## 四个输出方向

### 1. 生活场景图 (Lifestyle Scene)
- 产品在真实使用环境中的样子
- 自然光线、温暖色调
- 传达产品融入生活的感觉
- 适合社交媒体和广告

### 2. 微距细节图 (Macro Detail)
- 产品材质、纹理、工艺的极致特写
- 展示品质感和做工
- 突出设计细节和材质优势
- 适合产品详情页

### 3. 比例/场景图 (Scale/Context)
- 展示产品实际大小
- 与日常物品对比帮助感知尺寸
- 手持/桌面等真实比例场景
- 减少线上购物的尺寸不确定性

### 4. 营销排版图 (Marketing Layout)
- 产品 + 文案 + 卖点标注
- 适合落地页 Hero 图
- 品牌色协调
- 可直接用于广告素材

## 工作流程
1. 上传一张产品参考照片
2. 选择品牌风格（可选）
3. AI 自动生成 4 个方向的图片
4. 每个方向提供 2-3 个变体
5. 选择最佳方案进行微调

## 适用场景
- 电商新品上架（一次性生成全套产品图）
- 广告素材批量制作
- 社交媒体内容配图
- 品牌视觉统一
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["产品摄影", "电商", "虚拟摄影", "营销图片", "AI生图"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "jau123",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "广告创意批量生成 Skill",
        "desc": "为各付费广告平台批量生成广告创意，包括标题、描述、主文案和完整广告变体，支持静态/动态/无脸视频广告",
        "content": """# 广告创意批量生成

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - ad-creative
> 许可证: MIT | 44K+ Stars

为付费广告规模化生成创意内容。

## 覆盖平台
- **Google Ads**: RSA 响应式搜索广告
- **Facebook/Meta**: 图片广告、视频广告、轮播广告
- **LinkedIn**: 单图广告、文档广告、思考领导广告
- **TikTok**: 信息流视频广告
- **小红书**: 种草笔记广告

## 创意类型

### 静态广告
- 单图广告文案 + 图片描述
- 标题变体（至少5个）
- 描述文案（长/短版本）
- CTA 按钮文案

### 视频广告
- **无脸视频**: 产品 + 文字 + 配音脚本
- **真人风格**: 场景描述 + 台词 + 镜头指示
- **动画解说**: 分镜脚本 + 旁白
- **UGC风格**: 用户证言式脚本

### 创意策略
- **痛点切入**: 从用户问题出发
- **利益驱动**: 强调使用后的好处
- **社会认同**: 客户评价/数据背书
- **对比法**: 使用前后的差异
- **紧迫感**: 限时优惠/限量

## 工作流程
1. 输入产品信息和目标受众
2. 定义广告目标（品牌认知/转化/再营销）
3. 选择创意方向（3-5个角度）
4. 批量生成每个角度的变体
5. 创意审查与优化建议
6. 按平台格式输出

## 创意效果评估
- 创意多样性评分
- 平台规范合规检查
- A/B 测试建议
- 历史效果数据参考
""",
        "category": "文案内容创作",
        "sub_category": "海报文案",
        "tags": ["广告创意", "Google Ads", "Facebook广告", "广告文案", "批量生成"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "营销文案润色 Skill",
        "desc": "编辑、审查和改进现有营销文案，不是从零写而是让已有文案更好：更精炼、更锐利、更转化",
        "content": """# 营销文案润色

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - copy-editing
> 许可证: MIT | 44K+ Stars

编辑、审查和改进已有的营销文案。

## 润色维度

### 1. 清晰度检查
- 一句话能否更短？
- 有没有行话/术语可以替换？
- 主语和谓语是否紧邻？
- 读者能否 3 秒内理解核心意思？

### 2. 说服力增强
- 开头是否足够抓人？（前 7 个字决定一切）
- 价值主张是否明确？（用户能得到什么？）
- CTA 是否具体有力？（下一步做什么？）
- 社会认同是否充分？（凭什么相信你？）

### 3. 节奏与韵律
- 长短句交替创造节奏感
- 段落长度变化避免视觉疲劳
- 关键信息独立成段
- 列表打破大段文字

### 4. 品牌一致性
- 语气是否符合品牌调性？
- 用词是否统一？（同一概念不要换词）
- 人称是否一致？（你/您 不要混用）

### 5. 转化优化
- 每个段落是否有明确目的？
- 是否有不必要的信息可以删除？
- 行动路径是否清晰？
- 风险感知是否已降低？

## 润色流程
1. **通读全文**: 标记第一印象的问题
2. **结构分析**: 信息层级是否合理
3. **逐段精修**: 每句话都有存在的理由
4. **数据验证**: 数字和事实的准确性
5. **朗读测试**: 读出来别扭就改
6. **对比原版**: 标注修改点和理由

## 常见修改
- 「我们提供XXX」→「你将获得XXX」
- 「业界领先」→ 具体数据
- 「请点击」→ 行动导向文案
- 被动语态 → 主动语态
- 模糊表述 → 具体数字
""",
        "category": "文案内容创作",
        "sub_category": "公文写作",
        "tags": ["文案润色", "内容优化", "文案审查", "编辑", "转化率"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "专业简历生成 Skill",
        "desc": "通过对话式AI生成专业简历，符合Reactive Resume标准，支持PDF导出，涵盖个人信息、经历、技能等完整板块",
        "content": """# 专业简历生成

> 来源: [amruthpillai/reactive-resume](https://github.com/amruthpillai/reactive-resume) - resume-builder
> 许可证: MIT | 40K+ Stars

通过对话生成专业简历。

## 简历板块

### 1. 个人信息
- 姓名、联系方式、LinkedIn、GitHub
- 个人简介/职业目标（2-3句话）
- 所在城市/远程偏好

### 2. 工作经历
- 按时间倒序排列
- 每段经历用 STAR 法则描述:
  - **Situation**: 背景是什么
  - **Task**: 你的职责是什么
  - **Action**: 你做了什么
  - **Result**: 取得了什么成果（量化）
- 示例: 「主导微服务架构迁移，系统可用性从99.5%提升至99.99%，年节省运维成本30万」

### 3. 项目经历
- 项目名称和个人角色
- 技术栈和规模
- 核心贡献和成果
- GitHub 链接（如有）

### 4. 教育背景
- 学校、专业、学位
- GPA（如 > 3.5）
- 相关课程/荣誉

### 5. 技能清单
- 按类别分组（语言/框架/工具/平台）
- 熟练度标注（精通/熟练/了解）

### 6. 其他板块
- 证书/资质
- 开源贡献
- 演讲/发表
- 志愿者经历

## 简历原则
- **一页原则**: 10年以下经验控制在一页
- **量化成果**: 用数字说话
- **关键词优化**: 匹配目标职位 JD
- **去隐私**: 不放照片/年龄/婚姻状况
- **PDF 输出**: 确保格式不跑版

## 输出格式
- JSON (符合 Reactive Resume Schema)
- 可导入 rxresu.me 在线编辑
- 支持导出 PDF/Word
""",
        "category": "行业垂直Skill",
        "sub_category": "职场咨询",
        "tags": ["简历", "求职", "职业发展", "PDF", "Reactive Resume"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "amruthpillai",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "技术求职助手 Skill",
        "desc": "软件工程师求职全流程助手，包括JD分析、简历定制、求职信撰写、Offer评估、面试后跟进邮件",
        "content": """# 技术求职助手

> 来源: [github/awesome-copilot](https://github.com/github/awesome-copilot) - technical-job-search
> 许可证: MIT | 37K+ Stars

软件工程师求职全流程辅助工具。

## 功能模块

### 1. JD 分析
- 解析职位描述中的关键要求
- 提取必备技能 vs 加分项
- 评估匹配度（高/中/低）
- 识别关键词用于简历优化

### 2. 简历定制
- 根据目标 JD 调整简历重点
- 重新排列技能顺序
- 突出最相关的项目经历
- 量化成果匹配 JD 要求

### 3. 求职信撰写
- 开头：为什么对这家公司/职位感兴趣
- 中间：2-3个最匹配的亮点
- 结尾：明确的行动号召
- 控制在一页以内

### 4. Offer 评估
- 薪资构成分析（base + equity + bonus）
- 生活成本调整（城市对比）
- 职业发展路径评估
- 工作生活平衡考量
- 决策矩阵打分

### 5. 面试跟进
- 感谢信模板
- 面试中未答好的问题补充
- 表达对职位的持续兴趣
- 时间节点的把握

## 使用流程
1. 分享目标职位 JD
2. 提供当前简历
3. AI 分析匹配度并给出建议
4. 定制简历 + 撰写求职信
5. 面试准备要点
6. 面试后跟进邮件

## 注意事项
- 不要编造经历
- 诚实评估技能水平
- 每封求职信都要针对性定制
- 保持专业但有个性的表达
""",
        "category": "行业垂直Skill",
        "sub_category": "职场咨询",
        "tags": ["求职", "简历", "面试", "Offer评估", "求职信", "技术岗位"],
        "fit_tools": ["Copilot", "Claude", "Cursor"],
        "author": "github",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "商品文案写作 Skill",
        "desc": "阿里巴巴开源的商品文案写作助手，根据商品信息自动生成吸引人的营销文案，支持多风格多平台",
        "content": """# 商品文案写作

> 来源: [alibaba/spring-ai-alibaba](https://github.com/alibaba/spring-ai-alibaba) - copywriting
> 许可证: Apache 2.0 | 10K+ Stars

根据商品信息生成吸引人的营销文案。

## 文案类型

### 1. 商品标题
- 核心关键词 + 属性词 + 卖点词
- 示例: 「2024新款轻薄笔记本电脑 14英寸高性能商务办公学生本」
- 原则: 关键词前置、信息密度高、不堆砌

### 2. 卖点提炼
- 从产品参数提取用户利益
- 技术语言 → 用户语言
- 示例:
  - 参数: 「5000mAh电池」→ 卖点: 「充一次用两天」
  - 参数: 「1.2kg轻薄」→ 卖点: 「放包里忘了它的存在」

### 3. 详情页文案
- 首屏: 核心卖点 + 促销信息
- 痛点引入: 用户遇到了什么问题
- 解决方案: 产品如何解决
- 产品优势: 3-5个核心卖点详述
- 规格参数: 清晰的信息表格
- 售后保障: 降低决策风险

### 4. 推广短文案
- 朋友圈/小红书种草文案
- 直播口播脚本
- 短视频带货文案

## 写作原则
- **用户视角**: 说用户关心的，不说你想说的
- **具体化**: 「续航12小时」而非「超长续航」
- **场景化**: 描述使用场景而非罗列参数
- **差异化**: 找到竞品没有的卖点
- **信任感**: 数据、认证、用户评价

## 平台适配
- **淘宝/天猫**: 标题30字内，详情页重视觉
- **京东**: 标题45字内，重视规格参数
- **拼多多**: 标题突出性价比
- **小红书**: 种草风格，真实体验感
- **抖音**: 前3秒抓眼球的文案
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["商品文案", "电商", "营销文案", "淘宝", "京东", "阿里巴巴"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "alibaba",
        "source_type": "开源改编",
        "license": "Apache2.0",
    },
    {
        "title": "内容策略规划 Skill",
        "desc": "规划内容策略，决定做什么内容、覆盖什么话题、如何建立内容支柱和编辑日历，而非写单篇内容",
        "content": """# 内容策略规划

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - content-strategy
> 许可证: MIT | 44K+ Stars

帮你决定做什么内容，而不只是写内容。

## 策略框架

### 1. 内容支柱 (Content Pillars)
确定 3-5 个核心话题领域:
- 每个支柱代表一个主题集群
- 支柱之间有关联但不完全重叠
- 每个支柱有明确的受众画像

### 2. 话题集群 (Topic Clusters)
每个支柱下建立话题集群:
- **核心内容**: 深度长文（2000+字）
- **支撑内容**: 针对子话题的中等文章
- **社交内容**: 短内容引流到长文
- 内链连接集群内所有内容

### 3. 编辑日历
- 发布频率（周更/日更）
- 内容类型轮换（博客/视频/播客/社交）
- 季节性/热点话题预留
- 内容生命周期管理

### 4. 内容差距分析
- 竞品覆盖了哪些你没有的话题？
- 用户搜索了什么你还没回答的问题？
- 哪些关键词有机会但缺少内容？

### 5. 内容分配
| 内容类型 | 频率 | 目的 |
|---------|------|------|
| 深度博客 | 2-4/月 | SEO + 权威 |
| 教程/指南 | 2/月 | 引流 + 转化 |
| 社交帖子 | 每日 | 互动 + 品牌 |
| 视频内容 | 2/月 | 多平台覆盖 |
| 邮件通讯 | 1/周 | 留存 + 转化 |

## 输出物
- 内容支柱定义文档
- 3个月话题清单
- 编辑日历模板
- 内容 KPI 指标定义
""",
        "category": "文案内容创作",
        "sub_category": "公众号文案",
        "tags": ["内容策略", "话题规划", "编辑日历", "内容营销", "话题集群"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "引流磁铁设计 Skill",
        "desc": "规划和创建用于邮件获客的引流磁铁，包括电子书、清单、模板、工具等免费资源的设计与分发策略",
        "content": """# 引流磁铁设计

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - lead-magnets
> 许可证: MIT | 44K+ Stars

创建用于邮件获客的高质量免费资源。

## 引流磁铁类型

### 1. 文档类
- **电子书/白皮书**: 深度内容（20-50页）
- **清单/Checklist**: 可打印的行动清单
- **模板**: 可直接使用的模板文件
- **案例研究**: 详细的成功故事

### 2. 工具类
- **计算器**: ROI计算、成本估算等
- **评估工具**: 自我诊断/评分工具
- **生成器**: 自动生成某种内容
- **对比表**: 产品/方案对比表格

### 3. 课程类
- **迷你课程**: 3-5天的邮件序列教学
- **工作坊录像**: 限时免费回放
- **网络研讨会**: 直播 + 回放

## 设计原则
- **解决具体问题**: 不要泛泛而谈
- **即时价值**: 下载后 5 分钟内就能获得收获
- **与产品关联**: 自然引导到付费产品
- **感知价值高**: 让人觉得「这居然是免费的」

## 分发策略
- **落地页**: 独立页面 + 简洁表单
- **内容升级**: 在相关博客文章中嵌入
- **弹窗**: 退出意图/滚动触发
- **社交推广**: 在社交平台分享片段

## 转化漏斗
1. 用户看到引流磁铁
2. 填写邮箱下载
3. 自动发送欢迎邮件 + 资源
4. 培育邮件序列（3-7封）
5. 引导到付费产品

## 效果衡量
- 下载转化率 > 30% 为优秀
- 邮件打开率 > 40%
- 培育序列到产品页点击率
- 最终付费转化率
""",
        "category": "文案内容创作",
        "sub_category": "海报文案",
        "tags": ["引流", "邮件营销", "获客", "落地页", "内容升级"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "销售物料制作 Skill",
        "desc": "创建销售团队需要的各类物料，包括销售PPT、一页纸、异议处理文档、演示脚本和销售手册",
        "content": """# 销售物料制作

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - sales-enablement
> 许可证: MIT | 44K+ Stars

为销售团队创建高效的成交辅助物料。

## 物料类型

### 1. 销售演示 (Pitch Deck)
- **结构**: 问题 → 方案 → 证明 → 行动
- **10/20/30法则**: 不超过10页、不超过20分钟、字号不小于30
- 每页一个核心信息
- 数据可视化优先

### 2. 一页纸 (One-Pager)
- 产品概述（一段话）
- 3-5个核心卖点
- 目标客户画像
- 典型使用场景
- 定价概览
- CTA（预约演示/免费试用）

### 3. 异议处理文档
- 列出常见异议（价格/功能/竞品/时机）
- 每个异议的应对话术
- 支撑数据/案例
- 格式: 「我理解...实际上...例如...」

### 4. 演示脚本 (Demo Script)
- 开场白（建立关联）
- 需求发现（提问引导）
- 功能演示（对应需求）
- 价值总结（回到业务价值）
- 下一步（明确行动）

### 5. ROI 分析模板
- 客户当前成本（痛点量化）
- 使用产品后的节省
- 投资回报周期
- 具体计算过程

### 6. 竞品对比 (Battle Card)
- 功能对比矩阵
- 我们的优势（攻击点）
- 我们的劣势（防守策略）
- 常见竞品话术应对

## 制作原则
- **客户视角**: 说客户关心的，不说你想说的
- **数据驱动**: 用数字说话
- **可操作**: 销售拿到就能用
- **定期更新**: 随产品和市场变化迭代
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["销售", "PPT", "演示", "异议处理", "销售手册", "Battle Card"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    # ==================== 第9批: 更多专业实用类 Skill ====================
    # 来源: bytedance/deer-flow (79K⭐), harry0703/MoneyPrinterTurbo (102K⭐),
    #        coreyhaines31/marketingskills (44K⭐), phuryn/pm-skills (25K⭐),
    #        alchaincyf/nuwa-skill (30K⭐), nextlevelbuilder (116K⭐)
    {
        "title": "多平台内容引擎 Skill",
        "desc": "为X/LinkedIn/TikTok/YouTube/Newsletter创建平台原生内容系统，一份素材多平台分发适配",
        "content": """# 多平台内容引擎

> 来源: [affaan-m/ECC](https://github.com/affaan-m/ECC) - content-engine
> 许可证: MIT | 239K+ Stars

一份素材，多平台原生内容系统。

## 核心能力

### 1. 内容适配规则
每个平台有不同的内容语法:
- **X/Twitter**: 短平快、hook前置、thread结构
- **LinkedIn**: 专业叙事、数据支撑、个人洞察
- **TikTok**: 前3秒hook、视觉冲击、趋势音乐
- **YouTube**: 缩略图+标题决定一切、前30秒留存
- **Newsletter**: 深度长文、个人声音、CTA明确
- **小红书**: 种草风格、emoji标题、真实体验

### 2. 内容日历
- 周度内容规划
- 平台发布频率建议
- 热点话题预留位
- 内容类型轮换

### 3. 一鱼多吃工作流
1. 创建核心长内容（博客/视频/播客）
2. 拆解为社交帖子（5-10条）
3. 提取金句做图文
4. 剪辑短视频片段
5. 整合到Newsletter
6. 制作thread/长推文

### 4. 平台适配模板
| 平台 | 字数 | 格式 | 最佳时间 |
|------|------|------|----------|
| X | 280字 | text+media | 9-11am |
| LinkedIn | 1300字 | text+doc | Tue-Thu |
| TikTok | 60s | video | 7-9pm |
| YouTube | 10min+ | video | Sat 9am |
| 小红书 | 1000字 | image+text | 12-2pm |

## 适用场景
- 个人品牌建设
- 产品发布多渠道推广
- 内容营销团队日常运营
""",
        "category": "文案内容创作",
        "sub_category": "公众号文案",
        "tags": ["内容引擎", "多平台", "社交媒体", "内容日历", "分发"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "affaan-m",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "社媒内容日历 Skill",
        "desc": "规划多平台社交媒体营销活动，从创意简报到发布排期的完整工作流",
        "content": """# 社媒内容日历

> 来源: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) - social-media-content-calendar
> 许可证: MIT | 229K+ Stars

多平台社交媒体营销日历规划。

## 规划流程

### 1. 明确目标
- 品牌认知 → 曝光类内容
- 用户互动 → 话题/投票/问答
- 转化导流 → CTA明确的内容
- 社区建设 → UGC/互动类

### 2. 内容支柱
确定 3-5 个内容方向:
- **教育类**: 教程、技巧、行业洞察
- **灵感类**: 案例、故事、用户证言
- **互动类**: 投票、问答、挑战赛
- **促销类**: 产品更新、限时优惠
- **幕后类**: 团队日常、开发过程

### 3. 排期模板
| 周一 | 周二 | 周三 | 周四 | 周五 | 周六 | 周日 |
|------|------|------|------|------|------|------|
| 行业洞察 | 教程 | 用户故事 | 产品更新 | 互动话题 | 幕后 | 休息/复盘 |

### 4. 内容简报模板
每条内容需包含:
- 平台 + 发布时间
- 内容类型（图文/视频/轮播）
- 核心信息（一句话）
- 视觉需求
- CTA
- 相关标签

### 5. 执行清单
- [ ] 内容创建
- [ ] 视觉素材准备
- [ ] 文案审核
- [ ] 排期设置
- [ ] 发布后监控
- [ ] 数据复盘

## 输出物
- 月度内容日历（30天规划）
- 每条内容的创意简报
- 平台适配建议
- KPI追踪表
""",
        "category": "文案内容创作",
        "sub_category": "海报文案",
        "tags": ["社交媒体", "内容日历", "营销规划", "排期", "运营"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "NousResearch",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "短视频自动生成 Skill",
        "desc": "MoneyPrinterTurbo自动化视频生成，从主题/脚本到成品MP4，支持短视频、营销视频、教育视频等",
        "content": """# 短视频自动生成 (MoneyPrinterTurbo)

> 来源: [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)
> 许可证: Apache 2.0 | 102K+ Stars

从一个主题自动生成完整短视频。

## 工作流程

### 1. 输入
- 主题/标题（如「5个Python编程技巧」）
- 或完整脚本
- 选择视频类型

### 2. 自动处理
1. **脚本生成**: AI 根据主题生成旁白脚本
2. **语音合成**: TTS 生成配音音频
3. **字幕生成**: 基于音频自动对齐字幕
4. **素材匹配**: 自动搜索/生成匹配画面
5. **视频合成**: 拼接素材 + 音频 + 字幕
6. **背景音乐**: 添加免版权BGM

### 3. 视频类型
- **口播类**: 配音 + 字幕 + 相关画面
- **教程类**: 屏幕录制 + 旁白
- **营销类**: 产品展示 + 卖点文案
- **知识类**: 信息图 + 解说
- **混剪类**: 素材库 + AI剪辑

### 4. 配置选项
| 参数 | 说明 |
|------|------|
| 分辨率 | 1080x1920(竖) / 1920x1080(横) |
| 时长 | 15s / 30s / 60s / 自定义 |
| 语速 | 0.5x - 2.0x |
| 字幕样式 | 位置/字体/颜色/大小 |
| BGM | 自动匹配/指定/无 |
| TTS引擎 | Edge TTS / Azure / 自定义 |

### 5. 批量生成
- 一次输入多个主题
- 自动排队处理
- 输出到指定目录

## 适用场景
- 抖音/快手短视频批量制作
- 产品营销视频
- 知识科普类视频
- 新闻资讯类视频
""",
        "category": "文案内容创作",
        "sub_category": "短视频脚本",
        "tags": ["视频生成", "MoneyPrinterTurbo", "自动化", "短视频", "TTS", "批量"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "harry0703",
        "source_type": "开源改编",
        "license": "Apache2.0",
    },
    {
        "title": "播客生成器 Skill",
        "desc": "字节跳动Deer-Flow开源的播客生成器，将文本内容转换为双主持人对话式播客音频",
        "content": """# 播客生成器

> 来源: [bytedance/deer-flow](https://github.com/bytedance/deer-flow) - podcast-generation
> 许可证: MIT | 79K+ Stars

将文本内容转换为自然对话式播客音频。

## 工作流程

### 1. 内容输入
- 文章/报告/研究文本
- 主题大纲
- 已有脚本

### 2. 脚本生成
AI 将输入内容转换为双主持人对话:
- **Host A**: 提问者/引导者，推动话题
- **Host B**: 专家/回应者，提供深度见解

对话特点:
- 自然口语化表达
- 有来有回的互动
- 适当加入类比和例子
- 关键数据点的强调
- 过渡自然不生硬

### 3. 脚本结构
```
[开场] 话题引入 + 为什么重要
[主体] 3-5个核心观点展开
  - 每个观点: 解释 → 例子 → 洞察
[互动] 反问/讨论/不同视角
[收尾] 总结要点 + 行动建议
```

### 4. 音频生成
- 双声音 TTS（男+女 或 女+女）
- 自然的语速变化
- 适当的停顿和语气词
- 可选背景音乐

### 5. 输出格式
- 完整对话脚本（文本）
- 播客音频（MP3/WAV）
- 时间轴标记

## 适用场景
- 将研究报告转为音频内容
- 文章内容二次分发
- 教育内容音频化
- 会议纪要语音化
""",
        "category": "文案内容创作",
        "sub_category": "短视频脚本",
        "tags": ["播客", "音频生成", "对话", "TTS", "字节跳动", "Deer-Flow"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "bytedance",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "文章转播客脚本 Skill",
        "desc": "将Markdown文章转换为1-4人自然对话播客脚本，支持中英文，保留专业术语",
        "content": """# 文章转播客脚本

> 来源: [digoal/blog](https://github.com/digoal/blog) - article-to-podcast-script
> 许可证: MIT

将 Markdown 文章转换为多人播客对话脚本。

## 转换规则

### 1. 角色设定
- **1人模式**: 独白式播客，第一人称叙述
- **2人模式**: 主持+嘉宾对话
- **3人模式**: 主持+嘉宾+提问者
- **4人模式**: 圆桌讨论

### 2. 对话风格
- 口语化但不失专业
- 自然打断和接话
- 适当加入感叹/疑问
- 用类比解释复杂概念
- 保留英文专业术语

### 3. 结构转换
| 文章结构 | 播客转换 |
|---------|----------|
| 标题 | 开场话题引入 |
| 摘要 | 主持人概述 |
| 章节 | 对话话题切换 |
| 代码/数据 | 口语化解释 |
| 引用 | 嘉宾引述 |
| 结论 | 总结+行动建议 |

### 4. 脚本格式
```
Host1: 大家好，欢迎收听本期节目...
Host2: 今天我们来聊一个很有意思的话题...
Host1: 对，我看到文章里提到...
Host2: 是的，其实这个意思是...
```

### 5. 特殊处理
- 代码块 → 口述解释逻辑
- 表格 → 对比讨论
- 图片 → 描述性语言
- 公式 → 直觉解释

## 输出
- .txt 格式的播客脚本
- 默认中文，保留英文术语
- 可指定语言输出
""",
        "category": "文案内容创作",
        "sub_category": "短视频脚本",
        "tags": ["播客脚本", "文章转换", "对话生成", "多人播客", "中文"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "digoal",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "KOL营销合作 Skill",
        "desc": "运营网红/创作者/品牌大使合作计划，从寻找伙伴到结构化合约、效果衡量的全流程",
        "content": """# KOL营销合作

> 来源: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) - influencer-marketing
> 许可证: MIT | 44K+ Stars

运营KOL/创作者/品牌大使合作的全流程指南。

## 工作流程

### 1. 寻找合作伙伴
- 定义理想KOL画像
- 平台选择（抖音/小红书/B站/微博）
- 筛选标准:
  - 粉丝量级（头部/腰部/尾部）
  - 互动率 > 粉丝数
  - 内容调性匹配
  - 受众画像重合度

### 2. 评估与出价
- CPM/CPE 计算
- 合作形式定价参考:
  | 形式 | 价格区间 |
  |------|----------|
  | 图文种草 | 500-50000 |
  | 短视频 | 1000-100000 |
  | 直播专场 | 5000-200000 |
  | 品牌大使 | 月框谈判 |

### 3. 合作Brief
- 品牌背景（简短）
- 产品信息 + 核心卖点
- 目标受众
- 内容方向建议（非强制）
- 必须包含的信息
- 禁忌事项
- 时间节点

### 4. 合规要求
- FTC/广告法披露要求
- #广告 #合作 标记
- 虚假宣传红线
- 竞品排他条款

### 5. 效果衡量
- **曝光指标**: 播放量/阅读量
- **互动指标**: 点赞/评论/分享
- **转化指标**: 链接点击/优惠码使用
- **ROI计算**: (收益-成本)/成本

### 6. 长期关系
- 优秀KOL转为品牌大使
- 定期复盘优化
- 建立创作者社群

## 适用场景
- 新品上市KOL推广
- 日常种草合作
- 品牌大使计划
- UGC内容采购
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["KOL", "网红营销", "品牌合作", "创作者", "达人推广"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "coreyhaines31",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "NDA保密协议起草 Skill",
        "desc": "起草双方保密协议(NDA)，涵盖信息类型、管辖区域、保密期限等条款，支持多法域",
        "content": """# NDA保密协议起草

> 来源: [phuryn/pm-skills](https://github.com/phuryn/pm-skills) - draft-nda
> 许可证: MIT | 25K+ Stars

起草专业的保密协议(NDA)。

## NDA核心条款

### 1. 协议双方
- 披露方(Disclosing Party)
- 接收方(Receiving Party)
- 双方信息完整登记

### 2. 保密信息定义
- 书面标记为「保密」的信息
- 口头披露后书面确认的信息
- 合理应被视为保密的信息
- 排除项:
  - 公知信息
  - 接收前已拥有
  - 独立开发
  - 第三方合法提供

### 3. 保密义务
- 不低于保护自身信息的程度
- 不低于合理注意程度
- 仅限「需要知道」的人员
- 不得反向工程

### 4. 期限
- 协议有效期
- 保密义务存续期（通常2-5年）
- 商业秘密：无期限

### 5. 违约救济
- 禁令救济权
- 损害赔偿
- 返还/销毁义务

### 6. 管辖区域
- 适用法律
- 争议解决方式
- 仲裁/诉讼选择

## 使用流程
1. 确定NDA类型（单向/双向）
2. 填写双方信息
3. 定义保密信息范围
4. 设定保密期限
5. 选择管辖法律
6. 审核并签署

## 免责声明
本工具生成的文档仅供参考，不构成法律建议。重要协议请咨询专业律师。
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["NDA", "保密协议", "法律文档", "合同", "合规"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "phuryn",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "隐私政策起草 Skill",
        "desc": "起草详细的隐私政策文档，涵盖数据类型、管辖区域、GDPR合规等，适用于网站和App",
        "content": """# 隐私政策起草

> 来源: [phuryn/pm-skills](https://github.com/phuryn/pm-skills) - privacy-policy
> 许可证: MIT | 25K+ Stars

起草符合法规要求的隐私政策。

## 隐私政策结构

### 1. 概述
- 运营实体信息
- 政策适用范围
- 联系方式

### 2. 收集的信息
- **个人信息**: 姓名、邮箱、电话、地址
- **账户信息**: 用户名、密码（加密存储）
- **支付信息**: 卡号（由支付网关处理）
- **设备信息**: 设备ID、操作系统、IP地址
- **使用数据**: 浏览记录、点击行为、使用时长
- **Cookie**: 类型、用途、管理方式

### 3. 收集方式
- 用户直接提供
- 自动收集
- 第三方来源

### 4. 使用目的
- 提供服务
- 账户管理
- 客户支持
- 产品改进
- 营销通讯（可退订）
- 法律合规

### 5. 数据共享
- 服务提供商
- 法律要求
- 业务转让
- 用户同意

### 6. 用户权利
- 访问权
- 更正权
- 删除权
- 可携带权
- 反对权
- 撤回同意

### 7. 合规框架
- **GDPR** (欧盟): 数据保护官、DPIA
- **CCPA** (加州): 不出售个人信息
- **个人信息保护法** (中国): 告知同意
- **PDPA** (东南亚): 数据保护

### 8. 其他
- 数据保留期限
- 安全措施说明
- 儿童隐私保护
- 政策更新通知
- 跨境传输

## 免责声明
本文档仅供参考，不构成法律建议。请根据实际业务情况调整并咨询法律专业人士。
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["隐私政策", "GDPR", "合规", "数据保护", "法律文档"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "phuryn",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "商业合同撰写 Skill",
        "desc": "生成专业商业文档：自由职业合同、项目提案、SOW工作说明书、NDA、MSA主服务协议",
        "content": """# 商业合同撰写

> 来源: [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) - contract-and-proposal-writer
> 许可证: MIT | 24K+ Stars

生成专业的商业法律文档。

## 文档类型

### 1. 自由职业合同
- 服务范围描述
- 交付物定义
- 付款条款（固定/小时/里程碑）
- 知识产权归属
- 保密条款
- 终止条件
- 争议解决

### 2. 项目提案 (Proposal)
- 项目理解
- 解决方案概述
- 方法论/技术路线
- 时间线
- 团队介绍
- 定价方案
- 案例/参考

### 3. 工作说明书 (SOW)
- 项目背景
- 具体工作项
- 交付物清单
- 验收标准
- 时间表
- 变更管理流程

### 4. 主服务协议 (MSA)
- 通用条款
- 知识产权
- 保密义务
- 责任限制
- 赔偿条款
- 保险要求
- 不可抗力

### 5. 多法域支持
- 美国 (Delaware)
- 欧盟 (GDPR)
- 英国
- DACH (德国法)

## 生成流程
1. 选择文档类型
2. 填写基本信息（双方、项目）
3. 定义关键条款
4. AI 生成初稿
5. 审核修改
6. 输出 Markdown 格式

## 输出格式
- 结构化 Markdown
- 可转换为 .docx
- 包含法律审查标注

## 免责声明
生成的文档仅供参考，不构成法律建议。正式签署前请咨询专业律师。
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["合同", "提案", "SOW", "MSA", "商业文档", "法律"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "alirezarezvani",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "劳动合同模板 Skill",
        "desc": "创建符合法律最佳实践的劳动合同、录用信和HR政策文档，标准化雇佣文档管理",
        "content": """# 劳动合同模板

> 来源: [wshobson/agents](https://github.com/wshobson/agents) - employment-contract-templates
> 许可证: MIT | 38K+ Stars

创建标准化的雇佣文档。

## 文档类型

### 1. 录用信 (Offer Letter)
- 职位名称 + 部门
- 汇报关系
- 薪资构成（基本工资+奖金）
- 股权/期权（如有）
- 福利待遇概述
- 入职日期
- 试用期条款
- 接受/拒绝截止日期

### 2. 劳动合同
- 合同期限（固定/无固定）
- 工作内容与职责
- 工作地点
- 工作时间
- 薪酬与发放
- 社会保险与公积金
- 劳动保护与条件
- 合同变更与解除
- 违约责任
- 争议解决

### 3. HR政策文档
- **考勤制度**: 工作时间、请假、加班
- **薪酬福利**: 调薪、奖金、保险
- **行为规范**: 职业道德、利益冲突
- **保密协议**: 商业秘密、竞业限制
- **离职流程**: 交接、结算、证明

### 4. 合规检查
- 符合当地劳动法
- 最低工资标准
- 法定假期保障
- 社保公积金合规
- 反歧视条款

## 使用流程
1. 选择文档类型
2. 填写公司信息
3. 选择适用法域
4. 定制关键条款
5. 生成文档
6. 法律审核

## 免责声明
模板仅供参考，请根据当地法律法规调整并咨询专业律师。
""",
        "category": "行业垂直Skill",
        "sub_category": "职场咨询",
        "tags": ["劳动合同", "录用信", "HR政策", "雇佣文档", "合规"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "wshobson",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "PESTLE战略分析 Skill",
        "desc": "执行PESTLE分析，覆盖政治、经济、社会、技术、法律和环境六大宏观因素，辅助战略决策",
        "content": """# PESTLE战略分析

> 来源: [phuryn/pm-skills](https://github.com/phuryn/pm-skills) - pestle-analysis
> 许可证: MIT | 25K+ Stars

系统化的宏观环境分析框架。

## 六大维度

### P - 政治因素 (Political)
- 政府稳定性与政策方向
- 税收政策变化
- 贸易法规与关税
- 政治倾向对行业的影响
- 政府补贴/扶持政策

### E - 经济因素 (Economic)
- GDP增长率与趋势
- 通胀率/利率
- 汇率波动
- 消费者可支配收入
- 行业融资环境

### S - 社会因素 (Social)
- 人口结构与变化趋势
- 文化价值观与消费习惯
- 教育水平
- 健康意识与生活方式
- 社交媒体影响力

### T - 技术因素 (Technological)
- 技术创新与突破
- 自动化/AI 影响
- 研发投资水平
- 技术基础设施
- 技术采用生命周期

### L - 法律因素 (Legal)
- 行业监管法规
- 数据保护法律
- 劳动法规
- 知识产权法
- 消费者保护法

### E - 环境因素 (Environmental)
- 气候变化影响
- 碳排放法规
- 可持续发展趋势
- 资源稀缺性
- ESG 投资趋势

## 分析流程
1. 确定分析对象（公司/产品/市场）
2. 收集每个维度的信息
3. 评估影响程度（高/中/低）
4. 识别机会与威胁
5. 制定应对策略
6. 定期更新（季度/年度）

## 输出模板
| 维度 | 关键因素 | 影响 | 机会/威胁 | 应对策略 |
|------|---------|------|----------|----------|
| 政治 | ... | 高/中/低 | 机会 | ... |
| 经济 | ... | ... | 威胁 | ... |
| ... | ... | ... | ... | ... |

## 适用场景
- 市场进入决策
- 年度战略规划
- 投资尽职调查
- 产品国际化评估
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["PESTLE", "战略分析", "宏观环境", "商业分析", "决策"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "phuryn",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "X/Twitter运营导师 Skill",
        "desc": "价值$10K/hr的X/Twitter运营指导，融合6位顶级创作者方法论+算法深度分析+AI科技赛道专精",
        "content": """# X/Twitter运营导师

> 来源: [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) - x-mastery-mentor
> 许可证: MIT | 30K+ Stars

融合顶级创作者方法论的 X/Twitter 运营指导。

## 6大核心心智模型

### 1. Nicolas Cole - 分发优先
- 写作不是为了表达，是为了触达
- 选题 > 文笔
- 每个领域都有「已验证的话题」

### 2. Dickie Bush - 结构化写作
- Hook → Context → Value → CTA
- Thread结构: 标题推文 → 展开 → 总结
- 每句话都要推动阅读

### 3. Sahil Bloom - 好奇心驱动
- 反直觉开头
- 框架化思维
- 「我花了X年时间学到...」

### 4. Justin Welsh - 一人企业
- 内容即资产
- 常青内容 > 热点追踪
- 内容系统 → 邮件列表 → 产品

### 5. Dan Koe - 思维升级
- 挑战主流观点
- 跨领域连接
- 个人哲学输出

### 6. Alex Hormozi - 价值密度
- 每篇推文都要有可执行的建议
- 具体 > 抽象
- 「如何做」> 「是什么」

## 10条决策启发式
1. 3秒法则: Hook必须3秒内抓住注意力
2. 80/20选题: 80%已验证话题 + 20%实验
3. 10x标题: 写10个标题选最好的
4. 视觉优先: 有图/视频的推文互动高2-3x
5. 回复即内容: 在大号下高质量回复
6. 每日发布: 至少1条推文 + 1条回复
7. Thread策略: 每周1-2个深度Thread
8. 数据复盘: 周度分析最佳/最差内容
9. 粉丝≠收入: 聚焦转化路径
10. 长期主义: 6个月才能看到复利

## AI/科技赛道专精
- 技术解读类内容模板
- 产品发布推文策略
- 开发者社区互动方法
- 技术Thread写作框架

## 适用场景
- 技术人个人品牌建设
- AI/科技赛道内容创业
- 从0到10K粉丝增长
- 推文写作能力提升
""",
        "category": "文案内容创作",
        "sub_category": "公众号文案",
        "tags": ["Twitter", "X", "社交媒体运营", "个人品牌", "内容创作", "涨粉"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "alchaincyf",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "社媒Banner设计 Skill",
        "desc": "为社交媒体、广告、网站Banner和印刷品设计专业视觉素材，支持22种风格和全平台适配",
        "content": """# 社媒Banner设计

> 来源: [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - banner-design
> 许可证: MIT | 116K+ Stars

专业社交媒体与广告Banner设计。

## 支持平台
| 平台 | 尺寸 | 用途 |
|------|------|------|
| Facebook | 1200x630 | 封面/分享图 |
| Twitter/X | 1500x500 | Header |
| LinkedIn | 1584x396 | Banner |
| YouTube | 2560x1440 | Channel Art |
| Instagram | 1080x1080 | 帖子/Story |
| Google Ads | 多尺寸 | 展示广告 |
| 网站Hero | 1920x1080 | 首页大图 |

## 13种设计风格
1. **极简主义**: 留白 + 精简元素
2. **渐变**: 色彩渐变 + 现代感
3. **大胆排版**: 文字即设计
4. **摄影为主**: 高质量图片
5. **插画风**: 自定义插画
6. **几何**: 形状与线条
7. **复古**: 怀旧色调
8. **玻璃态**: 毛玻璃效果
9. **3D**: 立体元素
10. **霓虹**: 发光效果
11. **双色**: 双色调处理
12. **编辑式**: 杂志排版
13. **拼贴**: 混合素材

## 设计原则
- **品牌一致**: 颜色/字体/Logo统一
- **视觉层次**: 最重要的信息最突出
- **移动优先**: 在小屏幕上也要清晰
- **CTA明确**: 一眼看到行动按钮
- **对比度**: 文字与背景要有足够对比

## 工作流程
1. 确定平台和用途
2. 选择设计风格
3. 准备品牌素材（Logo/颜色/字体）
4. 确定核心信息（一句话）
5. AI 生成设计稿
6. 微调与输出

## 适用场景
- 社交媒体运营视觉
- 广告投放素材
- 网站首图
- 活动宣传
""",
        "category": "文案内容创作",
        "sub_category": "海报文案",
        "tags": ["Banner", "社交媒体", "视觉设计", "广告素材", "品牌"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "nextlevelbuilder",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "AI配音合成 Skill",
        "desc": "使用HeyGen Starfish TTS模型从文本生成语音音频，支持多语言、多音色、语速音调控制",
        "content": """# AI配音合成

> 来源: [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) - text-to-speech
> 许可证: MIT | 47K+ Stars

从文本生成高质量语音音频。

## 核心功能

### 1. 文本转语音
- 输入文本 → 输出音频文件
- 支持多种语言（中/英/日/韩等）
- 自然流畅的语音质量

### 2. 音色选择
- **男声**: 多种音色（成熟/年轻/磁性）
- **女声**: 多种音色（温柔/专业/活泼）
- 按语言筛选可用音色
- 试听后选择

### 3. 参数控制
| 参数 | 范围 | 说明 |
|------|------|------|
| 语速 | 0.5x - 2.0x | 慢速/正常/快速 |
| 音调 | -12 ~ +12 | 低沉/正常/尖锐 |
| 音量 | 0 - 100 | 相对音量 |

### 4. 输出格式
- MP3（默认，体积小）
- WAV（无损，后期编辑）
- 采样率: 22050 / 24000 / 44100 Hz

### 5. 批量处理
- 多段文本批量转换
- 不同段落可用不同音色
- 自动拼接或分段输出

## 应用场景
- **视频配音**: 为视频添加旁白
- **播客制作**: 生成播客音频
- **有声读物**: 文本转有声内容
- **教育内容**: 课程讲解音频
- **多语言版本**: 同一内容多语言配音

## 与其他工具配合
- 配合视频剪辑 → 完整视频
- 配合播客生成 → 对话音频
- 配合ElevenLabs → 更高质量语音
""",
        "category": "文案内容创作",
        "sub_category": "短视频脚本",
        "tags": ["TTS", "配音", "语音合成", "HeyGen", "音频生成"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "calesthio",
        "source_type": "开源改编",
        "license": "MIT",
    },
    {
        "title": "HR入职规划 Skill",
        "desc": "生成新员工入职计划，包含首周日程、导师介绍、学习路径、设备清单和完成标准",
        "content": """# HR入职规划

> 来源: [nexu-io/open-design](https://github.com/nexu-io/open-design) - hr-onboarding
> 许可证: MIT | 85K+ Stars

结构化的新员工入职计划。

## 入职计划结构

### 1. 首周日程
| 时间 | 活动 | 负责人 |
|------|------|--------|
| 9:00 | 欢迎 + 办公环境介绍 | HR |
| 10:00 | IT设置 + 设备领取 | IT |
| 11:00 | 团队介绍 + Buddy见面 | 直属经理 |
| 14:00 | 公司文化/制度培训 | HR |
| 16:00 | 岗位目标沟通 | 直属经理 |
| 17:00 | 首周总结 + Q&A | Buddy |

### 2. Buddy制度
- 指定一名同级别同事作为Buddy
- Buddy职责:
  - 日常问题解答
  - 非正式文化引导
  - 午餐/咖啡陪伴
  - 第一周每日check-in

### 3. 学习路径
- **第1周**: 公司/产品/团队概览
- **第2-4周**: 工具/流程/代码库熟悉
- **第2-3月**: 独立承担小任务
- **第3-6月**: 完全独立工作

### 4. 设备清单
- [ ] 电脑 + 配件
- [ ] 邮箱/IM 账号
- [ ] 代码仓库权限
- [ ] 内部系统权限
- [ ] 工位/门禁卡

### 5. 完成标准
「你已就绪当...」
- 能独立描述产品核心价值
- 能独立完成代码提交/项目交付
- 知道遇到问题找谁
- 理解团队OKR和自己的贡献

## 适用场景
- HR部门标准化入职流程
- 远程团队虚拟入职
- 实习生入职计划
- 管理层入职（增强版）
""",
        "category": "办公自动化SOP",
        "sub_category": "会议纪要",
        "tags": ["入职", "HR", "新员工", "Onboarding", "入职计划"],
        "fit_tools": ["Claude", "Cursor", "Copilot"],
        "author": "nexu-io",
        "source_type": "开源改编",
        "license": "MIT",
    },
]


def import_skills():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    count = 0

    for skill in SKILLS:
        cursor.execute("SELECT id FROM skills WHERE title = ?", (skill["title"],))
        if cursor.fetchone():
            print(f"  ⏭ 跳过（已存在）: {skill['title']}")
            continue

        cursor.execute("""
            INSERT INTO skills (title, desc, content, category, sub_category, tags, fit_tools,
                              author, source_type, license, collect_num, view_count, status,
                              uploader_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 'published', 1, ?, ?)
        """, (
            skill["title"], skill["desc"], skill["content"],
            skill["category"], skill["sub_category"],
            json.dumps(skill["tags"], ensure_ascii=False),
            json.dumps(skill["fit_tools"], ensure_ascii=False),
            skill["author"], skill["source_type"], skill["license"],
            now, now,
        ))
        count += 1
        print(f"  ✅ [{skill['category']}] {skill['title']}")

    conn.commit()
    conn.close()
    print(f"\n导入完成！新增 {count} 条 Skill")


if __name__ == "__main__":
    print("=" * 60)
    print("从开源社区导入高质量 Skill 数据")
    print("来源: SkillsMP API / prompts.chat / anthropics/skills / ECC")
    print("=" * 60)
    print()
    import_skills()
