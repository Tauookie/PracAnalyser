import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import re
import traceback
from random import randint


class Prac:
  def __init__(self, file, debug=False):
    self.data = None
    self.variables = None
    self.dimensions = None
    self.variablesDict = None
    self.x = None
    self.y = None
    self.xName = None
    self.yName = None
    self.dataFile = None
    self.debug = debug

    self.set_file_name(file)
    self.read_from_txt()


  def set_file_name(self, file):
    if file.endswith('.txt'):
      self.dataFile = file
    else:
      self.dataFile = file + ".txt"


  def read_from_txt(self):
    with open(self.dataFile, 'r', encoding="UTF-8") as f:
      rData = f.readlines()
      self.data = {}
      variables = self.get_variables(rData[0])

      rawData = [[] for v in variables]
      for i in rData[1:]:
        lineData = re.findall(r'\d*\.?\d+', i)
        for j in range(0, len(lineData)):
          rawData[j].append(float(lineData[j]))

      for v in variables:
        self.data[v] = np.array(rawData[variables.index(v)])

      self.log(self.data)


  def get_variables(self, line='user_use'):
    if line == 'user_use':
      return self.variables

    try:
      line = re.split(r'\s+', line)
      varList = []
      varDict = {}
      dimList = []

      i = 0
      while i < len(line)-1:
        if line[i] == ',':
          var, dim = line[i-1], line[i+1]
          i += 1
        elif line[i].endswith(','):
          var, dim = line[i][:-1], line[i+1]
          i += 1
        elif ',' in line[i]:
          var, dim = line[i].split(',')[0], line[i].split(',')[1]
        else:
          var, dim = line[i], None

        varDict[var] = sp.symbols(var)
        varList.append(var)
        dimList.append(dim)
        i += 1

      self.variables = varList
      self.variablesDict = varDict
      self.dimensions = dimList
      self.log(f'Successfully loaded variables {varList} with dimensions {dimList}.')
      return varList

    except Exception:
      raise Exception('File {self.dataFile} is corrupted.')


  def set_axis(self, axis, expr):
    axisData = self.get_axis_by_expr(expr)

    if axis in ['x', 'X']:
      self.x = axisData
      self.xName = expr
      self.log(f'Updated axis x: {self.xName} = {self.x}')
    elif axis in ['y', 'Y']:
      self.y = axisData
      self.yName = expr
      self.log(f'Updated axis y: {self.yName} = {self.y}')
    else:
      raise Exception('There is no that axis')


  def get_axis_by_expr(self, expr):
    try:
      expr = sp.parse_expr(expr, self.variablesDict)
    except SyntaxError:
      raise Exception('Axis expression is invalid.')
    symbols = list(expr.free_symbols)
    if not set([str(s) for s in symbols]).issubset(set(self.variables)):
      raise Exception('Axis expression contain invalid variables.')

    func = sp.lambdify(symbols, expr)

    return func(*[self.data[str(s)] for s in symbols])


  def approximate(self, plot=False, start=None, end=None):
    x, y = self.filter_axis(start, end)

    k, b = np.polyfit(x, y, 1)
    if plot:
      self.approximated_plot_chart(x, k, b)

    return float(k), float(b)


  def plot_chart(self):
      if self.x and self.y:
        plt.figure(randint(1, 10**6))
        plt.plot(self.x, self.y, marker='o')
        plt.title(f"Dependence of {self.yName} on {self.xName}")
        plt.grid()


  def approximated_plot_chart(self, x, k, b):
    f = k * x + b
    plt.figure(randint(1, 10**6))
    plt.plot(x, f)
    plt.scatter(self.x, self.y, color='black')


  @staticmethod
  def show():
    plt.show()


  def filter_axis(self, start, end):
    if not start and not end:
      return self.x, self.y
    elif start and not end:
        mask = self.x > start
    elif not start and end:
        mask = self.x < end
    else:
        mask = (start < self.x) & (self.x < end)
    return self.x[mask], self.y[mask]


  def log(self, text):
    if self.debug:
      stack = traceback.extract_stack()[-2]
      filename = stack.filename.split("\\")[-1]
      print(f'\033[1m{filename}, line {stack.lineno}, in {stack.name}():\033[0m {text}')


if __name__ == '__main__':
  pass
