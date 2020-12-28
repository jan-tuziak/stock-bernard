import logging

from src.alpha_vantage import AlphaVantageCustomScreener

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    av = AlphaVantageCustomScreener()
    print(av.stocks[0])