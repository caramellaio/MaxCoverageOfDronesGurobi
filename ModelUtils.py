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
  pass
