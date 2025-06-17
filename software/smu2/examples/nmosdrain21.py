
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'CURRENT')
s.set_source_function(1, 'CURRENT')
s.set_measure_function(1, 'VOLTAGE')

vd = concatenate((arange(0, 0.01, 0.001), arange(0.01, 0.1, 0.01), arange(0.1, 0.4, 0.02), arange(0.4, 3.05, 0.05)))[::-1]
isat = logspace(-10, -3, 15)[::-1]
vg = zeros(size(isat))
id_ = []

for i in range(len(isat)):
    s.source_current(1, isat[i])
    vg[i] = s.measure_voltage(1)
    currents = zeros(size(vd))
    for j in range(len(vd)):
        s.source_voltage(2, vd[j])
        s.autorange_once(2)
        s.source_voltage(2, vd[j])
        currents[j] = s.measure_current(2)
        if j > 0:
            plot(vd[0:j], currents[0:j])
            xlabel('Vd (V)')
            ylabel('Id (A)')
            ylabel(f'Isat = {isat[i]:.3E}A, Vg = {vg[i]:.3f}V', yaxis = 'right')
            draw_now()
    id_.append(currents)

semilogy(vd, id_)
xlabel('Vd (V)')
ylabel('Id (A)')

