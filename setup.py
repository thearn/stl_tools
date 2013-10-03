from setuptools import setup, find_packages

setup(name='stl_tools',
    version='0.1',
    install_requires=['numpy', 'scipy', 'matplotlib'],
    description="Python code to generate STL files from numpy arrays and text",
    author='Tristan Hearn',
    author_email='tristanhearn@gmail.com',
    url='https://github.com/thearn/stl_tools',
    license='Apache 2.0',
    packages=['stl_tools'],
)
