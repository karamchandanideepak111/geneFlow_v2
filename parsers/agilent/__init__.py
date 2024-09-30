import struct
import os
import numpy as np
import json


class Chemstation:
    def __init__(self, path, prec=None):
        try:
            r_data = self.read(path, prec)
            self.name = r_data['name']
            self.xlabel = r_data['xlabel'].tolist()
            self.ylabel = r_data['ylabel'].tolist()
            self.data = r_data['data'].tolist()
            self.metadata = r_data['metadata']
            self.detector = r_data['detector']
        except Exception as e:
            print(f"An error occurred while reading data: {e}")
            # Handle the error here (e.g., log it, display a message, etc.)

    def read(self, path, prec=None):
        ext = path.split(".")[1]
        if ext == "ch" or ext == "CH":
            return self.__parse_ch(path)
        elif ext == "ms" or ext == "MS":
            return self.__parse_ms(path, prec)
        elif ext == "uv" or ext == "UV":
            return self.__parse_uv(path)
        else:
            return {"data": None}

    def get_data(self):
        return json.dumps({'data': self.data})

    def get_xlabels(self):
        return json.dumps({'xlabel': self.xlabel})

    def get_ylabels(self):
        return json.dumps({'ylabel': self.ylabel})

    def get_metadata(self):
        return json.dumps({'metadata': self.metadata})

    def __read_string(self, f, offset, gap=2):
        f.seek(offset)
        str_len = struct.unpack("<B", f.read(1))[0] * gap
        try:
            return f.read(str_len)[::gap].decode().strip()
        except Exception:
            return ""

    def __read_header(self, f, offsets, gap=2):
        metadata = {}
        for key, offset in offsets.items():
            string = self.__read_string(f, offset, gap)
            if string:
                metadata[key] = string
        return metadata

    def __parse_ch(self, path):
        head = ""
        with open(path, 'rb') as f:
            head = self.__read_string(f, offset=0, gap=1)
            if head in ['179', '181']:
                return self.__parse_ch_fid(path, head)
            elif head in ['130', '30']:
                return self.__parse_ch_other(path, head)
            else:
                return "None"
        f.close()

    def __parse_ch_fid(self, path, head):
        global metadata_offsets
        if head == '181':
            data_offsets = {
                'num_times': 0x116,
                'scaling_factor': 0x127C,
                'data_start': 0x1800
            }
            metadata_offsets = {
                'notebook': 0x35A,
                'date': 0x957,
                'method': 0xA0E,
                'instrument': 0xC11,
                'unit': 0x104C,
            }
            gap = 2
        elif head == '179':
            data_offsets = {
                'num_times': 0x116,
                'scaling_factor': 0x127C,
                'data_start': 0x1800
            }
            metadata_offsets = {
                'notebook': 0x35A,
                'date': 0x957,
                'method': 0xA0E,
                'instrument': 0xC11,
                'unit': 0x104C,
                'signal': 0x1075
            }
        f = open(path, 'rb')
        raw_bytes = f.read()
        file_size = f.tell()

        # Extract the number of retention times.
        num_times = (file_size - data_offsets['data_start']) // 8

        f.seek(data_offsets['num_times'] + 4)
        # Compute retention times using the first and last times.
        start_time = struct.unpack(">f", f.read(4))[0]
        end_time = struct.unpack(">f", f.read(4))[0]
        delta_time = (end_time - start_time) / (num_times - 1)
        times = np.arange(start_time, end_time + 1e-3, delta_time)
        # Extract the raw data values.
        if head == '181':
            data = np.array(self.__decode_double_delta(f, data_offsets['data_start']), dtype=np.float64)
        else:
            data = np.ndarray(num_times, '<d', raw_bytes, data_offsets['data_start'], 8)
        data = data.copy().reshape(-1, 1)
        # Convert times into minutes.
        times /= 60000

        # Scale the absorbances.
        f.seek(data_offsets['scaling_factor'])
        scaling_factor = struct.unpack('>d', f.read(8))[0]
        data *= scaling_factor

        # No ylabel for FID data.
        ylabels = np.array([''])

        # Extract metadata from file header.
        metadata = self.__read_header(f, metadata_offsets)
        f.close()

        r_data = {
            'name': os.path.basename(path),
            'detector': 'FID',
            'xlabel': times,  # Convert numpy arrays to lists
            'ylabel': ylabels,  # Convert numpy arrays to lists
            'data': data,  # Convert numpy arrays to lists
            'metadata': metadata
        }
        return r_data

        # Read Absorbance

    def __parse_ch_other(self, path, head):
        if head == '130':
            data_offsets = {
                'time_range': 0x11A,
                'scaling_factor': 0x127C,
                'data_start': 0x1800
            }
            metadata_offsets = {
                'notebook': 0x35A,
                'date': 0x957,
                'method': 0xA0E,
                'instrument': 0xC11,
                'unit': 0x104C,
                'signal': 0x1075
            }
            gap = 2
        elif head == '30':
            data_offsets = {
                'time_range': 0x11A,
                'scaling_factor': 0x284,
                'data_start': 0x400
            }
            metadata_offsets = {
                'notebook': 0x18,
                'date': 0xB2,
                'method': 0xE4,
                'instrument': 0xDA,
                'unit': 0x244,
                'signal': 0x254
            }
            gap = 1
        else:
            return None

        f = open(path, 'rb')
        data = np.array(self.__decode_delta(f, data_offsets['data_start']))
        num_times = data.size
        if num_times == 0:
            return None

        # Calculate retention times using the first and last times.
        f.seek(data_offsets['time_range'])
        start_time, end_time = struct.unpack('>ii', f.read(8))
        delta_time = (end_time - start_time) / (num_times - 1)
        times = np.arange(start_time, end_time + 1e-3, delta_time)

        # Convert time to minutes
        times /= 60000

        # Process the absorbances.
        f.seek(data_offsets['scaling_factor'])
        scaling_factor = struct.unpack('>d', f.read(8))[0]
        data = data.reshape(-1, 1) * scaling_factor

        # Read file metadata.

        metadata = self.__read_header(f, metadata_offsets, gap=gap)
        f.close()

        # Determine the detector and ylabels using metadata.
        detector = None
        ylabel = ''
        signal = metadata['signal']
        if '=' in signal:
            ylabel = signal.split('=')[1].split(',')[0]
            detector = 'UV'
        elif 'ADC' in signal:
            detector = 'ELSD' if 'CHANNEL' in signal else 'CAD'
        ylabels = np.array([ylabel])

        r_data = {
            'name': os.path.basename(path),
            'detector': detector,
            'xlabel': times,
            'ylabel': ylabels,
            'data': data,
            'metadata': metadata
        }
        return r_data

    def __decode_delta(self, f, offset):
        byte_unpack = struct.Struct('>B').unpack
        short_unpack = struct.Struct('>h').unpack
        int_unpack = struct.Struct('>i').unpack
        # Extract the raw data values.
        # Count the total number of retention times.
        f.seek(offset)
        absorbances = []
        absorb_accum = 0
        while True:
            # If the segment header is invalid, stop reading.
            head = byte_unpack(f.read(1))[0]
            if head != 0x10:
                break
            num_times_seg = byte_unpack(f.read(1))[0]
            # If the next short is equal to -0x8000
            #     then the next absorbance value is the next integer.
            # Otherwise, the short is a delta from the last absorbance value.
            for _ in range(num_times_seg):
                check_int = short_unpack(f.read(2))[0]
                if check_int == -0x8000:
                    absorb_accum = int_unpack(f.read(4))[0]
                else:
                    absorb_accum += check_int
                absorbances.append(absorb_accum)
            return absorbances

    def __decode_double_delta(self, f, offset):
        short_unpack = struct.Struct('>h').unpack
        int_unpack = struct.Struct('>i').unpack
        f.seek(0, 2)
        file_size = f.tell()
        f.seek(offset)
        signals = []
        buffer = [0, 0, 0]
        while f.tell() < file_size:
            buffer[2] = short_unpack(f.read(2))[0]
            if buffer[2] == 0x7fff:
                buffer[0] = short_unpack(f.read(2))[0] << 32 | int_unpack(f.read(4))[0]
                buffer[1] = 0
            else:
                buffer[1] += buffer[2]
                buffer[0] += buffer[1]
            signals.append(buffer[0])
        return signals

    def __parse_ms_partial(self, path, prec=0):
        f = open(path, 'rb')
        short_unpack = struct.Struct('>H').unpack
        int_unpack = struct.Struct('>I').unpack

        # Partial .ms files do not store the start offset.
        # Shallow validation of filetype by checking that offset is null.
        f.seek(0x10A)
        if short_unpack(f.read(2))[0] != 0:
            f.close()
            return None

        # The start offset for data in .ms files is technically variable,
        #     but it has been constant for every .ms file we have tested.
        # Since the start offset is not stored in partials, this code uses that
        #     "constant" common starting offset. It may not work in all cases.
        f.seek(0x2F2)

        # Extract retention times and data pair counts for each time.
        # Store the bytes holding mz-intensity pairs.
        times = []
        pair_counts = []
        pair_bytearr = bytearray()
        while True:
            try:
                f.read(2)
                time = int_unpack(f.read(4))[0]
                f.read(6)
                pair_count = short_unpack(f.read(2))[0]
                f.read(4)
                pair_bytes = f.read(pair_count * 4)
                f.read(10)
                times.append(time)
                pair_counts.append(pair_count)
                pair_bytearr.extend(pair_bytes)
            except Exception:
                break

        raw_bytes = bytes(pair_bytearr)
        times = np.array(times) / 60000
        pair_counts = np.array(pair_counts)
        num_times = times.size
        total_paircount = np.sum(pair_counts)
        mzs = np.ndarray(total_paircount, '>H', raw_bytes, 0, 4)
        mzs = np.round(mzs / 20, prec)
        int_encs = np.ndarray(total_paircount, '>H', raw_bytes, 2, 4)
        int_heads = int_encs >> 14
        int_tails = int_encs & 0x3fff
        int_values = np.multiply(8 ** int_heads, int_tails, dtype=np.uint32)
        del int_encs, int_heads, int_tails, raw_bytes
        ylabels = np.unique(mzs)
        ylabels.sort()
        mz_indices = np.searchsorted(ylabels, mzs)
        data = np.zeros((num_times, ylabels.size), dtype=np.uint32)
        cur_index = 0
        for i in range(num_times):
            stop_index = cur_index + pair_counts[i]
            np.add.at(
                data[i],
                mz_indices[cur_index:stop_index],
                int_values[cur_index:stop_index])
            cur_index = stop_index
        del mz_indices, mzs, int_values, pair_counts
        metadata_offsets = {
            'date': 0xB2,
            'method': 0xE4
        }
        metadata = self.__read_header(f, metadata_offsets, 1)
        f.close()
        r_data = {
            'name': os.path.basename(path),
            'detector': 'MS',
            'xlabel': times,
            'ylabel': ylabels,
            'data': data,
            'metadata': metadata
        }
        return r_data

    def __parse_ms(self, path, prec=0):
        data_offsets = {
            'type': 0x4,
            'data_start': 0x10A,
            'lc_num_times': 0x116,
            'gc_num_times': 0x142
        }
        f = open(path, 'rb')
        short_unpack = struct.Struct('>H').unpack
        int_unpack = struct.Struct('>I').unpack
        head = int_unpack(f.read(4))[0]
        if head != 0x01320000:
            f.close()
            return self.__parse_ms_partial(path, prec)
        type_ms = self.__read_string(f, data_offsets['type'], 1)
        if type_ms == "MSD Spectral File":
            f.seek(data_offsets['lc_num_times'])
            num_times = int_unpack(f.read(4))[0]
        else:
            f.seek(data_offsets['gc_num_times'])
            num_times = struct.unpack('<I', f.read(4))[0]
        f.seek(data_offsets['data_start'])
        f.seek(short_unpack(f.read(2))[0] * 2 - 2)
        times = np.empty(num_times, dtype=np.uint32)
        pair_counts = np.zeros(num_times, dtype=np.uint16)
        pair_bytearr = bytearray()
        for i in range(num_times):
            f.read(2)
            times[i] = int_unpack(f.read(4))[0]
            f.read(6)
            pair_counts[i] = short_unpack(f.read(2))[0]
            f.read(4)
            pair_bytes = f.read(pair_counts[i] * 4)
            pair_bytearr.extend(pair_bytes)
            f.read(10)
        raw_bytes = bytes(pair_bytearr)
        times = times / 60000
        total_paircount = np.sum(pair_counts)
        mzs = np.ndarray(total_paircount, '>H', raw_bytes, 0, 4)
        mzs = np.round(mzs / 20, prec)
        int_encs = np.ndarray(total_paircount, '>H', raw_bytes, 2, 4)
        int_heads = int_encs >> 14
        int_tails = int_encs & 0x3fff
        int_values = np.multiply(8 ** int_heads, int_tails, dtype=np.uint32)
        del int_encs, int_heads, int_tails, raw_bytes
        ylabels = np.unique(mzs)
        ylabels.sort()
        mz_indices = np.searchsorted(ylabels, mzs)
        data = np.zeros((num_times, ylabels.size), dtype=np.uint32)
        cur_index = 0
        for i in range(num_times):
            stop_index = cur_index + pair_counts[i]
            np.add.at(
                data[i],
                mz_indices[cur_index:stop_index],
                int_values[cur_index:stop_index])
            cur_index = stop_index
        del mz_indices, mzs, int_values, pair_counts
        metadata_offsets = {
            'date': 0xB2,
            'method': 0xE4
        }
        metadata = self.__read_header(f, metadata_offsets, 1)
        f.close()
        r_data = {
            'name': os.path.basename(path),
            'detector': 'MS',
            'xlabel': times,
            'ylabel': ylabels,
            'data': data,
            'metadata': metadata
        }
        return r_data

    def __decode_uv_delta(self, f, data_offsets, num_times, num_wavelengths):
        uint_unpack = struct.Struct('<I').unpack
        int_unpack = struct.Struct('<i').unpack
        short_unpack = struct.Struct('<h').unpack
        f.seek(data_offsets["data_start"])
        times = np.empty(num_times, dtype=np.uint32)
        data = np.empty((num_times, num_wavelengths), dtype=np.int64)
        for i in range(num_times):
            f.read(4)
            times[i] = uint_unpack(f.read(4))[0]
            f.read(14)
            absorb_accum = 0
            for j in range(num_wavelengths):
                check_int = short_unpack(f.read(2))[0]
                if check_int == -0x8000:
                    absorb_accum = int_unpack(f.read(4))[0]
                else:
                    absorb_accum += check_int
                data[i, j] = absorb_accum

        return times, data

    def __parse_uv_partial(self, path):
        data_offsets = {
            'num_times': 0x116,
            'scaling_factor': 0xC0D,
            'data_start': 0x1000
        }
        f = open(path, 'rb')
        uint_unpack = struct.Struct('<I').unpack
        int_unpack = struct.Struct('<i').unpack
        short_unpack = struct.Struct('<h').unpack
        f.seek(data_offsets["data_start"] + 0x8)
        try:
            start_wlen, end_wlen, delta_wlen = \
                tuple(num // 20 for num in struct.unpack("<HHH", f.read(6)))
            wavelengths = np.arange(start_wlen, end_wlen + 1, delta_wlen)
        except Exception:
            return None
        f.seek(data_offsets['data_start'])
        times = []
        absorbances = []
        while True:
            try:
                f.read(4)
                time = uint_unpack(f.read(4))[0]
                times.append(time)
                f.read(14)
                absorb_accum = 0
                for _ in range(wavelengths.size):
                    check_int = short_unpack(f.read(2))[0]
                    if check_int == -0x8000:
                        absorb_accum = int_unpack(f.read(4))[0]
                    else:
                        absorb_accum += check_int
                    absorbances.append(absorb_accum)
            except Exception:
                break
        times = np.array(times) / 60000
        data = np.array(absorbances).reshape((times.size, wavelengths.size))
        f.seek(data_offsets['scaling_factor'])
        scaling_factor = struct.unpack('>d', f.read(8))[0]
        data = data * scaling_factor
        metadata_offsets = {
            "notebook": 0x35A,
            "date": 0x957,
            "method": 0xA0E,
            "unit": 0xC15,
            "signal": 0xC40,
            "vialpos": 0xFD7
        }
        metadata = self.__read_header(f, metadata_offsets)
        f.close()
        r_data = {
            'name': os.path.basename(path),
            'detector': 'UV',
            'xlabel': times,
            'ylabel': wavelengths,
            'data': data,
            'metadata': metadata
        }
        return r_data

    def __decode_uv_array(self, f, data_offsets, num_times, num_wavelengths):
        uint_unpack = struct.Struct('<I').unpack
        f.seek(data_offsets["data_start"])
        times = np.empty(num_times, dtype=np.uint32)
        data = np.empty((num_times, num_wavelengths), dtype=np.float64)
        for i in range(num_times):
            f.read(4)
            times[i] = uint_unpack(f.read(4))[0]
            f.read(14)
            for j in range(num_wavelengths):
                data[i, j] = struct.unpack('<d', f.read(8))[0]
        return times, data

    def __parse_uv(self, path):
        f = open(path, 'rb')
        head = self.__read_string(f, 0, gap=1)
        if head == '131':
            data_offsets = {
                'num_times': 0x116,
                'scaling_factor': 0xC0D,
                'data_start': 0x1000
            }
            metadata_offsets = {
                "notebook": 0x35A,
                "date": 0x957,
                "method": 0xA0E,
                "unit": 0xC15,
                "signal": 0xC40,
                "vialpos": 0xFD7
            }
            file_type = self.__read_string(f, 347, gap=2)
            if file_type.startswith('LC'):
                decode = self.__decode_uv_delta
            elif file_type.startswith('OL'):
                decode = self.__decode_uv_array
            else:
                return None
            gap = 2
        elif head == '31':
            data_offsets = {
                'num_times': 0x116,
                'scaling_factor': 0x13E,
                'data_start': 0x200
            }
            metadata_offsets = {
                "notebook": 0x18,
                "date": 0xB2,
                "method": 0xE4,
                "unit": 0x146
            }
            decode = self.__decode_uv_delta
            gap = 1
        else:
            f.close()
            return None
        f.seek(data_offsets["num_times"])
        num_times = struct.unpack(">I", f.read(4))[0]
        if num_times == 0:
            f.close()
            return self.__parse_uv_partial(path)
        f.seek(data_offsets["data_start"] + 0x8)
        start_wlen, end_wlen, delta_wlen = \
            tuple(num // 20 for num in struct.unpack("<HHH", f.read(6)))
        wavelengths = np.arange(start_wlen, end_wlen + 1, delta_wlen)
        num_wavelengths = wavelengths.size
        times, data = decode(f, data_offsets, num_times, num_wavelengths)
        times = times / 60000
        f.seek(data_offsets['scaling_factor'])
        scaling_factor = struct.unpack('>d', f.read(8))[0]
        data = data * scaling_factor
        metadata = self.__read_header(f, metadata_offsets, gap=gap)
        f.close()
        r_data = {
            'name': os.path.basename(path),
            'detector': 'UV',
            'xlabel': times,
            'ylabel': wavelengths,
            'data': data,
            'metadata': metadata
        }
        return r_data
