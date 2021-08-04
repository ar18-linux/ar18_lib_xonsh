#! /usr/bin/env xonsh
# ar18 Script version 2021-08-04_07:58:18
# Function template version 2021-08-03_00:24:44

try:
  assert ar18.script.read_targets
except:
##############################FUNCTION_START#################################

  def temp_func():
    file_path = f"/home/{$AR18_USER_NAME}/.config/ar18/INSTALLED_TARGETS"
    if not os.path.exists(file_path):
      file_path = None
    ret = Ar18.Struct(file_path)

    return ret

###############################FUNCTION_END##################################
  ar18.script.read_targets = temp_func
