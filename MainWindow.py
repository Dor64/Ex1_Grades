import csv
import os
import subprocess
import sys
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

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

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
            self.selected_file = file_path

            self.student_ids = []
            self.original_grades = []
            self.corrected_grades = []

            with open(self.selected_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # מדלג על שורת הכותרת (ID,Grade)

                for row in reader:
                    if row:
                        student_id = row[0]
                        grade = int(row[1])

                        self.student_ids.append(student_id)
                        self.original_grades.append(grade)
                        self.corrected_grades.append(grade)

            self.update_table()

    def apply_bonus(self):
        text = self.bonus_input.text()
        if not text or text == "-":
            return

        bonus = int(text)

        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade

        self.update_table()

    def update_file(self):
        if not self.selected_file:
            return

        with open(self.selected_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Grade"])

            for i in range(len(self.student_ids)):
                writer.writerow([self.student_ids[i], self.corrected_grades[i]])

        if sys.platform == "win32":
            os.startfile(self.selected_file)
        elif sys.platform == "darwin":
            subprocess.run(["open", self.selected_file])
        else:
            subprocess.run(["xdg-open", self.selected_file])

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
