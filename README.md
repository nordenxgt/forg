# forg

A simple command-line file organizer for cleaning up cluttered directories.

Organize based on the following:
1. File: File extension
2. Date: File creation date
3. Name: File alphabetical name range
4. Size: File size category

## Installation

### 1. Prerequisites

Ensure you have `Python>=3.10` and `pipenv` installed on your system:

Install `pipenv` with:

```sh
pip install pipenv
```

### 2. Clone the Repository

```sh
git clone https://github.com/nordenxgt/forg.git
cd forg
```

### 3. Installation Modes

#### Standard Usage:

Install the package and its runtime dependencies inside the virtual environment:

```sh
pipenv install
```

#### Development:

Install both runtime dependencies and development tools in editable mode (`e .`):

```sh
pipenv install --dev -e .
```

### 4. Usage

1. Activate the virtual environment:

```sh
pipenv shell 
```

2. Run the web scraper (Optional):

`forg` uses `extensions.json` to identify file extensions. If the file is missing or needs to be updated, run the scraper script:

```sh
python scrape_extension.py
```

> Note: The `extensions.json` file covers only the most common file extensions. Feel free to add more extensions as needed. 

3. Run the file organizer

Organize files in a directory using one of the supported modes:

```sh
forg run <directory> -o <file | date | name | size>
```

For example:

```sh
forg run ~/Downloads -o date 
```

### Run Tests:

Make sure `pytest` is installed. If it is not already installed then run the following command:

```sh
pipenv install pytest --dev
```

Then run the test:

```sh
pytest
```

Feel free to look into [tests](tests) directory. 

## Future Improvements
- Add undo Feature
- Handle files with multiple extensions more robustly
- Add detailed logs, information and summaries

## LICENSE

This project is licensed under the [MIT License](LICENSE).