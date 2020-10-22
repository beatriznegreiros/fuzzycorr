import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="valitools-Beatriz-Negreiros",
    version="0.0.1",
    author="Beatriz Negreiros",
    author_email="beatriz.negreiros@iws.uni-stuttgart.de",
    description="Fuzzy map comparison for the evaluation of hydro-morphodynamic numerical models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://beatriznegreiros.github.io/valitools/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
