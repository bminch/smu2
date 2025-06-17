
s.set_source_function(1, 'CURRENT')
s.set_measure_function(1, 'VOLTAGE')
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'CURRENT')
s.source_voltage(2, 0)

iin = linspace(-100e-6, 100e-6, 101)
iout = zeros(size(iin))

for i in range(len(iin)):
    s.source_current(1, iin[i])
    s.autorange_once(2)
    s.source_voltage(2, 0)
    iout[i] = s.measure_current(2)
    if i > 0:
        plot(iin[:i], iout[:i])
        xlabel('Iin (A)')
        ylabel('Iout (A)')
        draw_now()

plot(iin, iout)
xlabel('Iin (A)')
ylabel('Iout (A)')

