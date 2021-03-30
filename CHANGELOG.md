# CHANGELOG

## [UNRELEASED]
### Resolve paths on arguments.
You can now pass relative paths in arguments like this:

```shell
android-resources-checker --app-path=../../my-project
```

## Version 0.0.3
**2021-03-29**

### Features:

- Identify the unused resources in your android project.
- Identify the unused resources in your android library (when you have a multi-repo setup)
- Listing of the unused resources (name, type and size)
- Deletion of the unused resources
