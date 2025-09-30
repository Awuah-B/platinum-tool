from setuptools import setup, find_packages

setup(
    name="platinum-tool",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        "console_scripts": [
            "platinum-tool=cli:main",
        ],
    },
    author="Awuah Baffor Junior",
    author_email="awuahbj@example.com",
    description="A time calculator CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Awuah-B/platinum-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)