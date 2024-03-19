import smbus
import time
import datetime

# I2C-Adresse des PCF80063A
address = 0x51

# registar overview - crtl & status reg
RTC_CTRL_1 = 0x00
RTC_CTRL_2 = 0x01
RTC_OFFSET = 0x02
RTC_RAM_by = 0x03

# registar overview - time & data reg
RTC_SECOND_ADDR = 0x04
RTC_MINUTE_ADDR = 0x05
RTC_HOUR_ADDR   = 0x06
RTC_DAY_ADDR    = 0x07
RTC_WDAY_ADDR   = 0x08
RTC_MONTH_ADDR  = 0x09
RTC_YEAR_ADDR	= 0x0a # years 0-99; calculate real year = 1970 + RCC reg year

# registar overview - alarm reg
RTC_SECOND_ALARM = 0x0b
RTC_MINUTE_ALARM = 0x0c
RTC_HOUR_ALARM   = 0x0d
RTC_DAY_ALARM    = 0x0e
RTC_WDAY_ALARM   = 0x0f

# registar overview - timer reg
RTC_TIMER_VAL   = 0x10
RTC_TIMER_MODE  = 0x11
RTC_TIMER_TCF   = 0x08
RTC_TIMER_TE    = 0x04
RTC_TIMER_TIE   = 0x02
RTC_TIMER_TI_TP = 0x01

# format
RTC_ALARM          = 0x80	# set AEN_x registers
RTC_ALARM_AIE      = 0x80	# set AIE ; enable/disable interrupt output pin
RTC_ALARM_AF       = 0x40	# set AF register ; alarm flag needs to be cleared for alarm
RTC_CTRL_2_DEFAULT = 0x00
RTC_TIMER_FLAG     = 0x08

TIMER_CLOCK_4096HZ   = 0
TIMER_CLOCK_64HZ     = 1
TIMER_CLOCK_1HZ      = 2
TIMER_CLOCK_1PER60HZ = 3


# Erzeugen einer I2C-Instanz und Öffnen des Busses
class PCF85063():
    def __init__(self):
        self.pcf85063 = smbus.SMBus(1)

    def decToBcd(self, val):
        return ((val // 10 * 16) + (val % 10))

    def bcdToDec(self, val):
        return ((val // 16 * 10) + (val % 16))

    def constrain (self, val, min_val, max_val):
        return min (max_val, max(min_val, val))

    def reset(self):	# datasheet 8.2.1.3.
        self.pcf85063.write_byte_data (address, RTC_CTRL_1, 0x58)

    def setTime (self, hour, minute, second):
        self.pcf85063.write_byte_data (address, RTC_SECOND_ADDR, self.decToBcd(second))
        self.pcf85063.write_byte_data (address, RTC_MINUTE_ADDR, self.decToBcd(minute))
        self.pcf85063.write_byte_data (address, RTC_HOUR_ADDR, self.decToBcd(hour))


    def setDate (self, weekday, day, month, yr):

        year = yr - 1970; 	# convert to RTC year format 0-99

        self.pcf85063.write_byte_data (address, RTC_DAY_ADDR,   self.decToBcd(day))
        self.pcf85063.write_byte_data (address, RTC_WDAY_ADDR,  self.decToBcd(weekday))   # 0 for Sunday
        self.pcf85063.write_byte_data (address, RTC_MONTH_ADDR, self.decToBcd(month))
        self.pcf85063.write_byte_data (address, RTC_YEAR_ADDR,  self.decToBcd(year))

    def readTime(self):
        rdata = self.pcf85063.read_i2c_block_data (address, RTC_SECOND_ADDR, 7)
        # print (rdata)

        second= self.bcdToDec (rdata[0] & 0x7f) # second
        minute= self.bcdToDec (rdata[1])& 0x7f  # minute
        hour= self.bcdToDec (rdata[2] & 0x3f) # hour

        day= self.bcdToDec (rdata[3] & 0x3f) # day
        month= self.bcdToDec (rdata[5] & 0x1f) # month
        year= self.bcdToDec (rdata[6]) + 1970 # year
        return[second, minute, hour, day, month, year]


    def enableAlarm(self): # datasheet 8.5.6.
        # check Table 2. Control_2
        control_2 = RTC_CTRL_2_DEFAULT | RTC_ALARM_AIE #enable interrupt
        control_2 &= ~RTC_ALARM_AF                     # clear alarm flag

        self.pcf85063.write_byte_data (address, RTC_CTRL_2, control_2)

    def setAlarm (self, alarm_second, alarm_minute, alarm_hour, alarm_day, alarm_weekday):

        if (alarm_second < 99): # second
            alarm_second = self.constrain (alarm_second, 0, 59)
            alarm_second = self.decToBcd (alarm_second)
            alarm_second &= ~RTC_ALARM;
        else:
            alarm_second = 0x0
            alarm_second |= RTC_ALARM

        if (alarm_minute < 99): # minute
            alarm_minute = self.constrain (alarm_minute, 0, 59)
            alarm_minute = self.decToBcd (alarm_minute)
            alarm_minute &= ~RTC_ALARM
        else:
            alarm_minute = 0x0;
            alarm_minute |= RTC_ALARM

        if (alarm_hour < 99): #  hour
            alarm_hour = self.constrain(alarm_hour, 0, 23)
            alarm_hour = self.decToBcd(alarm_hour)
            alarm_hour &= ~RTC_ALARM
        else:
            alarm_hour = 0x0
            alarm_hour |= RTC_ALARM

        if (alarm_day < 99): # day
            alarm_day = self.constrain(alarm_day, 1, 31)
            alarm_day = self.decToBcd(alarm_day)
            alarm_day &= ~RTC_ALARM
        else:
            alarm_day = 0x0
            alarm_day |= RTC_ALARM

        if (alarm_weekday < 99): # weekday
            alarm_weekday = self.constrain(alarm_weekday, 0, 6)
            alarm_weekday = self.decToBcd(alarm_weekday)
            alarm_weekday &= ~RTC_ALARM
        else:
            alarm_weekday = 0x0
            alarm_weekday |= RTC_ALARM

        self.enableAlarm()

        self.pcf85063.write_byte_data (address, RTC_SECOND_ALARM, alarm_second)
        self.pcf85063.write_byte_data (address, RTC_MINUTE_ALARM, alarm_minute)
        self.pcf85063.write_byte_data (address, RTC_HOUR_ALARM,   alarm_hour)
        self.pcf85063.write_byte_data (address, RTC_DAY_ALARM,    alarm_day)
        self.pcf85063.write_byte_data (address, RTC_WDAY_ALARM,   alarm_weekday)   # 0 for Sunday

    def readAlarm():
        rdata = self.pcf85063.read_i2c_block_data (address, RTC_SECOND_ALARM, 5)    # datasheet 8.4.
        print (rdata)

        alarm_second = rdata[0]        # read RTC_SECOND_ALARM register

        if (RTC_ALARM & alarm_second): # check is AEN = 1 (second alarm disabled)
            alarm_second = 99           # using 99 as code for no alarm
        else:                          # else if AEN = 0 (second alarm enabled)
            alarm_second = self.bcdToDec (alarm_second & ~RTC_ALARM) # remove AEN flag and convert to dec number

        alarm_minute = rdata[1] # minute
        if (RTC_ALARM & alarm_minute):
            alarm_minute = 99
        else:
            alarm_minute = self.bcdToDec (alarm_minute & ~RTC_ALARM)

        alarm_hour = rdata[2] # hour
        if (RTC_ALARM & alarm_hour):
            alarm_hour = 99
        else:
            alarm_hour = self.bcdToDec (alarm_hour & 0x3F) # remove bits 7 & 6

        alarm_day = rdata[3] # day
        if (RTC_ALARM & alarm_day):
            alarm_day = 99
        else:
            alarm_day = self.bcdToDec (alarm_day & 0x3F) # remove bits 7 & 6

        alarm_weekday = rdata[4]  # weekday
        if (RTC_ALARM & alarm_weekday):
            alarm_weekday = 99
        else:
            alarm_weekday = self.bcdToDec (alarm_weekday & 0x07) # remove bits 7,6,5,4 & 3

        print (alarm_second, alarm_minute, alarm_hour, alarm_day, alarm_weekday)

    def timerSet (source_clock, val, int_enable, int_pulse):

        timer_reg = [0,0]

        # disable the countdown timer
        self.pcf85063.write_byte_data (address, RTC_TIMER_MODE, 0x18)

        # clear Control_2
        self.pcf85063.write_byte_data (address, RTC_CTRL_2, 0x00)

        # reconfigure timer
        timer_reg[1] |= RTC_TIMER_TE # enable timer

        if (int_enable):
            timer_reg[1] |= RTC_TIMER_TIE # enable interrupr

        if (int_pulse):
            timer_reg[1] |= RTC_TIMER_TI_TP # interrupt mode

        timer_reg[1] |= source_clock << 3   # clock source
        # timer_reg[1] = 0b00011111;

        timer_reg[0] = val

        # write timer value
        self.pcf85063.write_byte_data (address, RTC_TIMER_VAL, timer_reg[0])
        self.pcf85063.write_byte_data (address, RTC_TIMER_MODE, timer_reg[1])



# now = datetime.datetime.now()
# print ("Current date and time : ")
# print (now.strftime("%Y-%m-%d %H:%M:%S"))
# a=PCF85063()
# a.reset()
# a.setTime (now.hour, now.minute, now.second)
# print (" Wochentag :" , int(datetime.datetime.today().strftime('%w')))
# a.setDate (int(datetime.datetime.today().strftime('%w')), now.day, now.month, now.year)

# a.readTime ()

# a.setAlarm (21, 55, 14, 9, 6)
# a.readAlarm()