import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QFileDialog, QFrame, QScrollArea, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QDateTime

RATE_PER_KWH = 15  # Rate in PHP per kilowatt-hour


class BillCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utility Bill Calculator")
        self.setGeometry(250, 200, 600, 700)
        self.additional_bills = []  # Store dynamic bill entries
        self.setup_ui()

    def setup_ui(self):
        # Fonts
        title_font = QFont("Arial", 16, QFont.Weight.Bold)
        label_font = QFont("Arial", 11)

        # Title
        title = QLabel("🏠 Utility Bill Calculator (Electricity + Additional Bills)")
        title.setFont(title_font)
        title.setStyleSheet("color: #1F618D; margin-bottom: 10px;")

        # Electricity Inputs
        self.prev_label = QLabel("Previous Electricity Meter (kWh):")
        self.prev_label.setFont(label_font)
        self.prev_input = QLineEdit()
        self.prev_input.setPlaceholderText("Enter previous electricity reading")

        self.curr_label = QLabel("Current Electricity Meter (kWh):")
        self.curr_label.setFont(label_font)
        self.curr_input = QLineEdit()
        self.curr_input.setPlaceholderText("Enter current electricity reading")

        # Scrollable area for additional bills
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.bill_container = QWidget()
        self.bill_layout = QVBoxLayout(self.bill_container)
        self.scroll_area.setWidget(self.bill_container)

        # Add Bill Button
        self.add_bill_btn = QPushButton("➕ Add Another Bill")
        self.add_bill_btn.setStyleSheet("background-color: #F39C12; color: white; padding: 6px; font-weight: bold;")
        self.add_bill_btn.clicked.connect(self.add_bill_input)

        # Buttons
        self.calc_btn = QPushButton("Calculate Total Bill")
        self.calc_btn.setStyleSheet("background-color: #27AE60; color: white; padding: 6px; font-weight: bold;")
        self.calc_btn.clicked.connect(self.calculate_bill)

        self.save_btn = QPushButton("Save Receipt as Image")
        self.save_btn.setStyleSheet("background-color: #2E86C1; color: white; padding: 6px; font-weight: bold;")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_receipt_as_image)

        # Receipt display
        self.receipt_frame = QFrame()
        self.receipt_frame.setFrameShape(QFrame.Shape.Box)
        self.receipt_frame.setStyleSheet("background-color: white; border: 1px solid gray;")
        self.receipt_frame.setFixedHeight(350)

        self.receipt_label = QLabel("", self.receipt_frame)
        self.receipt_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.receipt_label.setFont(QFont("Courier New", 10))
        self.receipt_label.setWordWrap(True)
        self.receipt_label.setGeometry(10, 10, 560, 320)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.prev_label)
        layout.addWidget(self.prev_input)
        layout.addWidget(self.curr_label)
        layout.addWidget(self.curr_input)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Additional Bills:"))
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.add_bill_btn)
        layout.addWidget(self.calc_btn)
        layout.addWidget(self.receipt_frame)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        # Add one bill input by default
        self.add_bill_input()

    def add_bill_input(self):
        """Dynamically add a new bill name and amount input row."""
        h_layout = QHBoxLayout()

        name_input = QLineEdit()
        name_input.setPlaceholderText("Bill name (e.g. Water)")
        name_input.setFixedWidth(250)

        amount_input = QLineEdit()
        amount_input.setPlaceholderText("Amount ₱")
        amount_input.setFixedWidth(120)

        remove_btn = QPushButton("❌")
        remove_btn.setStyleSheet("background-color: #E74C3C; color: white; font-weight: bold;")
        remove_btn.setFixedWidth(40)

        # Store entry
        self.additional_bills.append((name_input, amount_input, remove_btn))

        # Remove action
        def remove_row():
            for widget in [name_input, amount_input, remove_btn]:
                widget.hide()
            self.bill_layout.removeItem(h_layout)
            self.additional_bills.remove((name_input, amount_input, remove_btn))

        remove_btn.clicked.connect(remove_row)

        # Add widgets to layout
        h_layout.addWidget(name_input)
        h_layout.addWidget(amount_input)
        h_layout.addWidget(remove_btn)
        self.bill_layout.addLayout(h_layout)

    def calculate_bill(self):
        try:
            prev = float(self.prev_input.text())
            curr = float(self.curr_input.text())

            if curr < prev:
                QMessageBox.warning(self, "Input Error", "Current reading must be greater than previous reading.")
                return

            # Electricity computation
            consumption = curr - prev
            elec_total = consumption * RATE_PER_KWH

            # Additional bills
            extra_total = 0
            extra_details = ""
            for name_input, amount_input, _ in self.additional_bills:
                name = name_input.text().strip()
                amount_text = amount_input.text().strip()
                if name and amount_text:
                    try:
                        amount = float(amount_text)
                        extra_total += amount
                        extra_details += f"{name:<20} ₱{amount:>8,.2f}\n"
                    except ValueError:
                        QMessageBox.warning(self, "Input Error", f"Invalid amount for '{name}'")
                        return

            total_due = elec_total + extra_total
            date_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss ap")

            # Build receipt
            receipt = (
                f"========================================\n"
                f"RENT BILL RECEIPT\n"
                f"========================================\n"
                f"Date & Time: {date_time}\n\n"
                f"--- ELECTRICITY BILL ---\n"
                f"Previous Reading : {prev:.2f} kWh\n"
                f"Current Reading  : {curr:.2f} kWh\n"
                f"Usage            : {consumption:.2f} kWh\n"
                f"Rate per kWh     : ₱{RATE_PER_KWH:.2f}\n"
                f"Electricity Bill : ₱{elec_total:,.2f}\n"
            )

            if extra_details:
                receipt += f"\n--- ADDITIONAL BILLS ---\n{extra_details}"

            receipt += (
                f"\n----------------------------------------\n"
                f"TOTAL AMOUNT DUE : ₱{total_due:,.2f}\n"
                f"========================================\n"
                f"Thank you for your payment!\n"
            )

            self.receipt_label.setText(receipt)
            self.save_btn.setEnabled(True)

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for meter readings.")

    def save_receipt_as_image(self):
        pixmap = QPixmap(self.receipt_frame.size())
        self.receipt_frame.render(pixmap)

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Receipt", "renter_bill_receipt.png", "PNG Files (*.png)"
        )
        if file_path:
            pixmap.save(file_path)
            QMessageBox.information(self, "Saved", f"Receipt saved successfully as:\n{file_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillCalculator()
    window.show()
    sys.exit(app.exec())
