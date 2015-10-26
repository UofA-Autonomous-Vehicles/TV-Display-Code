import time
from pymavlink import mavutil

data = mavutil.mavlink_connection('udp:localhost:14551', planner_format=False,
                                  notimestamps=True,
                                  robust_parsing=True)

while True:
	msg = data.recv_match();
	#If we have a valid message
	if msg is not None:
		#print msg.get_type()
		if msg.get_type() is "HEARTBEAT":
			print msg.autopilot