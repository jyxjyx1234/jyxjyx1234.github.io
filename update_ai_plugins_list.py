from Lib import *
import os
from urllib.parse import quote

files = os.listdir("datas")
ai_plugins_list_md = open("pages/ai_plugins_list.md", "w", encoding="utf-8")
ai_plugins_list_md.write('''---
layout: page
title: "AI补丁列表"
permalink: /all_plugins/
---
''')
#ai_plugins_list_md.write("# AI补丁列表\n\n")


def gen_game_md(data):
    day = data["times"].split(" ")[0]
    game_md = open(f"_posts/{day}-{data['name']}.md", "w", encoding="utf-8")
    name = data["name"]
    idx = data["idx"]
    date = data["times"] + " +0800"
    game_md.write(f'''---
title: {name}
layout: post
permalink: /games/{idx}
date: {date}
categories: AI translation
---\n\n
''')
    #game_md.write(f"# {name}\n\n")
    game_md.write(f"请务必阅读文件中的README.md中的使用说明。如有运行问题 or bug反馈，请使用页面下方的邮箱联系我。\n\n")
    if "comment" in data:
        game_md.write(f"{data['comment']}\n\n")
    if "urls" in data:
        game_md.write("## 机翻补丁文件：\n\n")
        for i in data["urls"]:
            fn = i["name"]
            u = "../" + i["url"]
            game_md.write(f"[{fn}]({u})\n\n \n\n")
    
    if "others" in data:
        game_md.write("## 相关链接：\n\n")
        for i in data["others"]:
            fn = i
            u = "../artical/" + i
            game_md.write(f"[{fn}]({u})\n\n \n\n")

    game_md.close()

for f in files:
    data = open_json(f"datas/{f}")
    encoded_name = quote(data['name'])
    title = f.replace(".json","")
    idx = data["idx"]
    text = f"## [{title}](/games/{idx})\n\n \n\n"
    gen_game_md(data)
    ai_plugins_list_md.write(text)
