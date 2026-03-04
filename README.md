# ♾️ LoopScreen

**LoopScreen** is a lightweight, stand-alone media and URL playlist manager designed for corporate digital signage, dashboards, and self-service totems. It allows users to seamlessly create an infinite loop playlist mixing web URLs and local media files, with precise timing controls for each screen.

## ✨ Features

- **Mixed Playlists:** Interleave web URLs (dashboards, websites) with local media files (MP4, AVI, JPG, PNG) in a single sequence.
- **Precision Timing:** Define custom display durations (in seconds) for each individual screen.
- **Auto-Save:** All configurations are automatically saved to a `playlist.json` file, ensuring no data is lost upon exit.
- **Modern UI/UX:** Features a fully custom dark-mode interface, responsive design, and a frameless window with custom native-like controls (Minimize, Maximize, Close).
- **Stand-alone Ready:** Can be compiled into a portable `.exe` file to run on any Windows machine without requiring Python installation.

## 🛠️ Tech Stack

The project utilizes a hybrid architecture, separating the core system logic from the graphical interface:

- **Backend:** Python 3
- **Desktop Engine:** `pywebview` (powered by Windows native WebView2 / Edge Chromium)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Packager:** PyInstaller

## 🚀 Getting Started (Development)

### Prerequisites

- Python 3.10 or higher.
- Windows 10 or 11 (recommended for native WebView2 support).

### Installation

1. Clone this repository or download the source code.
2. Open your terminal in the project's root folder and install the required dependency:
   ```Bash
      pip install pywebview
   ```

### Running the App

To open the management interface

```bash
   python main.py
```

(Note: The player script core.py will be triggered automatically when you click "Iniciar" in the dashboard).

## 📦 Building for Production (Generating the .exe)

To transform the project into a professional, double-click executable without the terminal console, we use PyInstaller.

1. Install PyInstaller:
   ```bash
      pip install pyinstaller
   ```
2. Run the following build command in the root directory (ensure you have an icone.ico file in the folder):
   ```bash
      pyinstaller --name "LoopScreen" --windowed --icon="icone.ico" --add-data "index.html;." --add-data "style.css;." --add-data "script.js;." main.py
   ```
3. The final executable will be generated inside the dist/LoopScreen folder.

## 🗂️ File Structure

- **`main.py:`** The entry point. Initializes the GUI and acts as the API bridge between Python and JavaScript.
- **`core.py`**: The Player engine. Reads the generated JSON and plays the media/URLs in full screen.
- **`index.html `**/ **`style.css`** / **`script.js`**: The frontend files that build the management dashboard.
- **`playlist.json:`** Auto-generated file storing the user's current playlist configuration.

---

Developed to streamline the management of visual panels.
