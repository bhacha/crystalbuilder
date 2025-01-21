from setuptools import setup


setup(
    name='crystalbuilder',
    version='0.0.5',
    description='A Python package to create various photonic crystal patterns',
    author='Brandon Hacha',
    license='MIT',
    packages=['crystalbuilder'],
    install_requires=['numpy', 'matplotlib'],
    extras_require={
        'full' : ['vedo', 'tidy3d', 'meep'],
        'windows': ['vedo', 'tidy3d'],
        'basic': ['vedo']
    }
)
