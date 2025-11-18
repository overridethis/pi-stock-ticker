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