# OPI - ORCA Python Interface

![Static Badge](https://img.shields.io/badge/license-GPL--3.0-orange)
![Static Badge](https://img.shields.io/badge/contributing-CLA-red)
![Static Badge](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.15688425-blue)
![Static Badge](https://img.shields.io/badge/release-1.0.0-%2300AEC3)

The ORCA Python Interface (OPI) is a Python library to create input and parse output of [ORCA](https://www.faccts.de/orca/). It is designed as an open source community effort to make ORCA calculations as accessible as possible and is consistently supported by [FACCTs](https://www.faccts.de/), the co-developers of the ORCA quantum chemistry program package. Note that OPI is first introduced with ORCA 6.1 and is not compatible with earlier versions.

### Helpful Links

- **OPI:**

  - Documentation (stable): https://www.faccts.de/docs/opi/1.0/docs
  - Documentation (nightly): https://www.faccts.de/docs/opi/nightly/docs
  - Source code: https://www.github.com/faccts/opi
  - Bug reports: https://www.github.com/faccts/opi/issues
  - PyPI: https://pypi.org/project/orca-pi/
  - MCP: https://context7.com/faccts/opi

- **ORCA:**

  - Manual: https://www.faccts.de/docs/orca/6.1/manual/
  - Tutorials: https://www.faccts.de/docs/orca/6.1/tutorials/
  - ORCA Forum: https://orcaforum.kofo.mpg.de/

## Installation

This package can either be installed directly from [PyPI](https://pypi.org/project/orca-pi/) with:

```
pip install orca-pi
```

or from GitHub:

```
git clone https://github.com/faccts/opi.git
cd opi
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install .
```

More details about the installation can be found in the [documentation](https://www.faccts.de/docs/opi/1.0/docs/contents/install.html).

### ORCA and Open MPI

OPI requires ORCA and for parallel calculations also Open MPI.
Details on how to install ORCA can be found in its manual or tutorials. See [Helpful Links](#Helpful-Links).
For most modern operating system Open MPI can usually be installed directly with the systems package manager.
Otherwise, a suitable version has to be obtained and compiled from their [website](https://www.open-mpi.org/).

**Note that OPI is first introduced with ORCA 6.1 and is not compatible with earlier versions.
The minimal supported ORCA version is always stored in [ORCA_MINIMAL_VERSION](https://github.com/faccts/opi/blob/main/src/opi/__init__.py)**

## Documentation

This package comes with a set of tutorials and automatic API reference.
The files can be found in [docs/](https://github.com/faccts/opi/tree/main/docs).
We also host the documentation for the latest stable release and nightly version online.
See [Helpful Links](#Helpful-Links).

The documentation can also be built from the `docs/` folder:

```
make html
```

This requires [`uv`](https://github.com/astral-sh/uv) which by default is also installed by the `Makefile`.

## License

### Open Source License

This open source project is released publicly under the following open source license: `GPL-3.0`. This license governs all public releases of the code and allows anyone to use, modify, and distribute the project freely, in accordance with its terms.

### Proprietary License

The program, including all contributions, may also be included in our proprietary software products under a commercial license.
This enables us to:

- Combine open source and closed source components into a single product,
- Offer the project under alternative licensing terms to customers with specific commercial needs,
- Ensure open source compliance for all public parts, while simplifying license obligations in private or embedded distributions.

## Contributing

Contributions are welcome. See [How To Contribute](https://www.faccts.de/docs/opi/nightly/docs/contents/how_to_contribute.html) for details.

### Contributor License Agreement (CLA)

To maintain this licensing model, all contributors must sign our Contributor License Agreement (CLA).
This CLA is an adapted industry-standard CLA (Apache CLA) with minor modifications. By signing the CLA, you

- Retain ownership of your contributions,
- Grant us a non-exclusive license to use, sublicense, relicense and distribute your contributions under both open source and proprietary terms.

### We use a two-part CLA system:

- [Individual CLA (ICLA) for personal contributions](CLA.md),
- Corporate CLA (CCLA) for contributions made on behalf of an employer (available upon request to info@faccts.de).

## Contact

For issues or bug reports please create an [issue](https://www.github.com/faccts/opi/issues) on GitHub.
For commercial inquiries contact us directly at [info@faccts.de](mailto:info@faccts.de).
