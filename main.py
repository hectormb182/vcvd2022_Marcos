import sys
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import pyqtgraph.exporters as exporters
import pyqtgraph as pg
from PyQt5 import uic, QtCore
import equations as formulas


class MyInterface(QMainWindow):
    def __init__(self):
        super(MyInterface, self).__init__()
        uic.loadUi('interface_SBD.ui', self)

        # define attributes
        self.vehicle_mass = 500.0  # minimum 500Kg
        self.velocities = []  # first value must be defined by user through interface
        self.deceleration = 0.0
        self.road_type = ""
        self.road_condition = ""
        self.road_inclination = 0
        self.positions = [0.0]
        self.initial_b_t = 0.0  # starting braking time
        self.initial_b_p = 0.0  # starting braking position

        # clock to measure at specific time the distance "driven"
        self.sample_time = 0.1  # 0.1sec
        self.times = [0.0]
        self.timer = QtCore.QTimer()  # Setup a timer to update the graph.
        self.timer.setInterval(int(self.sample_time * 1000))
        self.timer.timeout.connect(self.update_plot)

        # design graph
        # self.position_plot.setTitle(text='Simulation Breaking Distance', axis='top')
        labelStyle = {'color': '#FFF', 'font-size': '11pt'}
        self.position_plot.setLabel(text='Time', units='s', axis='bottom', **labelStyle)
        self.position_plot.setLabel(text='Position', units='m', axis='left', **labelStyle)
        pg.setConfigOption('background', 'w')
        self.velocity_plot.setLabel(text='Time', units='s', axis='bottom', **labelStyle)
        self.velocity_plot.setLabel(text='Velocity', units='m/s', axis='left', **labelStyle)

        # adding action to simulation button
        self.simulation_button.clicked.connect(self.simulate)

        # adding action to simulation button
        self.break_button.clicked.connect(self.press_break)

        # adding action to clear button
        self.clear_button.clicked.connect(self.clear_plot)

        # adding action to export button
        self.export_button.clicked.connect(self.export_plot)

    def simulate(self):
        self.initialize_parameters()  # initialize parameters

        # assign user-parameters to the attributes
        self.vehicle_mass = self.mass_value.value()
        self.velocities.append((self.velocity_value.value() * 1000) / 3600)  # change velocity into in m/s
        self.road_type = self.road_type_value.currentText()
        self.road_condition = self.road_condition_value.currentText()
        self.road_inclination = self.inclination_value.value()

        if formulas.get_friction_coefficient(self.road_type, self.road_condition) != 0:
            # enable/disable buttons
            self.simulation_button.setEnabled(False)
            self.break_button.setEnabled(True)
            self.export_button.setEnabled(False)
            # start clock
            self.timer.start()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Warning: road conditions does not match!")
            msg.setText("Select proper road conditions")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def update_plot(self):
        self.pos_vel_calculus()
        # plot positions and velocities against time
        self.position_plot.plot(self.times, self.positions)  # plot time vs position
        self.velocity_plot.plot(self.times, self.velocities)  # plot time vs velocity

        if self.velocities[-1] <= 0.0:
            self.timer.stop()  # stop sample clock
            # show brake parameters on the interface
            self.brake_distance_box.setValue(self.positions[-1] - self.initial_b_p)
            self.brake_time_box.setValue(self.times[-1] - self.initial_b_t)

    def pos_vel_calculus(self):
        # calculate next time to sample
        self.times.append(self.times[-1] + self.sample_time)

        # get current position and add into an array of positions to plot it afterwards
        self.positions.append(formulas.get_position(self.sample_time, self.positions[-1], self.velocities[-1],
                                                    self.deceleration))

        # get the current velocity and # add into an array of velocities to plot it afterwards
        self.velocities.append(formulas.get_velocity(self.velocities[-1], self.deceleration, self.sample_time))

    def press_break(self):
        # enable/disable buttons
        self.simulation_button.setEnabled(True)
        self.break_button.setEnabled(False)
        self.clear_button.setEnabled(True)
        self.export_button.setEnabled(True)

        # Calculate final distance-brake parameters
        f_c = formulas.get_friction_coefficient(self.road_type, self.road_condition)
        self.deceleration = formulas.get_deceleration(f_c, self.road_inclination)

        # set a vertical line to delimit the starting brake point
        self.initial_b_t = self.times[-1]  # set intial brake time
        brake_time = pg.InfiniteLine(self.initial_b_t, pen=({'color': [255, 0, 0, 100], 'width': 2.5}))
        self.initial_b_p = self.positions[-1]  # set initial brake position
        brake_pos = pg.InfiniteLine(self.initial_b_p, angle=0, pen=({'color': [255, 0, 0, 100], 'width': 2.5}))
        brake_vel = pg.InfiniteLine(self.initial_b_t, pen=({'color': [255, 0, 0, 100], 'width': 2.5}))
        self.position_plot.addItem(brake_time)
        self.position_plot.addItem(brake_pos)
        self.velocity_plot.addItem(brake_vel)

    def clear_plot(self):
        self.initialize_parameters()

    def initialize_parameters(self):
        # initialize parameters to recalculate a new brake distance
        self.positions = [0.0]
        self.times = [0.0]
        self.velocities = []
        self.deceleration = 0.0
        self.road_inclination = 0.0
        self.position_plot.clear()
        self.velocity_plot.clear()
        self.brake_distance_box.setValue(0)
        self.brake_time_box.setValue(0)

    def export_plot(self):
        brake_distance = exporters.ImageExporter(self.position_plot.plotItem)
        velocity = exporters.ImageExporter(self.velocity_plot.plotItem)
        # save to file
        brake_distance.export('brake_distance.png')
        velocity.export('velocity.png')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = MyInterface()
    interface.show()
    sys.exit(app.exec_())
