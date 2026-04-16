# 默认音效包

把你的音效文件按以下结构放好：

```
sounds/default/
├── success/     ← 命令成功时随机播放其中一个
│   ├── 任意名称.mp3
│   ├── 任意名称.mp3
│   └── ...
└── failure/     ← 命令失败时随机播放其中一个
    ├── 任意名称.mp3
    └── ...
```

## 命名规则

- 文件名随意，只要是 `.mp3` 格式即可
- 每个子目录里放多少个文件都行，每次触发时随机选一个播放
- 建议用有意义的名字方便管理，例如：`ding.mp3`、`cheer.mp3`、`sad_trombone.mp3`

## 自定义音效包

复制整个 `default/` 目录，改个名字（比如 `laugh_track/`），然后在 `config.yaml` 里修改：

```yaml
sound_pack: laugh_track
```

重启 `main.py` 生效。
