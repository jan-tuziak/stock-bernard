class AVTypeDefs:
   Functions = {
            'list': 'LISTING_STATUS',
            '1min-ly': 'TIME_SERIES_INTRADAY&interval=1min',
            'hourly': 'TIME_SERIES_INTRADAY&interval=60min',
            'daily': 'TIME_SERIES_DAILY',
            'weekly': 'TIME_SERIES_WEEKLY'
        }


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'