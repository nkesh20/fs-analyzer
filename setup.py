from setuptools import setup, find_packages

setup(
    name="fs-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["tabulate"],
    entry_points={
        "console_scripts": ["fs-analyzer = analyzer.cli:main"],
    },
)
