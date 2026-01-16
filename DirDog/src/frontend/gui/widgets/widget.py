from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg


class LiveChartWidget(QWidget):
    def __init__(self, max_points=50):
        super().__init__()

        self.max_points = max_points
        self.data = []

        layout = QVBoxLayout(self)

        self.plot = pg.PlotWidget()
        self.plot.setTitle("Live Data")
        self.plot.showGrid(x=True, y=True)

        layout.addWidget(self.plot)

        self.curve = self.plot.plot(pen=pg.mkPen(width=2))

    # === DATA INTERFACE ===
    # Push a single numeric value into the chart
    def add_value(self, value: int):
        self.data.append(value)

        if len(self.data) > self.max_points:
            self.data.pop(0)

        self.curve.setData(self.data)
