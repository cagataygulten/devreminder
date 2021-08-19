import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="devreminder",
    version="0.0.1",
    author="Çağatay Gülten",
    author_email="cagataygulten@gmail.com",
    description="DevReminder works as a reminder for developers who are engaged in fields having long execution time.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cagataygulten/devreminder",
    project_urls={
        "Bug Tracker": "https://github.com/cagataygulten/devreminder/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)