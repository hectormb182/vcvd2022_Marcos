import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
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
        self.current_velocity = 0.0
        self.velocities = []  # first value must be defined by user through interface
        self.deceleration = 0.0
        self.road_type = ""
        self.road_condition = ""
        self.road_inclination = 0
        self.initial_position = 0.0
        self.current_position = 0.0
        self.positions = [self.initial_position]
        self.current_time = 0.0

        # clock to measure at specific time the distance "driven"
        self.time_sample = 90  # msec
        self.times = [self.current_time]
        self.timer = QtCore.QTimer()  # Setup a timer to update the graph.
        self.timer.setInterval(self.time_sample)
        self.timer.timeout.connect(self.update_plot)

        # design graph
        # self.position_plot.setTitle(text='Simulation Breaking Distance', axis='top')
        labelStyle = {'color': '#FFF', 'font-size': '11pt'}
        self.position_plot.setLabel(text='Time', units='s', axis='bottom', **labelStyle)
        self.position_plot.setLabel(text='Position', units='m', axis='left', **labelStyle)
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
        # enable/disable buttons
        self.simulation_button.setEnabled(False)
        self.break_button.setEnabled(True)
        self.export_button.setEnabled(False)

        # assign user-parameters to the attributes
        self.vehicle_mass = self.mass_value.value()
        self.current_velocity = (self.velocity_value.value() * 1000) / 3600
        self.velocities.append(self.current_velocity)
        self.road_type = self.road_type_value.currentText()
        self.road_condition = self.road_condition_value.currentText()
        self.road_inclination = self.inclination_value.value()

        # start clock
        self.timer.start()

    def update_plot(self):

        # get current position
        self.current_position = formulas.get_position(self.times[-1], self.positions[-1], self.velocities[-1],
                                                      self.deceleration)
        # add into an array of positions to plot it afterwards
        self.positions.append(self.current_position)

        # calculate the current velocity
        self.current_velocity = formulas.get_velocity(self.times[-1],  self.velocities[-1], self.deceleration)
        # add into an array of velocities to plot it afterwards
        self.velocities.append(self.current_velocity)

        self.times.append(self.current_time)
        self.current_time += self.time_sample/1000

        # plot positions and velocities against time
        self.position_plot.plot(self.times, self.positions)  # plot time vs position
        self.velocity_plot.plot(self.times, self.velocities)  # plot time vs velocity

        # if the velocity is equal or less than 0, means the vehicle must be stopped
        print(self.current_velocity)
        if self.current_velocity <= 0.0:
            self.initialize_parameters()  # initialize parameters
            self.timer.stop()  # stops clock

    def press_break(self):
        # enable/disable buttons
        self.simulation_button.setEnabled(True)
        self.break_button.setEnabled(False)
        self.clear_button.setEnabled(True)
        self.export_button.setEnabled(True)

        # Calculate final distance-brake parameters
        f_c = formulas.get_friction_coefficient(self.road_type, self.road_condition)
        p_f = formulas.get_final_pos(self.velocities[-1], f_c, self.positions[-1])
        t_f = formulas.get_break_time(p_f, self.positions[-1], self.velocities[-1])
        self.deceleration = formulas.get_acceleration(t_f, 0, self.velocities[-1])
        self.brake_distance_box.setValue(p_f)
        self.brake_time_box.setValue(t_f)
        brake1 = pg.InfiniteLine(self.times[-1], pen=({'color': [255, 0, 0, 100], 'width': 2.5}))
        brake2 = pg.InfiniteLine(self.times[-1], pen=({'color': [255, 0, 0, 100], 'width': 2.5}))
        self.position_plot.addItem(brake1)
        self.velocity_plot.addItem(brake2)

    def clear_plot(self):
        self.initialize_parameters()
        self.position_plot.clear()
        self.velocity_plot.clear()

    def initialize_parameters(self):
        # initialize parameters to recalculate a new brake distance
        self.current_position = 0.0
        self.positions = [self.current_position]
        self.current_time = 0.0
        self.times = [self.current_time]
        self.velocities = []
        self.deceleration = 0.0

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
