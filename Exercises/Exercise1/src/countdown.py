from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path

events = {
    "summer_break": "2027-06-09 15:00",
    "lia_start": "2026-09-25 08:00",
    "christmas": "2026-12-24",
    "bellas_birthday": "2026-12-07",
    "new_year": "2027-01-01",
    "graduation_party": "2027-06-09 16:30"
}

now = datetime.now()
log_file = Path(__file__).parent.parent / "logs" / "countdown.log"

with open(log_file, "a") as file:
    file.write(f"Countdown from {now}\n")
    file.write("-" * 60 + "\n")

    for event_name, event_date in events.items():
        event_datetime = datetime.fromisoformat(event_date)
        difference = relativedelta(event_datetime, now)

        file.write(
            f"{event_name}: "
            f"{difference.years} years, "
            f"{difference.months} months, "
            f"{difference.days} days, "
            f"{difference.hours} hours, "
            f"{difference.minutes} minutes, "
            f"{difference.seconds} seconds\n"
        )

    file.write("\n")
