
s.set_source_function(1, 'VOLTAGE')
s.set_measure_function(1, 'CURRENT')

vg = concatenate((arange(0.2, 0.9, 0.01), arange(0.9, 1.2, 0.02), arange(1.2, 3.04, 0.04)))[::-1]
isat = zeros(size(vg))

for i in range(len(vg)):
    s.source_voltage(1, vg[i])
    s.autorange_once(1)
    s.source_voltage(1, vg[i])
    isat[i] = s.measure_current(1)

semilogy(vg, isat)
xlabel('Vg (V)')
ylabel('Isat (A)')

