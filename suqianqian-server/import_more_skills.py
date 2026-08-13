"""
从开源仓库导入更多 Skill/Prompt 数据
数据源：
1. PlexPt/awesome-chatgpt-prompts-zh (中文提示词 ~120条)
2. f/awesome-chatgpt-prompts (英文提示词 CSV)
"""
import sqlite3
import json
import csv
import os
from datetime import datetime

DB_PATH = "suqianqian.db"
CHINESE_JSON = "/Users/wangzhengsong/.qoder-cn/cache/projects/suqianqian_all-3486a35a/agent-tools/56e3d282/2eb8db8b.txt"
ENGLISH_CSV = "/tmp/prompts_en.csv"

# 关键词 → 分类映射
CATEGORY_RULES = [
    # 程序/测试/运维
    (["linux", "terminal", "sql", "php", "javascript", "console", "python", "code",
      "developer", "programming", "frontend", "全栈", "前端", "后端", "开发",
      "编程", "代码", "正则", "regex", "git", "commit", "stack", "dba",
      "数据库", "算法", "golang", "angular", "react", "svg", "solr",
      "ethereum", "blockchain", "smart contract", "r programming", "machine learning",
      "it专家", "it架构师", "网络安全", "fullstack"], "程序/测试/运维"),
    # 办公自动化SOP
    (["excel", "sheet", "工作表", "产品经理", "prd", "招聘", "简历",
      "logistics", "物流", "会计", "accountant", "财务", "ceo", "首席执行官",
      "office", "周报", "会议纪要", "manager", "hr", "人才"], "办公自动化SOP"),
    # 学习科研助手
    (["老师", "teacher", "教授", "professor", "数学", "math", "哲学",
      "philosophy", "论文", "thesis", "学术", "academic", "院士",
      "讲师", "lecturer", "教育", "education", "历史", "history",
      "雅思", "ielts", "翻译", "translator", "dictionary", "词典",
      "发音", "pronunciation", "语言", "language"], "学习科研助手"),
    # 行业垂直Skill
    (["医生", "doctor", "dentist", "牙医", "心理", "psycholog",
      "health", "营养", "nutrition", "fitness", "健身", "教练", "coach",
      "律师", "legal", "lawyer", "房产", "real estate", "金融", "finance",
      "投资", "invest", "银行", "医疗", "pet", "宠物", "兽医",
      "关系教练", "relationship", "career", "职业顾问"], "行业垂直Skill"),
    # 文案内容创作
    (["小说", "novel", "诗人", "poet", "poetry", "故事", "story",
      "作家", "writer", "编剧", "screenwriter", "说唱", "rapper",
      "喜剧", "comedy", "脱口秀", "音乐", "composer", "作曲家",
      "标题", "title", "广告", "advertis", "营销", "marketing",
      "文案", "copy", "评论员", "commentator", "记者",
      "美食评论", "food critic", "花店", "florist", "室内装饰",
      "interior", "设计师", "designer", "造型师", "stylist",
      "艺术家", "artist", "纹身", "emoji"], "文案内容创作"),
    # 通用AI能力
    (["面试", "interview", "辩手", "debate", "导游", "tour", "guide",
      "励志", "motivat", "人生教练", "life coach", "自助", "self-help",
      "魔术师", "magic", "棋", "chess", "游戏", "game", "冒险",
      "adventure", "时间旅行", "time travel", "浏览器", "browser",
      "ai", "人工智能", "提示词", "prompt", "生成器", "generator",
      "克隆", "clone", "角色", "act as", "扮演", "模仿",
      "域名", "domain", "启动", "startup", "创业"], "通用AI能力"),
]

# 英文 → 中文翻译映射（常见角色）
EN_CN_TITLE = {
    "Linux Terminal": "Linux 终端模拟器",
    "English Translator": "英语翻译改进者",
    "English Pronunciation Helper": "英语发音帮手",
    "Frontend Developer": "前端开发专家",
    "Software Engineer": "全栈软件工程师",
    "IT Expert": "IT 技术专家",
    "IT Architect": "IT 架构师",
    "Cyber Security Specialist": "网络安全专家",
    "Doctor": "AI 辅助医生",
    "Dentist": "AI 牙医",
    "Chef": "AI 私人厨师",
    "Mathematician": "数学家",
    "Math Teacher": "数学老师",
    "Philosophy Teacher": "哲学老师",
    "Philosopher": "哲学家",
    "Poet": "诗人",
    "Novelist": "小说家",
    "Screenwriter": "编剧",
    "Composer": "作曲家",
    "Rapper": "说唱歌手",
    "Motivational Speaker": "励志演讲者",
    "Motivational Coach": "励志教练",
    "Life Coach": "人生教练",
    "Career Counselor": "职业顾问",
    "Relationship Coach": "关系教练",
    "Mental Health Counselor": "心理健康顾问",
    "Psychologist": "心理学家",
    "Nutritionist": "营养师",
    "Personal Trainer": "私人健身教练",
    "Real Estate Agent": "房地产经纪人",
    "Financial Analyst": "金融分析师",
    "Investment Manager": "投资经理",
    "Accountant": "会计师",
    "Lawyer": "法律顾问",
    "Teacher": "AI 讲师",
    "Professor": "院士/教授",
    "Interviewer": "面试官",
    "Debater": "辩手",
    "Debate Coach": "辩论教练",
    "Tour Guide": "旅游指南",
    "Magician": "魔术师",
    "Pet Behaviorist": "宠物行为专家",
    "Interior Designer": "室内装饰师",
    "Personal Shopper": "个人购物员",
    "Food Critic": "美食评论家",
    "Personal Stylist": "个人造型师",
    "UX/UI Developer": "UX/UI 开发者",
    "SVG Designer": "SVG 设计师",
    "Web Designer": "网页设计顾问",
    "Product Manager": "产品经理",
    "Machine Learning Engineer": "机器学习工程师",
    "Full Stack Developer": "全栈开发工程师",
    "Regex Generator": "正则表达式生成器",
    "SQL Terminal": "SQL 终端",
    "PHP Interpreter": "PHP 解释器",
    "JavaScript Console": "JavaScript 控制台",
    "R Programming Interpreter": "R 编程解释器",
    "StackOverflow Post": "StackOverflow 助手",
    "Commit Message Generator": "Git 提交消息生成器",
    "Title Generator": "标题生成器",
    "Prompt Generator": "提示词生成器",
    "Domain Name Generator": "域名生成器",
    "Startup Idea Generator": "创业点子生成器",
    "Habit Tracker": "习惯追踪应用",
    "Ethereum Developer": "以太坊开发者",
    "Plagiarism Checker": "抄袭检查员",
    "Emoji Translator": "表情符号翻译器",
    "Language Detector": "语言检测器",
    "Solr Search Engine": "Solr 搜索引擎",
    "Graphviz DOT Generator": "图表生成器",
    "Time Travel Guide": "时间旅行向导",
    "Talent Coach": "人才教练",
    "Salesperson": "销售员",
    "Emergency Response": "应急响应专家",
    "Web Browser": "文本浏览器",
    "Senior Frontend Developer": "高级前端开发",
    "Artist Advisor": "艺人顾问",
    "Financial Advisor": "财务顾问",
    "Tea Taster": "品茶师",
    "Florist": "花店",
    "Logistician": "物流师",
    "Recruiter": "招聘人员",
    "CEO": "CEO 首席执行官",
    "Researcher": "研究员",
    "Etymologist": "词源学家",
    "Journalist": "评论员/记者",
    "AI Writing Tutor": "AI 写作导师",
    "Bible Translator": "圣经翻译",
    "Language Pathologist": "语言病理学家",
    "Startup Tech Lawyer": "创业技术律师",
    "Song Recommender": "歌曲推荐人",
    "Cover Letter": "求职信生成器",
    "Text Analyzer": "文本分析工具",
    "Image Editor": "图像编辑器",
    "Ads Specialist": "广告专家",
    "Real Estate Professional": "房产经纪人",
    "Travel Guide": "旅行向导",
    "Storyteller": "讲故事的人",
    "Stand-up Comedian": "脱口秀演员",
    "Football Commentator": "足球解说员",
    "Car Mechanic": "汽车修理工",
    "Chess Player": "棋手",
    "Math History Teacher": "数学历史老师",
    "Tarot Reader": "塔罗占卜师",
    "Virtual Doctor": "虚拟医生",
    "Personal Cook": "私人厨师",
    "Statistician": "统计学家",
    "Developer Relations": "开发者关系顾问",
    "Tech Reviewer": "技术审查员",
    "Habit Tracker App": "习惯追踪器",
}


def match_category(title, prompt_text):
    """根据标题和内容匹配分类"""
    text = (title + " " + prompt_text[:200]).lower()
    for keywords, category in CATEGORY_RULES:
        for kw in keywords:
            if kw.lower() in text:
                return category
    return "通用AI能力"


def extract_tags(title, prompt_text):
    """从标题和内容提取标签"""
    tags = []
    text = (title + " " + prompt_text[:300]).lower()

    tag_keywords = {
        "编程": ["code", "编程", "代码", "developer", "开发", "python", "javascript", "sql", "php"],
        "翻译": ["翻译", "translat", "字典", "dictionary"],
        "写作": ["写", "writ", "文章", "文案", "小说", "诗"],
        "教育": ["老师", "teacher", "教", "学", "教育", "学习"],
        "医疗": ["医生", "doctor", "医疗", "健康", "营养"],
        "金融": ["金融", "财务", "投资", "银行", "会计"],
        "设计": ["设计", "design", "ui", "ux", "svg"],
        "法律": ["法律", "lawyer", "律师", "合规"],
        "办公": ["excel", "办公", "报告", "周报", "会议"],
        "创意": ["创意", "创意", "故事", "艺术", "音乐"],
        "面试": ["面试", "interview", "简历", "求职"],
        "AI": ["ai", "人工智能", "prompt", "提示词"],
    }

    for tag, keywords in tag_keywords.items():
        for kw in keywords:
            if kw in text:
                tags.append(tag)
                break

    return tags[:5] if tags else ["通用"]


def fit_tools_for(title, prompt_text):
    """判断适用的 AI 工具"""
    text = (title + " " + prompt_text).lower()
    tools = []
    if any(k in text for k in ["ollama", "本地", "offline", "offline"]):
        tools.append("Ollama")
    if any(k in text for k in ["openwebui", "webui", "pipeline"]):
        tools.append("OpenWebUI")
    if any(k in text for k in ["dify", "workflow", "工作流"]):
        tools.append("Dify")
    if not tools:
        tools = ["其他"]
    return tools


def import_chinese_prompts(db):
    """导入中文提示词（来自 PlexPt/awesome-chatgpt-prompts-zh）"""
    print("\n=== 导入中文提示词 ===")

    with open(CHINESE_JSON, 'r', encoding='utf-8') as f:
        prompts = json.load(f)

    count = 0
    existing_titles = set()
    cur = db.cursor()
    cur.execute("SELECT title FROM skills")
    for row in cur.fetchall():
        existing_titles.add(row[0])

    for item in prompts:
        title = item.get("act", "").strip()
        prompt = item.get("prompt", "").strip()

        if not title or not prompt:
            continue

        # 跳过不适当的内容
        if any(kw in title + prompt for kw in ["涩涩", "魅魔", "DAN", "不受约束", "醉汉", "疯子"]):
            continue

        # 去重
        if title in existing_titles:
            continue

        category = match_category(title, prompt)
        tags = extract_tags(title, prompt)
        tools = fit_tools_for(title, prompt)
        now = datetime.now().isoformat()

        # 生成描述（取前100字）
        desc = prompt[:100].replace('\n', ' ') + "..." if len(prompt) > 100 else prompt

        db.execute("""
            INSERT INTO skills (title, desc, content, category, sub_category, tags, fit_tools,
                              source_type, license, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'published', ?, ?)
        """, (title, desc, prompt, category, "", json.dumps(tags, ensure_ascii=False),
              json.dumps(tools, ensure_ascii=False), "开源改编", "CC-BY-4.0", now, now))
        existing_titles.add(title)
        count += 1

    print(f"  导入中文提示词: {count} 条")
    return count


def import_english_prompts(db):
    """导入英文提示词（来自 f/awesome-chatgpt-prompts）"""
    print("\n=== 导入英文提示词 ===")

    if not os.path.exists(ENGLISH_CSV):
        print("  英文 CSV 文件不存在，跳过")
        return 0

    count = 0
    existing_titles = set()
    cur = db.cursor()
    cur.execute("SELECT title FROM skills")
    for row in cur.fetchall():
        existing_titles.add(row[0])

    with open(ENGLISH_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            act = row.get("act", "").strip()
            prompt = row.get("prompt", "").strip()
            prompt_type = (row.get("type") or "").strip()

            if not act or not prompt:
                continue

            # 只导入文本类型（跳过代码/应用类型）
            if prompt_type and prompt_type != "TEXT":
                continue

            # 翻译标题
            cn_title = EN_CN_TITLE.get(act, act)

            # 如果标题已存在，跳过
            if cn_title in existing_titles:
                continue

            # 翻译内容为中文摘要 + 保留英文原文
            content = f"## {act}\n\n{prompt}"
            desc = prompt[:100].replace('\n', ' ') + "..." if len(prompt) > 100 else prompt

            category = match_category(act, prompt)
            tags = extract_tags(act, prompt)
            tools = fit_tools_for(act, prompt)
            now = datetime.now().isoformat()

            db.execute("""
                INSERT INTO skills (title, desc, content, category, sub_category, tags, fit_tools,
                                  source_type, license, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'published', ?, ?)
            """, (cn_title, desc, content, category, "", json.dumps(tags, ensure_ascii=False),
                  json.dumps(tools, ensure_ascii=False), "开源改编", "CC-BY-4.0", now, now))
            existing_titles.add(cn_title)
            count += 1

    print(f"  导入英文提示词: {count} 条")
    return count


def main():
    print(f"数据库路径: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    # 统计导入前数量
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM skills")
    before = cur.fetchone()[0]
    print(f"导入前 Skill 总数: {before}")

    c1 = import_chinese_prompts(conn)
    c2 = import_english_prompts(conn)

    conn.commit()

    # 统计导入后数量
    cur.execute("SELECT COUNT(*) FROM skills")
    after = cur.fetchone()[0]
    print(f"\n=== 导入完成 ===")
    print(f"  中文: +{c1} 条")
    print(f"  英文: +{c2} 条")
    print(f"  总计: {before} → {after} (新增 {after - before} 条)")

    # 分类统计
    cur.execute("SELECT category, COUNT(*) as cnt FROM skills GROUP BY category ORDER BY cnt DESC")
    print(f"\n=== 分类分布 ===")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]} 条")

    conn.close()


if __name__ == "__main__":
    main()
