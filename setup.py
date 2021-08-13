from setuptools import setup, find_packages

setup(
    name='gpt_utils',
    version='0.0.7.2',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'transformers~=4.8.2',
        'openai~=0.9.3',
    ],
    url='https://github.com/nelsonlove/gpt-utils',
    license='LICENSE.txt',
    author='Nelson Love',
    author_email='nelson@nelson.love',
    description='Collection of utilities for use with GPT-3',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/nelsonlove/gpt-utils/issues',
        'Source': 'https://github.com/nelsonlove/gpt-utils/',
    },
)
