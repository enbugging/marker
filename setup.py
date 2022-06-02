from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Marker is a package helping improving readability'
LONG_DESCRIPTION = 'Marker is a Python module aiming for improving readability of text, in particular long and/or dense text and for audience with dyslexia condition. It is not designed to be an accurate highlighter, but to work fast and with streams of text, intended for further development.'

# Setting up
setup(
        name="marker", 
        version=VERSION,
        author="D. Dai, Nguyen",
        author_email="<ndoandai@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=['nltk'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: General",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)