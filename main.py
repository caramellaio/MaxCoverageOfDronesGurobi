""" Script file to run gurobi over increasing size problems

"""

import argparse
import os
from ModelUtils import write_model_to_file, create_models_incrementally
from MaxCov import solve_model
from plot import plot

MODEL_NAME = "model"
ACCEPTED_PARAMS = ["b", "U"]

def _check_param_correctness(options):
  """ Internal function to verify the validity of the options

      * ensure that 'incremental_param' is either b or U
      * ensure that all numerical parameters are positive
      * Warn user if `growth_val` has decimals and param is U
      * Warn user if `starting_val` has decimals and param is U
  """
  if not options.incremental_param in ACCEPTED_PARAMS:
    _error("Invalid option `--incremental-param`")

  if options.starting_val < 0:
    _error("Starting val must be > 0")

  if options.growth_val < 0:
    _error("Growth val must be > 0")

  if options.growth_val == 0:
    _warning("Growth val = 0. This script will generate the same model many times!")

  if options.times <= 0:
    _error("times option must be > 0")

  if "U" == options.incremental_param:
    int_starting_val = int(options.starting_val)
    int_growth_val = int(options.growth_val)

    if float(int_growth_val) != options.growth_val:
      _warning("Growth_val is not an integer value. New Growth_val = %d" \
               % int_growth_val)


    if float(int_starting_val) != options.starting_val:
      _warning("Starting_val is not an integer value. New Starting_val = %d" \
               % int_starting_val)


    # we need to parse the parameters to int if "U" is considered
    options.growth_val = int_growth_val
    options.starting_val = int_starting_val

def _process_output_folder(out_folder):
  """ Process output folder parameter

      * If the path is a file, print an error
      * If the folder does not exists, create it
      * If the folder is not empty, prints a warning

      If a generic IO error occur this function will raise an IOError
  """
  if os.path.isfile(out_folder):
    _error("%s is a file" % out_folder)

  if not os.path.exists(out_folder):
    _warning("%s folder does not exist. Creating it" % out_folder)
    os.mkdir(out_folder)
  else:
    assert(os.path.isdir(out_folder))

    files = os.listdir(out_folder)

    if len(files) > 0:
      _warning("%s folder is not empty." % out_folder)

def _warning(msg):
  print("Warning: %s\n" % msg)

def _error(msg):
  print("Error: %s\n" % msg)
  exit(1)

def _gen_options():
  parser = argparse.ArgumentParser()

  parser.add_argument('-o', '--out-folder', type=str, required=True,
                      help="output directory where data is saved")
  parser.add_argument('-p', '--incremental-param', type=str, required=True,
                      help="parameter to increment. Can be either: b|U")
  parser.add_argument('-t', '--times', type=int, required=True,
                      help="Number of incremental verifications")
  parser.add_argument('-s', '--starting-val', type=float, required=True,
                      help="Initial starting value for parameter")
  parser.add_argument('-g', '--growth-val', type=float, required=True,
                      help="Value to increment in each step")

  return parser.parse_args()

if __name__ == "__main__":
  options = _gen_options()

  _check_param_correctness(options)

  models = create_models_incrementally(bound_param=options.incremental_param,
                                       start=options.starting_val,
                                       incr_val=options.growth_val,
                                       times=options.times)

  _process_output_folder(options.out_folder)

  plt_data = []

  for m in models:
    model_name = "%s_%d_%d.txt" % (MODEL_NAME, m.U, m.n)

    model_file_path = os.path.join(options.out_folder, model_name)
    res = solve_model(n=m.n, U=m.U, w=m.w_data, b_data = m.b_data)
    print(res)
    write_model_to_file(m, model_file_path)

    param_val = sum(m.b_data) if "b" == options.incremental_param else m.U
    plt_data.append((param_val, res["obj_val"]))


  img_file = os.path.join(options.out_folder, "plot.png")
  plot(values=plt_data,
       x_axis_name="param value",
       y_axis_name="objective value",
       title="MaxCov analysis",
       out_file=img_file)

  print("Plot written to file %s" % img_file)
