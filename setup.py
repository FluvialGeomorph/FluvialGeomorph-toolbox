from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='FluvialGeomorph',
      version='0.1.42',
      author='Michael Dougherty',
      author_email='Michael.P.Dougherty@usace.army.mil',
      description='The FluvialGeomorph toolbox contains a set of tools for measuring river geometry and assessing river conditions.',
      url='https://github.com/FluvialGeomorph/FluvialGeomorph',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='CC0',
      packages=setuptools.find_packages(),
      classifiers=[
         "Development Status :: 4 - Beta",
         "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
         "Operating System :: Microsoft :: Windows",
         "Natural Language :: English",
         "Programming Language :: Python :: 3",
         "Programming Language :: R",
         "Topic :: Scientific/Engineering :: GIS",
         "Intended Audience :: Science/Research"
      ],
      python_requires='>=2.7'
      )
