import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import pywt
from scipy.fftpack import idct, idst
import gzip
import bz2
import lzma
import zlib
import zipfile
import tarfile
import lz4.frame
import brotli

class TransformDecompress:
    def perform_ifft(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = np.fromfile(f, dtype=np.complex64)

        ifft_data = np.fft.ifft(data)

        with open(output_file, 'wb') as f:
            ifft_data.astype(np.float32).tofile(f)

    def perform_idwt(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = np.fromfile(f, dtype=np.float32)

        idwt_data = pywt.idwt(data, None, 'db5')

        with open(output_file, 'wb') as f:
            idwt_data.astype(np.float32).tofile(f)

    def perform_idct(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = np.fromfile(f, dtype=np.float32)

        idct_data = idct(data)

        with open(output_file, 'wb') as f:
            idct_data.astype(np.float32).tofile(f)

    def perform_idst(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = np.fromfile(f, dtype=np.float32)

        idst_data = idst(data)

        with open(output_file, 'wb') as f:
            idst_data.astype(np.float32).tofile(f)

    def perform_none(self, input_file, output_file):
        with open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.write(f_in.read())

    def decompress_none(self, input_file, output_file):
        with open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.write(f_in.read())

    def decompress_gzip(self, input_file, output_file):
        with gzip.open(input_file, 'rb') as data_in:
            with open(output_file, 'wb') as data_out:
                data_out.write(data_in.read())

    def decompress_bz2(self, input_file, output_file):
        with bz2.BZ2File(input_file, 'rb') as data_in:
            with open(output_file, 'wb') as data_out:
                data_out.write(data_in.read())

    def decompress_lzma(self, input_file, output_file):
        with lzma.open(input_file, 'rb') as data_in:
            with open(output_file, 'wb') as data_out:
                data_out.write(data_in.read())

    def decompress_zlib(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            data_out = zlib.decompress(data_in.read())
            with open(output_file, 'wb') as f_out:
                f_out.write(data_out)

    def decompress_zip(self, input_file, output_file):
        with zipfile.ZipFile(input_file, 'r', compression=zipfile.ZIP_DEFLATED) as zipf:
            for file in zipf.namelist():
                zipf.extract(file)
                os.rename(file, output_file)
                break

    def decompress_tar(self, input_file, output_file):
        with tarfile.open(input_file, 'r:gz') as tarf:
            for file in tarf.getnames():
                tarf.extract(file)
                os.rename(file, output_file)
                break

    def decompress_lz4(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            data_out = lz4.frame.decompress(data_in.read())
            with open(output_file, 'wb') as f_out:
                f_out.write(data_out)

    def decompress_brotli(self, input_file, output_file):
        with open(input_file, 'rb') as data_in:
            data_out = brotli.decompress(data_in.read())
            with open(output_file, 'wb') as f_out:
                f_out.write(data_out)

class ProcessingThread(QThread):
    progress_signal = pyqtSignal(int)
    message_signal = pyqtSignal(str)

    def __init__(self, decompress_func, transform_func, input_file, temp_file, output_filename):
        super().__init__()
        self.transform_func = transform_func
        self.decompress_func = decompress_func
        self.input_file = input_file
        self.temp_file = temp_file
        self.output_filename = output_filename

    def run(self):
        self.message_signal.emit("Performing Decompression")
        self.decompress_func(self.input_file, self.temp_file)
        self.progress_signal.emit(50)

        self.message_signal.emit("Performing Transformation")
        self.transform_func(self.temp_file, self.output_filename)
        self.progress_signal.emit(100)

        self.message_signal.emit("Operation Complete")
        print(f"Find object here: {self.output_filename}")  # print the location of the final output file

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Decompress and Detransform'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.select_input_file = QPushButton('Select Input File', self)
        self.select_input_file.clicked.connect(self.showDialog)

        self.select_output_dir = QPushButton('Select Output Directory', self)
        self.select_output_dir.clicked.connect(self.showDialog)

        self.execute_button = QPushButton('Execute', self)
        self.execute_button.clicked.connect(self.execute_decompression_detransformation)

        self.progress_bar = QProgressBar(self)
        self.console_output = QTextEdit(self)
        self.console_output.setReadOnly(True)

        layout = QVBoxLayout()
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

    def execute_decompression_detransformation(self):
        if not hasattr(self, 'input_file') or not self.input_file:
            self.console_output.append("Please select an input file.")
            return

        if not hasattr(self, 'output_directory') or not self.output_directory:
            self.console_output.append("Please select an output directory.")
            return

        # Get decompress type and detransform type from file name
        filename = os.path.basename(self.input_file)
        detransform_type, decompress_type = filename.split("_")[2:4]

        # remove the extension from decompress_type
        decompress_type = decompress_type.split(".")[0]

        temp_file = "temp_decompress_file.bin"

        output_filename = os.path.join(self.output_directory, "decompressed_detransformed.bin")

        tc = TransformCompress()
        transform_func = getattr(tc, f"perform_{detransform_type}")
        decompress_func = getattr(tc, f"decompress_{decompress_type}")

        self.processing_thread = ProcessingThread(decompress_func, transform_func, self.input_file, temp_file, output_filename)
        self.processing_thread.progress_signal.connect(self.progress_bar.setValue)
        self.processing_thread.message_signal.connect(self.console_output.append)
        self.processing_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
