from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QMenuBar, \
    QTableView
from PySide6.QtCore import Qt, QSize, QAbstractTableModel
import nfl_data_py as nfl

from nfl_data import team_names


def years():
    nfl_years = []

    stat_years = list(range(1999, 2025))
    stat_years.sort(reverse=True)

    for i in stat_years:
        nfl_years.append(str(i))

    return nfl_years

def weekly_data(year: int):
    data = nfl.import_weekly_data([year],
                                  columns=['player_name', 'position', 'recent_team', 'season',
                                           'week', 'opponent_team', 'completions', 'attempts', 'passing_yards',
                                           'passing_tds', 'interceptions', 'sacks', ])
    return data



class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NFL Data")
        self.setFixedSize(QSize(800, 600))

        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        self.team_combobox = QComboBox()
        self.team_combobox.addItems(team_names()) # Pull all teams into a list with function and add function here.

        self.year_combobox = QComboBox()
        self.year_combobox.addItems(years())

        self.year_combobox.activated.connect(self.combobox_value)

        self.table = QTableView()
        self.model = TableModel(weekly_data(self.combobox_value()))
        self.table.setModel(self.model)

        self.table.setCurrentIndex()


        layout.addWidget(self.team_combobox)
        layout.addWidget(self.year_combobox)
        layout.addWidget(self.table)

    def combobox_value(self):
        value: int = int(self.year_combobox.currentText())
        return value


app = QApplication()
window = MainWindow()
window.show()

app.exec()