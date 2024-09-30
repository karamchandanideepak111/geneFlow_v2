# MassLynx

## Overview

### Masslynx Waters File:
A Waters instrument file with the extension .raw is associated with MassLynx, a software platform used for mass spectrometry data analysis. Let’s delve into the details:

Purpose and Content:
The .raw file contains raw mass spectral information acquired during mass spectrometry experiments.
It encompasses data related to ion intensities, m/z values, retention times, and other relevant parameters.
Data Acquisition:
Researchers use Waters instruments (such as liquid chromatography-mass spectrometers) to collect raw data during experiments.
The .raw file stores this data in its unprocessed form, directly from the instrument.
File Structure:
A typical .raw file consists of several components:
Header Information: Describes the instrument settings, acquisition parameters, and sample details.
Spectral Data: Contains the actual mass spectra (intensity vs. m/z) acquired during the experiment.
Chromatographic Data: If coupled with chromatography, this section includes retention time information.
Other Metadata: Additional information related to the experiment.

It may be useful to search for a binary format by detector.

| Detector | Formats |
| --- | --- |
| UV | Waters CHRO .DAT <br> Waters FUNC .IDX <br> Waters FUNC .DAT (6-byte) |
| MS | Waters FUNC .IDX <br> Waters FUNC .DAT (2-byte) <br> Waters FUNC .DAT (6-byte) <br> Waters FUNC .DAT (8-byte) |
| CAD | Waters CHRO .DAT |
| ELSD | Waters CHRO .DAT |

## Usage

1. **Installation**:
     ```
     pip install 
     ```

2. **Import the Library**:
   - In your project, import the API File Parser module:
     ```
     import waters
     ```

3. **Parsing API Files**:
   - Use the `parseFile(filePath)` function to read an API file and extract its contents:
     ```
     object = waters.Waters(path) #path = path of the file
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
