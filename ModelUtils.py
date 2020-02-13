from Model import Model
import random

DEF_BOUNDS = {'n' : (5,5), 'U' : (1,2), 'w' : (0.1, 9.55), 'b' : (15.3, 54.4)}

def create_random_model_file(bounds, out_file):
  """ generate a random model inside file `path`

      If file already exists try to override it.

      This function returns True if the model was succesfully written to the
      file
  """
  m = create_random_model(bounds)
  write_model_to_file(m, out_file)


def create_random_model(bounds):
  """ Construct a new model using random values

      It is possible to force bounds over values.
      The structure of `bounds` has not been decided yet.

      Returns the new model
  """

  n = _choose_random(bound_tuple=bounds["n"])
  U = _choose_random(bound_tuple=bounds["U"])
  w_data = _choose_random(bound_tuple=bounds["w"], is_int=False,
                          dim_x=(U+n), dim_y=(U+n))
  b_data = _choose_random(bound_tuple=bounds["b"], is_int=False, dim_x=U)

  return Model(n=n, U=U, w_data=w_data, b_data=b_data)

def _choose_random(bound_tuple, is_int=True, dim_x=0, dim_y=0):
  """ Return a random value in a given range

      If is int use normal random function, otherwise uses unif function
  """
  # < 0 is always invalid
  assert(dim_x >= 0 and dim_y >= 0)

  lb, ub = bound_tuple

  assert(ub >= lb)

  if dim_x == 0 and dim_y == 0:
    # randrange throws an exception if lb == ub.
    if lb == ub:
      return lb
    return random.randrange(lb, ub) if is_int else random.uniform(lb, ub)

  # if we consider an array dim_x > 0
  assert(dim_x > 0)

  outer_array = []

  for i in range(dim_x):
    inner_val = _choose_random(bound_tuple, is_int) if dim_y == 0 else []
    for j in range(dim_y):
      cell_val = 0 if i == j else _choose_random(bound_tuple, is_int)
      inner_val.append(cell_val)

    outer_array.append(inner_val)

  return outer_array

def write_model_to_file(model, out_file):
  """ Write a model specification inside the file `out_file`
      Raises IOError if an IO problem occur.
      Raises InvalidModelError if the model is not valid
  """

  model.check_validity()
  n = model.n
  U = model.U

  b_data = model.b_data
  w_data = model.w_data

  with open(out_file, "w") as out_f:
    out_f.write("%d,%d\n" % (U, n))

    for line in w_data:
      str_line = ','.join([str(field) for field in line])
      out_f.write("%s\n" % str_line)

    str_b_data = ','.join([str(b_ith) for b_ith in b_data])

    out_f.write("%s\n" % str_b_data)

  _log("Model succesfully written to file %s" % out_file)

def create_models_incrementally(count, bound_param, incr_val):
  """ Generate a list of models increasing bound_param by incr_val

      bound_param MUST be a parameter of type `int`
  """
  pass

def read_model_file(file_path):
  """ Read a model from a model files

      Return the model equivalent to the one described inside the file

      If an IOError is raised returns `None`
  """

  res_model = None

  try:
    with open(file_path, "r") as f_read:
      res_model = _read_model(f_read)
      _log("Model succesfully created from file %s" % file_path)
  except IOError:
    _log("IOError during model reading...\n")
    exit(1)

  return res_model


def _read_model(f):
  line = f.readline().split(',')

  if len(line) != 2:
    raise ReadModelStructureError("line %s not wellformed" % ",".join(line))

  try:
    u = int(line[0])
  except ValueError:
    raise ReadModelStructureError("u parameter %s has wrong type" % line[0])

  _log("u readed %d\n" % u)
  try:
    n = int(line[1])
  except ValueError:
    raise ReadModelStructureError("n parameter %s has wrong type" % line[1])

  _log("n readed %d\n" % n)
  w_data = []

  # quadratic matrix n+u X n+u
  for i in range(n + u):
    w_line_full = f.readline()
    w_line = w_line_full.split(',')

    if (len(w_line) != n + u):
      raise ReadModelStructureError("""expected %d fields in the line %s
                                    but %d are given"""
                                    % (n + u, w_line_full, len(w_line)))

    float_w_line = None

    try:
      float_w_line = [float(x) for x in w_line]
    except ValueError:
      raise ReadModelStructureError("Line %s has wrong type" % w_line_full)

    w_data.append(float_w_line)


  assert(len(w_data) == n+u);

  _log("W matrix readed: %s\n" % str(w_data))

  # array with cardinality u
  b_data_str = f.readline().split(',')

  if len(b_data_str) != u:
    raise ReadModelStructureError("""Expected %d fields in the line %s
                                   but %d are given""" %
                                   (u, ','.join(b_data_str), len(b_data_str)))

  try:
    b_data = [float(x) for x in b_data_str]
  except ValueError:
    raise ReadModelStructureError("Line %s has wrong type" % ','.join(b_data_str))


  _log("B array readed: %s\n" % str(b_data))

  return Model(n=n, U=u, w_data=w_data, b_data=b_data)

#TODO: Add a real logging function
def _log(message):
  print(message)

#TODO: Use this class in a more structured way:
#      e.g. instead of printing messages directly from raise use some sort of
#           error type + data information
class ReadModelStructureError(Exception):
  """
    Custom exception for model errors
  """
  pass


if __name__ == "__main__":
  #import argparse
  import os

  #parser = argparse.ArgumentParser()
  #parser.add_argument('-o', '--out-file', type=str, required=True)

  #options = parser.parse_args()

  create_random_model_file(DEF_BOUNDS, "example_rand.txt")
  m = read_model_file("example_rand.txt")
  os.remove("example_rand.txt")
