from setuptools import find_packages, setup

with open("requirements.txt") as f:
    reqs = f.read().split("\n")

setup(
    version="0.0.1",
    name="seis_cloud",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=reqs,
    author="Yiyu Ni, Marine Denolle",
    author_email="niyiyu@uw.edu,mdenolle@uw.edu",
    description="Python Cloud Tutorial for Seismology",
    license="MIT license",
    url="https://github.com/SeisSCOPED/seis_cloud",
)