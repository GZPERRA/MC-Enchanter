import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mc_enchanter",
    version="0.0.5",
    author="GZPERRA",
    description="A small python module that masters Minecraft enchanting mechanics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GZPERRA/MC-Enchanter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
