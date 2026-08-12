# Technical Documentation: Digital Footprint Intelligence Hub

## 1. System Architecture
The application follows the **Modular Asynchronous Service-Oriented (MASO)** architecture. It decouples the network scanning engines from the UI rendering layer using an Observer pattern and background threading.

### Engine Layer
- **OSINTScanner**: Uses `aiohttp.ClientSession` with an `asyncio.Semaphore` (default 50) to manage high-concurrency requests. It replicates the Sherlock logic by checking status codes and performing string-based exclusion for false positives.
- **GoogleDorker**: A scraping-based engine that generates target-specific dorks (filetype, inurl, intitle) and parses Google search results using `BeautifulSoup4`.

### UI Layer
- **Kivy/KivyMD**: Provides the cross-platform GUI framework.
- **CanvasController**: Manages the `NetworkX` graph. It calculates the `spring_layout` in real-time as new nodes are added, ensuring an organic and readable relationship map.
- **SidebarManager**: Orchestrates the glassmorphism sidebar, handling the live event log and the inspector panel.

## 2. Data Persistence
- **SQLite3**: Used to store investigation sessions.
- **Schema**:
  - `investigations`: Tracks the target and timestamp.
  - `discovered_accounts`: Stores found platform URLs and metadata.
  - `dork_results`: Stores URL snippets and titles from the dorking engine.

## 3. File Structure
```text
/engine
  /scanner.py      # Async scanning logic
  /dorker.py       # Google dorking implementation
/ui
  /canvas_controller.py  # Graph & Node management
  /sidebar_manager.py    # UI log & Input control
  /styles.kv             # Cyber-Cyan Dark styling
/utils
  /exporter.py           # Multi-format report generation
/data
  /schema.sql            # Database initialization
main.py                  # App entry point
```

## 4. Performance Tuning
The application is optimized for low-latency UI response. Network IO is isolated in a separate `threading.Thread` with its own `asyncio` loop, communicating back to the main thread via `kivy.clock.Clock`.

---
**Developer**: HSINI MOHAMED
**Version**: 2.0.0
