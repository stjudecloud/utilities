<p align="center">
  <h1>
  St. Jude Cloud Utilities
  </h1>
  <a href="https://github.com/stjudecloud/utilities/blob/master/LICENSE.md" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

> This repository contains utility scripts used on the St. Jude Cloud project.

### 🏠 [Homepage](https://stjude.cloud)

## Repository Structure

The repository is laid out as follows:

* `scripts` - A collection of utility scripts to be used with St. Jude Cloud genomics platform.
  * `deduplicate.py` - A utility script to deduplicate St. Jude Cloud file names. Assumes files are annotated with St. Jude project names. Retains files based on the `PRIORITIES` list of prioritized projects.
    * Usage: `dx ls /counts | python3 deduplicate.py | bash`
  * `gtf_to_RSeQC_bed.py` - A utility script for converting Gencode GTFs into the custom BED12 format used by the [RSeQC software package][http://rseqc.sourceforge.net/].
    * Usage: `python3 gtf_to_RSeQC_bed.py <gencode gtf> > gencode.vFOO.bed`

## Author

👤 **St. Jude Cloud Team**

* Website: https://stjude.cloud
* Github: [@stjudecloud](https://github.com/stjudecloud)
* Twitter: [@StJudeResearch](https://twitter.com/StJudeResearch)

## Tests

Given that this repo is still new, there are no tests. When we add tests, we will update the README.

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/stjudecloud/utilities/issues). You can also take a look at the [contributing guide](https://github.com/stjudecloud/utilities/blob/master/CONTRIBUTING.md).

## 📝 License

Copyright © 2020 [St. Jude Cloud Team](https://github.com/stjudecloud).<br />
This project is [MIT](https://github.com/stjudecloud/workflows/blob/master/LICENSE.md) licensed.