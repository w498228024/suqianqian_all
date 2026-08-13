#!/usr/bin/env python3
"""
SQLite → JSON 导出工具
将 SQLite 数据库中的 skills 和 settings 导出为云数据库可导入的 JSON 格式

使用方式:
  python3 export_to_cloud.py

输出:
  - cloud_skills.json  — 可直接在微信云开发控制台「导入」
  - cloud_settings.json — 同上
"""
import sqlite3
import json
from datetime import datetime

DB_PATH = "suqianqian.db"


def export_skills():
    """导出 skills 表为云数据库 JSON 格式"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM skills ORDER BY id")
    rows = cursor.fetchall()

    skills = []
    for row in rows:
        skill = {
            "title": row["title"],
            "desc": row["desc"] or "",
            "content": row["content"] or "",
            "category": row["category"] or "",
            "sub_category": row["sub_category"] or "",
            "tags": json.loads(row["tags"]) if row["tags"] else [],
            "fit_tools": json.loads(row["fit_tools"]) if row["fit_tools"] else [],
            "author": row["author"] or "",
            "source_type": row["source_type"] or "原创",
            "license": row["license"] or "MIT",
            "collect_num": row["collect_num"] or 0,
            "view_count": row["view_count"] or 0,
            "status": row["status"] or "published",
            "old_id": row["id"],
            "uploader_openid": "",
            "created_at": row["created_at"] or datetime.now().isoformat(),
            "updated_at": row["updated_at"] or datetime.now().isoformat(),
        }
        skills.append(skill)

    conn.close()

    output_path = "cloud_skills.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)

    print(f"✅ 导出 {len(skills)} 条 Skill → {output_path}")
    return len(skills)


def export_settings():
    """导出 settings 表为云数据库 JSON 格式"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM settings")
    rows = cursor.fetchall()

    settings = []
    for row in rows:
        settings.append({
            "key": row["key"],
            "value": row["value"],
        })

    conn.close()

    output_path = "cloud_settings.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

    print(f"✅ 导出 {len(settings)} 条设置 → {output_path}")
    return len(settings)


def main():
    print("=" * 50)
    print("SQLite → 云数据库 JSON 导出工具")
    print("=" * 50)

    skill_count = export_skills()
    settings_count = export_settings()

    print()
    print(f"总计: {skill_count} 条 Skill + {settings_count} 条设置")
    print()
    print("📋 导入步骤:")
    print("  1. 打开微信开发者工具 → 云开发控制台")
    print("  2. 进入「数据库」→ 选择集合（如 skills）")
    print("  3. 点击右上角「导入」→ 选择对应的 JSON 文件")
    print("  4. 对 settings 集合重复上述步骤")
    print("  5. 确保已创建全部 5 个集合: users, skills, favorites, admins, settings")


if __name__ == "__main__":
    main()
