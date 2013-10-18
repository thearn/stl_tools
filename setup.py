from setuptools import setup, Extension
import numpy as np

SRC_DIR = "stl_tools"
PACKAGES = [SRC_DIR]

ext_1 = Extension(SRC_DIR + ".cwrapped",
                  [SRC_DIR + "/cwrapped.c"],
                  libraries=[],
                  include_dirs=[np.get_include()])
EXTENSIONS = [ext_1]

setup(name='stl_tools',
      version='0.3.0',
      install_requires=['numpy', 'scipy', 'matplotlib'],
      description="Generate STL files from numpy arrays and text",
      author='Tristan Hearn',
      author_email='tristanhearn@gmail.com',
      url='https://github.com/thearn/stl_tools',
      license='Apache 2.0',
      packages=['stl_tools'],
      ext_modules=EXTENSIONS,
      entry_points={
          'console_scripts':
          ['image2stl=stl_tools.image2stl:image2stl']
      }
      )
