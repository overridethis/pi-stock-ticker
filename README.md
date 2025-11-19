# Pi Stock Ticker

A Raspberry Pi-based stock ticker display using a Waveshare e-Paper display. This project displays real-time stock prices and intraday charts on an e-ink screen, cycling through multiple stock symbols.

## Credits

This project is based on the original design by [Nico Burgos on MakerWorld](https://makerworld.com/en/models/1343492-raspberry-pi-stock-ticker). Special thanks for the inspiration and hardware design!

## Features

- Real-time stock price updates via Yahoo Finance API
- Intraday price charts with 5-minute intervals
- Support for multiple stock symbols (cycles through configured tickers)
- Market hours detection (displays "Market is closed" message when appropriate)
- Support for various currencies (USD, EUR, SEK, NOK, DKK, GBP, CAD, JPY, CHF, CNY, INR, AUD, ZAR)
- Optimized for Waveshare 3.52-inch e-Paper display
- Runs as a systemd service with automatic restart

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
  - **Tested on:** Raspberry Pi Zero running Raspbian Bookworm Legacy 32-bit
- Waveshare 3.52-inch e-Paper display
- SPI interface enabled on Raspberry Pi

## Project Structure

```
pi-stock-ticker/
├── main.py              # Entry point for the application
├── stock_ticker.py      # Main StockTicker class with display logic
├── stock_data.py        # Yahoo Finance data fetching functions
├── config.py            # Configuration loader
├── config.ini           # Configuration file (tickers, settings)
├── pyproject.toml       # Python project dependencies
├── install_service.sh   # Service installation script
└── README.md            # This file
```

## Installation

### 1. Install Git (if not already installed)

Git is required to clone repositories. Install it on your Raspberry Pi:

```bash
sudo apt-get update
sudo apt-get install git -y
```

### 2. Enable SPI on Raspberry Pi

```bash
sudo raspi-config
# Navigate to: Interfacing Options -> SPI -> Enable
```

### 3. Install Waveshare e-Paper Library

Follow the instructions at: https://github.com/waveshare/e-Paper

```bash
cd ~
git clone https://github.com/waveshare/e-Paper
cd e-Paper/RaspberryPi_JetsonNano/python
sudo python3 setup.py install
```

### 4. Clone This Repository

```bash
cd ~
git clone https://github.com/overridethis/pi-stock-ticker pi-stock-ticker
cd pi-stock-ticker
```

### 5. Set Up Python Virtual Environment

It's recommended to use a virtual environment to isolate dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 6. Install Python Dependencies

```bash
pip3 install -e .
```

**Note:** Make sure to activate the virtual environment (`source venv/bin/activate`) before running the application or installing the service.

### 7. Configure Your Stock Tickers

Edit `config.ini` to add your desired stock symbols:

```ini
[epaper]
lib_path=/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib/

[tickers]
symbols=AAPL,GOOGL,MSFT,TSLA
```

You can add any valid stock ticker symbols separated by commas. Examples:
- US Stocks: `AAPL`, `GOOGL`, `MSFT`, `TSLA`
- Indices: `^GSPC` (S&P 500), `^DJI` (Dow Jones), `^OMX` (OMX Stockholm)
- International: `SAP.DE` (Frankfurt), `VOD.L` (London), `HM-B.ST` (Stockholm)

## Running the Application

### Manual Run

```bash
python3 main.py
```

Press `Ctrl+C` to stop.

### Install as a Service (Recommended)

To have the stock ticker start automatically on boot:

```bash
chmod +x install_service.sh
./install_service.sh
```

The script will install the application as a systemd service.

## Service Management

After installing as a service, you can manage it with these commands:

```bash
# Start the service
sudo systemctl start pi-stock-ticker

# Stop the service
sudo systemctl stop pi-stock-ticker

# Restart the service
sudo systemctl restart pi-stock-ticker

# View service status
sudo systemctl status pi-stock-ticker

# View live logs
sudo journalctl -u pi-stock-ticker -f

# Disable service (prevent auto-start on boot)
sudo systemctl disable pi-stock-ticker

# Enable service (auto-start on boot)
sudo systemctl enable pi-stock-ticker
```

### Uninstall the Service

To remove the systemd service (but keep your project files):

```bash
chmod +x uninstall_service.sh
./uninstall_service.sh
```

This will:
- Stop the running service
- Disable it from auto-start on boot
- Remove the service file from systemd
- Keep your project files and virtual environment intact

You can reinstall the service at any time by running `./install_service.sh` again.

## Configuration

### config.ini

- **[epaper] lib_path**: Path to the Waveshare e-Paper library
- **[tickers] symbols**: Comma-separated list of stock ticker symbols to display
- **[display] update_frequency_seconds**: How often to update the display (in seconds, default: 30)

Example configuration:
```ini
[epaper]
lib_path=/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib/

[tickers]
symbols=AAPL,GOOGL,MSFT,TSLA

[display]
update_frequency_seconds=30
```

### Trading Hours

The application automatically detects trading hours based on the ticker:
- **Stockholm Exchange** (`.ST` suffix or `^OMX`): 09:00 - 17:30 CET
- **US Markets**: 15:30 - 22:00 CET (09:30 - 16:00 EST)

### Update Frequency

The display update frequency is configured in `config.ini` using the `update_frequency_seconds` setting. By default, the display updates every 30 seconds and cycles through all configured tickers. You can adjust this value to update more or less frequently based on your needs.

## Troubleshooting

### SPI Device Not Found

If you get an SPI-related error:
1. Ensure SPI is enabled: `sudo raspi-config`
2. Reboot your Raspberry Pi
3. Verify SPI devices exist: `ls /dev/spi*`

### Import Errors

If you get import errors for the waveshare_epd module:
1. Verify the library path in `config.ini` matches your installation
2. Make sure you've installed the Waveshare library: `cd e-Paper/RaspberryPi_JetsonNano/python && sudo python3 setup.py install`

### No Data Displayed

1. Check your internet connection
2. Verify ticker symbols are correct in `config.ini`
3. Check logs: `sudo journalctl -u pi-stock-ticker -f`

### Service Won't Start on Boot

The service includes a 5-second delay to ensure SPI services are initialized. If issues persist:
1. Check service status: `sudo systemctl status pi-stock-ticker`
2. View logs: `sudo journalctl -u pi-stock-ticker`
3. Try increasing the delay in `install_service.sh` (line 29: `ExecStartPre=/bin/sleep 5`)

## Dependencies

- **matplotlib**: Chart generation
- **pillow**: Image processing
- **yfinance**: Stock data from Yahoo Finance
- **pytz**: Timezone handling
- **pandas**: Data manipulation
- **waveshare-epd**: E-Paper display driver

## License

This project builds upon the original design from MakerWorld. Please refer to the original creator's license terms.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- Original hardware design: [Nico Burgos on MakerWorld](https://makerworld.com/en/models/1343492-raspberry-pi-stock-ticker)
- Waveshare for the e-Paper display library
- Yahoo Finance for providing free stock data API
