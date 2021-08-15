import setuptools

with open("requirements.txt", "r") as requirements_file:
    install_requires = requirements_file.readlines()

setuptools.setup(
    name="reddit_scraping",
    version="0.0.1",
    author="Michael Graf",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=install_requires,
    packages=["scraper"]

)
