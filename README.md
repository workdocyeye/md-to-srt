# md-to-srt

OpenCode Skill — 将 Markdown 文档转换为 SRT 字幕文件，智能分段 + 自动计算显示时长。

## 功能

- 将 Markdown 文档（标题、段落、列表）解析为字幕文本
- 按中英文标点智能断句（句号、问号、叹号、逗号等）
- 每行字幕最长 30 个字符，超长自动拆分
- 根据阅读速度（默认 4.0 字符/秒）自动计算每条字幕显示时长
- 时间戳首尾相接，输出标准 SRT 格式文件
- 支持调整阅读速度、每行最大字符数等参数

## 典型场景

写完视频文案后，需要生成 SRT 字幕文件导入剪映进行配音。直接用这个 Skill 把 Markdown 文案转成 SRT，省去手动对时间戳的工作。

## 安装

### 前置依赖

- Python 3.10+

### 方式一：OpenCode Skill（推荐）

克隆本仓库到 OpenCode 的 skills 目录：

```bash
git clone https://github.com/workdocyeye/md-to-srt.git ~/.config/opencode/skills/md-to-srt
```

安装后重启 OpenCode，使用 `/md-to-srt` 命令即可调用，在对话中 `@` 引用你的 Markdown 文件。

### 方式二：直接运行 Python

```bash
git clone https://github.com/workdocyeye/md-to-srt.git
cd md-to-srt
python scripts/md_to_srt.py input.md -o output.srt
```

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-o / --output` | 与输入同名 `.srt` | 输出文件路径 |
| `--max-chars` | `30` | 每行字幕最大字符数 |
| `--reading-speed` | `4.0` | 阅读速度（字符/秒），越小越慢 |
| `--gap-min` | `0.3` | 字幕间最小间隔（秒） |
| `--gap-max` | `0.6` | 字幕间最大间隔（秒） |

## 示例

```bash
# 默认设置
python scripts/md_to_srt.py content.md

# 自定义参数
python scripts/md_to_srt.py content.md --max-chars 25 --reading-speed 3.0

# 指定输出路径
python scripts/md_to_srt.py content.md -o subtitles.srt
```

## License

[MIT](LICENSE)
