import psutil
import sys
import logging
from datetime import datetime
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, DataTable, Static, Button, Label
from textual.reactive import reactive
from textual.binding import Binding

# Setup logging
logging.basicConfig(filename='tmkc.log', level=logging.DEBUG)

class SystemMonitor(Static):
    """Displays system CPU and Memory usage."""
    
    cpu_usage = reactive(0.0)
    memory_usage = reactive(0.0)
    memory_total = reactive(0.0)

    def on_mount(self) -> None:
        """Set up a timer to update system stats."""
        self.update_stats()
        self.set_interval(1, self.update_stats)

    def update_stats(self) -> None:
        """Update CPU and Memory stats."""
        try:
            self.cpu_usage = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            self.memory_usage = mem.used / (1024 * 1024)  # MB
            self.memory_total = mem.total / (1024 * 1024) # MB
            
            self.update(f"CPU: {self.cpu_usage:.1f}% | MEM: {self.memory_usage:.0f}/{self.memory_total:.0f} MB")
        except Exception as e:
            logging.error(f"Error updating stats: {e}")

class ProcessTable(DataTable):
    """Table widget to display process list."""
    
    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("PID", "Name", "Status", "CPU %", "Memory (MB)")
        self.set_interval(2, self.refresh_processes)
        self.refresh_processes()

    def refresh_processes(self) -> None:
        """Refresh the process list."""
        try:
            # Save selected row if any
            selected_row_index = self.cursor_row
            
            self.clear()
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
                try:
                    # Get process info
                    pinfo = proc.info
                    mem_mb = pinfo['memory_info'].rss / (1024 * 1024)
                    processes.append((
                        pinfo['pid'],
                        pinfo['name'],
                        pinfo['status'],
                        pinfo['cpu_percent'],
                        mem_mb
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # Sort by CPU usage descending
            processes.sort(key=lambda x: x[3], reverse=True)
            
            # Take top 50 for performance
            for p in processes[:50]:
                self.add_row(
                    str(p[0]),
                    p[1],
                    p[2],
                    f"{p[3]:.1f}",
                    f"{p[4]:.1f}",
                    key=str(p[0]) # Use PID as key
                )
                
            # Restore selection if possible (rudimentary)
            if selected_row_index is not None and selected_row_index < len(processes):
                 self.move_cursor(row=selected_row_index)
        except Exception as e:
            logging.error(f"Error refreshing processes: {e}")

class TMKCApp(App):
    """Task Monitoring and Kernel Controller Application."""

    CSS = """
    Screen {
        layout: vertical;
    }
    
    SystemMonitor {
        height: 3;
        border: solid green;
        content-align: center middle;
        text-style: bold;
    }
    
    ProcessTable {
        height: 1fr;
        border: solid blue;
    }
    
    .controls {
        height: 3;
        dock: bottom;
        layout: horizontal;
        align: center middle;
    }
    
    Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("k", "kill_process", "Kill Process"),
        Binding("s", "suspend_process", "Suspend Process"),
        Binding("r", "resume_process", "Resume Process"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield SystemMonitor()
        yield ProcessTable()
        yield Footer()

    def action_kill_process(self) -> None:
        table = self.query_one(ProcessTable)
        try:
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            if row_key:
                pid = int(row_key.value)
                self.kill_pid(pid)
        except Exception as e:
            self.notify(f"Error selecting process: {e}", severity="error")
            logging.error(f"Error in kill process action: {e}")

    def kill_pid(self, pid: int) -> None:
        try:
            p = psutil.Process(pid)
            p.terminate()
            self.notify(f"Process {pid} terminated.")
        except psutil.NoSuchProcess:
            self.notify(f"Process {pid} not found.", severity="warning")
        except psutil.AccessDenied:
            self.notify(f"Access denied to terminate process {pid}.", severity="error")
        except Exception as e:
            logging.error(f"Error killing process {pid}: {e}")
    
    def action_suspend_process(self) -> None:
        table = self.query_one(ProcessTable)
        try:
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            if row_key:
                pid = int(row_key.value)
                self.suspend_pid(pid)
        except Exception as e:
            logging.error(f"Error in suspend process action: {e}")

    def suspend_pid(self, pid: int) -> None:
        try:
            p = psutil.Process(pid)
            p.suspend()
            self.notify(f"Process {pid} suspended.")
        except Exception as e:
            self.notify(f"Error suspending process: {e}", severity="error")
            logging.error(f"Error suspending process {pid}: {e}")

    def action_resume_process(self) -> None:
        table = self.query_one(ProcessTable)
        try:
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            if row_key:
                pid = int(row_key.value)
                self.resume_pid(pid)
        except Exception as e:
            logging.error(f"Error in resume process action: {e}")

    def resume_pid(self, pid: int) -> None:
        try:
            p = psutil.Process(pid)
            p.resume()
            self.notify(f"Process {pid} resumed.")
        except Exception as e:
            self.notify(f"Error resuming process: {e}", severity="error")
            logging.error(f"Error resuming process {pid}: {e}")

if __name__ == "__main__":
    try:
        logging.info("Starting TMKC App...")
        app = TMKCApp()
        app.run()
        logging.info("TMKC App exited normally.")
    except Exception as e:
        logging.critical(f"App crashed: {e}", exc_info=True)
        print(f"App crashed: {e}")
