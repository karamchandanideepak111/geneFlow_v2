# Agilent

## Overview

### Agilent ChemStation File:
The Agilent ChemStation is a software platform used for data acquisition, processing, and analysis in analytical chemistry. It’s commonly employed in high-performance liquid chromatography (HPLC) and other analytical techniques.
ChemStation files store various types of data generated during experiments, including raw chromatograms, spectral data, and logbook entries.

- File Formats:
ChemStation files come in several formats:
  - **.ch (ChemStation Raw Data)**: These files contain raw chromatographic data, including retention times, peak areas, and detector responses. They are generated during HPLC runs.
  - **.ms (Mass Spectrometry Data)**: These files store mass spectrometry data, such as mass spectra, ion intensities, and mass-to-charge ratios. They are associated with mass spectrometers.
  - **.uv (Ultraviolet-Visible Spectroscopy Data)**: UV spectra, absorbance values, and wavelength information are stored in these files. They are used in UV-visible spectroscopy experiments.
  - **.D (Data Folder)**: ChemStation organizes related files into folders with the .D extension. These folders contain various data files, including .ch, .ms, and .uv files.

## Usage

1. **Installation**:
   - Install the API File Parser library using your preferred package manager:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import agilent
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
