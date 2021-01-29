from tool import Seat
from tool import parse_config
from pprint import pprint
import time


config = parse_config()

if config:
    for record in config:
        pprint(record)
        s = Seat(record['account'],record['password'],record['roomId'],record['seatNum'],record['startTime'],record['endTime'])
        s.login()
        s.get_token()
        s.get_time()
        s.submit()
        s.logout()
        s.delete()
        time.sleep(10)