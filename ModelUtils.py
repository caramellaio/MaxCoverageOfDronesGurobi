import Model

def create_random_model_file():
  """ generate a random model inside file `path`

      If file already exists try to override it.

      This function returns True if the model was succesfully written to the
      file
  """
  pass


def create_random_model(bounds):
  """ Construct a new model using random values

      It is possible to force bounds over values.
      The structure of `bounds` has not been decided yet.

      Returns the new model
  """
  pass

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
  except IOError:
    print("IOError during model reading...\n")
    exit(1)

  return res_model


def _read_model(f):
  line = f.readline(',')

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

  for i in range(n):
    w_line_full = f.readline()
    w_line = w_line_full.split(',')

    if (len(w_line) != n + u):
      raise ReadModelStructureError("""expected %d fields in the line %s
                                    but %d are given"""
                                    % (n + u, w_line_full, len(w_line)))

    float_w_line = None

    try:
      float_w_line = float(x) for x in w_line
    except ValueError:
      raise ReadModelStructureError("Line %s has wrong type" % w_line_full)

    w_data.append(float_w_line)


  assert(len(w_data == n));

  _log("W matrix readed: %s\n" % str(w_data))

  b_data_str = f.readline().split(',')

  if len(b_data_str != u):
    raise ReadModelStructureError("""Expected %d fields in the line %s
                                   but %d are given""" %
                                   (u, ','.join(b_data_str), len(b_data_str)))

  try:
    b_data = float(x) for x in b_data_str
  except ValueError:
    raise ReadModelStructureError("Line %s has wrong type" % ','.join(b_data_str))

  return Model(n=n, u=u, w_data=w_data, b_data=b_data)

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
