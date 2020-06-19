import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="valitools-Beatriz-Negreiros",  # Replace with your own username
    version="0.0.1",
    author="Beatriz Negreiros",
    author_email="beatriznegreiros@outlook.com",
    description="Fuzzy map comparison for model evaluation",
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
