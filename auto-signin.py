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
        #s.get_id()
        s.check_seat()
        #s.get_token()
        #s.get_id()
        s.signin()
        time.sleep(10)