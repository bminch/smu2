
s.set_source_function(1, 'VOLTAGE')
s.set_measure_function(1, 'CURRENT')
s.set_source_function(2, 'CURRENT')
s.set_measure_function(2, 'VOLTAGE')
s.source_current(2, 0)

vin = linspace(-1, 1, 101)
vout = zeros(size(vin))

for i in range(len(vin)):
    s.source_voltage(1, vin[i])
    s.autorange_once(1)
    s.source_voltage(1, vin[i])
    vout[i] = s.measure_voltage(2)
    if i > 0:
        plot(vin[:i], vout[:i])
        xlabel('Vin (V)')
        ylabel('Vout (V)')
        draw_now()

plot(vin, vout)
xlabel('Vin (V)')
ylabel('Vout (V)')

