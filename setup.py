import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SphinxPages",
    version="0.0.0",
    author="zengjf",
    author_email="zengjf42@163.com",
    description="Sphinx For Markdown Pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZengjfOS/SphinxPages",
    project_urls={
        "Bug Tracker": "https://github.com/ZengjfOS/SphinxPages/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    python_requires=">=3.0",
    install_requires=[
        'sphinx',
        'myst_parser',
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["SphinxPages=SphinxPages:main"]},
)
