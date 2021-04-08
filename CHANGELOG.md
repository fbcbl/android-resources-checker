# CHANGELOG

## [UNRELEASED]

# Version 0.0.10

- Specify automatic deletion of unused resources via the `--delete` flag.
- Fixes bugs in deletion that incorrectly deleted entries in file and whole files.

# Version 0.0.9

- Fix bug that was not considering resource names with '0' in the name.
- Fix bug that was not considering all files of the project.

## Version 0.0.8

- Add ability to use it as a validation tool using the `--check` option.
- Specify the type of report using the `--report=(CSV|STDOUT)` (the default is to run all).
- Fixes bug that didn't check for resource usages in the `AndroidManifest.xml`

## Version 0.0.7

- Add inspection to `style` resources.
- Update `LICENSE.md` and `README.md` with due copyright to Dotanuki Labs given that the structure/base of this project
  was highly inspired from [Bitrise Reports](https://github.com/dotanuki-labs/bitrise-reports).

## Version 0.0.6

**2021-04-02**

- Add CSV reports via the `--reports-dir` option.
- Fixes bug that ignored that didn't process resources that are not xml (such as the ones usually placed on `raw`)

## Version 0.0.4

**2021-04-01**

- Add inspection to resources declared as entries (`string`, `color`, `dimen`)
- Renamed `--app-path` to `--app`
- Renamed `--client-path` to `--client`
- Add ability to provide multiple clients.
    * This is done via the `--client` flag; you should use one for each of the clients.

## Version 0.0.3

**2021-03-29**

### Features:

- Identify the unused resources in your android project.
- Identify the unused resources in your android library (when you have a multi-repo setup)
- Listing of the unused resources (name, type and size)
- Deletion of the unused resources
