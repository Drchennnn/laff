# laff

一个 Windows 后台小工具：当终端命令执行成功或失败时，自动播放对应音效。

## 功能

- 命令成功（退出码 0）→ 播放成功音效
- 命令失败（退出码非 0）→ 播放失败音效（比如罐头笑声）
- 系统托盘图标，右键可开关、退出
- 支持音效包切换，换个目录就换一套声音
- 每种事件支持多个音效文件，每次随机播放一个
- 同类事件 2 秒冷却，不会连续刷屏

## 工作原理

```
终端命令结束
  → PowerShell $PROFILE 里的 hook.ps1 捕获退出码
  → 通过 TCP 发送 JSON 事件到本地 9876 端口
  → Python 后台接收事件 → 匹配音效文件 → pygame 播放
```

## 项目结构

```
laff/
├── main.py                  # 入口，事件主循环
├── config.yaml              # 配置文件
├── core/
│   ├── listener.py          # TCP socket 服务，接收 hook 事件
│   ├── router.py            # 将事件映射到音效文件路径
│   └── sound_engine.py      # 异步播放，管理冷却时间
├── tray/
│   └── tray_app.py          # 系统托盘图标
├── sounds/
│   ├── default/             # 默认音效包
│   │   ├── success/         # 成功音效（随机播放）
│   │   └── failure/         # 失败音效（随机播放）
│   └── laugh_track/         # 罐头笑声音效包（示例）
│       ├── success/
│       └── failure/
└── scripts/
    └── hook.ps1             # 注入 PowerShell 的 hook 脚本
```

## 快速开始

### 1. 安装依赖

```bash
pip install pygame pystray Pillow pyyaml
```

### 2. 准备音效文件

在 `sounds/default/` 下按子目录放入 MP3 文件：

```
sounds/default/
├── success/        ← 命令成功时随机播一个
│   ├── ding.mp3
│   └── cheer.mp3
└── failure/        ← 命令失败时随机播一个
    ├── sad_trombone.mp3
    └── laugh.mp3
```

文件名随意，只要是 `.mp3` 格式即可。短音效（0.5–2 秒）效果最好。

### 3. 启动后台进程

```bash
cd e:\laff
python main.py
```

启动后托盘区会出现一个绿色圆点图标。

### 4. 注入 PowerShell hook

在 PowerShell 里运行一次（或加入 `$PROFILE` 永久生效）：

```powershell
. "e:\laff\scripts\hook.ps1"
```

加入 `$PROFILE` 的方法：

```powershell
Add-Content $PROFILE '. "e:\laff\scripts\hook.ps1"'
```

### 5. 验证

不用 PowerShell 也能测试，直接发一条 socket 消息：

```bash
python -c "import socket,json; s=socket.socket(); s.connect(('127.0.0.1',9876)); s.sendall(json.dumps({'event':'success','command':'test','exit_code':0}).encode()+b'\n'); s.close()"
```

## 配置

编辑 `config.yaml`：

```yaml
port: 9876          # 监听端口
volume: 0.8         # 音量（0.0 ~ 1.0）
sound_pack: default # 音效包目录名
cooldown: 2.0       # 冷却时间（秒）
enabled: true       # 是否启用
```

### 切换音效包

在 `sounds/` 下新建一个目录，内部同样用 `success/` 和 `failure/` 子目录存放 MP3，然后修改 `config.yaml`：

```yaml
sound_pack: laugh_track
```

重启 `main.py` 生效。

## 开机自启

用 `pythonw` 启动可以隐藏控制台窗口，在 `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` 里创建快捷方式，目标设为：

```
pythonw e:\laff\main.py
```

## 依赖

| 包 | 用途 |
|---|---|
| pygame | 音频播放 |
| pystray | 系统托盘图标 |
| Pillow | 生成托盘图标图像 |
| pyyaml | 读取配置文件 |

全部为纯 Python，无需额外系统依赖。
