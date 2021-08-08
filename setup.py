from setuptools import dist, setup, Extension

dist.Distribution().fetch_build_eggs(['numpy>=1.7'])
import numpy as np

SRC_DIR = "stl_tools"
PACKAGES = [SRC_DIR]

ext_1 = Extension(SRC_DIR + ".cwrapped",
                  [SRC_DIR + "/cwrapped.pyx"],
                  libraries=[],
                  include_dirs=[np.get_include()])
EXTENSIONS = [ext_1]

setup(name='stl_tools',
      version='0.3.0',
      install_requires=['numpy>=1.7', 'scipy>=0.12', 'matplotlib>=1.2.1'],
      python_requires='>=2.7,!=3.0.*,!=3.1.*',
      description="Generate STL files from numpy arrays and text",
      author='Tristan Hearn',
      author_email='tristanhearn@gmail.com',
      url='https://github.com/thearn/stl_tools',
      license='Apache 2.0',
      packages=['stl_tools'],
      ext_modules=EXTENSIONS,
      setup_requires=['cython>=0.17.4'],
      entry_points={
          'console_scripts':
          ['image2stl=stl_tools.image2stl:image2stl']
      }
      )
