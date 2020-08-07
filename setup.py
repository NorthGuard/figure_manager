from setuptools import setup
from figure_manager import __version__

with open("pypi_description.md", "r") as fh:
    long_description = fh.read()

setup(
    # Main
    name='figure_manager',
    version=__version__,
    license='MIT License',
    packages=["figure_manager"],

    # Requirements
    install_requires=["matplotlib", "numpy"],

    # Display on PyPI
    author='Jeppe Nørregaard',
    author_email="northguard_serve@tutanota.com",
    description='Easily snap Matplotlib figures to suitable location on screen.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="matplotlib figure monitor screen",
    url='https://github.com/NorthGuard/figure_manager',

    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.0',
)