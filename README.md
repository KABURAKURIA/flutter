# Flutter App Generator

This repository contains a script to generate multiple Flutter applications with different templates.

## Prerequisites

- [Flutter SDK](https://flutter.dev/docs/get-started/install) installed and in your PATH.
- Python 3 installed.

## Usage

Run the script to generate apps:

```bash
python3 generate_apps.py <number_of_apps> [start_index]
```

Example:

```bash
python3 generate_apps.py 5
# OR for parallel generation
python3 generate_apps.py 50 0 &
python3 generate_apps.py 50 50 &
```

This will create folders: `flutter_app_001`, `flutter_app_002`, etc.

## Templates

The generator currently supports:
1.  **Hello World**: A simple app displaying text.
2.  **Counter**: The standard Flutter counter app.
3.  **Color Changer**: An app that changes background color on tap.

The script cycles through these templates.

## Generated Apps

- `sample_apps.zip`: Contains 3 generated sample apps.
- `flutter_apps_200.zip`: Contains 200 generated apps (apps 001-200).
