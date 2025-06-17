
s.set_source_function(1, 'VOLTAGE')
s.set_measure_function(1, 'CURRENT')
s.set_source_function(2, 'VOLTAGE')
s.set_measure_function(2, 'CURRENT')

vb = arange(0.25, 0.705, 0.005)[::-1]
ib = zeros(size(vb))
ic = zeros(size(vb))

for i in range(len(vb)):
    s.source_voltage(1, vb[i])
    s.autorange_once(1)
    s.source_voltage(2, vb[i])
    s.autorange_once(2)
    s.source_voltage(1, vb[i])
    s.source_voltage(2, vb[i])

    ib[i] = s.measure_current(1)
    ic[i] = s.measure_current(2)
    if i > 0:
        semilogy(vb[:i], [ib[:i], ic[:i]])
        xlabel('Vb (V)')
        ylabel('Ib, Ic (A)')
        draw_now()

semilogy(vb[:i], [ib[:i], ic[:i]])
xlabel('Vb (V)')
ylabel('Ib, Ic (A)')
