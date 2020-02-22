import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mcpyenchanter", # Replace with your own username
    version="0.0.1",
    author="GZPERRA",
    description="A small python program that masters Minecraft enchanting mechanics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Perrahmaouy/Minecraft-Enchanting-Master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
