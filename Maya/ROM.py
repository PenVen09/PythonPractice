from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
from maya import cmds
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

class ROM_UI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ROM_UI, self).__init__(parent)
        self.setFixedSize(500, 650)
        self.saved_data = {
        'spine': [-45.0, 45.0],
        'clavicle': [-45.0, 45.0],
        'arm':[-45.0, 45.0]}
        self.slot_data = []
        self.create_UI()

        
    def create_UI(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)


        tab_widget = QtWidgets.QTabWidget()

        tab1 = QtWidgets.QWidget()
        tab1_layout = QtWidgets.QVBoxLayout(tab1)
        start_layout = QtWidgets.QHBoxLayout(tab1)
        start_label= QtWidgets.QLabel("Start Frame")
        self.start_box = QtWidgets.QLineEdit("0")

        selection_layout = QtWidgets.QHBoxLayout()
        select_label = QtWidgets.QLabel("Select:")
        self.selection_radio = QtWidgets.QRadioButton("Selected")
        self.selection_radio.setChecked(True)
        self.hierarchy_radio = QtWidgets.QRadioButton("Hierarchy")
        self.all_radio = QtWidgets.QRadioButton("All")

        selection_layout.addWidget(select_label)
        selection_layout.addWidget(self.selection_radio)
        selection_layout.addWidget(self.hierarchy_radio)
        selection_layout.addWidget(self.all_radio)
        tab1_layout.addLayout(selection_layout)


        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_box)
        tab1_layout.addLayout(start_layout)

        step_label= QtWidgets.QLabel("Step Frame :")
        self.step_box = QtWidgets.QLineEdit("10")

        start_layout.addWidget(step_label)
        start_layout.addWidget(self.step_box)
        tab1_layout.addWidget(self._separator())
        grid_layout = QtWidgets.QGridLayout()


        # Header checkboxes (row 0)
        min_header_button = QtWidgets.QPushButton("v")
        min_header_button.setFixedSize(15, 15)
        max_header_button = QtWidgets.QPushButton("v")
        max_header_button.setFixedSize(15, 15)
        grid_layout.addWidget(min_header_button, 0, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(max_header_button, 0, 5, alignment=Qt.AlignCenter)

        self.axis_controls = []
        min_boxes = []
        max_boxes = []

        for row, axis in enumerate(("Rotate X", "Rotate Y", "Rotate Z"), start=1):
            axis_label = QtWidgets.QLabel(axis)
            min_checkbox = QtWidgets.QCheckBox()
            min_box = QtWidgets.QLineEdit("-90")

            slash_label = QtWidgets.QLabel("<----------------->")
            max_checkbox = QtWidgets.QCheckBox()
            max_box = QtWidgets.QLineEdit("90")
            min_boxes.append([min_checkbox, min_box])
            max_boxes.append([max_checkbox, max_box])
            self.axis_controls.append({
                "min_checkbox": min_checkbox,
                "min_box": min_box,
                "max_checkbox": max_checkbox,
                "max_box": max_box})

            grid_layout.addWidget(axis_label,row, 1)
            grid_layout.addWidget(min_checkbox,row, 2)
            grid_layout.addWidget(min_box,row, 3)
            grid_layout.addWidget(slash_label, row, 4)
            grid_layout.addWidget(max_checkbox, row, 5)
            grid_layout.addWidget(max_box,row, 6)


        tab1_layout.addLayout(grid_layout)

        min_header_button.clicked.connect(lambda :self._toggle_checkboxes(min_boxes))
        max_header_button.clicked.connect(lambda :self._toggle_checkboxes(max_boxes))


        tab1_layout.addWidget(self._separator())
        rotate_together_label = QtWidgets.QLabel("Rotate Together:")
        rotate_list = QtWidgets.QHBoxLayout()
        rotate_list_button_layout = QtWidgets.QVBoxLayout()
        add_list_button = QtWidgets.QPushButton()
        add_list_button.setIcon(QtGui.QIcon(":addClip.png"))
        add_list_button.clicked.connect(self.add_to_list)
        remove_list_button = QtWidgets.QPushButton()
        remove_list_button.setIcon(QtGui.QIcon(":delete.png"))
        remove_list_button.clicked.connect(self.remove_from_list)
        self.rotate_list_widget = QtWidgets.QListWidget()


        rotate_list_button_layout.addWidget(add_list_button)
        rotate_list_button_layout.addWidget(remove_list_button)
        rotate_list_button_layout.addStretch()
        rotate_list.addWidget(self.rotate_list_widget)
        rotate_list.addLayout(rotate_list_button_layout)

        tab1_layout.addWidget(rotate_together_label)
        tab1_layout.addLayout(rotate_list)


        tab1_layout.addWidget(self._separator())
        custom_keyframe_checkbox = QtWidgets.QCheckBox("Use custom key")
        execute_btn = QtWidgets.QPushButton("Execute")
        execute_btn.clicked.connect(lambda: self.execute_rom())

        clear_keyframe_btn = QtWidgets.QPushButton("Clear Keyframe")
        tab1_layout.addWidget(custom_keyframe_checkbox)
        tab1_layout.addWidget(execute_btn)
        tab1_layout.addWidget(clear_keyframe_btn)


        tab1_layout.addStretch()
        tab_widget.addTab(tab1, "ROM")

        tab2 = QtWidgets.QWidget()
        template_main_layout = QtWidgets.QVBoxLayout(tab2, alignment=QtCore.Qt.AlignTop)
        self.slot_layout = QtWidgets.QVBoxLayout()
        self.add_button = QtWidgets.QPushButton("Add Slot")
        self.add_button.clicked.connect(self._add_slot)
        self.submit_button = QtWidgets.QPushButton("Save(WORKINPROGRESS)")
        #self.submit_button.clicked.connect(self.submit_data)
        template_main_layout.addLayout(self.slot_layout)

        self.slot_count = 0
        if self.saved_data:
            for name, (min_val, max_val) in self.saved_data.items():
                self._add_slot(name, min_val, max_val)

        template_layout = QtWidgets.QHBoxLayout()
        template_layout.addWidget(self._separator())
        template_main_layout.addLayout(template_layout)
        template_layout.addWidget(self.add_button)
        template_layout.addWidget(self.submit_button)
        #template_layout.addStretch()
        tab_widget.addTab(tab2, "Template")
        main_layout.addWidget(tab_widget)


    def _separator(self):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setStyleSheet("margin-top: 5px; margin-bottom: 5px;")
        return line

    def _toggle_checkboxes(self, boxes):
        check = boxes[0][0]
        if check.isChecked():
            state = False
        else:
            state = True
        for checkbox, box in boxes:
            checkbox.setChecked(state)
            box.setEnabled(state)

    def _add_slot(self, name_text="", min_val=-40.0, max_val=40.0):
        #self.slot_count += 1
        hbox = QtWidgets.QHBoxLayout()

        name_field = QtWidgets.QLineEdit()
        name_field.setPlaceholderText("")
        name_field.setText(name_text)

        min_field = QtWidgets.QDoubleSpinBox()
        min_field.setDecimals(2)
        min_field.setRange(-9999, 9999)
        min_field.setValue(min_val)

        max_field = QtWidgets.QDoubleSpinBox()
        max_field.setDecimals(2)
        max_field.setRange(-9999, 9999)
        max_field.setValue(max_val)

        hbox.addWidget(name_field)
        hbox.addWidget(QtWidgets.QLabel("Min:"))
        hbox.addWidget(min_field)
        hbox.addWidget(QtWidgets.QLabel("Max:"))
        hbox.addWidget(max_field)

        self.slot_layout.addLayout(hbox)


        self.slot_data.append({
            "name": name_field,
            "min": min_field,
            "max": max_field
        })
        return

    def add_to_list(self):
        selection = cmds.ls(selection =True)
        joined_selection = ", ".join(selection)
        self.rotate_list_widget.addItem(joined_selection)

    def remove_from_list(self):
        current_row= self.rotate_list_widget.currentRow()
        self.rotate_list_widget.takeItem(current_row)

    def get_val(self):
        rotation_data = []
        for i, control in enumerate(self.axis_controls):
            axis_name = ["rotateX", "rotateY", "rotateZ"][i]
            min_enabled = control["min_checkbox"].isChecked()
            max_enabled = control["max_checkbox"].isChecked()
            min_value = control["min_box"].text()
            max_value = control["max_box"].text()
            rotation_data.append({"axis": axis_name,"min_enabled": min_enabled,"min_value": min_value,"max_enabled": max_enabled,"max_value": max_value})

        return rotation_data


    def execute_rom(self):
        selection = []
        if self.selection_radio.isChecked():
            selection= cmds.ls(selection=True)

        rotation_data = self.get_val()
        frame = 0
        offset = float(self.step_box.text())
        already_grouped = set()
        for rot in rotation_data:
            for selected in selection:
                result = []

                if self.rotate_list_widget.count() > 0:
                    for i in range(self.rotate_list_widget.count()):
                        text = self.rotate_list_widget.item(i).text()
                        if selected in already_grouped:
                            continue
                        if selected in text:
                            result = [x.strip() for x in text.split(',')]
                            break

                if result:
                    for joint in result:
                        if rot["min_enabled"]:
                            cmds.setKeyframe(joint, attribute=rot["axis"], time=frame, value=0)
                            cmds.setKeyframe(joint, attribute=rot["axis"], time=frame + offset, value=float(rot["min_value"]))
                            cmds.setKeyframe(joint, attribute=rot["axis"], time=frame + offset + offset, value=0)
                        frame += offset * 3

                        if rot["max_enabled"]:
                            cmds.setKeyframe(selected, attribute=rot["axis"], time=frame, value=0)
                            cmds.setKeyframe(selected, attribute=rot["axis"], time=frame + offset  , value=float(rot["max_value"]))
                            cmds.setKeyframe(selected, attribute=rot["axis"], time=frame + offset  + offset, value=0)
                        frame += offset * 3
                    already_grouped.update(result)

                for joint in selected:
                    if rot["min_enabled"]:
                        cmds.setKeyframe(joint, attribute=rot["axis"], time=frame, value=0)
                        cmds.setKeyframe(joint, attribute=rot["axis"], time=frame + offset, value=float(rot["min_value"]))
                        cmds.setKeyframe(joint, attribute=rot["axis"], time=frame + offset + offset, value=0)
                        frame += offset * 3

                    if rot["max_enabled"]:
                        cmds.setKeyframe(selected, attribute=rot["axis"], time=frame, value=0)
                        cmds.setKeyframe(selected, attribute=rot["axis"], time=frame + offset  , value=float(rot["max_value"]))
                        cmds.setKeyframe(selected, attribute=rot["axis"], time=frame + offset  + offset, value=0)
                        frame += offset * 3





def getWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def show_control_tool():
    global rangeofmotion_UI

    try:
        if rangeofmotion_UI is not None:
            rangeofmotion_UI.close()
            rangeofmotion_UI.deleteLater()
    except:
        pass

    parent = getWindow()
    rangeofmotion_UI = ROM_UI(parent)
    rangeofmotion_UI.show()



show_control_tool()
