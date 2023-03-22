from io import DEFAULT_BUFFER_SIZE
from setuptools import setup, find_packages

MAJOR = 0
MINOR = 1
MICRO = 23
ISRELEASED = True
VERSION = f"{MAJOR}.{MINOR}.{MICRO}"

DESCRIPTION = "General file and data processing tools"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rlylutils",
    version=VERSION,
    keywords="file, data processing",
    description=DESCRIPTION,
    #long_description_content_type="text/markdown",
    long_description=long_description,
    author="Ray Lam LYL",
    author_email="1027196450@qq.com",
    url="https://github.com/RayLam2022/rl-utils",
    packages=find_packages(),
    #include_package_data=True,
    #package_data={"evatool.resource": ["*.json", "*.conf", "*.html"], "evatool.bin": ["*"]},
    #install_requires=['Cython','ijson','numpy','pandas', 'lxml', 'scikit-learn','scipy','tqdm','opencv-python','psutil'],
    # extras_require={
    #     "dev": ["pytest"],
    #     "interactive": ["matplotlib"],
    # },
    license="GNU Lesser General Public License v2.1",
    platforms="any",
    #package_dir={"evatool": "evatool"},
    #python_requires=">=3.8",

)