import time

#x = linspace(-6000, 6000, 101)
x = linspace(-5000, 5000, 101)
y = linspace(-60000, 60000, 101)
z = linspace(-20000, 20000, 101)

s.set_current_range(1, 3)
s.set_source_function(1, 'CURRENT')
s.dev.dac16_set_ch1(0)
s.set_measure_function(1, 'VOLTAGE')

input('Connect CH1DUT+ to VREF and CH1DUT- to GND and press enter.')
ch1refp = s.avg_adc_readings(1)

input('Connect CH1DUT+ to GND and CH1DUT- to VREF and press enter.')
ch1refm = s.avg_adc_readings(1)

s.meas_voltage_gain[0] = 5. / (ch1refp - ch1refm)
s.meas_voltage_offset[0] = -0.5 * (ch1refp + ch1refm)

input('Connect a 1kΩ ± 0.01% resistor between CH1DUT+ and CH1DUT-, connect CH1DUT- to GND, and press enter.')
s.set_current_range(1, 0)
s.set_source_function(1, 'VOLTAGE')
s.set_measure_function(1, 'VOLTAGE')

ch1_0_svmv_vals = zeros(size(z))
for i in range(len(z)):
    s.dev.dac16_set_ch1(int(z[i]))
    ch1_0_svmv_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(z[:i], ch1_0_svmv_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MV ADC code')
        draw_now()

plot(z, ch1_0_svmv_vals)
xlabel('Source DAC code')
ylabel('SV/MV ADC code')
input('Press enter to continue.')

s.set_measure_function(1, 'CURRENT')

ch1_0_svmi_vals = zeros(size(z))
for i in range(len(z)):
    s.dev.dac16_set_ch1(int(z[i]))
    ch1_0_svmi_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(z[:i], ch1_0_svmi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MI ADC code')
        draw_now()

plot(z, ch1_0_svmi_vals)
xlabel('Source DAC code')
ylabel('SV/MI ADC code')
input('Press enter to continue.')

s.set_source_function(1, 'CURRENT')

ch1_0_simi_vals = zeros(size(y))
for i in range(len(y)):
    s.dev.dac16_set_ch1(int(y[i]))
    ch1_0_simi_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(y[:i], ch1_0_simi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SI/MI ADC code')
        draw_now()

plot(y, ch1_0_simi_vals)
xlabel('Source DAC code')
ylabel('SI/MI ADC code')
input('Press enter to continue.')

ch1_0_svmv_volts = s.meas_voltage_gain[0] * (ch1_0_svmv_vals + s.meas_voltage_offset[0])
[first, last, slope, intercept, numpoints] = linefit(ch1_0_svmv_volts, z)
s.src_voltage_gains[0][0] = slope
s.src_voltage_offsets[0][0] = intercept

plot(ch1_0_svmv_volts, [z, ch1_0_svmv_volts * slope + intercept], ['b.', 'k-'])
xlabel('SV/MV voltage (V)')
ylabel('Source DAC code')
input('Press enter to continue.')

ch1_0_svmv_amps = ch1_0_svmv_volts / 1E3
[first, last, slope, intercept, numpoints] = linefit(ch1_0_svmi_vals, ch1_0_svmv_amps)
s.meas_current_gains[0][0] = slope
s.meas_current_offsets[0][0] = intercept / slope

plot(ch1_0_svmi_vals, [ch1_0_svmv_amps, ch1_0_svmi_vals * slope + intercept], ['b.', 'k-'])
xlabel('SV/MI ADC code')
ylabel('SV/MV current (A)')
input('Press enter to continue.')

ch1_0_simi_amps = s.meas_current_gains[0][0] * (ch1_0_simi_vals + s.meas_current_offsets[0][0])
[first, last, slope, intercept, numpoints] = linefit(ch1_0_simi_amps, y)
s.src_current_gains[0][0] = slope
s.src_current_offsets[0][0] = intercept

plot(ch1_0_simi_amps, [y, ch1_0_simi_amps * slope + intercept], ['b.', 'k-'])
xlabel('SI/MI current (A)')
ylabel('Source DAC code')
input('Press enter to continue.')

input('Connect a 10kΩ ± 0.01% resistor between CH1DUT+ and CH1DUT-, connect CH1DUT- to GND, and press enter.')
s.set_current_range(1, 1)
s.set_source_function(1, 'VOLTAGE')
s.set_measure_function(1, 'VOLTAGE')

ch1_1_svmv_vals = zeros(size(x))
for i in range(len(x)):
    s.dev.dac16_set_ch1(int(x[i]))
    ch1_1_svmv_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(x[:i], ch1_1_svmv_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MV ADC code')
        draw_now()

plot(x, ch1_1_svmv_vals)
xlabel('Source DAC code')
ylabel('SV/MV ADC code')
input('Press enter to continue.')

s.set_measure_function(1, 'CURRENT')

ch1_1_svmi_vals = zeros(size(x))
for i in range(len(x)):
    s.dev.dac16_set_ch1(int(x[i]))
    ch1_1_svmi_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(x[:i], ch1_1_svmi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MI ADC code')
        draw_now()

plot(x, ch1_1_svmi_vals)
xlabel('Source DAC code')
ylabel('SV/MI ADC code')
input('Press enter to continue.')

s.set_source_function(1, 'CURRENT')

ch1_1_simi_vals = zeros(size(y))
for i in range(len(y)):
    s.dev.dac16_set_ch1(int(y[i]))
    ch1_1_simi_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(y[:i], ch1_1_simi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SI/MI ADC code')
        draw_now()

plot(y, ch1_1_simi_vals)
xlabel('Source DAC code')
ylabel('SI/MI ADC code')
input('Press enter to continue.')

ch1_1_svmv_volts = s.meas_voltage_gain[0] * (ch1_1_svmv_vals + s.meas_voltage_offset[0])
[first, last, slope, intercept, numpoints] = linefit(ch1_1_svmv_volts, x)
s.src_voltage_gains[0][1] = slope
s.src_voltage_offsets[0][1] = intercept

plot(ch1_1_svmv_volts, [x, ch1_1_svmv_volts * slope + intercept], ['b.', 'k-'])
xlabel('SV/MV voltage (V)')
ylabel('Source DAC code')
input('Press enter to continue.')

ch1_1_svmv_amps = ch1_1_svmv_volts / 10E3
[first, last, slope, intercept, numpoints] = linefit(ch1_1_svmi_vals, ch1_1_svmv_amps)
s.meas_current_gains[0][1] = slope
s.meas_current_offsets[0][1] = intercept / slope

plot(ch1_1_svmi_vals, [ch1_1_svmv_amps, ch1_1_svmi_vals * slope + intercept], ['b.', 'k-'])
xlabel('SV/MI ADC code')
ylabel('SV/MV current (A)')
input('Press enter to continue.')

ch1_1_simi_amps = s.meas_current_gains[0][1] * (ch1_1_simi_vals + s.meas_current_offsets[0][1])
[first, last, slope, intercept, numpoints] = linefit(ch1_1_simi_amps, y)
s.src_current_gains[0][1] = slope
s.src_current_offsets[0][1] = intercept

plot(ch1_1_simi_amps, [y, ch1_1_simi_amps * slope + intercept], ['b.', 'k-'])
xlabel('SI/MI current (A)')
ylabel('Source DAC code')
input('Press enter to continue.')

input('Connect a 1MΩ ± 0.01% resistor between CH1DUT+ and CH1DUT-, connect CH1DUT- to GND, and press enter.')
s.set_current_range(1, 2)
s.set_source_function(1, 'VOLTAGE')
s.set_measure_function(1, 'VOLTAGE')

ch1_2_svmv_vals = zeros(size(z))
s.dev.dac16_set_ch1(int(z[0]))
print('Settling', end = '', flush = True)
for i in range(5):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(z)):
    s.dev.dac16_set_ch1(int(z[i]))
    ch1_2_svmv_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(z[:i], ch1_2_svmv_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MV ADC code')
        draw_now()

plot(z, ch1_2_svmv_vals)
xlabel('Source DAC code')
ylabel('SV/MV ADC code')
input('Press enter to continue.')

s.set_measure_function(1, 'CURRENT')

ch1_2_svmi_vals = zeros(size(z))
s.dev.dac16_set_ch1(int(z[0]))
print('Settling', end = '', flush = True)
for i in range(5):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(z)):
    s.dev.dac16_set_ch1(int(z[i]))
    ch1_2_svmi_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(z[:i], ch1_2_svmi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MI ADC code')
        draw_now()

plot(z, ch1_2_svmi_vals)
xlabel('Source DAC code')
ylabel('SV/MI ADC code')
input('Press enter to continue.')

s.set_source_function(1, 'CURRENT')

ch1_2_simi_vals = zeros(size(y))
s.dev.dac16_set_ch1(int(y[0]))
print('Settling', end = '', flush = True)
for i in range(5):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(y)):
    s.dev.dac16_set_ch1(int(y[i]))
    ch1_2_simi_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(y[:i], ch1_2_simi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SI/MI ADC code')
        draw_now()

plot(y, ch1_2_simi_vals)
xlabel('Source DAC code')
ylabel('SI/MI ADC code')
input('Press enter to continue.')

ch1_2_svmv_volts = s.meas_voltage_gain[0] * (ch1_2_svmv_vals + s.meas_voltage_offset[0])
[first, last, slope, intercept, numpoints] = linefit(ch1_2_svmv_volts, z)
s.src_voltage_gains[0][2] = slope
s.src_voltage_offsets[0][2] = intercept

plot(ch1_2_svmv_volts, [z, ch1_2_svmv_volts * slope + intercept], ['b.', 'k-'])
xlabel('SV/MV voltage (V)')
ylabel('Source DAC code')
input('Press enter to continue.')

ch1_2_svmv_amps = ch1_2_svmv_volts / 1E6
[first, last, slope, intercept, numpoints] = linefit(ch1_2_svmi_vals, ch1_2_svmv_amps)
s.meas_current_gains[0][2] = slope
s.meas_current_offsets[0][2] = intercept / slope

plot(ch1_2_svmi_vals, [ch1_2_svmv_amps, ch1_2_svmi_vals * slope + intercept], ['b.', 'k-'])
xlabel('SV/MI ADC code')
ylabel('SV/MV current (A)')
input('Press enter to continue.')

ch1_2_simi_amps = s.meas_current_gains[0][2] * (ch1_2_simi_vals + s.meas_current_offsets[0][2])
[first, last, slope, intercept, numpoints] = linefit(ch1_2_simi_amps, y)
s.src_current_gains[0][2] = slope
s.src_current_offsets[0][2] = intercept

plot(ch1_2_simi_amps, [y, ch1_2_simi_amps * slope + intercept], ['b.', 'k-'])
xlabel('SI/MI current (A)')
ylabel('Source DAC code')
input('Press enter to continue.')

input('Connect a 10MΩ ± 0.01% resistor between CH1DUT+ and CH1DUT-, connect CH1DUT- to GND, and press enter.')
s.set_current_range(1, 3)
s.set_source_function(1, 'VOLTAGE')
s.set_measure_function(1, 'VOLTAGE')

ch1_3_svmv_vals = zeros(size(x))
s.dev.dac16_set_ch1(int(x[0]))
print('Settling', end = '', flush = True)
for i in range(10):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(x)):
    s.dev.dac16_set_ch1(int(x[i]))
    ch1_3_svmv_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(x[:i], ch1_3_svmv_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MV ADC code')
        draw_now()

plot(x, ch1_3_svmv_vals)
xlabel('Source DAC code')
ylabel('SV/MV ADC code')
input('Press enter to continue.')

s.set_measure_function(1, 'CURRENT')

ch1_3_svmi_vals = zeros(size(x))
s.dev.dac16_set_ch1(int(x[0]))
print('Settling', end = '', flush = True)
for i in range(10):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(x)):
    s.dev.dac16_set_ch1(int(x[i]))
    ch1_3_svmi_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(x[:i], ch1_3_svmi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MI ADC code')
        draw_now()

plot(x, ch1_3_svmi_vals)
xlabel('Source DAC code')
ylabel('SV/MI ADC code')
input('Press enter to continue.')

s.set_source_function(1, 'CURRENT')

ch1_3_simi_vals = zeros(size(y))
s.dev.dac16_set_ch1(int(y[0]))
print('Settling', end = '', flush = True)
for i in range(10):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(y)):
    s.dev.dac16_set_ch1(int(y[i]))
    ch1_3_simi_vals[i] = s.dev.adc18_get_ch1_avg()
    if i > 0:
        plot(y[:i], ch1_3_simi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SI/MI ADC code')
        draw_now()

plot(y, ch1_3_simi_vals)
xlabel('Source DAC code')
ylabel('SI/MI ADC code')
input('Press enter to continue.')

ch1_3_svmv_volts = s.meas_voltage_gain[0] * (ch1_3_svmv_vals + s.meas_voltage_offset[0])
[first, last, slope, intercept, numpoints] = linefit(ch1_3_svmv_volts, x)
s.src_voltage_gains[0][3] = slope
s.src_voltage_offsets[0][3] = intercept

plot(ch1_3_svmv_volts, [x, ch1_3_svmv_volts * slope + intercept], ['b.', 'k-'])
xlabel('SV/MV voltage (V)')
ylabel('Source DAC code')
input('Press enter to continue.')

ch1_3_svmv_amps = ch1_3_svmv_volts / 10e6
[first, last, slope, intercept, numpoints] = linefit(ch1_3_svmi_vals, ch1_3_svmv_amps)
s.meas_current_gains[0][3] = slope
s.meas_current_offsets[0][3] = intercept / slope

plot(ch1_3_svmi_vals, [ch1_3_svmv_amps, ch1_3_svmi_vals * slope + intercept], ['b.', 'k-'])
xlabel('SV/MI ADC code')
ylabel('SV/MV current (A)')
input('Press enter to continue.')

ch1_3_simi_amps = s.meas_current_gains[0][3] * (ch1_3_simi_vals + s.meas_current_offsets[0][3])
[first, last, slope, intercept, numpoints] = linefit(ch1_3_simi_amps, y)
s.src_current_gains[0][3] = slope
s.src_current_offsets[0][3] = intercept

plot(ch1_3_simi_amps, [y, ch1_3_simi_amps * slope + intercept], ['b.', 'k-'])
xlabel('SI/MI current (A)')
ylabel('Source DAC code')
input('Press enter to continue.')

s.set_source_function(1, 'CURRENT')
s.dev.dac16_set_ch1(0)
s.set_measure_function(1, 'VOLTAGE')

s.set_current_range(2, 3)
s.set_source_function(2, 'CURRENT')
s.dev.dac16_set_ch2(0)
s.set_measure_function(2, 'VOLTAGE')

input('Connect CH2DUT+ to VREF and CH2DUT- to GND and press enter.')
ch2refp = s.avg_adc_readings(2)

input('Connect CH2DUT+ to GND and CH2DUT- to VREF and press enter.')
ch2refm = s.avg_adc_readings(2)

s.meas_voltage_gain[1] = 5. / (ch2refp - ch2refm)
s.meas_voltage_offset[1] = -0.5 * (ch2refp + ch2refm)

input('Connect a 1kΩ ± 0.01% resistor between CH2DUT+ and CH2DUT-, connect CH2DUT- to GND, and press enter.')
s.set_current_range(2, 0)
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'VOLTAGE')

ch2_0_svmv_vals = zeros(size(z))
for i in range(len(z)):
    s.dev.dac16_set_ch2(int(z[i]))
    ch2_0_svmv_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(z[:i], ch2_0_svmv_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MV ADC code')
        draw_now()

plot(z, ch2_0_svmv_vals)
xlabel('Source DAC code')
ylabel('SV/MV ADC code')
input('Press enter to continue.')

s.set_measure_function(2, 'CURRENT')

ch2_0_svmi_vals = zeros(size(z))
for i in range(len(z)):
    s.dev.dac16_set_ch2(int(z[i]))
    ch2_0_svmi_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(z[:i], ch2_0_svmi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MI ADC code')
        draw_now()

plot(z, ch2_0_svmi_vals)
xlabel('Source DAC code')
ylabel('SV/MI ADC code')
input('Press enter to continue.')

s.set_source_function(2, 'CURRENT')

ch2_0_simi_vals = zeros(size(y))
for i in range(len(y)):
    s.dev.dac16_set_ch2(int(y[i]))
    ch2_0_simi_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(y[:i], ch2_0_simi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SI/MI ADC code')
        draw_now()

plot(y, ch2_0_simi_vals)
xlabel('Source DAC code')
ylabel('SI/MI ADC code')
input('Press enter to continue.')

ch2_0_svmv_volts = s.meas_voltage_gain[1] * (ch2_0_svmv_vals + s.meas_voltage_offset[1])
[first, last, slope, intercept, numpoints] = linefit(ch2_0_svmv_volts, z)
s.src_voltage_gains[1][0] = slope
s.src_voltage_offsets[1][0] = intercept

plot(ch2_0_svmv_volts, [z, ch2_0_svmv_volts * slope + intercept], ['b.', 'k-'])
xlabel('SV/MV voltage (V)')
ylabel('Source DAC code')
input('Press enter to continue.')

ch2_0_svmv_amps = ch2_0_svmv_volts / 1E3
[first, last, slope, intercept, numpoints] = linefit(ch2_0_svmi_vals, ch2_0_svmv_amps)
s.meas_current_gains[1][0] = slope
s.meas_current_offsets[1][0] = intercept / slope

plot(ch2_0_svmi_vals, [ch2_0_svmv_amps, ch2_0_svmi_vals * slope + intercept], ['b.', 'k-'])
xlabel('SV/MI ADC code')
ylabel('SV/MV current (A)')
input('Press enter to continue.')

ch2_0_simi_amps = s.meas_current_gains[1][0] * (ch2_0_simi_vals + s.meas_current_offsets[1][0])
[first, last, slope, intercept, numpoints] = linefit(ch2_0_simi_amps, y)
s.src_current_gains[1][0] = slope
s.src_current_offsets[1][0] = intercept

plot(ch2_0_simi_amps, [y, ch2_0_simi_amps * slope + intercept], ['b.', 'k-'])
xlabel('SI/MI current (A)')
ylabel('Source DAC code')
input('Press enter to continue.')

input('Connect a 10kΩ ± 0.01% resistor between CH2DUT+ and CH2DUT-, connect CH2DUT- to GND, and press enter.')
s.set_current_range(2, 1)
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'VOLTAGE')

ch2_1_svmv_vals = zeros(size(x))
for i in range(len(x)):
    s.dev.dac16_set_ch2(int(x[i]))
    ch2_1_svmv_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(x[:i], ch2_1_svmv_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MV ADC code')
        draw_now()

plot(x, ch2_1_svmv_vals)
xlabel('Source DAC code')
ylabel('SV/MV ADC code')
input('Press enter to continue.')

s.set_measure_function(2, 'CURRENT')

ch2_1_svmi_vals = zeros(size(x))
for i in range(len(x)):
    s.dev.dac16_set_ch2(int(x[i]))
    ch2_1_svmi_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(x[:i], ch2_1_svmi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MI ADC code')
        draw_now()

plot(x, ch2_1_svmi_vals)
xlabel('Source DAC code')
ylabel('SV/MI ADC code')
input('Press enter to continue.')

s.set_source_function(2, 'CURRENT')

ch2_1_simi_vals = zeros(size(y))
for i in range(len(y)):
    s.dev.dac16_set_ch2(int(y[i]))
    ch2_1_simi_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(y[:i], ch2_1_simi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SI/MI ADC code')
        draw_now()

plot(y, ch2_1_simi_vals)
xlabel('Source DAC code')
ylabel('SI/MI ADC code')
input('Press enter to continue.')

ch2_1_svmv_volts = s.meas_voltage_gain[1] * (ch2_1_svmv_vals + s.meas_voltage_offset[1])
[first, last, slope, intercept, numpoints] = linefit(ch2_1_svmv_volts, x)
s.src_voltage_gains[1][1] = slope
s.src_voltage_offsets[1][1] = intercept

plot(ch2_1_svmv_volts, [x, ch2_1_svmv_volts * slope + intercept], ['b.', 'k-'])
xlabel('SV/MV voltage (V)')
ylabel('Source DAC code')
input('Press enter to continue.')

ch2_1_svmv_amps = ch2_1_svmv_volts / 10E3
[first, last, slope, intercept, numpoints] = linefit(ch2_1_svmi_vals, ch2_1_svmv_amps)
s.meas_current_gains[1][1] = slope
s.meas_current_offsets[1][1] = intercept / slope

plot(ch2_1_svmi_vals, [ch2_1_svmv_amps, ch2_1_svmi_vals * slope + intercept], ['b.', 'k-'])
xlabel('SV/MI ADC code')
ylabel('SV/MV current (A)')
input('Press enter to continue.')

ch2_1_simi_amps = s.meas_current_gains[1][1] * (ch2_1_simi_vals + s.meas_current_offsets[1][1])
[first, last, slope, intercept, numpoints] = linefit(ch2_1_simi_amps, y)
s.src_current_gains[1][1] = slope
s.src_current_offsets[1][1] = intercept

plot(ch2_1_simi_amps, [y, ch2_1_simi_amps * slope + intercept], ['b.', 'k-'])
xlabel('SI/MI current (A)')
ylabel('Source DAC code')
input('Press enter to continue.')

input('Connect a 1MΩ ± 0.01% resistor between CH2DUT+ and CH2DUT-, connect CH2DUT- to GND, and press enter.')
s.set_current_range(2, 2)
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'VOLTAGE')

ch2_2_svmv_vals = zeros(size(z))
s.dev.dac16_set_ch2(int(z[0]))
print('Settling', end = '', flush = True)
for i in range(5):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(z)):
    s.dev.dac16_set_ch2(int(z[i]))
    ch2_2_svmv_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(z[:i], ch2_2_svmv_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MV ADC code')
        draw_now()

plot(z, ch2_2_svmv_vals)
xlabel('Source DAC code')
ylabel('SV/MV ADC code')
input('Press enter to continue.')

s.set_measure_function(2, 'CURRENT')

ch2_2_svmi_vals = zeros(size(z))
s.dev.dac16_set_ch2(int(z[0]))
print('Settling', end = '', flush = True)
for i in range(5):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(z)):
    s.dev.dac16_set_ch2(int(z[i]))
    ch2_2_svmi_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(z[:i], ch2_2_svmi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MI ADC code')
        draw_now()

plot(z, ch2_2_svmi_vals)
xlabel('Source DAC code')
ylabel('SV/MI ADC code')
input('Press enter to continue.')

s.set_source_function(2, 'CURRENT')

ch2_2_simi_vals = zeros(size(y))
s.dev.dac16_set_ch2(int(y[0]))
print('Settling', end = '', flush = True)
for i in range(5):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(y)):
    s.dev.dac16_set_ch2(int(y[i]))
    ch2_2_simi_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(y[:i], ch2_2_simi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SI/MI ADC code')
        draw_now()

plot(y, ch2_2_simi_vals)
xlabel('Source DAC code')
ylabel('SI/MI ADC code')
input('Press enter to continue.')

ch2_2_svmv_volts = s.meas_voltage_gain[1] * (ch2_2_svmv_vals + s.meas_voltage_offset[1])
[first, last, slope, intercept, numpoints] = linefit(ch2_2_svmv_volts, z)
s.src_voltage_gains[1][2] = slope
s.src_voltage_offsets[1][2] = intercept

plot(ch2_2_svmv_volts, [z, ch2_2_svmv_volts * slope + intercept], ['b.', 'k-'])
xlabel('SV/MV voltage (V)')
ylabel('Source DAC code')
input('Press enter to continue.')

ch2_2_svmv_amps = ch2_2_svmv_volts / 1E6
[first, last, slope, intercept, numpoints] = linefit(ch2_2_svmi_vals, ch2_2_svmv_amps)
s.meas_current_gains[1][2] = slope
s.meas_current_offsets[1][2] = intercept / slope

plot(ch2_2_svmi_vals, [ch2_2_svmv_amps, ch2_2_svmi_vals * slope + intercept], ['b.', 'k-'])
xlabel('SV/MI ADC code')
ylabel('SV/MV current (A)')
input('Press enter to continue.')

ch2_2_simi_amps = s.meas_current_gains[1][2] * (ch2_2_simi_vals + s.meas_current_offsets[1][2])
[first, last, slope, intercept, numpoints] = linefit(ch2_2_simi_amps, y)
s.src_current_gains[1][2] = slope
s.src_current_offsets[1][2] = intercept

plot(ch2_2_simi_amps, [y, ch2_2_simi_amps * slope + intercept], ['b.', 'k-'])
xlabel('SI/MI current (A)')
ylabel('Source DAC code')
input('Press enter to continue.')

input('Connect a 10MΩ ± 0.01% resistor between CH2DUT+ and CH2DUT-, connect CH2DUT- to GND, and press enter.')
s.set_current_range(2, 3)
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'VOLTAGE')

ch2_3_svmv_vals = zeros(size(x))
s.dev.dac16_set_ch2(int(x[0]))
print('Settling', end = '', flush = True)
for i in range(10):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(x)):
    s.dev.dac16_set_ch2(int(x[i]))
    ch2_3_svmv_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(x[:i], ch2_3_svmv_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MV ADC code')
        draw_now()

plot(x, ch2_3_svmv_vals)
xlabel('Source DAC code')
ylabel('SV/MV ADC code')
input('Press enter to continue.')

s.set_measure_function(2, 'CURRENT')

ch2_3_svmi_vals = zeros(size(x))
s.dev.dac16_set_ch2(int(x[0]))
print('Settling', end = '', flush = True)
for i in range(10):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(x)):
    s.dev.dac16_set_ch2(int(x[i]))
    ch2_3_svmi_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(x[:i], ch2_3_svmi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SV/MI ADC code')
        draw_now()

plot(x, ch2_3_svmi_vals)
xlabel('Source DAC code')
ylabel('SV/MI ADC code')
input('Press enter to continue.')

s.set_source_function(2, 'CURRENT')

ch2_3_simi_vals = zeros(size(y))
s.dev.dac16_set_ch2(int(y[0]))
print('Settling', end = '', flush = True)
for i in range(10):
    print('.', end = '', flush = True)
    time.sleep(1)
print('')

for i in range(len(y)):
    s.dev.dac16_set_ch2(int(y[i]))
    ch2_3_simi_vals[i] = s.dev.adc18_get_ch2_avg()
    if i > 0:
        plot(y[:i], ch2_3_simi_vals[:i])
        xlabel('Source DAC code')
        ylabel('SI/MI ADC code')
        draw_now()

plot(y, ch2_3_simi_vals)
xlabel('Source DAC code')
ylabel('SI/MI ADC code')
input('Press enter to continue.')

ch2_3_svmv_volts = s.meas_voltage_gain[1] * (ch2_3_svmv_vals + s.meas_voltage_offset[1])
[first, last, slope, intercept, numpoints] = linefit(ch2_3_svmv_volts, x)
s.src_voltage_gains[1][3] = slope
s.src_voltage_offsets[1][3] = intercept

plot(ch2_3_svmv_volts, [x, ch2_3_svmv_volts * slope + intercept], ['b.', 'k-'])
xlabel('SV/MV voltage (V)')
ylabel('Source DAC code')
input('Press enter to continue.')

ch2_3_svmv_amps = ch2_3_svmv_volts / 10E6
[first, last, slope, intercept, numpoints] = linefit(ch2_3_svmi_vals, ch2_3_svmv_amps)
s.meas_current_gains[1][3] = slope
s.meas_current_offsets[1][3] = intercept / slope

plot(ch2_3_svmi_vals, [ch2_3_svmv_amps, ch2_3_svmi_vals * slope + intercept], ['b.', 'k-'])
xlabel('SV/MI ADC code')
ylabel('SV/MV current (A)')
input('Press enter to continue.')

ch2_3_simi_amps = s.meas_current_gains[1][3] * (ch2_3_simi_vals + s.meas_current_offsets[1][3])
[first, last, slope, intercept, numpoints] = linefit(ch2_3_simi_amps, y)
s.src_current_gains[1][3] = slope
s.src_current_offsets[1][3] = intercept

plot(ch2_3_simi_amps, [y, ch2_3_simi_amps * slope + intercept], ['b.', 'k-'])
xlabel('SI/MI current (A)')
ylabel('Source DAC code')
input('Press enter to continue.')

s.set_source_function(2, 'CURRENT')
s.dev.dac16_set_ch2(0)
s.set_measure_function(2, 'VOLTAGE')
