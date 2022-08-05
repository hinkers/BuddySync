import setuptools

setuptools.setup(
    name="apisync",
    version="1.0.0",
    author="Hinkers",
    description="Sync APIs easly to SQL databases through config files and simple scripts.",
    url="https://github.com/hinkers/Api-Sync",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
