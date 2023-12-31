from pathlib import Path

from setuptools import find_packages, setup

cur_dir = Path(__file__).absolute().parent
long_description = (cur_dir / "README.md").read_text(encoding="utf-8")
version = "1.1.1"

setup(
    name="sykj_mtoc",
    version=version,
    url="https://github.com/Coder-Yifan/sykj_mtoc.git",
    description="Code-generation for various ML models into native code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="yifan.wu",
    packages=find_packages(exclude=["tests.*", "tests", "tools"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=("sklearn statsmodels lightning xgboost lightgbm "
              "machine-learning ml regression classification "
              "transpilation code-generation"),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "sykj_mtoc = sykj_mtoc.cli:main",
        ],
    }
)
