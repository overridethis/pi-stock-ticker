import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Config:
    """Configuration loader for the stock ticker application."""

    @staticmethod
    def get_epaper_lib_path():
        """
        Get the path to the Waveshare e-Paper library.

        Returns:
            str: Path to the e-Paper library directory
        """
        return config['epaper']['lib_path']

    @staticmethod
    def get_tickers():
        """
        Get the list of stock ticker symbols from configuration.

        Returns:
            list: List of ticker symbols (e.g., ['AAPL', 'GOOGL', 'MSFT'])
        """
        symbols = config['tickers']['symbols']
        return [ticker.strip() for ticker in symbols.split(',')]

    @staticmethod
    def get_update_frequency():
        """
        Get the display update frequency in seconds.

        Returns:
            int: Update frequency in seconds (default: 30)
        """
        return config.getint('display', 'update_frequency_seconds', fallback=30)