from datetime import datetime, timezone, timedelta

def ms_to_hhmmss(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    hours = minutes // 60
    return f"{hours:02}:{minutes % 60:02}:{seconds % 60:02}"

def ms_to_datetime(milliseconds):
    seconds = milliseconds // 1000
    dt_utc = datetime.fromtimestamp(seconds, tz=timezone.utc)

    # Set to CET (UTC+1)
    cet = timezone(timedelta(hours=1))
    # Convert to CET / CEST
    dt_local = dt_utc.astimezone(cet)
    return dt_local.strftime('%a %d %b %Y at %H:%M:%S')