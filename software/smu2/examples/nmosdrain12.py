
s.set_source_function(1, 'VOLTAGE')
s.set_measure_function(1, 'CURRENT')
s.set_source_function(2, 'CURRENT')
s.set_measure_function(2, 'VOLTAGE')

vd = concatenate((arange(0, 0.01, 0.001), arange(0.01, 0.1, 0.01), arange(0.1, 0.4, 0.02), arange(0.4, 3.05, 0.05)))[::-1]
isat = logspace(-10, -3, 15)[::-1]
vg = zeros(size(isat))
id_ = []

for i in range(len(isat)):
    s.source_current(2, isat[i])
    vg[i] = s.measure_voltage(2)
    currents = zeros(size(vd))
    for j in range(len(vd)):
        s.source_voltage(1, vd[j])
        s.autorange_once(1)
        s.source_voltage(1, vd[j])
        currents[j] = s.measure_current(1)
    id_.append(currents)

semilogy(vd, id_)
xlabel('Vd (V)')
ylabel('Id (A)')

