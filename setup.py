import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PortDatabaseProject",
    version="0.0.1",
    author="Angelos Anagnostopoulos, Michalis Drosiadis",
    description="A commercial port application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AngelosAnagnostopoulos/MySQLProject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
