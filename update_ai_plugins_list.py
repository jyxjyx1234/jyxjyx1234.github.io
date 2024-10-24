from Lib import *
import os
from urllib.parse import quote

files = os.listdir("resources")
ai_plugins_list_md = open("pages/ai_plugins_list.md", "w", encoding="utf-8")
ai_plugins_list_md.write('''---
layout: page
title: "AI补丁列表"
permalink: /all_plugins/
---
''')
#ai_plugins_list_md.write("# AI补丁列表\n\n")

for f in files:
    encoded_filename = quote(f)
    text = f"[{f}](https://github.com/jyxjyx1234/jyxjyx1234.github.io/blob/main/resources/{encoded_filename})\n\n \n\n"
    ai_plugins_list_md.write(text)