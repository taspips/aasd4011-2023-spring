import subprocess
import os
import platform
import sys


def identify_operating_system():
    # identify the core operating system
    operating_system = platform.system()
    print(f'Operating system: {operating_system}')
    return operating_system


def identify_processor_platform():
    return platform.machine()


def identify_shell(platform: str):
    # identify the shell environment:
    # e.g. bash and zsh - for Linux and Mac
    # or cmd and powershell - for Windows
    if (platform == 'Linux') | (platform == 'Darwin'):
        shell = os.environ["SHELL"]
    elif platform == 'Windows':
        shell = os.environ["COMSPEC"]
    print(f'Shell: {shell}')
    return shell


def identify_python_executable():
    # identify the filename of the Python interperater running this script.
    executable = sys.executable
    print(f'The python executable file is: {executable}')
    if (executable.endswith('python')) | (executable.endswith('python.exe')):
        executable = 'python'
    elif (executable.endswith('python3')) | (executable.endswith('python3.exe')):
        exectuable = 'python3'
    else:
        raise ValueError(f"executable is {executable} and it doesn't end with neither 'python', 'python.exe', 'python3', nor 'python3.exe'. "
                         "To support this executable, update this script"
                         )
    return executable


def validate_python_version():
    # check that python version is the recommended one, i.e.: 3.7.x-3.11.x
    if (sys.version_info >= (3, 7)) | (sys.version_info <= (3, 11)):
        print(
            f'Python version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is installed. '
            '(the recommended version for this repository is 3.7.x-3.11.x)'
        )
    else:
        sys.exit(
            f'The Python version installed is: {sys.version_info.major}.{sys.version_info.minor}, and is not supported. '
            'Please install the recommended version of Python and try again. '
            'See: https://www.python.org/downloads/'
        )


def is_git_installed():
    # check that Git is installed
    try:
        output = subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE)
        output = output.stdout.decode('ascii').replace('\n', '')
        print(f'Git is installed (version: {output})')
    except subprocess.CalledProcessError:
        raise ValueError(
            'Git is not installed. Please install Git and rerun this script.'
            'To install, see: https://git-scm.com/downloads'
        )


def is_pip_installed():
    # check if pip is installed
    try:
        import pip
        print(f'pip is installed (version: {pip.__version__})')
    except ImportError:
        raise ImportError('pip is not installed. Please install pip and run this script again')


def is_ensurepip_installed():
    # check if ensurepip is installed
    try:
        import ensurepip
        print(f'ensurepip is installed (version: {ensurepip.version()})')
    except ImportError:
        raise ImportError('ensurepip is not installed. Please install ensurepip and run this script again')


def create_venv(venv_path: str, platform: str, shell: str, executable: str):
    # create a virtual environment
    if os.path.exists(venv_path):
        print(
            f'{venv_path} - Virtual environment folder already exists. '
            'Skipping venv creation. '
            'If you want to recreate the venv, delete the folder and run this script again.'
        )
        return
    print(f'{venv_path} - Creating virtual environment...')
    subprocess.run(f'{executable} -m venv {venv_path}', shell=True)
    print(f'{venv_path} - Virtual environment created')


def install_packages(venv_path: str, requirements_path: str, platform: str, shell: str, executable: str):
    # install packages from requirements.txt
    print(f'{venv_path} - Installing packages...')
    if (platform == 'Linux') | (platform == 'Darwin'):
        subprocess.run(f'{venv_path}/bin/pip install -r {requirements_path}', shell=True)
    elif platform == 'Windows':
        subprocess.run(fr'{venv_path}\Scripts\pip install -r {requirements_path}', shell=True)
    print(f'{venv_path} - Packages installed')


def install_ipykernel(venv_path: str, venv_name: str, platform: str, shell: str, executable: str):
    # install ipykernel
    print(f'{venv_path} - Installing ipykernel...')
    if (platform == 'Linux') | (platform == 'Darwin'):
        subprocess.run(f'{venv_path}/bin/python -m ipykernel install --user --name={venv_name} --display-name={venv_name}', shell=True)
    elif platform == 'Windows':
        subprocess.run(fr'{venv_path}\Scripts\python -m ipykernel install --user --name={venv_name} --display-name={venv_name}', shell=True)
    print(f'{venv_path} - ipykernel installed')


def install_miniconda(miniconda_url: str, miniconda_file_name: str, miniconda_install_path: str = ""):
    print('Installing MiniConda...')
    if not miniconda_install_path:
        miniconda_install_path = os.path.join(os.path.expanduser('~'), 'miniconda')
    if os.path.exists(miniconda_install_path):
        print('MiniConda is already installed.')
        return
    subprocess.run(f'curl -o {miniconda_file_name} {miniconda_url}', shell=True, check=True)
    subprocess.run(f'bash {miniconda_file_name} -b -p {miniconda_install_path}', shell=True, check=True)
    subprocess.run(f'rm {miniconda_file_name}', shell=True, check=True)
    print('MiniConda installed successfully')


def create_miniconda_environment(venv_name: str, python_version: str):
    print(f'Creating Miniconda environment "{venv_name}" with Python {python_version}...')
    subprocess.run(f'conda create -n {venv_name} python={python_version}', shell=True, check=True)
    print(f'Miniconda environment "{venv_name}" created')


def install_tensorflow_deps(venv_name: str):
    print(f'Installing required packages for Tensorflow in "{venv_name}" environment...')
    subprocess.run(f'conda activate {venv_name} && conda install -c apple tensorflow-deps', shell=True, check=True)
    print(f'tensorflow-deps installed in "{venv_name}" environment')


def install_requirements_conda(venv_name: str, requirements_file: str):
    print(f'Installing required packages in {requirements_file} in "{venv_name}" environment...')
    subprocess.run(f'conda activate {venv_name} && python -m pip install -r {requirements_file}', shell=True, check=True)
    print(f'{requirements_file} installed in "{venv_name}" environment')


def main():
    operating_system = identify_operating_system()
    processor_platform = identify_processor_platform()

    # Installation for Windows, Linux, and MacOS running on x86_64 architecture
    if operating_system in ['Windows', 'Linux', 'Darwin'] and processor_platform == 'x86_64':
        shell = identify_shell(operating_system)
        validate_python_version()
        executable = identify_python_executable()
        is_git_installed()
        is_pip_installed()
        is_ensurepip_installed()
        venv_names = ['pytorch_cpu', 'tensorflow_cpu']
        if operating_system == 'Windows':
            venv_paths = [r'.\venv\\'+n for n in venv_names]
        elif (operating_system == 'Linux') | (operating_system == 'Darwin'):
            venv_paths = ['./venv/'+n for n in venv_names]
        requirements_paths = ['./setup/requirements_' + e + '.txt' for e in venv_names]
        for venv_path, requirements_path, venv_name in zip(venv_paths, requirements_paths, venv_names):
            create_venv(venv_path, operating_system, shell, executable)
            install_packages(venv_path, requirements_path, operating_system, shell, executable)
            install_ipykernel(venv_path, venv_name, operating_system, shell, executable)

    # Installation for macOS running on Apple Silicon
    elif operating_system == 'Darwin' and processor_platform == 'arm64':
        miniconda_url = 'https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh'
        miniconda_file_name = 'Miniconda3-latest-MacOSX-arm64.sh'
        install_miniconda(miniconda_url, miniconda_file_name)

        venv_name = 'tensorflow_metal'
        python_version = '3.10.10'
        create_miniconda_environment(venv_name, python_version)
        install_tensorflow_deps(venv_name)
        install_requirements_conda(venv_name, "setup/requirements_tensorflow_apple_silicon.txt")
        print(f"\n (1/2) Installation Succesful! Please run \'conda activate {venv_name}\' to activate the environment.")

        venv_name = 'pytorch_cpu'
        python_version = '3.10.10'
        create_miniconda_environment(venv_name, python_version)
        install_requirements_conda(venv_name, "setup/requirements_pytorch_cpu.txt")
        print(f"\n (2/2) Installation Succesful! Please run \'conda activate {venv_name}\' to activate the environment.")

    else:
        raise Exception('Could not identify the OS/ CPU Architecture of the machine!')


if __name__ == '__main__':
    main()
