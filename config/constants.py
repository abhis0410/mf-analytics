WEEKDAY_MAPPING = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

DROP_THRESHOLD_RANGE = (3, 8)
WEIGHTS = {
    "recent_vs_historical": 0.4,
    "peak_vs_average": 0.3
}

#WEEKLY SPECIFIC CONSTANTS
CARRY_FORWARD_WEEKLY = False
LUMPSUM_PER_WEEK = 5000
SIP_AMOUNT_WEEKLY = 1000
WEEKS = 150
WEEKDAY = 4  # Friday


#MONTHLY SPECIFIC CONSTANTS
CARRY_FORWARD_MONTHLY = False
LUMPSUM_PER_MONTH = 20000
SIP_AMOUNT_MONTHLY = 20000
MONTHS = 24
DATE_OF_INVESTMENT = 5