# Roche Cedex

## Overview
The `Thermo Fisher OsmoPRO` instrument is an automated osmometer designed for efficient workflows in mid- to high-volume clinical chemistry labs. It features a convenient carousel design that handles up to 20 samples, an intuitive touchscreen interface, and provides fast and accurate osmolality test results.

## Usage

1. **Installation**:
   - Install the API File Parser library using your preferred package manager:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import thermofisher
     ```

3. **Parsing API Files**:
   - Use the `parseFile(filePath)` function to read an API file and extract its contents:
     ```
     object = thermofisher.Osmopro(path) #path = path of the file
     ```

## Functions

### `get_metadata()`
- **Description**: Returns a dictonary containing the metadata data.
- **Parameters**:
  - `None` 
- **Returns**:
  - `metadata`:  

### `get_result()`
- **Description**: Returns a dictonary containing the processed result and osmolality.
- **Parameters**:
  - `None` 
- **Returns**:
  - `result`:  

### Example Usage
```python

```