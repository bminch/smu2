
s.set_source_function(2, 'CURRENT')
s.set_measure_function(2, 'VOLTAGE')

currents = logspace(-10, -3, 99)[::-1]
voltages = zeros(size(currents))

for i in range(len(currents)):
    s.source_current(2, currents[i])
    voltages[i] = s.measure_voltage(2)
    if i > 0:
        semilogx(currents[:i], voltages[:i])
        xlabel('Current (A)')
        ylabel('Voltage (V)')
        draw_now()

semilogx(currents, voltages)
xlabel('Current (A)')
ylabel('Voltage (V)')

