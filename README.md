<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <a href="#english">English</a> | <a href="#简体中文">简体中文</a> | <a href="#繁體中文">繁體中文</a>
</p>

---

<a name="english"></a>
# 🔍 CmdInsight

## 🎉 Project Introduction

**CmdInsight** is a lightweight terminal command history intelligent analysis engine that helps developers discover usage patterns, identify efficiency bottlenecks, and receive intelligent suggestions to boost productivity.

### 💡 What Problem Does It Solve?

- **Pattern Discovery**: Understand your command usage habits
- **Efficiency Analysis**: Identify repetitive commands that could be aliased
- **Smart Suggestions**: Get personalized command recommendations
- **Time Estimation**: See how much time you've saved through command history

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Multi-Shell Support** | Bash, Zsh, Fish, PowerShell |
| 📊 **Pattern Analysis** | Command frequency, categories, time distribution |
| 💡 **Smart Suggestions** | Alias recommendations, tool suggestions |
| 📈 **Efficiency Score** | Quantified productivity metrics |
| 🎨 **Beautiful Output** | Rich terminal UI with colors and charts |
| 📦 **Zero Config** | Auto-detects shell and history file |
| 🔒 **Privacy First** | All analysis runs locally |

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- Works on Linux, macOS, and Windows

### Installation

```bash
# Install from PyPI (recommended)
pip install cmdinsight

# Or install from source
git clone https://github.com/gitstq/CmdInsight.git
cd CmdInsight
pip install -e .
```

### Basic Usage

```bash
# Analyze your command history
cmdinsight analyze

# Get command suggestions
cmdinsight suggest

# Show history file statistics
cmdinsight stats

# Export aliases as shell script
cmdinsight suggest --export-aliases > ~/.config/cmdinsight/aliases.sh
```

## 📖 Detailed Usage Guide

### Analyze Command History

```bash
# Basic analysis
cmdinsight analyze

# Detailed report with charts
cmdinsight analyze --detailed

# Analyze specific history file
cmdinsight analyze --history ~/.bash_history --shell bash

# Export as JSON
cmdinsight analyze --format json --output report.json

# Export as Markdown
cmdinsight analyze --format markdown --output report.md
```

### Get Suggestions

```bash
# Get personalized suggestions
cmdinsight suggest

# Export suggested aliases
cmdinsight suggest --export-aliases >> ~/.bashrc
```

### Command Categories

CmdInsight automatically categorizes commands:

| Category | Examples |
|----------|----------|
| 🌿 Version Control | `git`, `svn`, `gh` |
| 📁 File Operations | `ls`, `cd`, `cp`, `mv` |
| 💻 Development | `python`, `npm`, `cargo` |
| 🐳 Docker | `docker`, `kubectl` |
| 🌐 Network | `curl`, `ssh`, `ping` |
| 📝 Text Editors | `vim`, `nano`, `code` |
| ⚙️ System | `sudo`, `systemctl`, `ps` |

## 💡 Design Philosophy

### Why CmdInsight?

1. **Privacy-First**: All analysis runs locally, no data leaves your machine
2. **Zero Dependencies Core**: Core functionality works without external packages
3. **Shell Agnostic**: Works with Bash, Zsh, Fish, and PowerShell
4. **Actionable Insights**: Not just statistics, but concrete suggestions

### Technical Choices

- **Python**: Cross-platform, easy to extend
- **Typer + Rich**: Beautiful CLI with minimal dependencies
- **Modular Design**: Parser, Analyzer, Suggester, Reporter

## 📦 Build & Deploy

### Build Package

```bash
# Install build tools
pip install build

# Build package
python -m build

# Upload to PyPI
pip install twine
twine upload dist/*
```

### Run Tests

```bash
pip install pytest
pytest tests/ -v
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
# 🔍 CmdInsight

## 🎉 项目介绍

**CmdInsight** 是一款轻量级终端命令历史智能分析引擎，帮助开发者发现使用模式、识别效率瓶颈、获取智能建议，从而提升工作效率。

### 💡 解决什么问题？

- **模式发现**：了解你的命令使用习惯
- **效率分析**：识别可以创建别名的重复命令
- **智能建议**：获取个性化的命令推荐
- **时间估算**：查看通过命令历史节省了多少时间

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **多Shell支持** | Bash、Zsh、Fish、PowerShell |
| 📊 **模式分析** | 命令频率、分类、时间分布 |
| 💡 **智能建议** | 别名推荐、工具建议 |
| 📈 **效率评分** | 量化的生产力指标 |
| 🎨 **美观输出** | 带颜色和图表的精美终端界面 |
| 📦 **零配置** | 自动检测Shell和历史文件 |
| 🔒 **隐私优先** | 所有分析均在本地运行 |

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 支持 Linux、macOS 和 Windows

### 安装方式

```bash
# 从 PyPI 安装（推荐）
pip install cmdinsight

# 或从源码安装
git clone https://github.com/gitstq/CmdInsight.git
cd CmdInsight
pip install -e .
```

### 基本用法

```bash
# 分析命令历史
cmdinsight analyze

# 获取命令建议
cmdinsight suggest

# 显示历史文件统计信息
cmdinsight stats

# 导出别名为Shell脚本
cmdinsight suggest --export-aliases > ~/.config/cmdinsight/aliases.sh
```

## 📖 详细使用指南

### 分析命令历史

```bash
# 基础分析
cmdinsight analyze

# 详细报告（含图表）
cmdinsight analyze --detailed

# 分析指定历史文件
cmdinsight analyze --history ~/.bash_history --shell bash

# 导出为JSON
cmdinsight analyze --format json --output report.json

# 导出为Markdown
cmdinsight analyze --format markdown --output report.md
```

### 获取建议

```bash
# 获取个性化建议
cmdinsight suggest

# 导出建议的别名
cmdinsight suggest --export-aliases >> ~/.bashrc
```

### 命令分类

CmdInsight 自动对命令进行分类：

| 分类 | 示例 |
|------|------|
| 🌿 版本控制 | `git`、`svn`、`gh` |
| 📁 文件操作 | `ls`、`cd`、`cp`、`mv` |
| 💻 开发工具 | `python`、`npm`、`cargo` |
| 🐳 容器 | `docker`、`kubectl` |
| 🌐 网络 | `curl`、`ssh`、`ping` |
| 📝 文本编辑 | `vim`、`nano`、`code` |
| ⚙️ 系统 | `sudo`、`systemctl`、`ps` |

## 💡 设计思路

### 为什么选择 CmdInsight？

1. **隐私优先**：所有分析均在本地运行，数据不离开你的机器
2. **核心零依赖**：核心功能无需外部包即可工作
3. **Shell无关**：支持 Bash、Zsh、Fish 和 PowerShell
4. **可操作洞察**：不只是统计，更提供具体建议

### 技术选型

- **Python**：跨平台，易于扩展
- **Typer + Rich**：美观的CLI，依赖最小化
- **模块化设计**：解析器、分析器、建议器、报告器

## 📦 打包与部署

### 构建包

```bash
# 安装构建工具
pip install build

# 构建包
python -m build

# 上传到PyPI
pip install twine
twine upload dist/*
```

### 运行测试

```bash
pip install pytest
pytest tests/ -v
```

## 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 开源协议

本项目采用 MIT 协议开源 - 详情请查看 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
# 🔍 CmdInsight

## 🎉 專案介紹

**CmdInsight** 是一款輕量級終端命令歷史智慧分析引擎，幫助開發者發現使用模式、識別效率瓶頸、獲取智慧建議，從而提升工作效率。

### 💡 解決什麼問題？

- **模式發現**：了解你的命令使用習慣
- **效率分析**：識別可以建立別名的重複命令
- **智慧建議**：獲取個人化的命令推薦
- **時間估算**：檢視透過命令歷史節省了多少時間

### ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🔍 **多Shell支援** | Bash、Zsh、Fish、PowerShell |
| 📊 **模式分析** | 命令頻率、分類、時間分佈 |
| 💡 **智慧建議** | 別名推薦、工具建議 |
| 📈 **效率評分** | 量化的生產力指標 |
| 🎨 **美觀輸出** | 帶顏色和圖表的精美終端介面 |
| 📦 **零配置** | 自動檢測Shell和歷史檔案 |
| 🔒 **隱私優先** | 所有分析均在本地執行 |

## 🚀 快速開始

### 環境要求

- Python 3.8 或更高版本
- 支援 Linux、macOS 和 Windows

### 安裝方式

```bash
# 從 PyPI 安裝（推薦）
pip install cmdinsight

# 或從原始碼安裝
git clone https://github.com/gitstq/CmdInsight.git
cd CmdInsight
pip install -e .
```

### 基本用法

```bash
# 分析命令歷史
cmdinsight analyze

# 獲取命令建議
cmdinsight suggest

# 顯示歷史檔案統計資訊
cmdinsight stats

# 匯出別名為Shell指令碼
cmdinsight suggest --export-aliases > ~/.config/cmdinsight/aliases.sh
```

## 📖 詳細使用指南

### 分析命令歷史

```bash
# 基礎分析
cmdinsight analyze

# 詳細報告（含圖表）
cmdinsight analyze --detailed

# 分析指定歷史檔案
cmdinsight analyze --history ~/.bash_history --shell bash

# 匯出為JSON
cmdinsight analyze --format json --output report.json

# 匯出為Markdown
cmdinsight analyze --format markdown --output report.md
```

### 獲取建議

```bash
# 獲取個人化建議
cmdinsight suggest

# 匯出建議的別名
cmdinsight suggest --export-aliases >> ~/.bashrc
```

### 命令分類

CmdInsight 自動對命令進行分類：

| 分類 | 範例 |
|------|------|
| 🌿 版本控制 | `git`、`svn`、`gh` |
| 📁 檔案操作 | `ls`、`cd`、`cp`、`mv` |
| 💻 開發工具 | `python`、`npm`、`cargo` |
| 🐳 容器 | `docker`、`kubectl` |
| 🌐 網路 | `curl`、`ssh`、`ping` |
| 📝 文字編輯 | `vim`、`nano`、`code` |
| ⚙️ 系統 | `sudo`、`systemctl`、`ps` |

## 💡 設計思路

### 為什麼選擇 CmdInsight？

1. **隱私優先**：所有分析均在本地執行，資料不離開你的機器
2. **核心零依賴**：核心功能無需外部套件即可工作
3. **Shell無關**：支援 Bash、Zsh、Fish 和 PowerShell
4. **可操作洞察**：不只是統計，更具體建議

### 技術選型

- **Python**：跨平台，易於擴充套件
- **Typer + Rich**：美觀的CLI，依賴最小化
- **模組化設計**：解析器、分析器、建議器、報告器

## 📦 打包與部署

### 構建套件

```bash
# 安裝構建工具
pip install build

# 構建套件
python -m build

# 上傳到PyPI
pip install twine
twine upload dist/*
```

### 執行測試

```bash
pip install pytest
pytest tests/ -v
```

## 🤝 貢獻指南

歡迎貢獻！請隨時提交 Pull Request。

1. Fork 本儲存庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'feat: Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 開源協議

本專案採用 MIT 協議開源 - 詳情請檢視 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  Made with ❤️ by CmdInsight Team
</p>
