import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def plot(values, x_axis_name, y_axis_name, title, out_file):


  fig, ax = plt.subplots()

  print(values)
  x = np.array([l[0] for l in values])
  y = np.array([int(l[1]) for l in values])

  ax.scatter(x, y, color='r', label="objective")

  ax.grid()


  print(x)
  print(y)
  ax.set_xlabel(x_axis_name)
  ax.set_ylabel(y_axis_name)
  ax.set_title(y_axis_name)
  ax.legend(loc="upper left")

  fig.savefig(out_file)
  plt.show()

if __name__ == "__main__":
  plot([[0, 0.0], [1, 2.0], [5, 0]], "foo", "bar","barfoo", "barfoo.png")
