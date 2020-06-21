import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'reddit_scraper'

setuptools.setup(
    name="reddit_scraper",
    version="0.0.3",
    author="Kristof",
    description="reddit_scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/py_reddit_scraper",
    packages=setuptools.find_packages(),
    install_requires=["jsoncodable", "kcu"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)