from datetime import datetime
import pytz

now = datetime.utcnow()
timezone = pytz.timezone('utc')
now = timezone.localize(now)
print(now)
print(now.tzinfo)
print(int(now.timestamp() * 1000))

timezone = pytz.timezone('Europe/Sofia')
now = datetime.now()
now = timezone.localize(now)
print(now)
print(now.tzinfo)
print(int(now.timestamp() * 1000))