from vac import VAC

vc = VAC('data/vac.txt')
vc.plot_chart()
vc.analyzer.get_derivatives()
print(vc.analyzer.is_there_diode())
vc.show()