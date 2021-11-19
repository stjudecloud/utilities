# St. Jude Cloud Utilities

This repository contains an easily installable package for all of the utility scripts created for and used on the St. Jude Cloud team (broadly speaking). The repository is structured as a single package that is goverened by [`poetry`]. 

You can use the snippet below to install the package and access the scripts outlined below.

```bash
pip install stjudecloud-utilities
```

## Scripts

The following scripts are included in the package:

### `deduplicate-samples`

A utility script to deduplicate St. Jude Cloud file names. Assumes files are annotated with St. Jude project names. Retains files based on the `PRIORITIES` list of prioritized projects.

Usage: `dx ls /counts | python3 deduplicate.py | bash`

### `gtf_to_rseqc_bed` 

A utility script for converting Gencode GTFs into the custom BED12 format used by the [RSeQC software package](http://rseqc.sourceforge.net/).

Usage: `python3 gtf_to_RSeQC_bed.py <gencode gtf> > gencode.vFOO.bed`

## Tests

Given that this repo is still new, there are no tests. When we add tests, we will update the README.

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/stjudecloud/utilities/issues). You can also take a look at the [contributing guide](https://github.com/stjudecloud/utilities/blob/master/CONTRIBUTING.md).

## 📝 License

Copyright © 2021 [St. Jude Cloud Team](https://github.com/stjudecloud).<br />
This project is [MIT](https://github.com/stjudecloud/workflows/blob/master/LICENSE.md) licensed.

[`poetry`]: https://python-poetry.org/docs/