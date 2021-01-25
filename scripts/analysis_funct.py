from os import path
from PyQt5.QtWidgets import QFileDialog


dir_dbc = path.expanduser('~/datasus_dbc/')


def get_shapefile(button, line):
    try:
        filename, _ = QFileDialog.getOpenFileName(button, 'Carregar Arquivo',
                                                  f'{dir_dbc}',
                                                  'File shp (*.shp)')
        line.setEnabled(True)
        line.setText(filename)
    except FileNotFoundError:
        pass


def get_csv(button, line):
    try:
        filename, _ = QFileDialog.getOpenFileName(button, 'Carregar Arquivo',
                                                  f'{dir_dbc}',
                                                  'File csv (*.csv)')
        line.setEnabled(True)
        line.setText(filename)
    except FileNotFoundError:
        pass


def trade_frame(layout, parent, frame):
    parent.setHidden(True)
    frame.setHidden(False)
