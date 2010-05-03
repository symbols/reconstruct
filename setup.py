from setuptools import setup, find_packages
import reconstruct

setup(
    name = 'reconstruct',
    version = reconstruct.__version__,
    packages = find_packages(),
    zip_safe = False, # to match the existing egg, maybe could be True

    # metadata for PyPI & Egg stuff
    maintainer = "Symbols",
    maintainer_email = "simplesymbols at gmail dot com",
    description = "library for constructing (parsing and building) of binary and textual data structures",
    url = "http://construct.wikispaces.com/",
    license = "Public Domain",
    long_description = """
ReConstruct is a continuation of the excellent 'Construct' library by 
Tomer Filiba <tomerfiliba [at] gmail dot com>. 
The original description is reproduced below. This version is maintained by 
Symbols <simplesymbols [at] gmail dot com>.

Original Description
====================
Construct is a library for parsing and building of data structures (binary or
textual).

The original description is 
It is based on the concept of defining data structures in a declarative manner,
rather than procedural code: more complex constructs are composed of a hierarchy
of simpler ones. It's the first library that makes parsing fun, instead of the
usual headache it is today.

Construct features bit and byte granularity, symmetrical operation (parsing
and building), component-oriented design (declarative), easy debugging and
testing, easy to extend (subclass constructs), and lots of primitive constructs
to make your work easier (fields, structs, unions, repeaters, meta constructs,
switches, on-demand parsing, pointers, etc.)
""",
    keywords = "parsing,binary,bitwise,bit level,constructing,struct",
    platforms = ["any"],
    classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: Public Domain",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Internet",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Networking",
    "Topic :: System :: Networking :: Monitoring",
    "Topic :: Text Processing"]
)
