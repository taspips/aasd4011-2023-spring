import subprocess
import os
from setup import identify_operating_system

def install_miniconda():
    print('Installing MiniConda...')
    
    miniconda_url = 'https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh'
    miniconda_file_name = 'Miniconda3-latest-MacOSX-arm64.sh'
    miniconda_install_path = os.path.join(os.path.expanduser('~'), 'miniconda')
    
    if os.path.exists(miniconda_install_path):
        print('MiniConda is already installed.')
        return

    # Download MiniConda installer
    subprocess.run(f'curl -o {miniconda_file_name} {miniconda_url}', shell=True, check=True)

    # Run the installer script
    subprocess.run(f'bash {miniconda_file_name} -b -p {miniconda_install_path}', shell=True, check=True)

    # Remove the installer file
    subprocess.run(f'rm {miniconda_file_name}', shell=True, check=True)

    print('MiniConda installed successfully')

def create_miniconda_environment(venv_name: str, python_version: str):
    print(f'Creating Miniconda environment "{venv_name}" with Python {python_version}...')
    subprocess.run(f'conda create -n {venv_name} python={python_version}', shell=True, check=True)
    print(f'Miniconda environment "{venv_name}" created')

def install_tensorflow_macos(venv_name: str):
    print(f'Installing required packages for Tensorflow in "{venv_name}" environment...')
    subprocess.run(f'conda activate {venv_name} && conda install -c apple tensorflow-deps', shell=True, check=True)
    subprocess.run(f'conda activate {venv_name} && python -m pip install tensorflow-macos', shell=True, check=True)
    subprocess.run(f'conda activate {venv_name} && python -m pip install tensorflow-metal', shell=True, check=True)
    print(f'Tensorflow installed in "{venv_name}" environment')
    
def install_requirements_conda(venv_name: str, requirements_file: str):
    print(f'Installing required packages in {requirements_file} in "{venv_name}" environment...')
    subprocess.run(f'conda activate {venv_name} && python -m pip install -r {requirements_file}', shell=True, check=True)
    print(f'{requirements_file} installed in "{venv_name}" environment')

def install_additional_packages(venv_name: str):
    print(f'Installing additional packages in "{venv_name}" environment...')
    subprocess.run(f'conda activate {venv_name} && pip install -U numpy', shell=True, check=True)
    subprocess.run(f'conda activate {venv_name} && pip install ipykernel tensorboard matplotlib nbconvert', shell=True, check=True)
    print(f'Additional packages installed in "{venv_name}" environment')

def main():
    platform = identify_operating_system()
    if platform != 'Darwin':
        raise Exception('This script is only for macOS with Apple Silicon!')
    
    venv_name = 'tensorflow'
    python_version = '3.10.10'
    
    install_miniconda()

    create_miniconda_environment(venv_name, python_version)
    install_tensorflow_macos(venv_name)
    install_additional_packages(venv_name)
    
    venv_name = 'pytorch_cpu'
    create_miniconda_environment(venv_name, python_version)
    install_requirements_conda(venv_name, "setup/requirements_pytorch_cpu.txt")

if __name__ == '__main__':
    main()