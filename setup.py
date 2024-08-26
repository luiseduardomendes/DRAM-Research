from setuptools import find_packages, setup

long_description = ''

setup(
  name='dramlib',
  version='0.0.10',
  description='Set of tools to analyse DRAM performance integrated with different systems',
  package_dir={"":"dramlib"},
  packages=find_packages(where="dramlib"),
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/luiseduardomendes/DRAM-Research',
  author='Luis Eduardo Pereira Mendes',
  author_email="lepmendes@inf.ufrgs.br",
  license='MIT',
)