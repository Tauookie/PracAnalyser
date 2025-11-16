from prac import Prac
import math


pr = Prac('data/data1.txt', True)

pr.set_axis('x', 't')
pr.set_axis('y', 'ln(V)')
pr.plot_chart()
print(pr.approximate(True, start=20, end=30))
pr.show()

