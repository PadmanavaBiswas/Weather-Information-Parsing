import time

import schedule

from Weather import Weather_Details


def run_pipeline(locations):
    print("Pipeline running...")
    Weather_Details(locations)
    print("Pipeline complete.")


locations = [
    "Barrackpore,WestBengal,India",
    "Udaipur,Rajasthan,India",
    "Noida,Delhi,India",
    "Leh,Ladakh,India",
    "Guwahati,Assam,India",
]

run_pipeline(locations)

schedule.every(1).minutes.do(run_pipeline, locations=locations)

while True:
    schedule.run_pending()
    time.sleep(15)

