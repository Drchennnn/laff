<div align="center">

![L](https://img.shields.io/badge/L-FF6B6B?style=for-the-badge&labelColor=FF6B6B&color=FF6B6B)![A](https://img.shields.io/badge/A-FFD93D?style=for-the-badge&labelColor=FFD93D&color=FFD93D)![F](https://img.shields.io/badge/F-6BCB77?style=for-the-badge&labelColor=6BCB77&color=6BCB77)![F](https://img.shields.io/badge/F-4D96FF?style=for-the-badge&labelColor=4D96FF&color=4D96FF)

<img src="assets/banner.png" width="180"/>

**当你的命令失败时，奶龙替你笑出来。**

![platform](https://img.shields.io/badge/platform-Windows-blue?style=flat-square)
![python](https://img.shields.io/badge/python-3.10+-yellow?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)

</div>

---

一个 Windows 后台小工具：终端命令执行成功或失败时，自动播放对应音效。

- 命令成功 → 播放成功音效
- 命令失败 → 播放失败音效（比如罐头笑声）
- 每种事件支持多个音效，每次随机播一个
- 系统托盘图标，右键可开关
- 支持自定义音效包，换目录就换一套声音
- 同类事件 2 秒冷却，不会连续触发

---

## 使用方法

### 音效文件

把 MP3 文件放到对应子目录，文件名随意：

```
sounds/
└── default/
    ├── success/    ← 命令成功时随机播一个
    │   └── ding.mp3
    └── failure/    ← 命令失败时随机播一个
        └── laugh.mp3
```

想换一套风格？在 `sounds/` 下新建目录，结构相同，然后改 `config.yaml`：

```yaml
sound_pack: laugh_track
```

### PowerShell Hook

加入 `$PROFILE` 后，每个新开的 PowerShell 窗口自动生效：

```powershell
Add-Content $PROFILE '. "e:\laff\scripts\hook.ps1"'
```

### 开机自启

把 `laff.exe` 的快捷方式放到以下目录即可：

```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

### 文件目录

```
laff/
├── laff.exe          # 主程序
├── config.yaml       # 配置（端口 / 音量 / 音效包 / 冷却时间）
├── assets/
│   └── icon.ico      # 托盘图标
└── sounds/
    └── default/
        ├── success/  ← 放 mp3
        └── failure/  ← 放 mp3
```
