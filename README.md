# Platinum-tool

A minimalistic time calculator CLI tool built in Python. Designed to run on Windows, macOS, and Linux. Includes time calculations, astronomical features, and proprietary licensing.

## Installation

### Option 1: Run from Source

1. Clone the repository:
   ```
   git clone https://github.com/Awuah-B/platinum-tool.git
   cd platinum-tool
   ```

2. Create and activate virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the tool:
   ```
   python src/cli.py
   ```

### Option 2: Use Pre-built Executable

Download the latest executable from the releases page and run it directly:
```
./platinum-tool  # On macOS/Linux
platinum-tool.exe  # On Windows
```

To build your own executable:
```
pip install pyinstaller
pyinstaller --onefile --paths src --name platinum-tool main.py
```

## Usage

- Start the tool and enter your access key when prompted.
- Navigate through the menus to perform time calculations or astronomical queries.
- Contact: awuahbj@gmail.com for support.

## Features

- Time difference calculations
- Date offset calculations
- Astronomical ephemeris (planetary positions, synodic angles)
- Proprietary licensing with expiring keys

## Development

- Run tests: `pytest`
- Build executable: See installation instructions

## License

Proprietary software. Unauthorized distribution is prohibited.