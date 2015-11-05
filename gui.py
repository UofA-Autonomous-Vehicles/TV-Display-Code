#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import time, math
import threading
from pymavlink import mavutil


class simpleapp_tk(threading.Thread):
    def __init__(self):
        self.root=Tkinter.Tk()

        #ARM Display
        self.ARM = Tkinter.StringVar()
        self.ARML = Tkinter.Label(self.root,font=("Courier", 16), textvariable=self.ARM)
        self.ARML.grid(row=0, column=0, columnspan=2)
		
        #Mode Display
        self.mode = Tkinter.StringVar()
        self.mode_label = Tkinter.Label(self.root,font=("Courier", 16), text="MODE:")
        self.mode_label.grid(row=1, sticky='E')
        self.mode_value = Tkinter.Label(self.root,font=("Courier", 16), textvariable=self.mode)
        self.mode_value.grid(row=1, column=1, sticky='W')
		
        #altitude Display
        self.altitude = Tkinter.StringVar()
        self.altitude_label = Tkinter.Label(self.root,font=("Courier", 16), text="Altitude:")
        self.altitude_label.grid(row=2, sticky='E')
        self.altitude_value = Tkinter.Label(self.root,font=("Courier", 16), textvariable=self.altitude)
        self.altitude_value.grid(row=2, column=1, sticky='W')
		
        #Ground (Horizontal) Speed display
        self.ground_speed = Tkinter.StringVar()
        self.ground_speed_label = Tkinter.Label(self.root,font=("Courier", 16), text="Horizontal Speed:")
        self.ground_speed_label.grid(row=3, sticky='E')
        self.ground_speed_value = Tkinter.Label(self.root,font=("Courier", 16), textvariable=self.ground_speed)
        self.ground_speed_value.grid(row=3, column=1, sticky='W')
		
		#Vertical Speed
        self.vertical_speed = Tkinter.StringVar()
        self.vertical_speed_label = Tkinter.Label(self.root,font=("Courier", 16), text="Vertical Speed:")
        self.vertical_speed_label.grid(row=4, sticky='E')
        self.vertical_speed_value = Tkinter.Label(self.root,font=("Courier", 16), textvariable=self.vertical_speed)
        self.vertical_speed_value.grid(row=4, column=1, sticky='W')
		
		#Distance to the Next Waypoint (Distance used in navigation)
        self.distance_to_next_waypoint = Tkinter.StringVar()
        self.distance_to_next_waypoint_label = Tkinter.Label(self.root,font=("Courier", 16), text="Distance to the Next Waypoint:")
        self.distance_to_next_waypoint_label.grid(row=5, sticky='E')
        self.distance_to_next_waypoint_value = Tkinter.Label(self.root,font=("Courier", 16), textvariable=self.distance_to_next_waypoint)
        self.distance_to_next_waypoint_value.grid(row=5, column=1, sticky='W')
		        
        threading.Thread.__init__(self)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    data = mavutil.mavlink_connection('udp:localhost:14551', planner_format=False,
                                  notimestamps=True,
                                  robust_parsing=True)
    app = simpleapp_tk()
    app.start()
    while True:
        msg = data.recv_match();
        size = int(math.ceil(app.root.winfo_height()/10))	#7.25
        app.ARML.config(font=("Courier", size))
        app.mode_label.config(font=("Courier", size))
        app.mode_value.config(font=("Courier", size))
        app.altitude_label.config(font=("Courier", size))
        app.altitude_value.config(font=("Courier", size))
        app.ground_speed_label.config(font=("Courier", size))
        app.ground_speed_value.config(font=("Courier", size))
        app.vertical_speed_label.config(font=("Courier", size))
        app.vertical_speed_value.config(font=("Courier", size))
        app.distance_to_next_waypoint_label.config(font=("Courier", size))
        app.distance_to_next_waypoint_value.config(font=("Courier", size))
		
		
        #If we have a valid message
        if msg is not None:
            if msg.get_type() is "HEARTBEAT":
                app.mode.set(str(mavutil.mode_string_v10(msg)))
                if '{0:08b}'.format(msg.base_mode)[0] is "0":
                    app.ARM.set("DISARMED")
                    app.ARML.config(foreground="black")
                else:
                    app.ARM.set("ARMED")
                    app.ARML.config(foreground="red")
            if msg.get_type() is "VFR_HUD":
				app.altitude.set("{0:.2f} feet".format(msg.alt*3.28084))					#feet
				app.ground_speed.set("{0:.2f} knots".format(msg.groundspeed*1.943844))		#knots
				app.vertical_speed.set("{0:.2f} feet/min".format(msg.climb*196.85))			#feet/min
            if msg.get_type() is "NAV_CONTROLLER_OUTPUT":
				app.distance_to_next_waypoint.set("{0:.2f} nautical miles".format(msg.wp_dist*0.000539957))		#nautical miles/metres