from prac import Prac
from analyzer import Analyzer

class VAC(Prac):
  def __init__(self, file, x_expr='I', y_expr='U', debug=False):
    super().__init__(file, debug)
    self.set_axis('x', x_expr)
    self.set_axis('y', y_expr)
    self.analyzer = Analyzer(self.x, self.y, debug)


  def R(self, start, end):
    return self.approximate(False, start, end)


if __name__ == '__main__':
    pass
