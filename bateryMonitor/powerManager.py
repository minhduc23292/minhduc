from enum import Enum
from smbus import SMBus
import time

BQ27510_REG_TEMP = 0x06
BQ27510_REG_VOLT = 0x08
BQ27510_REG_FLAGS = 0x0a
# Time to Empty
BQ27510_REG_TTE = 0x16
# Time to Full
BQ27510_REG_TTF = 0x18
# State-of-Charge
# register has been changed in new fw version
BQ27510_REG_SOC = 0x0a
# Average Current
BQ27510_REG_AI = 0x14
# Remainning Capacity
BQ27510_REG_RM = 0x20
# Full Charge Capacity
BQ27510_REG_FCC = 0x12
# Standby Current
BQ27510_REG_SI = 0x1a
# FilteredRM
BQ27510_REG_FRM = 0x6C
# Control
BQ27510_REG_CTRL = 0x00
# Control Status
BQ27510_REG_CTRS = 0x0000
# Data Flash Class
BQ27510_REG_DFCLS = 0x3e
BQ27510_REG_CLASS_ID = 82
BQ27510_REG_QMAX = 0x42
BQ27510_REG_QMAX1 = 0x43
BQ27510_REG_FLASH = 0x40
BQ27510_REG_FIRMWARE_ID = 0x0008
BQ27510_REG_FIRMWARE_VERSION = 0x0039

# both words and bytes are LSB
# Full-charged bit
BQ27510_FLAG_FC = 1 << 9
BQ27510_FLAG_DET = 1 << 3
# Over-Temperature-Charge bit
BQ27510_FLAG_OTC = 1 << 15
# Over-Temperature-Discharge bit
BQ27510_FLAG_OTD = 1 << 14
# State-of-Charge-Threshold 1 bit
BQ27510_FLAG_SOC1 = 1 << 2
# State-of-Charge-Threshold Final bit
BQ27510_FLAG_SOCF = 1 << 1
BQ27510_FLAG_LOCK = (BQ27510_FLAG_SOC1 | BQ27510_FLAG_SOCF)
# Discharging detected bit
BQ27510_FLAG_DSG = 1 << 0
CONST_NUM_10 = 10
CONST_NUM_2730 = 2730
ADCSENSOR_PIN = "gpio_170"

# added for Firmware upgrade begine
BSP_UPGRADE_FIRMWARE_BQFS_CMD = "upgradebqfs"
BSP_UPGRADE_FIRMWARE_DFFS_CMD = "upgradedffs"
# the whole firmware
BSP_UPGRADE_FIRMWARE_BQFS_NAME = "/system/etc/coulometer/bq27510_pro.bqfs"
# gas gauge data info
BSP_UPGRADE_FIRMWARE_DFFS_NAME = "/system/etc/coulometer/bq27510_pro.dffs"
BSP_ROM_MODE_I2C_ADDR = 0x0B
BSP_NORMAL_MODE_I2C_ADDR = 0x55
BSP_FIRMWARE_FILE_SIZE = 400 * 1024
BSP_I2C_MAX_TRANSFER_LEN = 128
BSP_MAX_ASC_PER_LINE = 400
BSP_ENTER_ROM_MODE_CMD = 0x00
BSP_ENTER_ROM_MODE_DATA = 0x0F00
BSP_FIRMWARE_DOWNLOAD_MODE = 0xDDDDDDDD
BSP_NORMAL_MODE = 0x00

DEFALUT_MONITOR_TIME = 30
NO_BATTERY_CAPACITY = 40
CHARGE_FULL_TIME = 80
START_CAPACITY_CACL = 0
REACH_EMPTY_RESAMPLE_THRESHOLD = 10
REACH_EMPTY_SAMPLE_INTERVAL = 5
CHARGER_ONLINE = 1
CAPACITY_FULL = 100
CAPACITY_NEAR_FULL = 96
CAPACITY_JUMP_THRESHOLD = 5
CAPACITY_DEBOUNCE_MAX = 4
CUTOFF_LEVEL = 2
FAKE_CUTOFF_LEVEL = 3
CUTOFF_VOLTAGE = 3450
MAX_SOC_CHANGE = 1
ADR_READ = BSP_NORMAL_MODE_I2C_ADDR
ADR_WRITE = 0xAA
DEFALUT_CAPACITY = 50

BQ27441_CONTROL_DEVICE_TYPE = 0x01
BQ27441_EXTENDED_CONTROL = 0x61
BQ27441_EXTENDED_DATACLASS = 0x3E
BQ27441_EXTENDED_CAPACITY = 0x3C
BQ27441_EXTENDED_DATABLOCK = 0x3F
BQ27441_EXTENDED_BLOCKDATA = 0x40
BQ27441_EXTENDED_CHECKSUM = 0x60
BQ27441_ID_STATE = 82
BQ27441_STATUS_SS = 1 << 13
BQ27441_CONTROL_STATUS = 0x0000
BQ27441_CONTROL_SEALED = 0x20
BQ27441_UNSEAL_KEY = 0x8000
BQ27441_CONTROL_RESET = 0x0041


class STATUS(Enum):
    POWER_SUPPLY_STATUS_UNKNOWN = 0,
    POWER_SUPPLY_STATUS_CHARGING = 1,
    POWER_SUPPLY_STATUS_DISCHARGING = 2,
    POWER_SUPPLY_STATUS_NOT_CHARGING = 3,
    POWER_SUPPLY_STATUS_FULL = 4,


class BQ27510():
    def __init__(self):
        self.bus = SMBus(1)

    def i2c_send_turn_off(self):
        self.bus.write_byte(0x08, ord('c'))

    def i2c_set_precharge_current(self):
        self.bus.write_byte_data(0x6b, 0x05, 0x43)

    # Check if the BQ27441-G1A is sealed or not.
    def sealed(self):
        stat = self.status()
        print("stattus:", stat)
        return stat & BQ27441_STATUS_SS

    def status(self):
        return self.readControlWord(BQ27441_CONTROL_STATUS)

    # Seal the BQ27441-G1A
    def seal(self):
        return self.readControlWord(BQ27441_CONTROL_SEALED)

    # UNseal the BQ27441-G1A
    def reset(self):
        ret = self.writeControlWord(BQ27441_CONTROL_RESET)
        return ret

    def unseal(self):
        self.writeControlWord(0x0414)
        self.writeControlWord(0x3672)
        # self.writeControlWord(0xFFFF)
        # self.writeControlWord(0xFFFF)

    def fullAcess(self):
        self.writeControlWord(0xFFFF)
        self.writeControlWord(0xFFFF)

    def deviceType(self):
        return self.readControlWord(0x01)

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
        # self.bus.write_word_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, value)
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, 0x00, subCommandLSB)
        self.bus.write_byte_data(BSP_NORMAL_MODE_I2C_ADDR, 0x01, subCommandMSB)

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