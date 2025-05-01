---
permalink: /artical/unbalance机翻笔记/
layout: post
title:  "Unbalance 机翻笔记"
date:   2024-10-24 15:33:30 +0800
---
Cherry Soft搞的第4作，4作引擎都不同，无语……（其实CRAVE和这个理论上是一个引擎，但是二进制脚本结构、封包结构都迥异）

拆包garbro可以拆，但是garbro自动解密了。脚本文件的文本部分加密了，加密方法是：第i位与i异或。

```
def dec(data):
    data_ = list(data)
    dec = []
    for i in range(len(data_)):
        dec.append(data_[i] ^ (i % 256))
    return bytes(dec)
```

封包结构很简单，4字节文件数，4字节文件开始的地址，然后是entry list：16字节文件名，4字节offset（从最开头的文件开始地址开始计算），4字节长度。后面就是文件内容。很容易就搓出了封包代码，封包回去的时候注意还原加密即可。

```python
fileCount = data.readU32()
fileStart = data.readU32()
for i in range(self.fileCount):
    filename = data.read(0x10)
    offset = data.readU32()
    length = data.readU32()
    file = data.data[fileStart + offset : fileStart + offset + length]
```

脚本结构相对比较简单，0x50字节的文件信息之类的，8个字节作用未知，接着依次是后面内容部分的总长、命令部分长度、文本部分长度、不知道干什么的部分的长度/20。后面依次是命令部分、文本部分以及不知道是干什么的部分。

命令是定长的，文本和命令分离，非常好文明。命令4字节一组，简单分析即可找到文本命令：\x00\x00\x10\x00或\x00\x00\x11\x00或\x00\x00\x12\x00 + 4字节序号+文本offset（从文本起始部分开始计算）。没提到文本长度，文本是靠\x00作为结尾的。这样可以提取出所有文本。

文本中有特殊代码#W#M#N#F#D，进游戏观察找含义。#M对应主角的名，#N对应姓这两个替换掉；#W是强制换行，删了；#F是人名标识，用这个分隔人名，之后处理译文的时候得加回来；#D是……不知道，加词典里让AI保留吧：

```
#D	#D	code, don't change it
```

日文处理采用了字体替换，用自研的汉字替换和字体处理组件 `Hanzireplacer.py`处理文本，用自研的 `FONTCHANGER.dll` hook了createfont相关函数导入字体。这个主程序没有加保护，直接用setdll.exe修改主程序就能加载FONTCHANGE.dll了：

```bash
setdll /d:FONTCHANGE.dll UB.EXE
```

封回时，采用了处理yuris时的思路。不直接替换原文本，直接把译文放在文本部分的末尾，然后改前面的offset。因为文本部分不只是文本，还有其他资源代码。如果直接在前面文本，长度改变会导致资源代码的offset改变，那还得去着资源代码的调用命令，太麻烦了。

```
    def append_trans(self, translist):
        self.readCommand()
        for command in self.strs:
            new_text = translist.pop(0).encode("932")
            offset = to_bytes(len(self.content), 4)
            self.content += new_text + b"\x00" #把译文放在文本部分最后
            self.command = self.command[:command.offset] + offset + self.command[command.offset + 4:] #更改原本的命令中的偏移。
```

最后封包，封包名字改成了SCW.CHS，然后去exe里搜SCW.PAK，改成SCW.CHS，这样安装补丁就不用覆盖原文件了。
