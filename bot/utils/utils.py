
def calculate_month_delta(start_dt, end_dt):
    year_delta = end_dt.year - start_dt.year
    month_delta = end_dt.month - start_dt.month
    day_delta = end_dt.day - start_dt.day

    if day_delta < 0:
        month_delta -= 1

    if month_delta < 0:
        year_delta -= 1
        month_delta += 12

    return year_delta * 12 + month_delta

