import copy

class Model:
  def __init__(self, n, U, w_data, b_data):
    self.w_data = w_data
    self.b_data = b_data
    self.n = n
    self.U = U

    self.check_validity()

  def check_validity(self):
    """
      Verify that data stored expose only valid values
    """
    if not self.is_valid():
      raise NotValidModelError()

  def is_valid(self):
    return self.n >= 0 and self.U >= 0 and \
           self._is_valid_w() and self._is_valid_b()


  def copy(self):
    return copy.copy(self)

  def set_all_b(self, new_b_val):
    self.b_data = [new_b_val for x in self.b_data]

  def remove_U(self):
    if self.U <= 1:
      raise NotValidModelError("Invalid value of U")

    self.U -= 1
    self.b_data = self.b_data[:-1]

    # remove last row (which refers to the last depot) and last column
    self.w_data = [x[:-1] for x in self.w_data][:-1]

    self.check_validity()

  def _is_valid_w(self):
    if len(self.w_data) != self.n+self.U:
      return False

    for w_arr in self.w_data:
      if len(w_arr) != self.n+self.U:
        return False

      for w_elem in w_arr:
        if w_elem < 0.0:
          return False

    return True

  def _is_valid_b(self):
    if len(self.b_data) != self.U:
      return False

    for b_val in self.b_data:
      if b_val < 0.0:
        return False

    return True



class NotValidModelError(Exception):
  pass
