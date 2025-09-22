import pandas as pd
from PySide6.QtCore import Qt, QSize, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QTableView

from nfl_data import team_names, years, weekly_data
import nfl_data_py as nfl

class TableModel(QAbstractTableModel):
    """
    Represents a table model for managing and displaying data using Qt's model-view framework.

    This class is designed to interface between a pandas DataFrame and a Qt TableView. It manages
    the data and provides the necessary methods to access data for display and interaction with
    the Qt view. It supports retrieving data for display, determining the number of rows and
    columns, and fetching header information for rows and columns.

    :ivar _data: The pandas DataFrame containing the model's data.
    :type _data: pandas.DataFrame
    """

    def __init__(self, data) -> None:
        super().__init__()
        self._data = data

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> str | None:
        if index.isValid() and role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        return None

    def rowCount(self, index: QModelIndex = ...):
        return self._data.shape[0]

    def columnCount(self, index: QModelIndex = ...):
        return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> str | None:
        # this section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        return None


class MainWindow(QMainWindow):
    """
    Main application window for displaying NFL data.

    This class represents the main window of the application, providing a graphical user
    interface for viewing NFL data. It includes dropdown menus for selecting a team
    and a year and displays data in a table format. The application dynamically updates
    the table content based on the selected year. The data is retrieved via functions
    that supply team names, available years, and weekly data.

    :ivar team_combobox: Dropdown menu for selecting an NFL team.
    :type team_combobox: QComboBox
    :ivar year_combobox: Dropdown menu for selecting a year.
    :type year_combobox: QComboBox
    :ivar table: Table view to display NFL data based on the selections.
    :type table: QTableView
    :ivar model: Data model for managing and presenting data in the table view.
    :type model: TableModel
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("NFL Data")
        self.setFixedSize(QSize(1280, 720))

        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        self.team_combobox = QComboBox()
        self.team_combobox.addItems(team_names())
        self.team_combobox.activated.connect(self.update_table_model)

        self.year_combobox = QComboBox()
        self.year_combobox.addItems(years())

        self.year_combobox.activated.connect(self.update_table_model)

        self.table = QTableView()
        self.model = TableModel(weekly_data(self.year_combobox_value(), self.team_combobox_value()))
        self.table.setModel(self.model)

        layout.addWidget(self.team_combobox)
        layout.addWidget(self.year_combobox)
        layout.addWidget(self.table)


    def team_combobox_value(self) -> str | None:
        """
        Returns the value of the team combobox selection as string.
        :return:
        """
        data = nfl.import_weekly_data([2024], columns=['recent_team'])
        teams = [team for team in team_names()]
        abbr = sorted(set([abbr for abbr in data["recent_team"]]))
        teams_dict = dict(zip(teams, abbr))

        selected_team: str = str(self.team_combobox.currentText())

        for keys in teams_dict.keys():
            if selected_team in keys:
                return teams_dict[selected_team]
        return None

    def year_combobox_value(self) -> int:
        """
        Returns the value of the combobox year selection as int.
        :return:
        """
        value: int = int(self.year_combobox.currentText())
        return value

    def update_table_model(self) -> None:
        """
        Replace the data in the model whenever the combobox selection changes.
        Retrieves year from combobox value
            Sets data to weekly data for that year using weekly_data function
            Ensures data is a pandas dataframe and not empty
                Sets model to TableModel with data
                Resets the table view

        Handles invalid data using an else statement
        """
        team = self.team_combobox_value()
        year = self.year_combobox_value()
        if year and team:
            data = weekly_data(year, team)
            if isinstance(data, pd.DataFrame) and not data.empty:
                self.model = TableModel(data)
                self.table.setModel(self.model)
            else:
                print("Invalid or empty data returned.") # Add PySide pop up window for invalid data??


app = QApplication()
window = MainWindow()
window.show()

app.exec()