from setuptools import setup, find_packages

setup(
    name="python_sharp",  # Unique name of your package on PyPI
    version="1.0.1",  # Version of the package, following semantic versioning
    author="Juan Carlos Lopez Garcia",  # Author's name
    author_email="juanclopgar@gmail.com",  # Contact email
    description="python# (python sharp) is a module created to add EOP (event oriented programing) into python in the most native feeling, easy sintax way possible. Based on C# event implementation structure",  # Short description
    long_description=open("README.md", "r", encoding="utf-8").read(),  # Reads the content of the README file
    long_description_content_type="text/markdown",  # Specifies the format of the README file
    url="https://github.com/juanclopgar97/python_sharp.git",  # Repository URL 
    py_modules=["python_sharp"],
    classifiers=[
        "Programming Language :: Python :: 3",  # Indicates the supported Python version
        "License :: OSI Approved :: MIT License",  # Type of license
        "Operating System :: OS Independent",  # Compatible operating systems
    ],
    python_requires=">=3.6",  # Minimum required Python version
    install_requires=[  # Dependencies needed by package
    ]
)
