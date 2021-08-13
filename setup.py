import setuptools

import codecs
from os import path


def read(rel_path):
    here = path.abspath(path.dirname(__file__))
    with codecs.open(path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# read the contents of README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='gpt_utils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=get_version("src/gpt_utils/__init__.py"),
    package_dir={"": "src"},
    setup_requires=["wheel"],
    packages=setuptools.find_packages(where="src"),
)
