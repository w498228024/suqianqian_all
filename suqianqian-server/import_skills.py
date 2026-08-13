"""
批量导入 Skill 数据到数据库
覆盖全部 8 大分类，每类 3-5 条高质量 Skill
"""
import sqlite3
import json
from datetime import datetime

DB_PATH = "suqianqian.db"

SKILLS = [
    # ==================== 1. 通用AI能力 ====================
    {
        "title": "万能角色设定 Skill",
        "desc": "让 AI 精准扮演任何角色，从语气、知识边界到行为模式全面锁定",
        "content": """# 万能角色设定 Skill

## 使用方式
将以下模板中的 `[占位符]` 替换为你需要的角色信息，粘贴给 AI 即可。

## 模板

```
请你扮演以下角色，在整个对话中始终保持该角色身份：

### 角色信息
- 名称：[角色名]
- 职业/身份：[职业]
- 专业领域：[领域]
- 经验年限：[X年]

### 行为规则
1. 始终以该角色的视角和口吻回答
2. 只使用该角色专业范围内的知识
3. 遇到超出专业范围的问题，诚实说明"这不在我的专业范围内"
4. 使用该角色常用的表达方式和术语
5. 保持角色的性格特征：[描述性格]

### 限制
- 不要跳出角色
- 不要说"作为一个AI语言模型"
- 不要提供角色不会知道的信息
```

## 示例：资深产品经理
```
请你扮演一位有10年经验的资深产品经理...
```

## 适配说明
- Ollama：推荐 llama3 / qwen2 以上模型
- Dify：可直接作为系统提示词
- OpenWebUI：设置为 System Prompt
""",
        "category": "通用AI能力",
        "sub_category": "角色设定Skill",
        "tags": ["角色设定", "角色扮演", "Prompt"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "思维链 CoT 深度思考 Skill",
        "desc": "引导 AI 逐步拆解复杂问题，避免跳跃式回答，提升推理准确性",
        "content": """# 思维链 CoT 深度思考 Skill

## 使用场景
- 复杂逻辑推理问题
- 数学/编程问题求解
- 需要严谨分析的场景

## 提示词模板

```
请按以下步骤思考并回答我的问题：

### 第一步：理解问题
- 复述问题的核心要点
- 明确需要解决什么

### 第二步：拆解分析
- 将问题分解为若干子问题
- 列出已知条件和约束

### 第三步：逐步推理
- 对每个子问题逐一分析
- 展示完整的推理过程
- 如果有多条路径，分别评估

### 第四步：验证检查
- 回顾推理过程是否有逻辑漏洞
- 检查是否有遗漏的情况

### 第五步：总结答案
- 给出最终结论
- 用简洁的语言概括
```

## 注意事项
- 适合复杂问题，简单问题无需使用
- 会消耗更多 token，注意上下文长度
- 可配合"请再检查一遍"增强验证效果
""",
        "category": "通用AI能力",
        "sub_category": "思维链CoT",
        "tags": ["思维链", "CoT", "推理", "深度思考"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "AI 自我校验反思 Skill",
        "desc": "让 AI 在回答后自动检查、反思、修正，减少幻觉和错误",
        "content": """# AI 自我校验反思 Skill

## 核心理念
让 AI 输出答案后，自动进入"审查者"模式，对自身回答进行质疑和修正。

## 提示词

```
请在每次回答后，自动执行以下自检流程：

### 自检清单
1. 【事实性】我回答中的事实是否准确？有没有编造的信息？
2. 【完整性】是否遗漏了问题的重要方面？
3. 【逻辑性】推理过程是否严密？有没有逻辑跳跃？
4. 【相关性】回答是否切题？有没有跑偏？
5. 【不确定性】有哪些部分我不确定？需要标注吗？

### 输出格式
先给出正式回答，然后附加：
---
🔍 自检：
- 置信度：[高/中/低]
- 可能的错误点：[列出]
- 补充说明：[如有]
---

### 规则
- 如果发现错误，直接修正并说明
- 不确定的地方必须标注
- 不要为了自信而忽略不确定性
```

## 适用模型
- 推荐 7B 以上模型使用
- 小模型可能自检效果不佳
""",
        "category": "通用AI能力",
        "sub_category": "自我校验Skill",
        "tags": ["自我校验", "反思", "去幻觉", "准确性"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "RAG 问答优化 Skill",
        "desc": "优化 RAG 场景下 AI 的检索增强回答质量，减少幻觉，提升引用准确性",
        "content": """# RAG 问答优化 Skill

## 使用场景
配合 RAG（检索增强生成）系统使用，优化 AI 基于检索文档的回答质量。

## System Prompt

```
你是一个基于检索文档进行回答的 AI 助手。请严格遵守以下规则：

### 回答规则
1. 只基于提供的检索内容回答，不要使用自身训练数据补充
2. 如果检索内容中没有相关信息，明确告知用户"根据现有资料未找到相关信息"
3. 回答时标注信息来源，格式：[来源1]、[来源2]
4. 如果多个来源有不同观点，分别列出
5. 不要编造检索内容中不存在的细节

### 回答格式
- 先给出直接答案
- 再展开详细说明
- 最后列出参考来源

### 特殊情况处理
- 检索内容相互矛盾 → 指出矛盾，分别说明
- 检索内容不完整 → 说明信息不完整，给出已有部分
- 问题超出检索范围 → 诚实说明，不要猜测
```

## Dify 集成建议
- 放入 Chatflow 的 LLM 节点 System Prompt
- 配合 Knowledge Retrieval 节点使用
- Temperature 建议设为 0.1-0.3
""",
        "category": "通用AI能力",
        "sub_category": "RAG问答优化",
        "tags": ["RAG", "检索增强", "知识库", "引用"],
        "fit_tools": ["Dify", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "长文本分块处理 Skill",
        "desc": "指导 AI 高效处理超长文本，分段摘要、提取关键信息、保持上下文连贯",
        "content": """# 长文本分块处理 Skill

## 使用场景
- 处理超出模型上下文窗口的长文本
- 长文档摘要、信息提取
- 论文/报告分析

## 处理策略

### 策略一：分段摘要法
```
我将分多次给你一份长文档的各部分内容。
请你：
1. 每次收到内容后，给出该段的核心摘要（不超过200字）
2. 等我发送完所有部分后，我会说"全部发送完毕"
3. 届时请你综合所有摘要，给出完整文档的总结

理解请回复"请发送第一部分"
```

### 策略二：关键信息提取
```
请阅读以下长文本，提取并整理：
1. 核心论点/结论（不超过5条）
2. 关键数据/事实
3. 重要人物/组织/概念
4. 时间线/逻辑链

输出为结构化格式。
```

### 策略三：递归压缩
```
请按以下流程处理：
1. 将文本分为若干段落
2. 对每段进行摘要
3. 将所有摘要合并，再做一次总结
4. 最终输出：一句话概括 + 500字详细摘要
```

## 配合建议
- Ollama 推荐 4K+ 上下文模型
- 设置足够大的 num_ctx 参数
""",
        "category": "通用AI能力",
        "sub_category": "长文本处理",
        "tags": ["长文本", "分块", "摘要", "信息提取"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },

    # ==================== 2. 文案内容创作 ====================
    {
        "title": "短视频脚本生成 Skill",
        "desc": "快速生成抖音/快手/视频号短视频脚本，包含开头钩子、正文结构、结尾引导",
        "content": """# 短视频脚本生成 Skill

## 使用方式
告诉 AI 你的主题、时长、风格，即可生成完整脚本。

## 提示词模板

```
你是一个专业的短视频编导，请根据以下信息生成短视频脚本：

### 基本信息
- 主题：[填写]
- 目标时长：[30秒/60秒/3分钟]
- 发布平台：[抖音/快手/视频号/B站]
- 风格：[口播/剧情/知识科普/vlog]

### 输出要求
请按以下格式输出：

**【开头钩子】（前3秒）**
- 画面描述：
- 台词/文字：
- 目的：吸引停留

**【正文内容】**
按时间轴列出：
| 时间 | 画面 | 台词/旁白 | 字幕/特效 |
|------|------|-----------|-----------|

**【结尾引导】**
- 引导互动的话术
- CTA（关注/点赞/评论引导）

**【发布建议】**
- 推荐标题（3个备选）
- 推荐标签
- 最佳发布时间
```

## 爆款公式
- 知识类：痛点开头 → 解决方案 → 效果对比
- 种草类：场景代入 → 产品介绍 → 使用体验
- 剧情类：冲突设置 → 反转 → 情感共鸣
""",
        "category": "文案内容创作",
        "sub_category": "短视频脚本",
        "tags": ["短视频", "脚本", "抖音", "爆款"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "公众号爆款文案 Skill",
        "desc": "生成微信公众号爆款文章，包含标题党技巧、排版建议、阅读节奏控制",
        "content": """# 公众号爆款文案 Skill

## 提示词

```
你是一个资深公众号运营，擅长写出阅读量10W+的文章。

### 请根据以下信息撰写公众号文章：
- 主题：[填写]
- 目标读者：[描述]
- 文章类型：[干货/观点/故事/清单]
- 期望字数：[1500/3000/5000]

### 输出要求

**1. 标题（提供5个备选）**
- 至少包含1个数字
- 制造好奇心缺口
- 不超过30字

**2. 正文结构**
- 开头（100字内）：用故事/数据/提问引入
- 正文：每段不超过4行，多用短句
- 每300字设置一个"钩子"保持阅读
- 结尾：金句总结 + 引导转发

**3. 排版建议**
- 重点内容加粗
- 适当使用分割线
- 配图位置标注

### 写作原则
- 说人话，不要学术腔
- 多用"你"而不是"我们"
- 每段只讲一个点
- 数据要具体，不要模糊
```
""",
        "category": "文案内容创作",
        "sub_category": "公众号文案",
        "tags": ["公众号", "文案", "爆款", "标题"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "公文写作助手 Skill",
        "desc": "规范撰写各类公文、通知、报告、请示，符合党政机关公文格式标准",
        "content": """# 公文写作助手 Skill

## 角色设定
```
你是一位有20年经验的政府机关文秘，精通各类公文写作。
请严格按照《党政机关公文处理工作条例》和《党政机关公文格式》(GB/T 9704)标准撰写公文。
```

## 支持的公文类型
- 通知、通报、报告
- 请示、批复、函
- 意见、决定、公告
- 会议纪要、工作总结

## 使用模板
```
请帮我撰写一份[公文类型]：

- 发文单位：[XXX]
- 收文单位：[XXX]
- 主题：[简述]
- 关键内容：[需要包含的要点]
- 语气要求：[严肃/一般]

请按标准公文格式输出，包括：
1. 标题
2. 主送机关
3. 正文（缘由+事项+要求）
4. 落款和日期
```

## 注意事项
- AI 生成的公文需要人工审核
- 注意核实具体数据和政策引用
- 涉密内容不要输入 AI
""",
        "category": "文案内容创作",
        "sub_category": "公文写作",
        "tags": ["公文", "通知", "报告", "请示"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },

    # ==================== 3. 网文小说专用 ====================
    {
        "title": "小说人物设定锁死 Skill",
        "desc": "创建并锁定小说角色的人物卡，确保长篇连载中角色性格、口癖、行为逻辑一致不崩",
        "content": """# 小说人物设定锁死 Skill

## 使用方式
为每个重要角色创建人物卡，AI 在后续写作中严格遵守。

## 人物卡模板

```
### 角色人物卡

**基础信息**
- 姓名：
- 年龄：
- 性别：
- 外貌特征：（3个标志性特征）

**性格内核**
- 核心性格：（用3个关键词）
- 性格成因：（什么经历塑造了这个性格）
- 性格表现：
  - 日常状态：
  - 压力状态：
  - 极端状态：

**行为模式**
- 口头禅/语言习惯：
- 标志性动作：
- 决策倾向：（冲动/理性/犹豫）
- 底线/禁区：

**人际关系**
- 对[角色A]的态度：
- 对[角色B]的态度：

**成长弧线**
- 起点状态：
- 关键转折：
- 终点走向：

**绝对禁止**
- 该角色绝对不会做的事：
- 该角色绝对不会说的话：
```

## 使用规则
1. 每次写作前，将相关角色的人物卡放入上下文
2. 如果 AI 写出 OOC 的内容，立即指出并要求修改
3. 角色成长要循序渐进，不能突然转变
""",
        "category": "网文小说专用",
        "sub_category": "人物设定锁死Skill",
        "tags": ["人物设定", "角色卡", "OOC", "小说"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "剧情逻辑自检 Skill",
        "desc": "自动检查小说剧情中的逻辑漏洞、时间线矛盾、设定冲突",
        "content": """# 剧情逻辑自检 Skill

## 使用方式
将章节内容或大纲发给 AI，让它进行逻辑审查。

## 提示词

```
请作为小说剧情逻辑审查专家，检查以下内容：

### 检查维度

**1. 时间线一致性**
- 事件发生顺序是否合理
- 时间间隔是否合理（如"三天后"和"一周后"是否矛盾）
- 角色年龄与时间线是否匹配

**2. 空间逻辑**
- 角色位置移动是否合理
- 距离和交通时间是否合理
- 场景描述是否前后一致

**3. 人物行为逻辑**
- 角色行为是否符合已建立的性格
- 动机是否充分
- 信息获取是否合理（角色不应该知道他没接触过的信息）

**4. 设定一致性**
- 力量体系/世界观设定是否前后一致
- 专有名词是否统一
- 规则是否被无故打破

**5. 因果链**
- 事件因果关系是否成立
- 是否有无因之果或无果之因
- 巧合是否过多

### 输出格式
| 问题类型 | 位置 | 问题描述 | 修改建议 |
|----------|------|----------|----------|
```

## 建议
- 每写完一章就自检一次
- 保持一份"设定圣经"文档，记录所有已确立的设定
""",
        "category": "网文小说专用",
        "sub_category": "剧情逻辑自检",
        "tags": ["剧情", "逻辑", "自检", "漏洞"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "网文伏笔埋点工具 Skill",
        "desc": "帮助作者在长篇连载中系统性地埋设和追踪伏笔，确保前后呼应",
        "content": """# 网文伏笔埋点工具 Skill

## 伏笔管理模板

```
请帮我规划以下伏笔：

### 当前剧情阶段：[开头/发展/高潮前/高潮]

### 请设计 3-5 个伏笔，每个包含：

**伏笔名称：**
**埋设章节：**（预计在第几章植入）
**回收章节：**（预计在第几章揭晓）

**埋设方式：**
- 表面情节：（读者第一次看到时以为是什么）
- 真实含义：（回头看才明白的深意）
- 植入手法：（对话/场景/描写/角色行为）

**追踪标记：**
- 关键词：[用于全文搜索确认]
- 关联角色：
- 关联事件：

**回收效果：**
- 读者预期反应：
- 对主线的推动：
```

## 伏笔类型参考
1. **角色伏笔**：角色的某个细节暗示其真实身份/目的
2. **事件伏笔**：看似无关的事件后来成为关键转折
3. **物品伏笔**：一个不起眼的物品后来发挥重要作用
4. **对话伏笔**：一句随意的话后来一语成谶
5. **环境伏笔**：场景描写中暗含后续剧情线索

## 管理建议
- 维护一份"伏笔追踪表"
- 每50章回顾一次，检查是否有遗忘的伏笔
""",
        "category": "网文小说专用",
        "sub_category": "伏笔埋点工具",
        "tags": ["伏笔", "埋点", "长篇", "连载"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "文风统一模仿 Skill",
        "desc": "分析并模仿特定作者/作品的文风，确保代笔或续写时风格一致",
        "content": """# 文风统一模仿 Skill

## 使用方式

### 第一步：文风分析
```
请分析以下文本的写作风格：

[粘贴参考文本 1000-2000字]

请从以下维度分析：
1. 句式特征：（长句为主/短句为主/混合）
2. 用词倾向：（华丽/朴素/口语化/书面化）
3. 修辞偏好：（比喻多/白描多/意识流）
4. 叙事视角：（第几人称/全知/限知）
5. 节奏感：（快节奏/慢热/张弛有度）
6. 情感表达：（含蓄/直白/讽刺）
7. 对话风格：（简洁/啰嗦/文绉绉/接地气）
8. 标志性手法：（最突出的2-3个特征）
```

### 第二步：模仿写作
```
请以上述文风，续写/创作以下内容：
- 场景：
- 角色：
- 情节：
- 字数要求：

要求：
- 句式结构模仿原文
- 用词风格保持一致
- 叙事节奏匹配
- 让读者感觉是同一人所写
```

## 注意事项
- 提供的参考文本越长，分析越准确
- 可以提供多段不同场景的文本
- 模仿结果需要人工微调
""",
        "category": "网文小说专用",
        "sub_category": "文风统一Skill",
        "tags": ["文风", "模仿", "续写", "风格"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },

    # ==================== 4. 程序/测试/运维 ====================
    {
        "title": "代码生成助手 Skill",
        "desc": "根据需求描述生成高质量代码，支持多种语言，包含注释和错误处理",
        "content": """# 代码生成助手 Skill

## System Prompt

```
你是一个资深软件工程师，请根据需求生成高质量代码。

### 代码规范
1. 添加清晰的注释和文档字符串
2. 包含错误处理和边界情况
3. 遵循该语言的最佳实践和编码规范
4. 变量命名清晰有意义
5. 函数/方法保持单一职责

### 输出格式
1. 先简要说明实现思路
2. 给出完整可运行的代码
3. 标注关键设计决策
4. 提供使用示例
5. 说明时间/空间复杂度

### 语言偏好
- 未指定时默认使用 Python
- 前端默认 TypeScript
- 根据用户提到的框架选择

### 要求
- 代码必须完整，不要用 "..." 省略
- 包含必要的 import
- 考虑异常处理
```

## 使用示例
```
请用 Python 实现一个带缓存的 HTTP 请求工具：
- 支持 GET/POST
- 相同 URL+参数 5分钟内返回缓存
- 支持手动清除缓存
- 包含超时和重试机制
```
""",
        "category": "程序/测试/运维",
        "sub_category": "代码生成",
        "tags": ["代码", "编程", "开发", "生成"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "代码解释与审查 Skill",
        "desc": "逐行解释复杂代码，审查代码质量，发现潜在 Bug 和性能问题",
        "content": """# 代码解释与审查 Skill

## 模式一：代码解释
```
请逐段解释以下代码：

[粘贴代码]

请按以下格式：
1. 整体功能：一句话概括
2. 核心逻辑：流程图或步骤说明
3. 逐段解释：
   - 代码片段
   - 作用说明
   - 关键语法点
4. 数据流向：输入 → 处理 → 输出
5. 可能的疑问点：初学者可能困惑的地方
```

## 模式二：代码审查
```
请审查以下代码，从以下维度给出建议：

[粘贴代码]

### 审查维度
1. **Bug 风险**：可能的空指针、越界、竞态条件
2. **性能问题**：不必要的循环、内存泄漏、N+1 查询
3. **安全性**：注入风险、敏感信息泄露、权限检查
4. **可读性**：命名规范、代码结构、注释质量
5. **最佳实践**：是否符合语言惯用法

### 输出格式
| 严重度 | 位置 | 问题 | 建议修改 |
|--------|------|------|----------|
| 🔴 严重 | ... | ... | ... |
| 🟡 建议 | ... | ... | ... |
| 🟢 优化 | ... | ... | ... |
```
""",
        "category": "程序/测试/运维",
        "sub_category": "代码解释",
        "tags": ["代码审查", "Bug", "性能", "安全"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "单元测试生成 Skill",
        "desc": "根据源代码自动生成全面的单元测试用例，覆盖正常/异常/边界场景",
        "content": """# 单元测试生成 Skill

## 提示词

```
请为以下代码生成完整的单元测试：

[粘贴源代码]

### 测试要求
1. 使用 [pytest/Jest/JUnit] 框架
2. 覆盖以下场景：
   - 正常输入（至少3个用例）
   - 边界条件（空值、极大值、极小值）
   - 异常输入（错误类型、非法参数）
   - 特殊情况（并发、超时等）

### 测试命名规范
- test_[功能]_[场景]_[预期结果]
- 例：test_login_valid_credentials_returns_token

### 输出格式
- 完整的测试代码
- 每个测试用例的注释说明
- Mock/Stub 的使用说明
- 预估覆盖率
```

## 测试金字塔建议
- 单元测试（70%）：函数/方法级别
- 集成测试（20%）：模块间交互
- E2E 测试（10%）：完整流程
""",
        "category": "程序/测试/运维",
        "sub_category": "测试用例",
        "tags": ["测试", "单元测试", "pytest", "Jest"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },

    # ==================== 5. 办公自动化SOP ====================
    {
        "title": "Excel 数据分析 Skill",
        "desc": "指导 AI 分析 Excel 数据，生成公式、透视表建议、数据可视化方案",
        "content": """# Excel 数据分析 Skill

## 使用方式
将数据样本或需求描述给 AI，获取分析方案。

## 提示词模板

```
请帮我分析以下 Excel 数据：

### 数据描述
- 列名：[列出所有列名]
- 数据行数：[约X行]
- 数据样本（前5行）：
[粘贴或描述]

### 分析需求
- 目标：[想要得出什么结论]
- 需要的输出：[公式/图表/透视表/数据清洗]

### 请提供：
1. 数据清洗建议（如有脏数据）
2. 推荐的分析方法
3. 具体 Excel 公式（可直接复制使用）
4. 图表类型建议
5. 关键发现/洞察
```

## 常用公式速查
- 条件求和：`=SUMIFS()`
- 查找匹配：`=VLOOKUP()` / `=XLOOKUP()`
- 数据透视：插入 → 数据透视表
- 条件计数：`=COUNTIFS()`
- 文本处理：`=TEXTJOIN()`, `=LEFT()`, `=MID()`
""",
        "category": "办公自动化SOP",
        "sub_category": "Excel分析",
        "tags": ["Excel", "数据分析", "公式", "透视表"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "周报月报自动生成 Skill",
        "desc": "根据工作记录快速生成结构化的周报/月报，支持多种格式模板",
        "content": """# 周报月报自动生成 Skill

## 提示词

```
请根据以下工作记录，生成一份[周报/月报]：

### 基本信息
- 姓名：
- 部门：
- 时间段：[X月X日 - X月X日]

### 本周/月完成的工作
[列出所有完成事项，可以很随意]

### 进行中的工作
[列出正在做的事]

### 遇到的问题
[可选]

### 下阶段计划
[列出接下来的安排]

### 请输出：
1. 按重要程度排序
2. 每项工作用"动词+成果"格式
3. 量化成果（完成了X个、提升了X%）
4. 问题部分附带解决方案或需要的支持
5. 语气专业但不生硬
```

## 格式模板
```markdown
## 本周工作总结

### 一、重点工作
1. [项目A] 完成了XX，达成XX效果
2. [项目B] 推进至XX阶段

### 二、日常工作
- 处理XX事项X件
- 完成XX报表

### 三、问题与建议
- 问题：XX
- 建议：XX

### 四、下周计划
1. 推进XX至XX阶段
2. 完成XX
```
""",
        "category": "办公自动化SOP",
        "sub_category": "周报月报",
        "tags": ["周报", "月报", "工作总结", "汇报"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "会议纪要整理 Skill",
        "desc": "将杂乱的会议记录整理为结构清晰的会议纪要，提取待办事项",
        "content": """# 会议纪要整理 Skill

## 提示词

```
请将以下会议记录整理为正式的会议纪要：

[粘贴原始记录/语音转写文本]

### 输出格式

# 会议纪要

**会议主题：**
**会议时间：**
**参会人员：**
**记录人：**

---

## 一、会议议题
1. [议题1]
2. [议题2]

## 二、讨论内容

### 议题1：[名称]
- 主要观点：
- 讨论结论：

### 议题2：[名称]
- 主要观点：
- 讨论结论：

## 三、决议事项
| 序号 | 事项 | 负责人 | 截止日期 |
|------|------|--------|----------|

## 四、待跟进
- [ ] [事项] - @负责人 - [日期]
```

## 处理规则
- 去除口语化表达和废话
- 合并重复观点
- 明确区分"讨论中"和"已决议"
- 提取所有待办事项并指定负责人
""",
        "category": "办公自动化SOP",
        "sub_category": "会议纪要",
        "tags": ["会议纪要", "整理", "待办", "记录"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },

    # ==================== 6. 学习科研助手 ====================
    {
        "title": "学术论文润色 Skill",
        "desc": "对学术论文进行语言润色，提升表达的专业性和流畅度，支持中英文",
        "content": """# 学术论文润色 Skill

## System Prompt

```
你是一位学术写作专家，请对以下论文内容进行润色。

### 润色原则
1. 保持原意不变
2. 提升语言的学术规范性
3. 消除语法错误和不地道表达
4. 增强逻辑连接词的使用
5. 避免口语化表达

### 润色标记
- 修改的部分用 **加粗** 标注
- 删除建议用 ~~删除线~~ 标注
- 新增建议用 [方括号] 标注

### 输出格式
1. 润色后的全文
2. 修改说明（列出主要修改点及原因）
3. 整体建议（结构/逻辑/论证方面的改进方向）
```

## 英文论文专用
```
Please polish the following academic text:
- Improve grammar and clarity
- Use formal academic language
- Maintain the original meaning
- Highlight changes made
- Target journal: [期刊名]
```

## 注意事项
- 专业术语不要随意替换
- 数据引用保持原样
- 润色后务必人工复核
""",
        "category": "学习科研助手",
        "sub_category": "论文润色",
        "tags": ["论文", "润色", "学术", "写作"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "文献快速总结 Skill",
        "desc": "快速提取学术论文的核心信息：研究问题、方法、结论、贡献",
        "content": """# 文献快速总结 Skill

## 提示词

```
请阅读以下论文内容，提取关键信息：

[粘贴论文摘要/正文]

### 输出结构

**📄 论文信息**
- 标题：
- 作者：
- 发表年份/期刊：

**🎯 研究问题**
- 核心问题：（一句话）
- 研究背景：（为什么这个问题重要）

**🔬 研究方法**
- 方法类型：[实验/调查/理论/综述]
- 具体方法：
- 数据来源：
- 样本量：

**📊 主要发现**
1. 
2. 
3. 

**💡 核心贡献**
- 理论贡献：
- 实践意义：

**⚠️ 局限性**
- 

**🔗 与相关工作的关系**
- 支持了哪些已有研究：
- 与哪些研究存在分歧：

**📝 个人思考**
- 可以借鉴的方法：
- 可以延伸的方向：
```

## 批量处理
对于多篇论文，可以简化为表格：
| 论文 | 问题 | 方法 | 核心发现 | 贡献 |
""",
        "category": "学习科研助手",
        "sub_category": "文献总结",
        "tags": ["文献", "论文", "总结", "学术"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "思维导图生成 Skill",
        "desc": "将任意主题快速转化为结构化的思维导图格式，支持 Markdown/Mermaid",
        "content": """# 思维导图生成 Skill

## 提示词

```
请将以下主题/内容转化为思维导图结构：

主题：[填写]

### 输出要求
1. 使用 Markdown 缩进格式（方便导入思维导图工具）
2. 中心主题 → 一级分支（不超过7个）→ 二级分支 → 三级分支
3. 每个节点用简洁的关键词，不超过10个字
4. 适当使用 emoji 增加辨识度

### 格式
# 中心主题
## 📌 一级分支1
### 二级分支
- 关键词
- 关键词
## 📌 一级分支2
...

### 同时提供 Mermaid 格式
```mermaid
mindmap
  root((中心主题))
    分支1
      子节点
    分支2
      子节点
```
```

## 适用场景
- 读书笔记整理
- 项目规划
- 知识点梳理
- 会议头脑风暴
- 学习计划制定

## 导入工具
- XMind：直接粘贴 Markdown
- MindNode：支持 Markdown 导入
- ProcessOn：在线编辑
- Mermaid：支持渲染的平台直接显示
""",
        "category": "学习科研助手",
        "sub_category": "思维导图生成",
        "tags": ["思维导图", "Markdown", "Mermaid", "结构化"],
        "fit_tools": ["Ollama", "OpenWebUI", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },

    # ==================== 7. 行业垂直Skill ====================
    {
        "title": "电商运营文案 Skill",
        "desc": "生成商品标题、详情页文案、促销活动方案、客服话术等电商运营内容",
        "content": """# 电商运营文案 Skill

## 功能模块

### 1. 商品标题优化
```
请为以下商品生成5个电商标题：
- 商品：[名称]
- 核心卖点：[3个]
- 目标平台：[淘宝/京东/拼多多]
- 目标人群：[描述]

要求：
- 包含核心搜索关键词
- 突出差异化卖点
- 不超过60字符
- 符合平台标题规范
```

### 2. 详情页文案
```
请撰写商品详情页文案：
- 商品：[名称+核心参数]
- 目标客户：[画像]
- 竞品对比：[优势点]

结构：
1. 痛点引入（你是不是遇到过...）
2. 产品介绍（核心卖点×3）
3. 使用场景（3个场景描述）
4. 品质背书（材质/认证/数据）
5. 购买理由（为什么选我们）
```

### 3. 客服话术
```
请生成以下场景的客服回复话术：
- 场景：[催发货/退换货/差评回复/咨询...]
- 语气：[亲切/专业/诚恳]
- 品牌调性：[描述]
```
""",
        "category": "行业垂直Skill",
        "sub_category": "电商运营",
        "tags": ["电商", "淘宝", "商品", "文案"],
        "fit_tools": ["Ollama", "Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "心理咨询对话 Skill",
        "desc": "辅助心理咨询师整理案例记录、生成咨询方案建议、学习咨询技术",
        "content": """# 心理咨询对话 Skill

## 重要声明
⚠️ 本 Skill 仅供学习和辅助使用，不能替代专业心理咨询。
AI 不具备真正的共情能力，所有建议需要专业咨询师评估。

## 功能一：案例概念化
```
请根据以下来访者信息，进行案例概念化：

### 基本信息
- 年龄/性别/职业：
- 主诉问题：
- 持续时间：
- 既往史：

### 请分析：
1. 可能的心理学解释（CBT/精神分析/人本主义视角）
2. 维持因素分析
3. 风险评估
4. 建议的咨询方向
5. 需要注意的伦理问题
```

## 功能二：咨询技术练习
```
请扮演来访者，我来练习咨询技术：
- 来访者设定：[描述]
- 本次议题：[描述]
- 我的练习目标：[倾听/共情/面质/重构]

请在每轮对话后，以督导身份评价我的回应：
- 做得好的地方：
- 可以改进的地方：
- 示范回应：
```

## 伦理提醒
- 不要输入可识别的来访者真实信息
- AI 建议仅供参考
""",
        "category": "行业垂直Skill",
        "sub_category": "心理咨询",
        "tags": ["心理咨询", "案例", "CBT", "共情"],
        "fit_tools": ["Ollama", "OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },

    # ==================== 8. Agent 工作流模板 ====================
    {
        "title": "Dify 知识库问答工作流 Skill",
        "desc": "Dify Chatflow 完整模板：知识库检索 → LLM 回答 → 来源引用",
        "content": """# Dify 知识库问答工作流 Skill

## 工作流结构

```
[开始] → [知识库检索] → [LLM 节点] → [输出]
```

## 节点配置

### 1. 知识库检索节点
```json
{
  "node_type": "knowledge_retrieval",
  "dataset_ids": ["你的知识库ID"],
  "retrieval_mode": "semantic",
  "top_k": 5,
  "score_threshold": 0.5,
  "query_variable": "sys.query"
}
```

### 2. LLM 节点
```
System Prompt:
你是一个知识库问答助手。请严格基于检索到的知识库内容回答用户问题。

规则：
1. 只基于提供的知识库内容回答
2. 如果知识库中没有相关信息，请说明"根据现有知识库未找到相关信息"
3. 回答时标注来源 [序号]
4. 保持回答简洁准确

用户问题：{{sys.query}}

检索到的内容：
{{knowledge_retrieval.result}}
```

### 3. 参数建议
- Temperature: 0.1
- Max Tokens: 2000
- 模型推荐: gpt-4o-mini / qwen-turbo

## 优化技巧
- 知识库文档做好分段和标题
- 上传前清理文档格式
- 定期更新知识库内容
- 设置合理的 score_threshold
""",
        "category": "Agent工作流模板",
        "sub_category": "Dify工作流",
        "tags": ["Dify", "工作流", "知识库", "Chatflow"],
        "fit_tools": ["Dify"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "Ollama 本地角色定制 Skill",
        "desc": "通过 Modelfile 定制 Ollama 本地模型的角色、参数和行为",
        "content": """# Ollama 本地角色定制 Skill

## Modelfile 模板

```
# 基础模型
FROM llama3.1:8b

# 系统提示词
SYSTEM \"\"\"
你是一个[角色描述]。

## 核心设定
- 身份：[具体身份]
- 专长：[专业领域]
- 风格：[回答风格]

## 行为规则
1. [规则1]
2. [规则2]
3. [规则3]

## 回答格式
[期望的输出格式]
\"\"\"

# 模型参数
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
PARAMETER repeat_penalty 1.1

# 对话示例
MESSAGE user 你好，请介绍一下你自己
MESSAGE assistant [示例回答]
```

## 创建步骤
```bash
# 1. 创建 Modelfile
vim MyModel

# 2. 构建模型
ollama create my-assistant -f MyModel

# 3. 运行
ollama run my-assistant
```

## 常用参数说明
| 参数 | 说明 | 推荐值 |
|------|------|--------|
| temperature | 创造性 | 0.1-0.9 |
| num_ctx | 上下文长度 | 4096-8192 |
| top_p | 核采样 | 0.9 |
| repeat_penalty | 重复惩罚 | 1.1 |
| num_predict | 最大输出token | 2048 |

## 进阶技巧
- 使用 ADAPTER 加载 LoRA 微调权重
- 使用 TEMPLATE 自定义对话格式
- 多个 MESSAGE 示例提升 few-shot 效果
""",
        "category": "Agent工作流模板",
        "sub_category": "Ollama角色Skill",
        "tags": ["Ollama", "Modelfile", "本地模型", "角色"],
        "fit_tools": ["Ollama"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
    {
        "title": "OpenWebUI Pipeline 处理 Skill",
        "desc": "OpenWebUI 自定义 Pipeline 配置模板，实现请求预处理和输出后处理",
        "content": """# OpenWebUI Pipeline 处理 Skill

## 什么是 Pipeline
Pipeline 可以在请求发送到模型前（预处理）或收到响应后（后处理）进行自定义处理。

## Pipeline 模板

### 预处理 Pipeline（请求拦截）
```python
import json
from typing import AsyncGenerator

class Pipeline:
    def __init__(self):
        self.name = "预处理 Pipeline"

    async def run(self, body: dict) -> dict:
        # 获取用户消息
        messages = body.get("messages", [])

        # 在系统消息后注入自定义指令
        system_msg = {
            "role": "system",
            "content": "请用简洁的中文回答，并在末尾给出关键词标签。"
        }

        if messages and messages[0]["role"] == "system":
            messages[0]["content"] += "\\n" + system_msg["content"]
        else:
            messages.insert(0, system_msg)

        body["messages"] = messages
        return body
```

### 后处理 Pipeline（响应过滤）
```python
class Pipeline:
    def __init__(self):
        self.name = "敏感词过滤"
        self.blocked_words = ["敏感词1", "敏感词2"]

    async def run(self, body: dict) -> dict:
        # 过滤响应中的敏感内容
        choices = body.get("choices", [])
        for choice in choices:
            content = choice.get("message", {}).get("content", "")
            for word in self.blocked_words:
                content = content.replace(word, "***")
            choice["message"]["content"] = content
        return body
```

## 部署方式
1. 将 Pipeline 代码放入 OpenWebUI 的 pipelines 目录
2. 或通过 Web UI → Admin → Pipelines 上传
3. 确保安装了必要的依赖

## 常见用途
- 注入系统提示词
- 敏感词过滤
- 日志记录
- 请求限流
- 格式转换
""",
        "category": "Agent工作流模板",
        "sub_category": "OpenWebUI Pipeline",
        "tags": ["OpenWebUI", "Pipeline", "预处理", "过滤"],
        "fit_tools": ["OpenWebUI"],
        "author": "AI Skill库",
        "source_type": "原创",
        "license": "MIT",
    },
]


def import_skills():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 确保表存在
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            desc TEXT DEFAULT '',
            content TEXT DEFAULT '',
            category TEXT NOT NULL,
            sub_category TEXT DEFAULT '',
            tags TEXT DEFAULT '[]',
            fit_tools TEXT DEFAULT '[]',
            author TEXT DEFAULT '',
            source_type TEXT DEFAULT '原创',
            license TEXT DEFAULT 'MIT',
            collect_num INTEGER DEFAULT 0,
            view_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            uploader_id INTEGER DEFAULT 1,
            reviewer_id INTEGER,
            review_note TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    now = datetime.now().isoformat()
    count = 0

    for skill in SKILLS:
        # 检查是否已存在同名
        cursor.execute("SELECT id FROM skills WHERE title = ?", (skill["title"],))
        if cursor.fetchone():
            print(f"  跳过（已存在）: {skill['title']}")
            continue

        cursor.execute("""
            INSERT INTO skills (title, desc, content, category, sub_category, tags, fit_tools,
                              author, source_type, license, collect_num, view_count, status,
                              uploader_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'published', 1, ?, ?)
        """, (
            skill["title"],
            skill["desc"],
            skill["content"],
            skill["category"],
            skill["sub_category"],
            json.dumps(skill["tags"], ensure_ascii=False),
            json.dumps(skill["fit_tools"], ensure_ascii=False),
            skill["author"],
            skill["source_type"],
            skill["license"],
            0,
            0,
            now,
            now,
        ))
        count += 1
        print(f"  ✅ {skill['category']} / {skill['title']}")

    conn.commit()
    conn.close()
    print(f"\n导入完成！新增 {count} 条 Skill，共 {len(SKILLS)} 条待处理")


if __name__ == "__main__":
    print("开始导入 Skill 数据...\n")
    import_skills()
