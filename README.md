<div align="center">

# 🚀 TMKC (Task Monitoring & Kernel Controller)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Textual](https://img.shields.io/badge/TUI-Textual-green?style=for-the-badge&logo=terminal&logoColor=white)](https://textual.textualize.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/Aamod007/TMKC/graphs/commit-activity)

**A modern, cross-platform terminal-based system monitor and process manager.**
Built for developers and sysadmins who live in the terminal.

[Features](#-key-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[Architecture](#-architecture) •
[Roadmap](#-roadmap) •
[Contributing](#-contributing)

![TMKC Demo Placeholder](https://placehold.co/800x400/1a1a1a/FFF?text=TMKC+TUI+Screenshot)

</div>

---

## 🌟 Key Features

TMKC combines the functionality of `top`/`htop` with an interactive, modern UI.

### 📊 Real-Time Monitoring
- **CPU Visualization**: Live tracking of overall CPU utilization.
- **Memory Analytics**: Instant view of RAM usage (Used vs Total).
- **Process Metrics**: Detailed statistics per process including PID, Name, Status, CPU%, and Memory consumption.

### 🎮 Interactive Control
- **Process Management**:
  - `Kill`: Force terminate unresponsive applications.
  - `Suspend`: Pause execution to free up CPU cycles without losing state.
  - `Resume`: Continue execution of paused processes.
- **Smart Sorting**: Automatically surfaces resource-hungry processes to the top.
- **Keyboard Navigation**: Fully keyboard-driven workflow for efficiency.

### 🌍 Cross-Platform
- **Windows**: Native support (tested on Windows 10/11).
- **Linux**: Works on all major distributions.
- **macOS**: Fully compatible.

---

## 🛠 Installation

### Prerequisites
- Python 3.8 or higher
- Terminal with UTF-8 support (e.g., Windows Terminal, iTerm2, Alacritty)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Aamod007/TMKC.git
   cd TMKC
   ```

2. **Set Up Environment (Recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥 Usage

Launch the application directly from your terminal:

```bash
python tmkc.py
```

### ⌨️ Key Bindings

| Key | Action | Description |
|:---:|:---|:---|
| <kbd>k</kbd> | **Kill** | Terminate the selected process immediately (SIGTERM/SIGKILL). |
| <kbd>s</kbd> | **Suspend** | Pause the selected process execution. |
| <kbd>r</kbd> | **Resume** | Resume a suspended process. |
| <kbd>q</kbd> | **Quit** | Exit the application safely. |
| <kbd>↑</kbd> / <kbd>↓</kbd> | **Navigate** | Scroll through the process list. |

---

## 🏗 Architecture

TMKC is built using a reactive architecture powered by **Textual**.

- **Core Logic (`tmkc.py`)**:
  - `SystemMonitor`: A reactive widget that polls `psutil` for global system stats.
  - `ProcessTable`: A dynamic data table that updates in real-time. It handles the complexity of diffing process lists to minimize UI redraws.
  - `TMKCApp`: The main application controller handling input events and coordinating between widgets.
- **Data Layer**:
  - Uses `psutil` for cross-platform system calls.
  - Handles permission errors gracefully (e.g., trying to kill a root process).

---

## 🗺 Roadmap

- [ ] **Network Monitoring**: Add real-time upload/download speeds.
- [ ] **Disk I/O**: Track read/write operations per process.
- [ ] **Process Filtering**: Search bar to filter processes by name.
- [ ] **Tree View**: Visualize process hierarchy (parent/child relationships).
- [ ] **Themes**: Customizable color schemes (Dracula, Nord, Monokai).

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
Made with ❤️ by Aamod using Python & Textual
</div>
