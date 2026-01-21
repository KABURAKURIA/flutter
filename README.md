# Flutter App Generator

This repository contains a script to generate multiple Flutter applications with different templates.

## Prerequisites

- [Flutter SDK](https://flutter.dev/docs/get-started/install) installed and in your PATH.
- Python 3 installed.

## Usage

Run the script to generate apps:

```bash
python3 generate_apps.py <number_of_apps>
```

Example:

```bash
python3 generate_apps.py 5
```

This will create 5 folders: `flutter_app_001`, `flutter_app_002`, etc.

## Templates

The generator currently supports:
1.  **Hello World**: A simple app displaying text.
2.  **Counter**: The standard Flutter counter app.
3.  **Color Changer**: An app that changes background color on tap.

The script cycles through these templates.

## Sample Apps

A zip file `sample_apps.zip` is included containing 3 generated sample apps.
