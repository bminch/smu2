
import copy
import smu_base

class smu:

    VREF = 2.5
    DIVIDER1 = 5. / 2.
    DIVIDER2 = 10.
    RESISTORS = (316., 10E3, 316E3, 10E6)
    CURRENT_RANGES = (1. / RESISTORS[0], 
                      1. / RESISTORS[1], 
                      1. / RESISTORS[2], 
                      1. / RESISTORS[3])

    VOLTAGE = 0
    CURRENT = 1

    nominal_meas_voltage_gain = [DIVIDER2 * VREF / DIVIDER1 / 2 ** 17, 
                                 DIVIDER2 * VREF / DIVIDER1 / 2 ** 17]
    nominal_meas_voltage_offset = [0, 0]

    nominal_src_voltage_gains = [[2 ** 16 * DIVIDER1 / VREF / DIVIDER2, 
                                  2 ** 16 * DIVIDER1 / VREF / DIVIDER2, 
                                  2 ** 16 * DIVIDER1 / VREF / DIVIDER2, 
                                  2 ** 16 * DIVIDER1 / VREF / DIVIDER2], 
                                 [2 ** 16 * DIVIDER1 / VREF / DIVIDER2, 
                                  2 ** 16 * DIVIDER1 / VREF / DIVIDER2, 
                                  2 ** 16 * DIVIDER1 / VREF / DIVIDER2, 
                                  2 ** 16 * DIVIDER1 / VREF / DIVIDER2]]
    nominal_src_voltage_offsets = [[0, 0, 0, 0], [0, 0, 0, 0]]

    nominal_src_current_gains = [[RESISTORS[0] * DIVIDER1 * 2 ** 16 / VREF, 
                                  RESISTORS[1] * DIVIDER1 * 2 ** 16 / VREF, 
                                  RESISTORS[2] * DIVIDER1 * 2 ** 16 / VREF, 
                                  RESISTORS[3] * DIVIDER1 * 2 ** 16 / VREF], 
                                 [RESISTORS[0] * DIVIDER1 * 2 ** 16 / VREF, 
                                  RESISTORS[1] * DIVIDER1 * 2 ** 16 / VREF, 
                                  RESISTORS[2] * DIVIDER1 * 2 ** 16 / VREF, 
                                  RESISTORS[3] * DIVIDER1 * 2 ** 16 / VREF]]
    nominal_src_current_offsets = [[0, 0, 0, 0], [0, 0, 0, 0]]

    nominal_meas_current_gains = [[VREF / DIVIDER1 / RESISTORS[0] / 2 ** 17, 
                                   VREF / DIVIDER1 / RESISTORS[1] / 2 ** 17, 
                                   VREF / DIVIDER1 / RESISTORS[2] / 2 ** 17, 
                                   VREF / DIVIDER1 / RESISTORS[3] / 2 ** 17], 
                                  [VREF / DIVIDER1 / RESISTORS[0] / 2 ** 17, 
                                   VREF / DIVIDER1 / RESISTORS[1] / 2 ** 17, 
                                   VREF / DIVIDER1 / RESISTORS[2] / 2 ** 17, 
                                   VREF / DIVIDER1 / RESISTORS[3] / 2 ** 17]]
    nominal_meas_current_offsets = [[0, 0, 0, 0], [0, 0, 0, 0]]


    def __init__(self, port = ''):
        self.meas_voltage_gain = copy.deepcopy(smu.nominal_meas_voltage_gain)
        self.meas_voltage_offset = copy.deepcopy(smu.nominal_meas_voltage_offset)

        self.src_voltage_gains = copy.deepcopy(smu.nominal_src_voltage_gains)
        self.src_voltage_offsets = copy.deepcopy(smu.nominal_src_voltage_offsets)

        self.src_current_gains = copy.deepcopy(smu.nominal_src_current_gains)
        self.src_current_offsets = copy.deepcopy(smu.nominal_src_current_offsets)

        self.meas_current_gains = copy.deepcopy(smu.nominal_meas_current_gains)
        self.meas_current_offsets = copy.deepcopy(smu.nominal_meas_current_offsets)

        self.dev = smu_base.smu_base(port)

        if not self.dev.connected:
            return

        # Enable +/-12V power supplies.
        self.dev.set_ena12V(1)

        # Set both channels initially to SI/MV mode in the 100nA range.
        self.dev.set_portd(0b1001111)
        self.dev.set_porte(0b1001111)

        self.read_calibration_values()

    def set_source_function(self, channel, function):
        if not self.dev.connected:
            return

        if function in ('CURRENT', 'VOLTAGE'):
            if channel == 1:
                self.dev.set_rd(3, 1 if function == 'CURRENT' else 0)
                self.dev.set_rd(5, 0 if function == 'CURRENT' else 1)
            elif channel == 2:
                self.dev.set_re(3, 1 if function == 'CURRENT' else 0)
                self.dev.set_re(5, 0 if function == 'CURRENT' else 1)
        else:
            if channel == 1:
                self.dev.set_rd(3, function)
                self.dev.set_rd(5, 1 - function)
            elif channel == 2:
                self.dev.set_re(3, function)
                self.dev.set_re(5, 1 - function)

    def get_source_function(self, channel):
        if not self.dev.connected:
            return

        if channel == 1:
            return 'CURRENT' if self.dev.get_rd(3) == 1 else 'VOLTAGE'
        elif channel == 2:
            return 'CURRENT' if self.dev.get_re(3) == 1 else 'VOLTAGE'

    def set_measure_function(self, channel, function):
        if not self.dev.connected:
            return

        if function in ('CURRENT', 'VOLTAGE'):
            if channel == 1:
                self.dev.set_rd(2, 1 if function == 'VOLTAGE' else 0)
            elif channel == 2:
                self.dev.set_re(2, 1 if function == 'VOLTAGE' else 0)
        else:
            if channel == 1:
                self.dev.set_rd(2, 1 if function == smu.VOLTAGE else 0)
            elif channel == 2:
                self.dev.set_re(2, 1 if function == smu.VOLTAGE else 0)

    def get_measure_function(self, channel):
        if not self.dev.connected:
            return

        if channel == 1:
            return 'VOLTAGE' if self.dev.get_rd(2) == 1 else 'CURRENT'
        elif channel == 2:
            return 'VOLTAGE' if self.dev.get_re(2) == 1 else 'CURRENT'

    def set_current_range(self, channel, value):
        if not self.dev.connected:
            return

        if channel == 1:
            self.dev.set_portd((self.dev.get_portd() & 0x7C) | (value & 0x03))
        elif channel == 2:
            self.dev.set_porte((self.dev.get_porte() & 0x7C) | (value & 0x03))

    def get_current_range(self, channel):
        if not self.dev.connected:
            return

        if channel == 1:
            return self.dev.get_portd() & 0x03
        elif channel == 2:
            return self.dev.get_porte() & 0x03

    def source_current(self, channel, current):
        if not self.dev.connected:
            return

        if channel != 1 and channel != 2:
            print('WARNING: Channel value must be either 1 or 2.')
            return

        if abs(current) > smu.CURRENT_RANGES[0]:
            print(f'WARNING: Specified current for channel {channel} exceeds maximum of ±3.165mA.')
            return
        elif abs(current) > smu.CURRENT_RANGES[1]:
            current_range = 0
        elif abs(current) > smu.CURRENT_RANGES[2]:
            current_range = 1
        elif abs(current) > smu.CURRENT_RANGES[3]:
            current_range = 2
        else:
            current_range = 3

        value = round(current * self.src_current_gains[channel - 1][current_range] + self.src_current_offsets[channel - 1][current_range])

        if abs(value) > 65535:
            if current_range > 0:
                current_range = current_range - 1
                value = round(current * self.src_current_gains[channel - 1][current_range] + self.src_current_offsets[channel - 1][current_range])
            elif value > 0:
                value = 65535
            else:
                value = -65535

        if channel == 1:
            self.dev.set_portd((self.dev.get_portd() & 0x54) | 0b0001000 | current_range)
            self.dev.dac16_set_ch1(value)
        else:
            self.dev.set_porte((self.dev.get_porte() & 0x54) | 0b0001000 | current_range)
            self.dev.dac16_set_ch2(value)

    def source_voltage(self, channel, voltage):
        if not self.dev.connected:
            return

        if channel != 1 and channel != 2:
            print('WARNING: Channel value must be either 1 or 2.')
            return

        if abs(voltage) > 10.:
            print(f'WARNING: Specified voltage for channel {channel} exceeds maximum of ±10V.')
            return

        current_range = self.get_current_range(channel)
        value = round(voltage * self.src_voltage_gains[channel - 1][current_range] + self.src_voltage_offsets[channel - 1][current_range])

        self.set_source_function(channel, smu.VOLTAGE)
        if channel == 1:
            self.dev.dac16_set_ch1(value)
        else:
            self.dev.dac16_set_ch2(value)

    def measure_current(self, channel):
        if not self.dev.connected:
            return

        if channel != 1 and channel != 2:
            print('WARNING: Channel value must be either 1 or 2.')
            return

        self.set_measure_function(channel, smu.CURRENT)
        current_range = self.get_current_range(channel)
        value = self.dev.adc18_get_ch1_avg() if channel == 1 else self.dev.adc18_get_ch2_avg()
        return self.meas_current_gains[channel - 1][current_range] * (value + self.meas_current_offsets[channel - 1][current_range])

    def measure_voltage(self, channel):
        if not self.dev.connected:
            return

        if channel != 1 and channel != 2:
            print('WARNING: Channel value must be either 1 or 2.')
            return

        self.set_measure_function(channel, smu.VOLTAGE)
        value = self.dev.adc18_get_ch1_avg() if channel == 1 else self.dev.adc18_get_ch2_avg()
        return self.meas_voltage_gain[channel - 1] * (value + self.meas_voltage_offset[channel - 1])

    def autorange_once(self, channel):
        if not self.dev.connected:
            return

        if channel != 1 and channel != 2:
            print('WARNING: Channel value must be either 1 or 2.')
            return

        if self.get_measure_function(channel) == 'VOLTAGE':
            return

        done = False
        while not done:
            current_range = self.get_current_range(channel)
            value = self.dev.adc18_get_ch1_avg() if channel == 1 else self.dev.adc18_get_ch2_avg()
            value = value + self.meas_current_offsets[channel - 1][current_range]
            if abs(value) > 0.97 * 2 ** 17 and current_range > 0:
                current_range = current_range - 1
            elif abs(value) < 0.03 * 2 ** 17 and current_range < 3:
                current_range = current_range + 1
            else:
                done = True
            self.set_current_range(channel, current_range)

    def read_serial_number(self):
        if not self.dev.connected:
            return ''

        vals = self.dev.flash_read(0xFC00, 4)
        if vals[2] == 255:
            return ''
        length = vals[0] + 256 * vals[1]
        words = length // 3
        extra_bytes = length % 3

        address = 0xFC02
        vals = []
        for i in range(words):
            vals.extend(self.dev.flash_read(address, 3)[0:3])
            address += 2
        if extra_bytes != 0:
            vals.extend(self.dev.flash_read(address, extra_bytes)[0:extra_bytes])

        return bytes(vals).decode()

    def write_serial_number(self, serial_number):
        if not self.dev.connected:
            return

        length = len(serial_number)
        if length == 0 or length > 765:
            return
        self.dev.flash_erase(0xFC00)
        vals = [length & 0xFF, length >> 8, 0, 0]
        self.dev.flash_write(0xFC00, vals)

        serial_number_vals = list(serial_number.encode())
        words = length // 3
        extra_bytes = length % 3
        address = 0xFC02
        for i in range(words):
            vals = serial_number_vals[3 * i:3 * i + 3]
            vals.append(0)
            self.dev.flash_write(address, vals)
            address += 2
        if extra_bytes != 0:
            vals = serial_number_vals[3 * words:]
            vals.extend([0] * (4 - extra_bytes))
            self.dev.flash_write(address, vals)

    def read_calibration_values(self):
        if not self.dev.connected:
            return

        for channel in range(2):
            vals = self.dev.flash_read(0x10000 + 2 * channel, 4)
            if (vals[0] != 255) or (vals[1] != 255) or (vals[2] != 255):
                val = (vals[0] + 256 * vals[1] + 65536 * vals[2]) / 2 ** 23
                self.meas_voltage_gain[channel] = val * smu.nominal_meas_voltage_gain[channel]

        for channel in range(2):
            vals = self.dev.flash_read(0x10004 + 2 * channel, 4)
            if (vals[0] != 255) or (vals[1] != 255) or (vals[2] != 255):
                val = (vals[0] + 256 * vals[1] + 65536 * vals[2])
                mag = (val & 0x7FFFFF) / 256.
                self.meas_voltage_offset[channel] = mag if val < 0x800000 else -mag

        for channel in range(2):
            for current_range in range(4):
                vals = self.dev.flash_read(0x10008 + 2 * (4 * channel + current_range), 4)
                if (vals[0] != 255) or (vals[1] != 255) or (vals[2] != 255):
                    val = (vals[0] + 256 * vals[1] + 65536 * vals[2]) / 2 ** 23
                    self.src_voltage_gains[channel][current_range] = val * smu.nominal_src_voltage_gains[channel][current_range]

        for channel in range(2):
            for current_range in range(4):
                vals = self.dev.flash_read(0x10018 + 2 * (4 * channel + current_range), 4)
                if (vals[0] != 255) or (vals[1] != 255) or (vals[2] != 255):
                    val = (vals[0] + 256 * vals[1] + 65536 * vals[2])
                    mag = (val & 0x7FFFFF) / 256.
                    self.src_voltage_offsets[channel][current_range] = mag if val < 0x800000 else -mag

        for channel in range(2):
            for current_range in range(4):
                vals = self.dev.flash_read(0x10028 + 2 * (4 * channel + current_range), 4)
                if (vals[0] != 255) or (vals[1] != 255) or (vals[2] != 255):
                    val = (vals[0] + 256 * vals[1] + 65536 * vals[2]) / 2 ** 23
                    self.src_current_gains[channel][current_range] = val * smu.nominal_src_current_gains[channel][current_range]

        for channel in range(2):
            for current_range in range(4):
                vals = self.dev.flash_read(0x10038 + 2 * (4 * channel + current_range), 4)
                if (vals[0] != 255) or (vals[1] != 255) or (vals[2] != 255):
                    val = (vals[0] + 256 * vals[1] + 65536 * vals[2])
                    mag = (val & 0x7FFFFF) / 256.
                    self.src_current_offsets[channel][current_range] = mag if val < 0x800000 else -mag

        for channel in range(2):
            for current_range in range(4):
                vals = self.dev.flash_read(0x10048 + 2 * (4 * channel + current_range), 4)
                if (vals[0] != 255) or (vals[1] != 255) or (vals[2] != 255):
                    val = (vals[0] + 256 * vals[1] + 65536 * vals[2]) / 2 ** 23
                    self.meas_current_gains[channel][current_range] = val * smu.nominal_meas_current_gains[channel][current_range]

        for channel in range(2):
            for current_range in range(4):
                vals = self.dev.flash_read(0x10058 + 2 * (4 * channel + current_range), 4)
                if (vals[0] != 255) or (vals[1] != 255) or (vals[2] != 255):
                    val = (vals[0] + 256 * vals[1] + 65536 * vals[2])
                    mag = (val & 0x7FFFFF) / 256.
                    self.meas_current_offsets[channel][current_range] = mag if val < 0x800000 else -mag

    def write_calibration_values(self):
        if not self.dev.connected:
            return

        self.dev.flash_erase(0x10000)

        vals = []
        for channel in range(2):
            val = self.meas_voltage_gain[channel] / smu.nominal_meas_voltage_gain[channel]
            val = round(2 ** 23 * val)
            vals.append(val & 0x0000FF)
            vals.append((val >> 8) & 0x0000FF)
            vals.append(val >> 16)
            vals.append(0)

        for channel in range(2):
            val = round(256. * abs(self.meas_voltage_offset[channel])) | (0x800000 if self.meas_voltage_offset[channel] < 0 else 0x000000)
            vals.append(val & 0x0000FF)
            vals.append((val >> 8) & 0x0000FF)
            vals.append(val >> 16)
            vals.append(0)

        self.dev.flash_write(0x10000, vals)
        read_vals = self.dev.flash_read(0x10000, len(vals))
        if not all([read_vals[i] == vals[i] for i in range(len(vals))]):
            print(f'WARNING: Problem writing calibration values at 0x10000: wrote {vals} but read {read_vals}.')

        for channel in range(2):
            vals = []
            for current_range in range(4):
                val = self.src_voltage_gains[channel][current_range] / smu.nominal_src_voltage_gains[channel][current_range]
                val = round(2 ** 23 * val)
                vals.append(val & 0x0000FF)
                vals.append((val >> 8) & 0x0000FF)
                vals.append(val >> 16)
                vals.append(0)
            self.dev.flash_write(0x10008 + 8 * channel, vals)
            read_vals = self.dev.flash_read(0x10008 + 8 * channel, len(vals))
            if not all([read_vals[i] == vals[i] for i in range(len(vals))]):
                print(f'WARNING: Problem writing calibration values at 0x{0x10008 + 8 * channel:X}: wrote {vals} but read {read_vals}.')

        for channel in range(2):
            vals = []
            for current_range in range(4):
                val = round(256. * abs(self.src_voltage_offsets[channel][current_range])) | (0x800000 if self.src_voltage_offsets[channel][current_range] < 0 else 0x000000)
                vals.append(val & 0x0000FF)
                vals.append((val >> 8) & 0x0000FF)
                vals.append(val >> 16)
                vals.append(0)
            self.dev.flash_write(0x10018 + 8 * channel, vals)
            read_vals = self.dev.flash_read(0x10018 + 8 * channel, len(vals))
            if not all([read_vals[i] == vals[i] for i in range(len(vals))]):
                print(f'WARNING: Problem writing calibration values at 0x{0x10018 + 8 * channel:X}: wrote {vals} but read {read_vals}.')

        for channel in range(2):
            vals = []
            for current_range in range(4):
                val = self.src_current_gains[channel][current_range] / smu.nominal_src_current_gains[channel][current_range]
                val = round(2 ** 23 * val)
                vals.append(val & 0x0000FF)
                vals.append((val >> 8) & 0x0000FF)
                vals.append(val >> 16)
                vals.append(0)
            self.dev.flash_write(0x10028 + 8 * channel, vals)
            read_vals = self.dev.flash_read(0x10028 + 8 * channel, len(vals))
            if not all([read_vals[i] == vals[i] for i in range(len(vals))]):
                print(f'WARNING: Problem writing calibration values at 0x{0x10028 + 8 * channel:X}: wrote {vals} but read {read_vals}.')

        for channel in range(2):
            vals = []
            for current_range in range(4):
                val = round(256. * abs(self.src_current_offsets[channel][current_range])) | (0x800000 if self.src_current_offsets[channel][current_range] < 0 else 0x000000)
                vals.append(val & 0x0000FF)
                vals.append((val >> 8) & 0x0000FF)
                vals.append(val >> 16)
                vals.append(0)
            self.dev.flash_write(0x10038 + 8 * channel, vals)
            read_vals = self.dev.flash_read(0x10038 + 8 * channel, len(vals))
            if not all([read_vals[i] == vals[i] for i in range(len(vals))]):
                print(f'WARNING: Problem writing calibration values at 0x{0x10038 + 8 * channel:X}: wrote {vals} but read {read_vals}.')

        for channel in range(2):
            vals = []
            for current_range in range(4):
                val = self.meas_current_gains[channel][current_range] / smu.nominal_meas_current_gains[channel][current_range]
                val = round(2 ** 23 * val)
                vals.append(val & 0x0000FF)
                vals.append((val >> 8) & 0x0000FF)
                vals.append(val >> 16)
                vals.append(0)
            self.dev.flash_write(0x10048 + 8 * channel, vals)
            read_vals = self.dev.flash_read(0x10048 + 8 * channel, len(vals))
            if not all([read_vals[i] == vals[i] for i in range(len(vals))]):
                print(f'WARNING: Problem writing calibration values at 0x{0x10048 + 8 * channel:X}: wrote {vals} but read {read_vals}.')

        for channel in range(2):
            vals = []
            for current_range in range(4):
                val = round(256. * abs(self.meas_current_offsets[channel][current_range])) | (0x800000 if self.meas_current_offsets[channel][current_range] < 0 else 0x000000)
                vals.append(val & 0x0000FF)
                vals.append((val >> 8) & 0x0000FF)
                vals.append(val >> 16)
                vals.append(0)
            self.dev.flash_write(0x10058 + 8 * channel, vals)
            read_vals = self.dev.flash_read(0x10058 + 8 * channel, len(vals))
            if not all([read_vals[i] == vals[i] for i in range(len(vals))]):
                print(f'WARNING: Problem writing calibration values at 0x{0x10058 + 8 * channel:X}: wrote {vals} but read {read_vals}.')

    def load_calibration_values(self, filename):
        try:
            file = open(filename, 'r')
        except FileNotFoundError:
            return

        for channel in range(2):
            val = int(file.readline().strip(), 16)
            val = val / 2 ** 23
            self.meas_voltage_gain[channel] = val * smu.nominal_meas_voltage_gain[channel]

        for channel in range(2):
            val = int(file.readline().strip(), 16)
            mag = (val & 0x7FFFFF) / 256.
            self.meas_voltage_offset[channel] = mag if val < 0x800000 else -mag

        for channel in range(2):
            for current_range in range(4):
                val = int(file.readline().strip(), 16)
                val = val / 2 ** 23
                self.src_voltage_gains[channel][current_range] = val * smu.nominal_src_voltage_gains[channel][current_range]

        for channel in range(2):
            for current_range in range(4):
                val = int(file.readline().strip(), 16)
                mag = (val & 0x7FFFFF) / 256.
                self.src_voltage_offsets[channel][current_range] = mag if val < 0x800000 else -mag

        for channel in range(2):
            for current_range in range(4):
                val = int(file.readline().strip(), 16)
                val = val / 2 ** 23
                self.src_current_gains[channel][current_range] = val * smu.nominal_src_current_gains[channel][current_range]

        for channel in range(2):
            for current_range in range(4):
                val = int(file.readline().strip(), 16)
                mag = (val & 0x7FFFFF) / 256.
                self.src_current_offsets[channel][current_range] = mag if val < 0x800000 else -mag

        for channel in range(2):
            for current_range in range(4):
                val = int(file.readline().strip(), 16)
                val = val / 2 ** 23
                self.meas_current_gains[channel][current_range] = val * smu.nominal_meas_current_gains[channel][current_range]

        for channel in range(2):
            for current_range in range(4):
                val = int(file.readline().strip(), 16)
                mag = (val & 0x7FFFFF) / 256.
                self.meas_current_offsets[channel][current_range] = mag if val < 0x800000 else -mag

        file.close()

    def save_calibration_values(self, filename):
        file = open(filename, 'w')

        for channel in range(2):
            val = self.meas_voltage_gain[channel] / smu.nominal_meas_voltage_gain[channel]
            val = round(2 ** 23 * val)
            file.write(f'{val:06X}\n')

        for channel in range(2):
            val = round(256. * abs(self.meas_voltage_offset[channel])) | (0x800000 if self.meas_voltage_offset[channel] < 0 else 0x000000)
            file.write(f'{val:06X}\n')

        for channel in range(2):
            for current_range in range(4):
                val = self.src_voltage_gains[channel][current_range] / smu.nominal_src_voltage_gains[channel][current_range]
                val = round(2 ** 23 * val)
                file.write(f'{val:06X}\n')

        for channel in range(2):
            for current_range in range(4):
                val = round(256. * abs(self.src_voltage_offsets[channel][current_range])) | (0x800000 if self.src_voltage_offsets[channel][current_range] < 0 else 0x000000)
                file.write(f'{val:06X}\n')

        for channel in range(2):
            for current_range in range(4):
                val = self.src_current_gains[channel][current_range] / smu.nominal_src_current_gains[channel][current_range]
                val = round(2 ** 23 * val)
                file.write(f'{val:06X}\n')

        for channel in range(2):
            for current_range in range(4):
                val = round(256. * abs(self.src_current_offsets[channel][current_range])) | (0x800000 if self.src_current_offsets[channel][current_range] < 0 else 0x000000)
                file.write(f'{val:06X}\n')

        for channel in range(2):
            for current_range in range(4):
                val = self.meas_current_gains[channel][current_range] / smu.nominal_meas_current_gains[channel][current_range]
                val = round(2 ** 23 * val)
                file.write(f'{val:06X}\n')

        for channel in range(2):
            for current_range in range(4):
                val = round(256. * abs(self.meas_current_offsets[channel][current_range])) | (0x800000 if self.meas_current_offsets[channel][current_range] < 0 else 0x000000)
                file.write(f'{val:06X}\n')

        file.close()

    def avg_adc_readings(self, channel, numavg = 10):
        if not self.dev.connected:
            return

        if channel != 1 and channel != 2:
            print('WARNING: Channel value must be either 1 or 2.')
            return

        val = 0
        for i in range(numavg):
            val = val + (self.dev.adc18_get_ch1_avg() if channel == 1 else self.dev.adc18_get_ch2_avg())
        return val / numavg

