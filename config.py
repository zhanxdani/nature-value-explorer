"""Global constants. Every number shown in the app comes from here or from data/*.csv."""

TOTAL_AVG_TN = 33.268      # Costanza average, trillion US$/yr (1994 $)
TOTAL_LOW_TN = 16
TOTAL_HIGH_TN = 54
WORLD_GNP_1997_TN = 18
WORLD_POP_1997 = 5.85e9    # approx.
CPI_FACTOR = 2.12          # 1994 -> 2024 US$, CPI-U; update if needed
DEFAULT_DISCOUNT = 0.05    # rate used by Costanza to convert stocks to flows
APP_URL = ""               # set after deploy, used for QR code
