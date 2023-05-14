import utils

def main():
    core_os = utils.identify_operating_system()
    processor_platform = utils.identify_processor_platform()
    if core_os == 'Darwin' and processor_platform == 'arm64':
        raise Exception('You are using an Apple-Silicon (ARM) Device. Please run \'setup_apple_silicon.py\' instead!')
    shell = utils.identify_shell(core_os)
    utils.validate_python_version()
    executable = utils.identify_python_executable()
    utils.is_git_installed()
    utils.is_pip_installed()
    utils.is_ensurepip_installed()
    venv_names = ['pytorch_cpu', 'tensorflow_cpu']
    if core_os == 'Windows':
        venv_paths = [r'.\venv\\'+n for n in venv_names]
    elif (core_os == 'Linux') | (core_os == 'Darwin'):
        venv_paths = ['./venv/'+n for n in venv_names]
    requirements_paths = ['./setup/requirements_' + e + '.txt' for e in venv_names]
    for venv_path, requirements_path, venv_name in zip(venv_paths, requirements_paths, venv_names):
        utils.create_venv(venv_path, core_os, shell, executable)
        utils.install_packages(venv_path, requirements_path, core_os, shell, executable)
        utils.install_ipykernel(venv_path, venv_name, core_os, shell, executable)

if __name__ == '__main__':
    main()
