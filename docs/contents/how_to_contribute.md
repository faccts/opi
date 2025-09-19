# How To Contribute

The ORCA Python Interface OPI is designed as an open-source community project and therefore contributions from external developers are welcome. In order to maintain the high quality of the project, we would like to ask all contributors to adhere to certain standards and to read the information provided here beforehand.

## GitHub

The development of OPI is based on [GitHub](https://github.com/faccts/opi).
If you want to contribute, we recommend to fork the project and submit your changes and improvements via pull-requests.
Problems and/or bugs are tracked via [GitHub issues](https://github.com/faccts/opi/issues).

## License & CLA

### Open Source License

This open source project is released publicly under the following open source license: `GPL-3.0`. This license governs all public releases of the code and allows anyone to use, modify, and distribute the project freely, in accordance with its terms.

### Proprietary License

The program, including all contributions, may also be included in our proprietary software products under a commercial license.
This enables us to:

- Combine open source and closed source components into a single product,
- Offer the project under alternative licensing terms to customers with specific commercial needs,
- Ensure open source compliance for all public parts, while simplifying license obligations in private or embedded distributions.

### Contributor License Agreement (CLA)

To maintain this licensing model, all contributors must sign our Contributor License Agreement (CLA). This CLA is an adapted industry-standard CLA (Apache CLA) with minor modifications. By signing the CLA, you

- Retain ownership of your contributions,
- Grant us a non-exclusive license to use, sublicense, relicense and distribute your contributions under both open source and proprietary terms.

### We use a two-part CLA system:

- [Individual CLA (ICLA) for personal contributions](https://github.com/faccts/opi/blob/main/CLA.md),
- Corporate CLA (CCLA) for contributions made on behalf of an employer (available upon request to info@faccts.de).

(sec:howto_code)=
## Code & Dev Guidelines

For code and development guidelines refer to the [dev guide](dev_guide.md)

(sec:howto_examples)=
### Example Notebooks and Scripts

Example from the community can be contributed as Jupyter notebooks or Python scripts. In any case, the documentation of these scripts should be included as a Jupyter notebook with corresponding Markdown explanations.

- Jupyter notebooks must be stored in the [docs/notebooks](https://github.com/faccts/opi/tree/main/docs/contents/notebooks) directory and should have the `.ipynb` extension.

- Python scripts should be stored in the [docs/scripts](https://github.com/faccts/opi/tree/main/docs/contents/scripts) directory.

  :::{tip}
  Jupyter notebooks can be converted into Python scripts and vice versa with the `jupyter` and `jupytext` packages:

  ```
  jupyter nbconvert --to script example.ipynb
  ```

  ```
  jupytext example.py --to notebook
  ```

  :::

- Please provide file names in snake_case separating the words with underscores (e.g. `this_is_my_file.py`).

- Please ensure that the scripts in both formats are sufficiently well [documented](sec:howto_docs) and comprehensible for others.

- Please only contribute fully functional code.

- Community-based long-term maintenance of contributed example notebooks is highly appreciated! The FACCTs team can only maintain the official tutorial examples.

  :::{note}
  The Community Notebooks and external software linked within are contributed by third parties and are not reviewed, endorsed, or controlled by FACCTs. 
  We assume no liability for the content, functionality, or consequences arising from the use of these materials. 
  Users are advised to independently verify the legality, security, and suitability of any external software or resources before use.
  :::

(sec:howto_docs)=
## Documentation Pages

Please document each contributed example as complete and easily comprehensible as possible. For the documentation pages we primarily use [Sphinx](https://www.sphinx-doc.org/en/master/) in combination with [MyST Markdown](https://mystmd.org/). MyST Markdown is an easy-to-learn and forgiving flavor of Markdown that makes text-based documentation very easy.

:::{tip}
If you are more common to ReStructuredText (ReST), there are some [conversion tools](https://rst-to-myst.readthedocs.io/en/latest/index.html) to convert ReST to MyST.
:::

- To directly include Jupyter notebooks into the text documentation, simply include them into the [index.md](https://github.com/faccts/opi/blob/main/docs/index.md) file (e.g. `docs/contents/notebooks/example.ipynb`). The `myst_nb` Sphinx extension will render the notebook and the included Markdown documentation as an individual documentation page.

- If you want to document specific Python scripts or code, you can create a Markdown page (e.g. `example.md`) and include either the full script via

  ````
  ```{literalinclude} ../docs/scripts/example.py
  :language: python
  ```
  ````

- Stay with Markdown Syntax for text documentation if possible. Markdown is more forgiving than ReST and easier to learn for new contributors.
