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
    game_md = open(f"pages/games/{data['name']}.md", "w", encoding="utf-8")
    encoded_name = quote(data['name'])
    name = data["name"]
    game_md.write(f'''---
title: "{data['name']}"
permalink: /{encoded_name}
---\n\n
''')
    game_md.write(f"# {name}\n\n")
    if "urls" in data:
        game_md.write("## 机翻补丁文件：\n\n")
        for i in data["urls"]:
            fn = i["name"]
            u = i["url"]
            game_md.write(f"[{fn}]({u})\n\n \n\n")
    game_md.close()

for f in files:
    data = open_json(f"datas/{f}")
    encoded_name = quote(data['name'])
    text = f"## [{f}](/{encoded_name})\n\n \n\n"
    gen_game_md(data)
    ai_plugins_list_md.write(text)
