
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'CURRENT')

voltages = arange(0.25, 0.705, 0.005)[::-1]
currents = zeros(size(voltages))

for i in range(len(voltages)):
    s.source_voltage(2, voltages[i])
    s.autorange_once(2)
    s.source_voltage(2, voltages[i])
    currents[i] = s.measure_current(2)
    if i > 0:
        semilogy(voltages[:i], currents[:i])
        xlabel('Voltage (V)')
        ylabel('Current (A)')
        draw_now()

semilogy(voltages, currents)
xlabel('Voltage (V)')
ylabel('Current (A)')

