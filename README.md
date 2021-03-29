# Android Resources Check


[![Flake8](https://img.shields.io/badge/codestyle-flake8-yellow)](https://flake8.pycqa.org/en/latest/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/fabiocarballo/android-resources-checker)](https://choosealicense.com/licenses/mit)

## What

This program will inspect the resources of your app and help you understand which ones are not being used and could
potentially be removed.

Main features:

- Identify the unused resources in your android project.
- Identify the unused resources in your android library (when you have a multi-repo setup)
- Listing of the unused resources (name, type and size)
- Deletion of the unused resources

## Using

This program requires Python, supporting from 3.8.X and 3.9.x

## Inspecting your app resources.

Imagining your app in the project `subject-app`, you can trigger the resources inspection by running:

```shell
make standard-inspection --app-path=/path/to/subject-app
```

## License

```
Copyright (c) 2021 Fábio Carballo

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```




