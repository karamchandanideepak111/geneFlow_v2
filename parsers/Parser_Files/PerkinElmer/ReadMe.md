# PerkinElmer DropSense96

## Overview
The `DropSense96` is a system designed for the quantification of microliter samples, offering detailed analysis of DNA and protein concentrations, built-in calibration features, and rapid UV/VIS measurements. It's widely used in applications such as nucleic acids, oligo measurements, proteins, and general UV/Vis and standard curve. It's known for its reliability and extensive options for experimental setup.
## Usage

1. **Installation**:
   - Install the API File Parser library using your preferred package manager:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import perkinelmer
     ```

3. **Parsing API Files**:
   - Use the `parseFile(filePath)` function to read an API file and extract its contents:
     ```
     object = perkinelmer.Dropsense96(path) #path = path of the file
     ```

## Functions

### `get_info(self)`
- **Description**: Retrieves the basic information from the file.
- **Parameters**: None
- **Returns**:
  - `info`: A JSON string containing the extracted data.

### `get_plateNum(self)`
- **Description**: Retrieves the number of unique plates.
- **Parameters**: None
- **Returns**:
  - `plate count`: A JSON string containing the number of unique plates.

### `get_plateId(self)`
- **Description**: Retrieves the unique plate IDs.
- **Parameters**: None
- **Returns**:
  - `ID`: A JSON string containing unique plate IDs.

### `get_plateInfo(self, plateId)`
- **Description**: Retrieves the plate details by providing Plate ID.
- **Parameters**:
  - `plateId`: The ID of the plate.
- **Returns**:
  - `plate info`: A JSON string containing the plate details.

### `get_allPlateInfo(self)`
- **Description**: Retrieves all plate details.
- **Parameters**: None
- **Returns**:
  - `plates`: A JSON string containing all plate details. 

### Example Usage
```python

```


# PerkinElmer DropSense96

## Overview
The `DropSense96` is a system designed for the quantification of microliter samples, offering detailed analysis of DNA and protein concentrations, built-in calibration features, and rapid UV/VIS measurements. It's widely used in applications such as nucleic acids, oligo measurements, proteins, and general UV/Vis and standard curve. It's known for its reliability and extensive options for experimental setup.
## Usage

1. **Installation**:
   - Install the API File Parser library using your preferred package manager:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import perkinelmer
     ```

3. **Parsing API Files**:
   - Use the `parseFile(filePath)` function to read an API file and extract its contents:
     ```
     object = perkinelmer.Dropsense96(path) #path = path of the file
     ```

## Functions

### `get_plateInfo(self)`
- **Description**: Fetches Plate Information from the file.
- **Parameters**: None
- **Returns**:
  - `info`: A JSON string containing the plate information. 

### `get_backgound(self)`
- **Description**: Fetches Background Information from the file.
- **Parameters**: None
- **Returns**:
   - `background`: A JSON string containing the background information. 

### `get_allPlateInfo(self)`
- **Description**: Fetches All Plate Details from the file.
- **Parameters**: None
- **Returns**:
   - `plates info`: A JSON string containing all the plate details. 

### `get_basicAssayInfo(self)`
- **Description**: Fetches Basic Assay Information from the file.
- **Parameters**: None
- **Returns**:
   - `assay info`: A JSON string containing the basic assay information. 

### `get_protocolInfo(self)`
- **Description**: Fetches Protocol Information from the file.
- **Parameters**: None
- **Returns**:
   - `protocol`: A JSON string containing the protocol information. 

### `get_plateTypeInfo(self)`
- **Description**: Fetches Plate Type Information from the file.
- **Parameters**: None
- **Returns**:
   - `plate type`: A JSON string containing the plate type information. 

### `get_autoExportParaInfo(self)`
- **Description**: Fetches Auto Export Parameters Information from the file.
- **Parameters**: None
- **Returns**:
   - `export parameters`: A JSON string containing the auto export parameters information. 

### `get_operationInfo(self)`
- **Description**: Fetches Operations Information from the file.
- **Parameters**: None
- **Returns**:
   - `operation`: A JSON string containing the operations information. 

### `get_labelInfo(self)`
- **Description**: Fetches Label Information from the file.
- **Parameters**: None
- **Returns**:
   - `label`: A JSON string containing the label information. 

### `get_filterInfo(self)`
- **Description**: Fetches Filter Information from the file.
- **Parameters**: None
- **Returns**:
   - `filter`: A JSON string containing the filter information. 

### `get_mirrorModuleInfo(self)`
- **Description**: Fetches Mirror Module Information from the file.
- **Parameters**: None
- **Returns**:
   - `mirror module`: A JSON string containing the mirror module information. 

### `get_instrumentInfo(self)`
- **Description**: Fetches Instrument Information from the file.
- **Parameters**: None
- **Returns**:
   - `instrument`: A JSON string containing the instrument information. 

## Example Usage
```python

```