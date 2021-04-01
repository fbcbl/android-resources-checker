# CHANGELOG

## [UNRELEASED]

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
