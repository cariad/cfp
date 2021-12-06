from pathlib import Path

from setuptools import setup  # pyright: reportMissingTypeStubs=false

from cfp import __version__

readme_path = Path(__file__).parent / "README.md"

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Typing :: Typed",
]

if "a" in __version__:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in __version__:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.earth",
    classifiers=classifiers,
    description="Builds Amazon Web Services CloudFormation parameters",
    include_package_data=True,
    install_requires=[
        "ansiscape~=1.0",
        "boto3~=1.18",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="cfp",
    packages=[
        "cfp",
        "cfp.exceptions",
        "cfp.resolver_factories",
        "cfp.resolvers",
        "cfp.sources",
    ],
    package_data={
        "cfp": ["py.typed"],
        "cfp.exceptions": ["py.typed"],
        "cfp.resolver_factories": ["py.typed"],
        "cfp.resolvers": ["py.typed"],
        "cfp.sources": ["py.typed"],
    },
    python_requires=">=3.8",
    url="https://github.com/cariad/cfp",
    version=__version__,
)
