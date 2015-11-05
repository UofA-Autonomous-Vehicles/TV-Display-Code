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
		elif msg.get_type() is "NAV_CONTROLLER_OUTPUT":
			print msg
#RAW_IMU
#SCALED_IMU2
#SCALED_PRESSURE
#SYS_STATUS
#MEMINFO
#MISSION_CURRENT
#GPS_RAW_INT
#NAV_CONTROLLER_OUTPUT
#GLOBAL_POSITION_INT
#SERVO_OUTPUT_RAW
#RC_CHANNELS_RAW
#ATTITUDE
#SIMSTATE
#AHRS2
#VFR_HUD
#AHRS
#HWSTATUS
#SYSTEM_TIME
#TERRAIN_REPORT
#EKF_STATUS_REPORT
#VIBRATION