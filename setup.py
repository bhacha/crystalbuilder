from setuptools import setup


setup(
    name='crystalbuilder',
    version='0.3.0',
    description='A Python package to create various photonic crystal patterns in 2D and 3D; includes Vedo visualizer wrapper',
    author='Brandon Hacha',
    license='MIT',
    packages=['crystalbuilder'],
    install_requires=['numpy', 'matplotlib'],
    extras_require={
        'full' : ['vedo', 'tidy3d', 'pymeep'],
        'windows': ['vedo', 'tidy3d'],
        'basic': ['vedo']
    }
)
