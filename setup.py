from setuptools import find_packages, setup

description = (
    "Wild Animals Detection and Alert System (WADAS) is a project for "
    "AI-based detection and alert of wildlife in dangerous areas."
)


setup(
    name="wadas",
    version="0.1.0",
    packages=find_packages(),
    package_data={"": ["*.ui", "*.png", "*.jpg"]},
    include_package_data=True,
    author="Stefano Dell'Osa, Alessandro Palla, Antonio Farina, Cesare Di Mauro",
    author_email="stefano.dellosa@gmail.com, alespalla.ap@gmail.com, hexfati@gmail.com, cesare.di.mauro@gmail.com",  # noqa
    description=description,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stefanodellosa-personal/WADAS",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    keywords="wildlife detection alert system ai",
)
