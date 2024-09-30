# Brucker Iconnmr 

## Overview
The `Iconnmr` class is designed to parse Iconnmr set files and extract relevant information. These set files contain data related to NMR (nuclear magnetic resonance) experiments. Below, you'll find documentation for the key methods and functionalities of this class.

## Usage

1. **Installation**:
   - Install the API File Parser library using your preferred package manager:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import brucker
     ```

3. **Parsing API Files**:
   - Use the `parseFile(filePath)` function to read an API file and extract its contents:
     ```
     object = brucker.Iconnmr(path) #path = path of the file
     ```

## Functions

### `get_data()`
- **Description**: Retrieves the parsed data dictionary.
- **Parameters**:
  - `None` 
- **Returns**:
  - `data`:  

### Example Usage
```python

```




# Chromatography Data Parser

The `Chromatography` class is designed to parse data from Empower Chromatography Instrument files. These files contain information related to chromatography experiments. Below, you'll find documentation for the key methods and functionalities of this class.

## Class: `Chromatography`

### Constructor

#### `__init__(self, path: str)`

Initializes the `Chromatography` object with the specified path to the folder containing data files.

- **Parameters**:
  - `path` (str): Absolute path of the folder containing data files.

### Methods

#### `numberOfSamples(self) -> int`

Returns the number of samples in the file.

- **Returns**:
  - `int`: Number of samples.

#### `getSampleInfo(self) -> str`

Returns information about each sample.

- **Returns**:
  - `str`: JSON string containing sample information.

#### `getChannelInfo(self) -> str`

Returns information about all channels.

- **Returns**:
  - `str`: JSON string containing channel information.

#### `getAllData(self) -> str`

Returns all available information from the file, including sample and channel details.

- **Returns**:
  - `str`: JSON string containing comprehensive data.

#### `getImages(self) -> str`

Extracts and saves images from the file.

- **Returns**:
  - `str`: JSON string containing image information.

## Example Usage

```python
# Instantiate a Chromatography object
chromatography_parser = Chromatography("path/to/your/data_folder")

# Retrieve sample information
sample_info = chromatography_parser.getSampleInfo()

# Retrieve channel information
channel_info = chromatography_parser.getChannelInfo()

# Retrieve all available data
all_data = chromatography_parser.getAllData()

# Extract and save images
image_info = chromatography_parser.getImages()
```
```python
# Example usage continued:

# Get the number of samples
num_samples = chromatography_parser.numberOfSamples()

# Print the sample information
print(sample_info)

# Print the channel information
print(channel_info)

# Print all available data
print(all_data)

# Print image information
print(image_info)
```