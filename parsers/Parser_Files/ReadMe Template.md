# Vendor Instrument

## Overview

About the Instrument


## Usage

1. **Installation**:
   - Install the API File Parser library using your preferred package manager:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import <vendor name>
     ```

3. **Parsing API Files**:
   - Use the `parseFile(filePath)` function to read an API file and extract its contents:
     ```
     object = agilent.Chemstation(path) #path = path of the file
     ```

4. **Accessing API Data**:
   - The parsed data includes essential information such as endpoints, methods, parameters, and responses.
   - Example:
     ```
     cobject.get_data()
     // Output: {'data' : [ <Data> ] }
     ```

## Functions

### `get_data()`
- **Description**: Get all Data present in 2D list
- **Parameters**:
  - `None` 
- **Returns**:
  - `data`: A 2D Array with all the data values in int/float

### `get_xlabels()`
- **Description**: Get the X-labels Values
- **Parameters**:
  - `None` 
- **Returns**:
  - `xlabel`: An Array with x-label values in int/float

### `get_ylabels()`
- **Description**: Get the Y-labels Values
- **Parameters**:
  - `None` 
- **Returns**:
  - `ylabel`: An Array with y-label values in int/float

### `get_metadata()`
- **Description**: Get the Metadata of the file
- **Parameters**:
  - `None` 
- **Returns**:
  - `metadata`: 
