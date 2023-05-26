import gzip
import bz2
import lzma
import zlib
import zipfile
import tarfile
import lz4.frame
import brotli

import gzip
import bz2
import lzma
import zlib
import zipfile
import tarfile
import lz4.frame
import brotli

# Compression functions
def compress_gzip(input_file, output_file):
    with open(input_file, 'rb') as data_in:
        with gzip.open(output_file, 'wb') as data_out:
            data_out.writelines(data_in)

def compress_bz2(input_file, output_file):
    with open(input_file, 'rb') as data_in:
        with bz2.BZ2File(output_file, 'wb') as data_out:
            data_out.writelines(data_in)

def compress_lzma(input_file, output_file):
    with open(input_file, 'rb') as data_in:
        with lzma.open(output_file, 'wb') as data_out:
            data_out.writelines(data_in)

def compress_zlib(input_file, output_file):
    with open(input_file, 'rb') as data_in:
        data_out = zlib.compress(data_in.read())
        with open(output_file, 'wb') as f_out:
            f_out.write(data_out)

def compress_zip(input_file, output_file):
    with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_file)

def compress_tar(input_file, output_file):
    with tarfile.open(output_file, 'w:gz') as tarf:
        tarf.add(input_file)

def compress_lz4(input_file, output_file):
    with open(input_file, 'rb') as data_in:
        data_out = lz4.frame.compress(data_in.read())
        with open(output_file, 'wb') as f_out:
            f_out.write(data_out)

def compress_brotli(input_file, output_file):
    with open(input_file, 'rb') as data_in:
        data_out = brotli.compress(data_in.read())
        with open(output_file, 'wb') as f_out:
            f_out.write(data_out)


# List of files to compress
files_to_compress = [
    'output_fft.bin',
    'output_dwt_cA.bin',
    'output_dwt_cD.bin',
    'output_dct.bin',
    'output_dst.bin',
    'fft_dwtcA.bin',
    'fft_dwtcD.bin',
    'fft_dct.bin',
    'fft_dst.bin',
]

# Perform all compressions on all files
for file in files_to_compress:
    compress_gzip(file, file + '.gz')
    compress_bz2(file, file + '.bz2')
    compress_lzma(file, file + '.xz')
    compress_zlib(file, file + '.zlib')
    compress_zip(file, file + '.zip')
    compress_tar(file, file + '.tar.gz')
    compress_lz4(file, file + '.lz4')
    compress_brotli(file, file + '.brotli')
