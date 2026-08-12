# HOW TO USE: AI Mention Velocity Ticker

![Screenshot](asset/1.PNG)


## Setup Instructions
1. **Python Environment**: Ensure you have Python 3.8+ installed.
2. **Dependencies**: Install the required libraries using the provided requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## Operation
1. **Launch the Terminal**:
   ```bash
   python main.py
   ```
2. **Reading the Dashboard**:
   - **Scrolling Marquee (Top)**: Displays real-time headlines detected across the web.
   - **Metrics (Right)**:
     - `VELOCITY`: Shows real-time mentions per minute.
     - `HIGH-INTENT`: Tracks critical industry shifts.
   - **Histogram (Center)**: Visualizes volume spikes over the last 60 seconds.
   - **Console (Bottom)**: Detailed log of every detected signal and its classification.

## Customization
You can modify the monitored feeds in `main.py` under the `DataEngine.fetch_feeds` method to include your specific brand keywords or competitor URLs.

## Exporting Data
Click events and velocity spikes are logged internally. In future versions, these will be synced directly to your central GEO dashboard.
