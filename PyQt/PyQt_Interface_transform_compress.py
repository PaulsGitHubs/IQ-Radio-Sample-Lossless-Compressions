import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLabel, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import pywt
from scipy.fftpack import dct, dst
import gzip
import bz2
import lzma
import zlib
import zipfile
import tarfile
import lz4.frame
import brotli

class TransformCompress:
    def perform_fft(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = np.fromfile(f, dtype=np.float32)

        fft_data = np.fft.fft(data)

        with open(output_file, 'wb') as f:
            fft_data.astype(np.complex64).tofile(f)

    def perform_dwt(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = np.fromfile(f, dtype=np.float32)

        dwt_data = pywt.dwt(data, 'db5')

        with open(output_file, 'wb') as f:
            dwt_data[0].astype(np.float32).tofile(f)

    def perform_dct(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = np.fromfile(f, dtype=np.float32)

        dct_data = dct(data)

        with open(output_file, 'wb') as f:
            dct_data.astype(np.float32).tofile(f)

    def perform_dst(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = np.fromfile(f, dtype=np.float32)

        dst_data = dst(data)

        with open(output_file, 'wb') as f:
        
            dst_data.astype(np.float32).tofile(f)
    def perform_none(self, input_file, output_file):
        with open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.write(f_in.read())

    def compress_none(self, input_file, output_file):
        with open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.write(f_in.read())
                
    def compress_gzip(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            with gzip.open(output_file, 'wb') as data_out:
                data_out.writelines(data_in)

    def compress_bz2(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            with bz2.BZ2File(output_file, 'wb') as data_out:
                data_out.writelines(data_in)

    def compress_lzma(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            with lzma.open(output_file, 'wb') as data_out:
                data_out.writelines(data_in)

    def compress_zlib(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            data_out = zlib.compress(data_in.read())
            with open(output_file, 'wb') as f_out:
                f_out.write(data_out)

    def compress_zip(self, input_file, output_file):
        with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(input_file)

    def compress_tar(self, input_file, output_file):
        with tarfile.open(output_file, 'w:gz') as tarf:
            tarf.add(input_file)

    def compress_lz4(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            data_out = lz4.frame.compress(data_in.read())
            with open(output_file, 'wb') as f_out:
                f_out.write(data_out)

    def compress_brotli(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            data_out = brotli.compress(data_in.read())
            with open(output_file, 'wb') as f_out:
                f_out.write(data_out)


class ProcessingThread(QThread):
    progress_signal = pyqtSignal(int)
    message_signal = pyqtSignal(str)

    def __init__(self, transform_func, compress_func, input_file, temp_file, output_filename):
        super().__init__()
        self.transform_func = transform_func
        self.compress_func = compress_func
        self.input_file = input_file
        self.temp_file = temp_file
        self.output_filename = output_filename

    def run(self):
        self.message_signal.emit("Performing Transformation")
        self.transform_func(self.input_file, self.temp_file)
        self.progress_signal.emit(50)

        self.message_signal.emit("Performing Compression")
        self.compress_func(self.temp_file, self.output_filename)
        self.progress_signal.emit(100)

        self.message_signal.emit("Operation Complete")
        print(f"Find object here: {self.output_filename}")  # print the location of the final output file



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Transform and Compress'
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        
        self.transform_type = QComboBox(self)
        self.transform_type.addItem("None")  # Added "None" option
        self.transform_type.addItem("FFT (makes file larger)")
        self.transform_type.addItem("DWT (splits into 2 files)")
        self.transform_type.addItem("DCT (Recommended)")
        self.transform_type.addItem("DST (Recommended)")

        self.compress_type = QComboBox(self)
        self.compress_type.addItem("None")  # Added "None" option
        self.compress_type.addItem("gzip")
        self.compress_type.addItem("bz2")
        self.compress_type.addItem("lzma (Recommended)")
        self.compress_type.addItem("zlib")
        self.compress_type.addItem("zip")
        self.compress_type.addItem("tar")
        self.compress_type.addItem("lz4")
        self.compress_type.addItem("brotli (Recommended)")

        self.select_input_file = QPushButton('Select Input File', self)
        self.select_input_file.clicked.connect(self.showDialog)

        self.select_output_dir = QPushButton('Select Output Directory', self)
        self.select_output_dir.clicked.connect(self.showDialog)

        self.execute_button = QPushButton('Execute', self)
        self.execute_button.clicked.connect(self.execute_transformation_compression)

        self.progress_bar = QProgressBar(self)
        self.console_output = QTextEdit(self)
        self.console_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Transformation Type"))
        layout.addWidget(self.transform_type)
        layout.addWidget(QLabel("Select Compression Type"))
        layout.addWidget(self.compress_type)
        layout.addWidget(self.select_input_file)
        layout.addWidget(self.select_output_dir)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.console_output)
        
        self.setLayout(layout)

    def showDialog(self):
        sender = self.sender()
        if sender.text() == 'Select Input File':
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
            self.input_file = fname[0]
            self.console_output.append(f"Input File: {self.input_file}")
        elif sender.text() == 'Select Output Directory':
            dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory', '/home')
            self.output_directory = dir
            self.console_output.append(f"Output Directory: {self.output_directory}")

    def execute_transformation_compression(self):
        if not hasattr(self, 'input_file') or not self.input_file:
            self.console_output.append("Please select an input file.")
            return

        if not hasattr(self, 'output_directory') or not self.output_directory:
            self.console_output.append("Please select an output directory.")
            return

        # Get selected transform and compress types
        transform_type = self.transform_type.currentText().lower()
        compress_type = self.compress_type.currentText().lower()

        # remove the "(recommended)" suffix if it exists
        transform_type = transform_type.split(" ")[0]
        compress_type = compress_type.split(" ")[0]

        # Set the extension of output file based on compression type
        extensions = {"gzip": ".bin.gz", "bz2": ".bin.bz2", "lzma": ".bin.lzma", 
              "zlib": ".bin.zip", "zip": ".bin.zip", "tar": ".bin.tar", 
              "lz4": ".bin.lz4", "brotli": ".bin.brotli", "none": ".bin"}

        # Create output filename using transformation type and appropriate extension
        output_filename = f'output_file_{transform_type}{extensions[compress_type]}'
        output_filename = os.path.join(self.output_directory, output_filename)

        # Create output filename using transformation type and appropriate extension
        output_filename = f'output_file_{transform_type}{extensions[compress_type]}'
        output_filename = os.path.join(self.output_directory, output_filename)

        tc = TransformCompress()
        transform_func = getattr(tc, f"perform_{transform_type}")
        compress_func = getattr(tc, f"compress_{compress_type}")

        temp_file = "temp_transform_file.bin"

        self.processing_thread = ProcessingThread(transform_func, compress_func, self.input_file, temp_file, output_filename)
        self.processing_thread.progress_signal.connect(self.progress_bar.setValue)
        self.processing_thread.message_signal.connect(self.console_output.append)
        self.processing_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
