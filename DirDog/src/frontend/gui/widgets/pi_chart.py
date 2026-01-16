from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class PieChartWidget(QWidget):
    def __init__(self, title="Alltime actions"):
        super().__init__()

        self.series = QPieSeries()
        self.slices = {}  # label -> QPieSlice

        # --- Chart setup ---
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(title)
        self.chart.legend().setAlignment(Qt.AlignRight)

        # --- Enable animations ---
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setAnimationDuration(600)

        # --- Chart view ---
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        
        layout = QVBoxLayout(self)
        self.chart.setBackgroundBrush(QColor("#1E1E1E"))


        layout.addWidget(self.view)

    # === DATA INTERFACE ===
    # This method is the main entry point for external data updates
    def update_data(self, data: dict[str, float]):
        """
        Expected format:
        {
            "PDF": 30,
            "Images": 50,
            "Videos": 20
        }
        """

        for label, value in data.items():
            if label not in self.slices:
                slice_ = self.series.append(label, value)
                slice_.setLabelVisible(True)
                self.slices[label] = slice_
            else:
                slice_ = self.slices[label]
                slice_.setValue(value)

            # --- Display absolute values ---
            slice_.setLabel(f"{label}: {int(value)}")

    # === OPTIONAL DATA INTERFACE ===
    # Completely reset the chart with new categories
    def reset_data(self, data: dict[str, float]):
        self.series.clear()
        self.slices.clear()
        self.update_data(data)
