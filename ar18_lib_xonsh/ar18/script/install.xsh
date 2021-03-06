#! /usr/bin/env xonsh
# ar18 Script version 2021-08-05_08:58:53
# Function template version 2021-08-03_00:24:44

try:
  assert ar18.script.install
except:
##############################FUNCTION_START#################################
  def temp_func(install_dir:str, module_name:str, script_dir:str, user_name:str, deployment_target:str=""):
    ar18.script.include("sudo.ask_pass")
    ar18.sudo.ask_pass()

    ar18.script.include("sudo.exec_as")
    ar18.sudo.exec_as(f"mkdir -p '{install_dir}'")
    ar18.sudo.exec_as(f"rm -rf '{install_dir}/{module_name}'")
    ar18.sudo.exec_as(f"cp -rf '{script_dir}' '{install_dir}/{module_name}'")
    for file_name in os.listdir(f"{install_dir}/{module_name}/{module_name}"):
      if file_name[-4:] == ".xsh":
        ar18.sudo.exec_as(f"ln -s '{install_dir}/{module_name}/{module_name}/{os.path.basename(file_name)}' '/usr/bin/ar18.{module_name}.{file_name[0:-4]}'")
    ar18.sudo.exec_as(f"chmod +x '{install_dir}/{module_name}' -R")

    mkdir -p @(f"/home/{user_name}/.config/ar18/{module_name}")
    ar18.sudo.exec_as(f"chown {user_name}:{user_name} '/home/{user_name}/.config/ar18/{module_name}'")
    echo @(f"{install_dir}") > @(f"/home/{user_name}/.config/ar18/{module_name}/INSTALL_DIR")

    script_config_dir = f"{script_dir}/{module_name}/config"
    if os.path.isdir(script_config_dir):
      home_config_dir = f"/home/{user_name}/.config/ar18/{module_name}"
      mkdir -p @(home_config_dir)
      for file_path in os.listdir(script_config_dir):
        base_name = os.path.basename(file_path)
        file_path = f"{script_config_dir}/{base_name}"
        home_config_path = f"{home_config_dir}/{base_name}"
        if not os.path.isfile(home_config_path):
          cp @(file_path) @(home_config_path)
          ar18.sudo.exec_as(f"chown {user_name}:{user_name} '{home_config_path}'")

    service_file_path = f"{script_dir}/{module_name}/{module_name}.service"
    service_file_path_install = f"{install_dir}/{module_name}/{module_name}.service"
    if os.path.isfile(service_file_path):
      with open(service_file_path, "r") as in_file:
        content = in_file.read()
        content = content.replace("{{INSTALL_DIR}}", install_dir)
        content = content.replace("{{DEPLOYMENT_TARGET}}", deployment_target)
        with open(service_file_path_install, "w") as out_file:
          out_file.write(content)
      ar18.sudo.exec_as(f"chmod 644 '{service_file_path_install}'")
      ar18.sudo.exec_as(f"rm -rf '/etc/systemd/{module_name}.service'")
      ar18.sudo.exec_as(f"ln -s '{service_file_path_install}' '/etc/systemd/{module_name}.service'")
      ar18.sudo.exec_as(f"systemctl enable {module_name}.service")
      ar18.sudo.exec_as(f"systemctl start {module_name}.service")

    autostart_path = f"{install_dir}/{module_name}/autostart.sh"
    autostart_path_script = f"{script_dir}/{module_name}/autostart.sh"
    if os.path.isfile(autostart_path):
      autostart_dir = f"/home/{user_name}/.config/ar18/autostarts"
      if not os.path.isdir(autostart_dir):
        mkdir -p @(autostart_dir)
      auto_start = f"/home/{user_name}/.config/ar18/autostarts/{module_name}.sh"
      with open(autostart_path_script, "r") as in_file:
        content = in_file.read()
        content = content.replace("{{INSTALL_DIR}}", install_dir)
        with open(auto_start, "w") as out_file:
          out_file.write(content)
      ar18.sudo.exec_as(f"chmod 4750 '{auto_start}'")
      ar18.sudo.exec_as(f"chown root:{user_name} '{auto_start}'")
      
    ar18.script.include("script.read_targets")
    targets = ar18.script.read_targets()
    targets[module_name] = {
      "install_dir": f"{install_dir}",
      "install_date": f"{date_time()}"
    }
    
    ar18.script.include("script.store_targets")
    ar18.script.store_targets(targets)

###############################FUNCTION_END##################################
  ar18.script.install = temp_func
