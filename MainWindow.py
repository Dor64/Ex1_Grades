from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from About import AboutDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grade Corrector")
        self.resize(750, 600)

        # TODO: Initialize your data attributes here (e.g., file_path, data lists)
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Header / Title bar
        header_layout = QHBoxLayout()
        title_label = QLabel("Grade Corrector")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("secondaryButton")
        self.about_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_button.clicked.connect(self.open_about)
        header_layout.addWidget(self.about_button)

        main_layout.addLayout(header_layout)

        # Controls toolbar
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)

        self.load_button = QPushButton("Load File")
        self.load_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.load_button.clicked.connect(self.load_file)
        controls_layout.addWidget(self.load_button)

        bonus_label = QLabel("Bonus Points:")
        bonus_label.setObjectName("fieldLabel")
        controls_layout.addWidget(bonus_label)

        self.bonus_input = QLineEdit()
        self.bonus_input.setPlaceholderText("Enter integer & press Enter...")
        self.bonus_input.setValidator(QIntValidator(-100, 100, self))
        self.bonus_input.setFixedWidth(200)
        self.bonus_input.returnPressed.connect(self.apply_bonus)
        controls_layout.addWidget(self.bonus_input)

        controls_layout.addStretch()

        self.update_button = QPushButton("Update File")
        self.update_button.setObjectName("accentButton")
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.clicked.connect(self.update_file)
        controls_layout.addWidget(self.update_button)

        main_layout.addLayout(controls_layout)

        # Grades Table (50 rows, 3 columns)
        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Original Grades", "Corrected Grades"]
        )
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setDefaultSectionSize(32)
        main_layout.addWidget(self.table)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Grades CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if file_path:
            # TODO: Save file_path, read the CSV contents into self.student_ids and self.original_grades,
            #       and call self.update_table()
            pass

    def apply_bonus(self):
        # TODO: Read the integer bonus from self.bonus_input.text(), compute self.corrected_grades,
        #       and call self.update_table()
        pass

    def update_file(self):
        # TODO: Write the updated data (ID, Original Grades, Corrected Grades) to the CSV file
        pass

    def update_table(self):
        """Populate the QTableWidget from self.student_ids, self.original_grades, and self.corrected_grades."""
        self.table.clearContents()

        for row, student_id in enumerate(self.student_ids):
            item = QTableWidgetItem(str(student_id))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item)

        for row, grade in enumerate(self.original_grades):
            item = QTableWidgetItem(str(grade))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, item)

        for row, corrected in enumerate(self.corrected_grades):
            item = QTableWidgetItem(str(corrected))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, item)

    def open_about(self):
        dialog = AboutDialog(self)
        dialog.exec()
