from datetime import datetime
import pytz

now = datetime.now()
print(now)
print(now.tzinfo)
print(int(now.timestamp() * 1000))

timezone = pytz.timezone('Europe/Sofia')
print(timezone)
now = datetime.now()
now = timezone.localize(now)
print(now)
print(now.tzinfo)
print(int(now.timestamp() * 1000))