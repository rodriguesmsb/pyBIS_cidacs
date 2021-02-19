import sys
from os import path, system
import psutil
import webbrowser
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import json


sys.path.append(path.join(path.dirname(__file__), 'SpatialSUSapp'))
dir_spatial = path.join(path.dirname(__file__), 'SpatialSUSapp/conf/')
dir_dbc = path.expanduser('~/datasus_dbc/')


class MyThread(QThread):

    totsignal = pyqtSignal(int)
    cnt = pyqtSignal(int)

    def __init__(self, func, *args):
        super().__init__()
        self.threadactive = True
        self.func = func
        self.args = args

    def stop(self):
        self.threadactive = False
        self.kill()

    def run(self):
        try:
            self.func(*self.args)
        except TypeError:
            self.func()


def load_items(filename, frame):
    data = gpd.read_file(filename)
    combobox_s = [frame.comboBox, frame.comboBox_2, frame.comboBox_3]
    [combobox.clear() for combobox in combobox_s]
    [combobox.addItems(list(data.columns)) for combobox in combobox_s]


def get_shapefile(button):
    filename, _ = QFileDialog.getOpenFileName(button, 'Carregar Arquivo',
                                              f'{dir_dbc}',
                                              'File shp (*.shp)')
    # button.setEnabled(True)
    button.setText(filename)
    try:
        load_items(filename, frame)
    except fiona.errors.DriverError:
        pass


def get_csv(button, line):
    try:
        filename, _ = QFileDialog.getOpenFileName(
            button, 'Carregar Arquivo', f'{dir_dbc}', 'File csv (*.csv)'
        )
        line.setEnabled(True)
        line.setText(filename)
    except FileNotFoundError:
        pass


def trade_frame(layout, parent, frame):
    parent.setHidden(True)
    frame.setHidden(False)


def activate(checkbox, program):

    def write_conf(checkbox):
        with open(dir_spatial + 'conf.json', 'r') as f:
            data = json.load(f)
        with open(dir_spatial + 'conf.json', 'w') as f:
            data["type"] = checkbox
            json.dump(data, f, indent=2)

    if checkbox == "spatio_temporal":
        program.comboBox_2.setEnabled(True)
    elif checkbox == "spatial":
        program.comboBox_2.setEnabled(False)

    write_conf(checkbox)


def start_server(program):
    import index

    def restart_server(thread):
        if thread:
            thread.terminate()
            thread.start()
        else:
            thread.start()

    program.analysis = MyThread(index.app.run_server)
    program.nav = MyThread(webbrowser.open, '127.0.0.1:8050')
    program.nav.moveToThread(program.analysis)
    program.analysis.started.connect(program.nav.run)

    restart_server(program.analysis)
