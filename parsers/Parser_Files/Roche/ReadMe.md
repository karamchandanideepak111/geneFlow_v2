# Roche Cedex

## Overview
The `Roche Cedex` instrument is a bioprocess analyzer designed for cell culture monitoring and fermentation control, providing precise measurements of nutrients, metabolites, and cell morphology. It’s optimized for small throughput workloads, utilizing photometric analysis and ion selective electrodes.
## Usage

1. **Installation**:
   - Install the API File Parser library using your preferred package manager:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import roche
     ```

3. **Parsing API Files**:
   - Use the `parseFile(filePath)` function to read an API file and extract its contents:
     ```
     object = roche.Cedex(path) #path = path of the file
     ```

## Functions

### `get_data()`
- **Description**: Returns a dictonary containing the processed result data.
- **Parameters**:
  - `None` 
- **Returns**:
  - `data`:  

### Example Usage
```python

```