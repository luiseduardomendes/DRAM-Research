from setuptools import find_packages, setup

with open('README.md', 'r') as f:
  long_description = f.read()

setup(
  name='dramlib',
  version='1.0.0',
  description='Set of tools to analyse DRAM performance integrated with different systems',
  package_dir={"":"app"},
  packages=find_packages(where="app"),
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/luiseduardomendes/DRAM-Research',
  author='Luis Eduardo Pereira Mendes',
  author_email="lepmendes@inf.ufrgs.br",
  license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Operating System :: Ubuntu'
    ],
    install_requires=['pandas','matplotlib'],
    python_requires='>=3.9',
)