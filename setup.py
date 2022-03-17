from setuptools import setup, find_packages
from packages.python import accern_data

with open("./README.md", "r") as readme:
    description = readme.read()

with open('requirements.txt') as file:
    required = file.read().splitlines()

setup(
    name="accern_data",
    version=accern_data.__version__,
    description="",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Accern Corp.",
    author_email="ankur.goswami@accern.com",
    url="https://github.com/Accern/accern-data-client",
    package_dir={"": "packages/python"},
    packages=find_packages(where="packages/python"),
    install_requires=required,
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
    ]
)
