import utils

def main():
    core_os = utils.identify_operating_system()
    processor_platform = utils.identify_processor_platform()
    if core_os != 'Darwin' and processor_platform != 'arm64':
        raise Exception('This script is only for macOS with Apple Silicon!')
    
    miniconda_url = 'https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh'
    miniconda_file_name = 'Miniconda3-latest-MacOSX-arm64.sh'
    utils.install_miniconda(miniconda_url, miniconda_file_name)

    venv_name = 'tensorflow_metal'
    python_version = '3.10.10'
    utils.create_miniconda_environment(venv_name, python_version)
    utils.install_tensorflow_deps(venv_name)
    utils.install_requirements_conda(venv_name, "setup/requirements_tensorflow_apple_silicon.txt")
    print(f"\n (1/2) Installation Succesful! Please run \'conda activate {venv_name}\' to activate the environment.")

    venv_name = 'pytorch_cpu'
    python_version = '3.10.10'
    utils.create_miniconda_environment(venv_name, python_version)
    utils.install_requirements_conda(venv_name, "setup/requirements_pytorch_cpu.txt")
    print(f"\n (2/2) Installation Succesful! Please run \'conda activate {venv_name}\' to activate the environment.")

if __name__ == '__main__':
    main()