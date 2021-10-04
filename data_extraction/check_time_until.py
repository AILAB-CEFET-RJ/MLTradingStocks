from time import sleep
from datetime import datetime

current_time = datetime.now()
current_time_str = datetime.now().strftime('%H:%M:%S')
print(current_time_str)

lower_limit = datetime.strptime('09:30:00', '%H:%M:%S')
lower_limit_str = datetime.strptime('09:30:00', '%H:%M:%S').strftime('%H:%M:%S')

time_until = current_time - lower_limit

print(f'Time Until 09:30: {time_until}')
