import serial
import serial.tools.list_ports as list_ports
import string, array

class smu_base:

    def __init__(self, port = ''):
        self.FCY = 16e6
        self.TCY = 62.5e-9
        self.timer_multipliers = [self.TCY, 8. * self.TCY, 64. * self.TCY, 256. * self.TCY]

        if port == '':
            self.dev = None
            self.connected = False
            devices = list_ports.comports()
            for device in devices:
                if device.vid == 0x6666 and device.pid == 0xCDC2:
                    try:
                        self.dev = serial.Serial(device.device)
                        self.connected = True
                        print(f'Connected to {device.device}...')
                    except:
                        pass
                if self.connected:
                    break
        else:
            try:
                self.dev = serial.Serial(port)
                self.connected = True
            except:
                self.dev = None
                self.connected = False

        if self.connected:
            self.write('')

    def write(self, command):
        if self.connected:
            self.dev.write(f'{command}\r'.encode())

    def read(self):
        if self.connected:
            return self.dev.readline().decode()

    def toggle_led1(self):
        if self.connected:
            self.write('UI:LED1 TOGGLE')

    def set_led1(self, val):
        if self.connected:
            self.write(f'UI:LED1 {int(val):X}')

    def get_led1(self):
        if self.connected:
            self.write('UI:LED1?')
            return int(self.read())

    def toggle_led2(self):
        if self.connected:
            self.write('UI:LED2 TOGGLE')

    def set_led2(self, val):
        if self.connected:
            self.write(f'UI:LED2 {int(val):X}')

    def get_led2(self):
        if self.connected:
            self.write('UI:LED2?')
            return int(self.read())

    def toggle_led3(self):
        if self.connected:
            self.write('UI:LED3 TOGGLE')

    def set_led3(self, val):
        if self.connected:
            self.write(f'UI:LED3 {int(val):X}')

    def get_led3(self):
        if self.connected:
            self.write('UI:LED3?')
            return int(self.read())

    def read_sw1(self):
        if self.connected:
            self.write('UI:SW1?')
            return int(self.read())

    def toggle_ena12V(self):
        if self.connected:
            self.write('PWR:ENA12V TOGGLE')

    def set_ena12V(self, val):
        if self.connected:
            self.write(f'PWR:ENA12V {int(val):X}')

    def get_ena12V(self):
        if self.connected:
            self.write('PWR:ENA12V?')
            return int(self.read())

    def dac10_set_dac1(self, val):
        if self.connected:
            self.write(f'DAC10:DAC1 {int(val):X}')

    def dac10_get_dac1(self):
        if self.connected:
            self.write('DAC10:DAC1?')
            return int(self.read(), 16)

    def dac10_set_dac2(self, val):
        if self.connected:
            self.write(f'DAC10:DAC2 {int(val):X}')

    def dac10_get_dac2(self):
        if self.connected:
            self.write('DAC10:DAC2?')
            return int(self.read(), 16)

    def dac10_set_diff(self, val):
        if self.connected:
            if -1023 <= val <= 1023:
                val = val if val >=0 else val + 65536
                self.write(f'DAC10:DIFF {int(val):X}')

    def dac10_get_diff(self):
        if self.connected:
            self.write('DAC10:DIFF?')
            val = int(self.read(), 16)
            return val if val < 32768 else val - 65536

    def dac16_set_dac0(self, val):
        if self.connected:
            self.write(f'DAC16:DAC0 {int(val):X}')

    def dac16_get_dac0(self):
        if self.connected:
            self.write('DAC16:DAC0?')
            return int(self.read(), 16)

    def dac16_set_dac1(self, val):
        if self.connected:
            self.write(f'DAC16:DAC1 {int(val):X}')

    def dac16_get_dac1(self):
        if self.connected:
            self.write('DAC16:DAC1?')
            return int(self.read(), 16)

    def dac16_set_dac2(self, val):
        if self.connected:
            self.write(f'DAC16:DAC2 {int(val):X}')

    def dac16_get_dac2(self):
        if self.connected:
            self.write('DAC16:DAC2?')
            return int(self.read(), 16)

    def dac16_set_dac3(self, val):
        if self.connected:
            self.write(f'DAC16:DAC3 {int(val):X}')

    def dac16_get_dac3(self):
        if self.connected:
            self.write('DAC16:DAC3?')
            return int(self.read(), 16)

    def dac16_set_ch1(self, val):
        if self.connected:
            if -65535 <= val <= 65535:
                pos = (65536 + int(val)) >> 1
                neg = (65536 - int(val)) >> 1
                self.write(f'DAC16:CH1 {pos:X},{neg:X}')

    def dac16_get_ch1(self):
        if self.connected:
            self.write('DAC16:CH1?')
            ret = self.read()
            vals = [int(s, 16) for s in ret.split(',')]
            return vals[0] - vals[1]

    def dac16_set_ch2(self, val):
        if self.connected:
            if -65535 <= val <= 65535:
                pos = (65536 + int(val)) >> 1
                neg = (65536 - int(val)) >> 1
                self.write(f'DAC16:CH2 {pos:X},{neg:X}')

    def dac16_get_ch2(self):
        if self.connected:
            self.write('DAC16:CH2?')
            ret = self.read()
            vals = [int(s, 16) for s in ret.split(',')]
            return vals[0] - vals[1]

    def adc18_get_ch1(self):
        if self.connected:
            self.write('ADC18:CH1?')
            ret = self.read()
            vals = [int(s, 16) for s in ret.split(',')]
            val = (vals[1] << 16) + vals[0]
            return val if val < 2147483648 else val - 4294967296

    def adc18_get_ch2(self):
        if self.connected:
            self.write('ADC18:CH2?')
            ret = self.read()
            vals = [int(s, 16) for s in ret.split(',')]
            val = (vals[1] << 16) + vals[0]
            return val if val < 2147483648 else val - 4294967296

    def adc18_get_ch1_avg(self):
        if self.connected:
            self.write('ADC18:CH1AVG?')
            ret = self.read()
            vals = [int(s, 16) for s in ret.split(',')]
            val = (vals[1] << 16) + vals[0]
            return val if val < 2147483648 else val - 4294967296

    def adc18_get_ch2_avg(self):
        if self.connected:
            self.write('ADC18:CH2AVG?')
            ret = self.read()
            vals = [int(s, 16) for s in ret.split(',')]
            val = (vals[1] << 16) + vals[0]
            return val if val < 2147483648 else val - 4294967296

    def adc18_get_both(self):
        if self.connected:
            self.write('ADC18:BOTH?')
            ret = self.read()
            vals = [int(s, 16) for s in ret.split(',')]
            val1 = (vals[1] << 16) + vals[0]
            val1 = val1 if val1 < 2147483648 else val1 - 4294967296
            val2 = (vals[3] << 16) + vals[2]
            val2 = val2 if val2 < 2147483648 else val2 - 4294967296
            return [val1, val2]

    def adc18_get_both_avg(self):
        if self.connected:
            self.write('ADC18:BOTHAVG?')
            ret = self.read()
            vals = [int(s, 16) for s in ret.split(',')]
            val1 = (vals[1] << 16) + vals[0]
            val1 = val1 if val1 < 2147483648 else val1 - 4294967296
            val2 = (vals[3] << 16) + vals[2]
            val2 = val2 if val2 < 2147483648 else val2 - 4294967296
            return [val1, val2]

    def set_portd(self, val):
        if self.connected:
            self.write(f'MODE:PORTD {int(val):X}')

    def get_portd(self):
        if self.connected:
            self.write('MODE:PORTD?')
            return int(self.read(), 16)

    def toggle_rd(self, bit):
        if self.connected:
            if 0 <= bit < 7:
                self.write(f'MODE:RD{int(bit)} TOGGLE')

    def set_rd(self, bit, val):
        if self.connected:
            if 0 <= bit < 7:
                self.write(f'MODE:RD{int(bit)} {int(val):X}')

    def get_rd(self, bit):
        if self.connected:
            if 0 <= bit < 7:
                self.write(f'MODE:RD{int(bit)}?')
                return int(self.read())

    def set_porte(self, val):
        if self.connected:
            self.write(f'MODE:PORTE {int(val):X}')

    def get_porte(self):
        if self.connected:
            self.write('MODE:PORTE?')
            return int(self.read(), 16)

    def toggle_re(self, bit):
        if self.connected:
            if 0 <= bit < 7:
                self.write(f'MODE:RE{int(bit)} TOGGLE')

    def set_re(self, bit, val):
        if self.connected:
            if 0 <= bit < 7:
                self.write(f'MODE:RE{int(bit)} {int(val):X}')

    def get_re(self, bit):
        if self.connected:
            if 0 <= bit < 7:
                self.write(f'MODE:RE{int(bit)}?')
                return int(self.read())

    def digout_set_mode(self, pin, mode):
        if self.connected:
            self.write(f'DIGOUT:MODE {int(pin):X},{int(mode):X}')

    def digout_get_mode(self, pin):
        if self.connected:
            self.write(f'DIGOUT:MODE? {int(pin):X}')
            return int(self.read(), 16)

    def digout_set(self, pin):
        if self.connected:
            self.write(f'DIGOUT:SET {int(pin):X}')

    def digout_clear(self, pin):
        if self.connected:
            self.write(f'DIGOUT:CLEAR {int(pin):X}')

    def digout_toggle(self, pin):
        if self.connected:
            self.write(f'DIGOUT:TOGGLE {int(pin):X}')

    def digout_write(self, pin, val):
        if self.connected:
            self.write(f'DIGOUT:WRITE {int(pin):X},{int(val):X}')

    def digout_read(self, pin):
        if self.connected:
            self.write(f'DIGOUT:READ {int(pin):X}')
            return int(self.read(), 16)

    def digout_set_od(self, pin, val):
        if self.connected:
            self.write(f'DIGOUT:OD {int(pin):X},{int(val):X}')

    def digout_get_od(self, pin):
        if self.connected:
            self.write(f'DIGOUT:OD? {int(pin):X}')
            return int(self.read(), 16)

    def digout_set_freq(self, pin, freq):
        if self.connected:
            val = int(self.FCY / freq - 1.)
            val = val if val < 65536 else 65535
            self.write(f'DIGOUT:PERIOD {int(pin):X},{val:X}')

    def digout_get_freq(self, pin):
        if self.connected:
            self.write(f'DIGOUT:PERIOD? {int(pin):X}')
            val = int(self.read(), 16)
            return self.FCY / (val + 1.)

    def digout_set_duty(self, pin, duty):
        if self.connected:
            val = int(65536 * duty)
            val = val if val < 65536 else 65535
            self.write(f'DIGOUT:DUTY {int(pin):X},{val:X}')

    def digout_get_duty(self, pin):
        if self.connected:
            self.write(f'DIGOUT:DUTY? {int(pin):X}')
            val = int(self.read(), 16)
            return val / 65536.

    def digout_set_width(self, pin, width):
        if self.connected:
            val = int(self.FCY * width + 0.5)
            val = val if val > 1 else 1
            val = val if val < 65535 else 65535
            self.write(f'DIGOUT:WIDTH {int(pin):X},{val:X}')

    def digout_get_width(self, pin):
        if self.connected:
            self.write(f'DIGOUT:WIDTH? {int(pin):X}')
            val = int(self.read(), 16)
            return val * self.TCY

    def digout_set_period(self, period):
        if self.connected:
            if period > 256. * 65536. * self.TCY:
                return
            elif period > 64. * 65536. * self.TCY:
                T1CON = 0x0030
                PR1 = int(period * (self.FCY / 256.)) - 1
            elif period > 8. * 65536. * self.TCY:
                T1CON = 0x0020
                PR1 = int(period * (self.FCY / 64.)) - 1
            elif period > 65536. * self.TCY:
                T1CON = 0x0010
                PR1 = int(period * (self.FCY / 8.)) - 1
            elif period >= 8. * self.TCY:
                T1CON = 0x0000
                PR1 = int(period * self.FCY) - 1
            else:
                return
            self.write(f'DIGOUT:T1PERIOD {PR1:X},{T1CON:X}')

    def digout_get_period(self):
        if self.connected:
            self.write('DIGOUT:T1PERIOD?')
            vals = self.read().split(',')
            PR1 = int(vals[0], 16)
            T1CON = int(vals[1], 16)
            prescalar = (T1CON & 0x0030) >> 4
            return self.timer_multipliers[prescalar] * (float(PR1) + 1.)

    def ble_set_reset(self, val):
        if self.connected:
            self.write(f'BLE:RESET {int(val):X}')

    def ble_get_reset(self):
        if self.connected:
            self.write('BLE:RESET?')
            return int(self.read(), 16)

    def ble_toggle_reset(self):
        if self.connected:
            self.write('BLE:RESET TOGGLE')

    def ble_forward(self):
        if self.connected:
            self.write('BLE:FORWARD')

    def flash_read(self, address, num_bytes):
        if self.connected:
            self.write('FLASH:READ {:X},{:X},{:X}'.format(int(address) >> 16, int(address) & 0xFFFF, int(num_bytes)))
            ret = self.read()
            vals = ret.split(',')
            return [int(val, 16) for val in vals]

    def flash_write(self, address, values):
        if self.connected:
            cmd = 'FLASH:WRITE {:X},{:X}'.format(int(address) >> 16, int(address) & 0xFFFF)
            for value in values:
                cmd += ',{:X}'.format(int(value & 0xFF))
            self.write(cmd)

    def flash_erase(self, address):
        if self.connected:
            self.write('FLASH:ERASE {:X},{:X}'.format(int(address) >> 16, int(address) & 0xFFFF))

