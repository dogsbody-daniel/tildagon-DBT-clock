import asyncio
import utime
import app
import ntptime
import imu
import math

from events.input import Buttons, BUTTON_TYPES

class clockapp(app.App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.acc_read = None

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.minimise()
        else:
            self.acc_read = imu.acc_read()

    def draw(self, ctx):
        ctx.save()

        try:
            ntptime.settime()
        except Exception as e:
            pass

        current_time_utc = utime.time()
        bst_offset = 3600

        current_time_plus_one = current_time_utc + bst_offset
        current_time_tuple = utime.localtime(current_time_plus_one)

        hour = current_time_tuple[3]
        minute = current_time_tuple[4]
        second = current_time_tuple[5]

        current_time = "{:02}:{:02}:{:02}".format(hour, minute, second)


        ctx.rgb(0,0,0).rectangle(-120,-120,240,240).fill()

        if self.acc_read:
            ax, ay, az = self.acc_read
            pitch = math.atan2(ay, math.sqrt(ax*ax + az*az)) * 180 / math.pi
            roll = math.atan2(ax, math.sqrt(ay*ay + az*az)) * 180 / math.pi
            
            if ax < 0:
                ctx.rotate(math.pi)
            ctx.rgb(1,1,1).move_to(-55,15).text(current_time)
        else:
            ctx.rgb(1,1,1).move_to(-55,15).text(current_time)

        utime.sleep(1)
        ctx.restore()
__app_export__ = clockapp
