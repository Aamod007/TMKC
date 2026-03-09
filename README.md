# TMKC - Task Monitoring and Kernel Controller

**TMKC** is a lightweight, terminal-based system monitor and process controller built with Python and [Textual](https://github.com/Textualize/textual). It provides a real-time overview of your system's performance and allows you to manage running processes directly from the command line with a modern TUI (Terminal User Interface).

![TMKC TUI](https://raw.githubusercontent.com/Textualize/textual/main/imgs/textual.png)
*(Note: Screenshot placeholder)*

## 🚀 Features

*   **Real-time System Monitoring**:
    *   Live CPU usage tracking.
    *   Real-time Memory usage (Used vs Total).
*   **Process Management**:
    *   View running processes with details (PID, Name, Status, CPU%, Memory).
    *   Auto-sorting by CPU usage to highlight resource-heavy tasks.
*   **Process Control**:
    *   **Kill**: Terminate unresponsive or unwanted processes.
    *   **Suspend**: Temporarily pause a process to free up resources.
    *   **Resume**: Continue execution of suspended processes.
*   **Cross-Platform**: Works on Windows, macOS, and Linux (thanks to Python & psutil).

## 🛠️ Installation

### Prerequisites

*   Python 3.8 or higher
*   pip (Python package manager)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Aamod007/TMKC.git
    cd TMKC
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    # Create virtual environment (optional but recommended)
    python -m venv venv
    
    # Activate virtual environment
    # Windows:
    .\venv\Scripts\activate
    # Linux/macOS:
    source venv/bin/activate

    # Install requirements
    pip install -r requirements.txt
    ```

## 🖥️ Usage

Run the application using Python:

```bash
python tmkc.py
```

### ⌨️ Controls / Keybindings

| Key | Action | Description |
| :--- | :--- | :--- |
| **`k`** | **Kill Process** | Terminates the currently selected process. |
| **`s`** | **Suspend** | Suspends (pauses) the currently selected process. |
| **`r`** | **Resume** | Resumes a previously suspended process. |
| **`q`** | **Quit** | Exits the application. |
| **`↑` / `↓`** | **Navigation** | Move selection up or down in the process list. |

## 📦 Dependencies

*   [**Textual**](https://textual.textualize.io/): A Rapid Application Development framework for Python TUI.
*   [**psutil**](https://psutil.readthedocs.io/): Cross-platform library for retrieving information on running processes and system utilization.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source.
