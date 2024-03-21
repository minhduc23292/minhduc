from enum import Enum
from smbus import SMBus
import time
from array import array
# Registers
BSP_NORMAL_MODE_I2C_ADDR=0x0B
DEV_ADDR = 0x0B # Device address
MAC_REG = 0x44 # Register of MAC
BQ40Z50_CONTROL_STATUS=0x00
# Read word
TEMPERATURE_REG = 0x08
VOLTAGE_REG = 0x09
CURRENT_REG = 0x0A
AVERAGECURRENT_REG = 0x0B
MAXERROR_REG = 0x0C
RELATIVESOC_REG = 0x0D
ABSOLUTESOC_REG = 0x0E
REMAININGCAPACITY_REG = 0x0F
FULLCHARGECAPACITY_REG = 0x10
CHARGINGCURRENT_REG = 0x14
CHARGINGVOLTAGE_REG = 0x15
BATTERYSTATUS_REG = 0x16
CYCLECOUNT_REG = 0x17
CELLVOLTAGE4_REG = 0x3C
CELLVOLTAGE3_REG = 0x3D
CELLVOLTAGE2_REG = 0x3E
CELLVOLTAGE1_REG = 0x3F
SOH_REG = 0x4F

# Read block
DEVICENAME_REG = 0x21

# Manufacturer Access (MAC) Commands
# Available in SEALED Mode
SAFETYALERT_CMD = array('B', b'\x50\x00')
SAFETYSTATUS_CMD = array('B', b'\x51\x00')
PFALERT_CMD = array('B', b'\x52\x00')
PFSTATUS_CMD = array('B', b'\x53\x00')
# OPERATIONSTATUS_CMD = array('B', b'\x54\x00')
OPERATIONSTATUS_CMD=[0x54, 0x00]
GAUGINGSTATUS_CMD = array('B', b'\x55\x00')

LIFETIMEDATABLOCK1_CMD = array('B', b'\x60\x00')
LIFETIMEDATABLOCK2_CMD = array('B', b'\x61\x00')
LIFETIMEDATABLOCK3_CMD = array('B', b'\x62\x00')
LIFETIMEDATABLOCK4_CMD = array('B', b'\x63\x00')
LIFETIMEDATABLOCK5_CMD = array('B', b'\x64\x00')

DASTATUS1_CMD = array('B', b'\x71\x00')
DASTATUS2_CMD = array('B', b'\x72\x00')

GAUGESTATUS1_CMD = array('B', b'\x73\x00')
GAUGESTATUS2_CMD = array('B', b'\x74\x00')
GAUGESTATUS3_CMD = array('B', b'\x75\x00')

lifetime_1_thresholds = {'Cell 1 max mV': (2700, 4200),
                         'Cell 2 max mV': (2700, 4200),
                         'Cell 3 max mV': (2700, 4200),
                         'Cell 4 max mV': (2700, 4200),
                         'Cell 1 min mV': (2700, 4200),
                         'Cell 2 min mV': (2700, 4200),
                         'Cell 3 min mV': (2700, 4200),
                         'Cell 4 min mV': (2700, 4200),
                         'Max Delta Cell mV': (0, 250),
                         'Max Charge mA': 4037,
                         'Max Discharge mA': 37641,
                         'Max Avg Dsg mA': 47230,
                         'Max Avg Dsg mW': 41479,
                         'Max temp cell': 46,
                         'Min temp cell': 15,
                         'Max delta cell temp': (0, 10),
                         'Max Temp Int Sensor': 51,
                         'Min Temp Int Sensor': 13,
                         'Max Temp Fet': 61}




class STATUS(Enum):
    POWER_SUPPLY_STATUS_UNKNOWN = 0,
    POWER_SUPPLY_STATUS_CHARGING = 1,
    POWER_SUPPLY_STATUS_DISCHARGING = 2,
    POWER_SUPPLY_STATUS_NOT_CHARGING = 3,
    POWER_SUPPLY_STATUS_FULL = 4,


class BQ40Z50():
    def __init__(self):
        self.bus = SMBus(1)
    def i2c_send_turn_off(self):
        pass

    # Check if the BQ27441-G1A is sealed or not.
    def status(self):
        return self.readControlWord(BQ40Z50_CONTROL_STATUS)
    
    def sealed(self):
        stat = self.status()
        print("stattus:", stat)
        return stat & BQ27441_STATUS_SS

    def seal(self):
        # return self.readControlWord(BQ27441_CONTROL_SEALED)
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x30, 0x00])
        time.sleep(1)

    def read_security_key(self):
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x35, 0x00])
        time.sleep(0.5)
        ret = self.bus.read_i2c_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x23, 7)
        return ret
    # UNseal the BQ27441-G1A

    def reset(self):
        ret=self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x41, 0x00])
        return ret

    def unseal(self):
        self.bus.write_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, 0x0414)
        time.sleep(1)
        self.bus.write_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, 0x3672)
        time.sleep(0.5)
        # self.writeControlWord(0xFFFF)
        # self.writeControlWord(0xFFFF)

    def fullAcess(self):
        self.bus.write_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, 0xFFFF)
        time.sleep(1)
        self.bus.write_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, 0xFFFF)
        time.sleep(0.5)

    def toggle_the_charge_fet(self):
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x20, 0x00])
        # self.bus.write_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, 0x0020)
        time.sleep(0.5)
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x1f, 0x00])

    def fet_en(self):
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x22, 0x00])

    def enable_gauge(self):
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x21, 0x00])

    def deviceType(self):
        return self.readControlWord(0x01)
    
    def read_device_name(self):
        ret = self.bus.read_i2c_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x21,9)
        return ret
    
    def read_from_flash(self):
        self.bus.write_block_data(0x0B, 0x44, [0x5B, 0x49])
        time.sleep(0.1)
        ret=self.bus.read_i2c_block_data(0x0B, 0x44, 5 )
        return ret
    
    def write_to_flash(self):
        self.bus.write_block_data(0x0B, 0x44, [0x5C, 0x49, 0x04])
        time.sleep(0.1)

    def change_design_cap(self):
        self.bus.write_block_data(0x0B, 0x44, [0x11, 0x48, 0x80, 0x0C])
        time.sleep(0.1)
    
    def change_design_voltage(self):
        self.bus.write_block_data(0x0B, 0x44, [0x15, 0x48, 0xC8, 0x32])
        time.sleep(0.1)

    def change_design_cell1_cap(self):
        self.bus.write_block_data(0x0B, 0x44, [0x06, 0x43, 0x80, 0x0C])
        time.sleep(0.1)
    
    def change_design_cell2_cap(self):
        self.bus.write_block_data(0x0B, 0x44, [0x08, 0x43, 0x80, 0x0C])
        time.sleep(0.1)

    def change_design_cell3_cap(self):
        self.bus.write_block_data(0x0B, 0x44, [0x0A, 0x43, 0x80, 0x0C])
        time.sleep(0.1)

    def config_gauge(self):
        self.change_design_cap()
        # self.change_design_voltage()
        self.change_design_cell1_cap()
        self.change_design_cell2_cap()
        self.change_design_cell3_cap()
        
    def read_design_cap(self):
        self.bus.write_block_data(0x0B, 0x44, [0x11, 0x48])
        time.sleep(0.1)
        ret=self.bus.read_i2c_block_data(0x0B, 0x44, 5 )
        return ret[3]+ret[4]*256

    def change_temperature_sensor_to_internal(self):
        self.bus.write_block_data(0x0B, 0x44, [0x5B, 0x49, 0x01])
        time.sleep(0.1)
    
    def read_temperature_enable_flash(self):
        self.bus.write_block_data(0x0B, 0x44, [0x5B, 0x49])
        time.sleep(0.1)
        ret=self.bus.read_i2c_block_data(0x0B, 0x44, 5 )
        return ret

    def read_voltage(self):
        ret = self.bus.read_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x09)
        return ret

    def read_current(self):
        ret = self.bus.read_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x0A)
        if ret < 32768:
            pass
        else:
            ret -= 65536
        return ret
    
    def read_temp(self):
        ret = self.bus.read_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x08)
        return int(ret*0.1-273.0)

    def read_fullcharge_cap(self):
        ret = self.bus.read_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x10)
        return ret

    def read_remain_cap(self):
        ret = self.bus.read_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x0E)
        return ret
    

    def read_operation_status(self):
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x54, 0x00])
        time.sleep(0.5)
        ret = self.bus.read_i2c_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, 7)
        return ret
    
    def read_charging_status(self):
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x55, 0x00])
        time.sleep(0.5)
        ret = self.bus.read_i2c_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, 7)
        return ret

    def read_manufactoring_status(self):
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x57, 0x00])
        time.sleep(0.5)
        ret = self.bus.read_i2c_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, 7)
        return ret
    
    def read_gauging_status(self):
        self.bus.write_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, [0x56, 0x00])
        time.sleep(0.5)
        ret = self.bus.read_i2c_block_data(BSP_NORMAL_MODE_I2C_ADDR, 0x44, 7)
        return ret

    def calibMode(self):
        return self.readControlWord(0x0040)

    def batInsert(self):
        return self.readControlWord(0x21)

    def ItEnable(self):
        return self.readControlWord(0x21)

    def writeControlWord(self, function):
        subCommandMSB = function >> 8
        subCommandLSB = function & 0x00FF
        value = subCommandLSB | subCommandMSB
        self.bus.write_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, function)
        # self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, subCommandLSB)
        # self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, subCommandMSB)

    def readControlWord(self, function):
        subCommandMSB = function >> 8
        subCommandLSB = function & 0x00FF
        value = subCommandLSB | subCommandMSB
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, subCommandLSB)
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, 0x01, subCommandMSB)
        time.sleep(0.5)
        ret = self.bus.read_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00)
        return ret

    
    def set_capacity(self, capacity):
        capMSB = capacity >> 8
        capLSB = capacity & 0x00FF
        capacityData = [capMSB, capLSB]
        print("capacity: ", capacityData)
        self.writeExtendedData(capacityData, 2, 0x30, 0x0A)

    def set_tempurature(self, tem):
        capMSB = tem >> 8
        capLSB = tem & 0x00FF
        temData = [capMSB, capLSB]
        print("tempurature: ", temData)
        self.writeExtendedData(temData, 2, 0x30, 0x0F)

    def set_opconfigD(self, configD, classID, offset):
        capMSB = configD >> 8
        capLSB = configD & 0x00FF
        temData = [capMSB, capLSB]
        print("config: ", temData)
        self.writeExtendedData(temData, 2, classID, offset)

    def blockDataControl(self):
        enableByte = 0x00
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, BQ27441_EXTENDED_CONTROL, enableByte)

    def blockDataClass(self, classID=0x30):
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, BQ27441_EXTENDED_DATACLASS, classID)

    def blockDataOffset(self, block_number):
        print("block number:", block_number)
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, BQ27441_EXTENDED_DATABLOCK, block_number)

    def computeBlockChecksum(self):
        data = self.bus.read_i2c_block_data(BSP_NORMAL_MODE_I2C_ADDR, BQ27441_EXTENDED_BLOCKDATA, 32)
        csum = 0
        for i in range(32):
            csum += data[i]
        csum = 255 - csum

        return csum

    # Read the current checksum using BlockDataCheckSum()
    def blockDataChecksum(self):
        csum = self.bus.read_byte_data(BSP_NORMAL_MODE_I2C_ADDR, BQ27441_EXTENDED_CHECKSUM)
        return csum

    # Use BlockData() to write a byte to an offset of the loaded data
    def writeBlockData(self, offset, data):
        address = offset + BQ27441_EXTENDED_BLOCKDATA
        # address=0x3A
        print("write block address:", address)
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, address, data)

    def readBlockData(self, offset, num):
        address = offset + BQ27441_EXTENDED_BLOCKDATA
        print("read block address: ", address)
        if num == 2:
            ret = self.bus.read_byte_data(BSP_NORMAL_MODE_I2C_ADDR, address)
            ret2 = self.bus.read_byte_data(BSP_NORMAL_MODE_I2C_ADDR, address + 1)
            return ret2 + ret * 256
        elif num == 1:
            print("num=1")
            ret = self.bus.read_byte_data(BSP_NORMAL_MODE_I2C_ADDR, address)
            return ret

    def writeBlockChecksum(self, csum):
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, BQ27441_EXTENDED_CHECKSUM, csum)

    def writeExtendedData(self, data, len, classID=0x30, offset=0x0A):
        # if len>32:
        #     return False
        self.blockDataControl()  # enable block data memory control ọk
        time.sleep(1)
        self.blockDataClass(classID)  # Write class ID using DataBlockClass()ok
        time.sleep(1)
        self.blockDataOffset(0x00)  # Write 32-bit block offset (usually 0)
        time.sleep(1)
        self.computeBlockChecksum()  # Compute checksum going in
        time.sleep(0.5)
        oldCsum = self.blockDataChecksum()
        print("old checksum:", oldCsum)
        time.sleep(0.5)
        # Write data bytes:
        for i in range(len):
            self.writeBlockData((offset % 32) + i, data[i])
            time.sleep(0.1)
        # self.bus.write_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x4C, 0x0BB8)

        # Write new checksum using BlockDataChecksum (0x60)
        newCsum = self.computeBlockChecksum()  # Compute the new checksum
        print("new checksum:", newCsum)
        self.writeBlockChecksum(newCsum)

    def readExtendedData(self, classID=0x40, offset=0x0D, num=2):
        print("offset:", offset % 32)
        retData = 0
        self.blockDataControl()
        time.sleep(0.5)
        self.blockDataClass(classID)
        time.sleep(0.5)
        self.blockDataOffset(0x00 if offset / 32 < 1 else 0x01)
        time.sleep(0.5)
        self.computeBlockChecksum()
        time.sleep(0.5)
        oldCsum = self.blockDataChecksum()
        print("old check sum:", oldCsum)
        time.sleep(0.5)
        retData = self.readBlockData(offset % 32, num)
        return retData

    def sociDelta(self):
        return self.readExtendedData(BQ27441_ID_STATE, 26, 2)

    def _read(self, register_address):
        data = self.bus.read_word_data(BSP_NORMAL_MODE_I2C_ADDR, register_address)
        return data

    def bq27510_battery_voltage(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_VOLT)
            else:
                break
        return data / 1000

    def bq27510_battery_current(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_AI)
            else:
                break
        if data < 32768:
            pass
        else:
            data -= 65536
        return data

    def bq27510_battery_temperature(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_TEMP)
            else:
                break
        return data

    def bq27510_flag(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_SOC)
            else:
                break
        return data

    # Return the battery RemainingCapacity
    # The reture value is mAh
    # Or < 0 if something fails.

    def bq27510_battery_remaining_capacity(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_RM)
            else:
                break
        return data

    # Return the battery FullChargeCapacity
    # The reture value is mAh
    # Or < 0 if something fails

    def bq27510_battery_full_charge_capacity(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_FCC)
            else:
                break
        return data

    def bq27510_battery_tte(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_TTE)
            else:
                break
        return data

    def bq27510_battery_ttf(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_TTF)
            else:
                break
        return data

    def bq27510_battery_status_charge(self):
        m_current = self.bq27510_battery_current()
        data = -1
        status = 0
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_FLAGS)
            else:
                break

        # if data & BQ27510_FLAG_FC:
        #     status = STATUS.POWER_SUPPLY_STATUS_FULL
        if (data & BQ27510_FLAG_DSG):
            status = STATUS.POWER_SUPPLY_STATUS_DISCHARGING
        else:
            status = STATUS.POWER_SUPPLY_STATUS_CHARGING
        return status

    def get_remaining_capacity(self):
        remainCap = int(self.bq27510_battery_remaining_capacity() * 1.176 - 17.647)
        # if status==STATUS.POWER_SUPPLY_STATUS_DISCHARGING:
        #     remainCap=int(self.bq27510_battery_remaining_capacity())
        # remainCap= -326.912*pow(m_volt, 4)+4606.417*pow(m_volt, 3)-24154.220*pow(m_volt, 2)+55955.353*pow(m_volt, 1) -48389.351
        # elif status==STATUS.POWER_SUPPLY_STATUS_CHARGING:
        # remainCap=142.85*m_volt-500
        # remainCap=453.8*pow(m_volt,3)-5130.14*pow(m_volt,2)+19406*m_volt-24534.5
        # remainCap= 544.079*pow(m_volt, 4)+ -8046.870*pow(m_volt, 3)+44568.645*pow(m_volt, 2)-109461.347*pow(m_volt, 1)+100521.924
        if remainCap <= 0:
            remainCap = 0
        if remainCap > 100:
            remainCap = 100
        return remainCap

    def FilteredRM(self):
        data = -1
        for i in range(3):
            if data < 0:
                data = self.bus.read_word_data(ADR_READ, BQ27510_REG_FRM)
                print("i2c error in reading TTF!")
            else:
                break
        return data