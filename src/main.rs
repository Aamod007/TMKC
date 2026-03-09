use std::{
    io,
    time::{Duration, Instant},
};

use anyhow::Result;
use crossterm::{
    event::{self, Event, KeyCode, KeyEventKind},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{
    prelude::*,
    widgets::{Block, Borders, List, ListItem, Paragraph, Wrap},
};
use sysinfo::{ProcessRefreshKind, RefreshKind, System};

struct App {
    system: System,
    should_quit: bool,
    selected_process_index: usize,
    process_list_state: usize, // Simplified for now, usually use ListState
}

impl App {
    fn new() -> Self {
        let mut system = System::new_with_specifics(
            RefreshKind::new()
                .with_cpu(sysinfo::CpuRefreshKind::everything())
                .with_memory()
                .with_processes(ProcessRefreshKind::everything()),
        );
        system.refresh_all();
        
        Self {
            system,
            should_quit: false,
            selected_process_index: 0,
            process_list_state: 0,
        }
    }

    fn on_tick(&mut self) {
        self.system.refresh_all();
    }
}

fn main() -> Result<()> {
    // Setup terminal
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    // Create app state
    let mut app = App::new();
    let tick_rate = Duration::from_millis(1000);
    let mut last_tick = Instant::now();

    loop {
        terminal.draw(|f| ui(f, &mut app))?;

        let timeout = tick_rate
            .checked_sub(last_tick.elapsed())
            .unwrap_or_else(|| Duration::from_secs(0));

        if crossterm::event::poll(timeout)? {
            if let Event::Key(key) = event::read()? {
                if key.kind == KeyEventKind::Press {
                    match key.code {
                        KeyCode::Char('q') => app.should_quit = true,
                        _ => {}
                    }
                }
            }
        }

        if last_tick.elapsed() >= tick_rate {
            app.on_tick();
            last_tick = Instant::now();
        }

        if app.should_quit {
            break;
        }
    }

    // Restore terminal
    disable_raw_mode()?;
    execute!(
        terminal.backend_mut(),
        LeaveAlternateScreen
    )?;
    terminal.show_cursor()?;

    Ok(())
}

fn ui(f: &mut Frame, app: &mut App) {
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3), // Header / System Info
            Constraint::Min(0),    // Process List
            Constraint::Length(3), // Footer / Help
        ])
        .split(f.area());

    // Header: System Info
    let memory_used = app.system.used_memory() / 1024 / 1024;
    let memory_total = app.system.total_memory() / 1024 / 1024;
    let cpu_usage = app.system.global_cpu_info().cpu_usage();
    
    let header_text = format!(
        "TMKC - Task Monitoring & Kernel Controller | CPU: {:.1}% | MEM: {}/{} MB",
        cpu_usage, memory_used, memory_total
    );

    let header = Paragraph::new(header_text)
        .block(Block::default().borders(Borders::ALL).title("System Info"))
        .style(Style::default().fg(Color::Cyan));
    
    f.render_widget(header, chunks[0]);

    // Body: Process List
    // Convert process map to a sorted list for display
    let mut processes: Vec<_> = app.system.processes().values().collect();
    processes.sort_by(|a, b| b.cpu_usage().partial_cmp(&a.cpu_usage()).unwrap_or(std::cmp::Ordering::Equal));
    
    // Take top 50 for performance in this basic version
    let items: Vec<ListItem> = processes.iter().take(50).map(|p| {
        let name = p.name().to_string_lossy();
        let pid = p.pid();
        let cpu = p.cpu_usage();
        let mem = p.memory() / 1024 / 1024;
        
        let content = format!("{:6} | {:<20} | CPU: {:>5.1}% | MEM: {:>5} MB", pid, name, cpu, mem);
        ListItem::new(content)
    }).collect();

    let list = List::new(items)
        .block(Block::default().borders(Borders::ALL).title("Top Processes (Sorted by CPU)"))
        .highlight_style(Style::default().add_modifier(Modifier::BOLD));
    
    f.render_widget(list, chunks[1]);

    // Footer: Help
    let footer = Paragraph::new("Press 'q' to quit")
        .block(Block::default().borders(Borders::ALL).title("Controls"))
        .wrap(Wrap { trim: true });
        
    f.render_widget(footer, chunks[2]);
}
