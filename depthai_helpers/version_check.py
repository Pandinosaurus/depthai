import depthai
from pathlib import Path


def getVersionFromRequirements(package_name, req_path):
    with req_path.resolve().open() as f:
        for line in f.readlines():
            if package_name in line:
                #not commented out and has version indicator (==)
                if not line.startswith('#') and '==' in line:
                    try:
                        version = line.split('==')[1]
                        version = version.split(';')[0]
                        #remove any whitespace
                        version = version.strip()
                    except:
                        version = None
                    return version


def getVersion(module_name):
    try:
        import importlib
        module = importlib.import_module(module_name)
        if hasattr(module, '__version__'):
            return module.__version__
        if hasattr(module, 'version'):
            return module.version
    except:
        pass
    try:
        import pkg_resources
        return pkg_resources.get_distribution(module_name).version
    except:
        pass

    try:
        from importlib.metadata import version
        return version(module_name)
    except:
        pass

    return None

def checkRequirementsVersion():
    daiVersionRequired = getVersionFromRequirements('depthai', Path(__file__).parent / Path('../requirements.txt'))
    if daiVersionRequired is not None:
        if depthai.__version__.endswith('+dev'):
            print('Depthai development version found, skipping check.')
        elif daiVersionRequired != getVersion('depthai'):
            raise SystemExit(f"\033[1;5;31mVersion mismatch\033[0m\033[91m between installed depthai lib and the required one by the script.\033[0m \n\
                Required:  {daiVersionRequired}\n\
                Installed: {getVersion('depthai')}\n\
                \033[91mRun: python3 install_requirements.py \033[0m")
