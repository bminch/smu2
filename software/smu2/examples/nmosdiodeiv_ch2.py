
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'CURRENT')

vg = concatenate((arange(0.2, 0.9, 0.01), arange(0.9, 1.2, 0.02), arange(1.2, 3.04, 0.04)))[::-1]
isat = zeros(size(vg))

for i in range(len(vg)):
    s.source_voltage(2, vg[i])
    s.autorange_once(2)
    s.source_voltage(2, vg[i])
    isat[i] = s.measure_current(2)

semilogy(vg, isat)
xlabel('Vg (V)')
ylabel('Isat (A)')

