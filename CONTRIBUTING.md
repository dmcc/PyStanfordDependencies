# Contributing to PyStanfordDependencies

We love pull requests from everyone. By participating in this project, you agree to abide by the thoughtbot [code of conduct].

## Getting involved

If you're looking for ideas, see [issues][issues], specifically those marked [`help-wanted`][helpwanted].

## Submitting changes

* Sign the [Contributor License Agreement](https://www.dropbox.com/s/woyyhxej4y0t2rw/cla-individual-PyStanfordDependencies.rtf?dl=1).
  Email us if you have any questions about this.

* Fork, then clone the repo:

        git clone git@github.com:your-username/PyStanfordDependencies.git

* Make your changes (please include an update to `CONTRIBUTORS.md`)

* Test your changes with `flake8 StanfordDependencies` and `nosetests` (you will need the `flake8` and `nose` packages. More information is available in the [release checklist][checklist]). If you add new code, please add appropriate testing code as well in `tests/`. See [coveralls][coveralls] for current test coverage.

* Push to your fork. [Travis CI][travisci] will test your changes on various Python versions. If the tests pass, [submit a pull request][pr].

[code of conduct]: https://thoughtbot.com/open-source-code-of-conduct
[issues]: https://github.com/dmcc/PyStanfordDependencies/issues
[helpwanted]: https://github.com/dmcc/PyStanfordDependencies/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22
[checklist]: https://github.com/dmcc/PyStanfordDependencies/blob/master/CHECKLIST.txt
[coveralls]: https://coveralls.io/r/dmcc/PyStanfordDependencies?branch=master
[travisci]: https://travis-ci.org/dmcc/PyStanfordDependencies/
[pr]: https://github.com/dmcc/PyStanfordDepdendencies/compare/
