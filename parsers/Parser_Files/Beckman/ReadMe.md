# Vi-Cell XR

## Overview
The `Vi-Cell XR` class is designed to process data from Vi-CELL instruments. It reads a text file containing relevant data, extracts information about results and settings, and creates a combined data structure for further analysis.

## Usage

1. **Installation**:
   - Install the API File Parser library using your preferred package manager:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import beckman
     ```

3. **Parsing API Files**:
   - Use the `parseFile(filePath)` function to read an API file and extract its contents:
     ```
     object = beckman.Vicellxr(path) #path = path of the file
     ```

## Functions

### `get_results()`
- **Description**: A dictionary to store result values and units. Returns a list containing the processed result data. Includes result values, units, run date, and sample ID.
- **Parameters**:
  - `None` 
- **Returns**:
  - `result`:  

### `get_metadata()`
- **Description** : A dictionary to store additional metadata , Returns a dictionary containing metadata related to the Vi-CELL instrument. Includes default metadata and any additional user-defined metadata.
- **Parameters**:
  - `None` 
- **Returns**:
  - `metadata`:   

### `get_settings()`
- **Description** : A dictionary to store instrument settings. Returns a dictionary containing instrument settings.
- **Parameters**:
  - `None` 
- **Returns**:
  - `settings`:   

### `get_combined_data()`
- **Description** : A final combined JSON structure containing metadata, results, and settings. Returns the complete combined data structure.
- **Parameters**:
  - `None` 
- **Returns**:
  - `combined-data` :   

### Example Usage
```python

```