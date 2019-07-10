from setuptools import setup, find_packages

try:
    with open('requirements.txt') as reqs:
        install_requires = [
            line for line in reqs.read().split('\n')
            if (line and not line.startswith('--')) and (";" not in line)]
except Exception:
    install_requires = []

setup(
    name="mapserverapi",
    version="0.1.0",
    license="BSD",
    url="https://github.com/metwork-framework/mapserverapi_python",
    description="tiny python library to invoke mapserver engine as a library",
    packages=find_packages(),
    install_requires=install_requires
)
