import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fuzzycorr-Beatriz-Negreiros",
    version="0.0.1",
    author="Beatriz Negreiros",
    author_email="beatriz.negreiros@iws.uni-stuttgart.de",
    description="A Python package for correlating simulated and observed datasets via Fuzzy Map Comparison",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://beatriznegreiros.github.io/fuzzycorr/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
