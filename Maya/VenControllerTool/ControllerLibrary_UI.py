from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os
import json
USER_SCRIPTS_DIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.normpath(os.path.join(USER_SCRIPTS_DIR, "scripts","VenControllerTool", "controller_folder"))


class ControllerLibrary_UI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ControllerLibrary_UI, self).__init__(parent)
        self.checkbox_dict = {}
        self.data = control_library()
        controller_UI = None
        self.setWindowTitle("Ven Controller Tool")
        self.setFixedSize(500, 700)
        self.createUI()
        self.populate()
    def createUI(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        tab_widget = QtWidgets.QTabWidget()
        main_layout.addWidget(tab_widget)

        ##########################################
        controller_scroll_area = QtWidgets.QScrollArea()
        controller_scroll_area.setWidgetResizable(True)
        controller_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.controller_scroll_content = QtWidgets.QWidget()

        self.controller_main_layout = QtWidgets.QVBoxLayout(self.controller_scroll_content)
        self.controller_main_layout.setAlignment(QtCore.Qt.AlignTop)

        controller_scroll_area.setWidget(self.controller_scroll_content)
        main_layout.addWidget(controller_scroll_area)



        ########################
        controller_widget, controller_collapsible_button, controller_container = self._collapsible_button("Create Controller")
        controller_name_layout = QtWidgets.QHBoxLayout()
        controller_name_field = QtWidgets.QLineEdit("")
        controller_name_field.setPlaceholderText("Search or Name")

        style = QtWidgets.QApplication.style()
        search_icon = QtGui.QIcon(":zoom.png")   


        search_action = QtWidgets.QAction(search_icon, "", controller_name_field)
        search_action.triggered.connect(lambda: print("Search clicked!"))
        controller_name_field.addAction(search_action, QtWidgets.QLineEdit.TrailingPosition)


        save_controller_checkbox = QtWidgets.QCheckBox("")
        save_controller_button = QtWidgets.QPushButton("Save")
        save_controller_button.setFixedWidth(100)
        save_controller_button.setEnabled(False)
        save_controller_checkbox.toggled.connect(save_controller_button.setEnabled)
        save_controller_button.clicked.connect(lambda: (self.data.save(controller_name_field.text()), self.populate()))

        folder_button =QtWidgets.QPushButton("")
        folder_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        controller_name_layout.addWidget(folder_button)
        controller_name_layout.addWidget(controller_name_field)
        controller_name_layout.addWidget(save_controller_checkbox)
        controller_name_layout.addWidget(save_controller_button)

        controller_container.addLayout(controller_name_layout)


        row_controller_layout = QtWidgets.QHBoxLayout()

        thickness_layout = QtWidgets.QHBoxLayout()
        thickness_label = QtWidgets.QLabel("Thickness")

        self.thickness_box = QtWidgets.QDoubleSpinBox()
        self.thickness_box.setMinimum(0.0)
        self.thickness_box.setValue(1.0)
        self.thickness_box.setFixedWidth(60)
        self.thickness_box.setDecimals(2)
        self.thickness_box.valueChanged.connect(self.shape_thickness)

        thickness_layout.addWidget(thickness_label)
        thickness_layout.addWidget(self.thickness_box)


        self.ctrlListWidget = QtWidgets.QListWidget()
        self.ctrlListWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.ctrlListWidget.setFixedSize(430, 250)
        self.ctrlListWidget.setIconSize(QtCore.QSize(105,105))
        self.ctrlListWidget.setDragEnabled(False)

        row_controller_layout.addWidget(self.ctrlListWidget, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)


        full_buttons_layout = QtWidgets.QHBoxLayout()
        styled_buttons_layout = QtWidgets.QHBoxLayout()


        styled_container = QtWidgets.QWidget()
        styled_container.setStyleSheet("""background-color: #3c3c3c;""")

        self.offset_checkboxes = QtWidgets.QCheckBox("Add Offset group")
        self.create_button = QtWidgets.QPushButton("Create")
        self.replace_button = QtWidgets.QPushButton("Replace")
        self.create_button.clicked.connect(lambda : self.import_controller(True))
        self.replace_button.clicked.connect(lambda : self.import_controller(False))

        self.create_button.setStyleSheet(''' QPushButton {background-color: #555 ;color: white;}''')

        styled_buttons_layout.addWidget(self.offset_checkboxes)
        styled_buttons_layout.addWidget(self.create_button)



        styled_container.setLayout(styled_buttons_layout)
        full_buttons_layout.addWidget(styled_container)
        full_buttons_layout.addWidget(self.replace_button)


        size_layout = QtWidgets.QHBoxLayout()

        size_label = QtWidgets.QLabel("Size")
        self.decrease_size_button = QtWidgets.QPushButton("◀")
        self.increase_size_button = QtWidgets.QPushButton("▶")
        self.increase_size_button.clicked.connect(lambda : self.shape_size(0.1))
        self.decrease_size_button.clicked.connect(lambda :self.shape_size(-0.1))

        thickness_layout.addWidget(size_label)
        thickness_layout.addWidget(self.decrease_size_button)
        thickness_layout.addWidget(self.increase_size_button)
        controller_container.addLayout(row_controller_layout)
        controller_container.addLayout(full_buttons_layout, alignment=QtCore.Qt.AlignTop)
        controller_container.addLayout(thickness_layout)


        controller_container.addLayout(size_layout)

        self.controller_main_layout.addWidget(controller_widget)


        ########################
        color_widget, color_collapsible_button, color_layout = self._collapsible_button("Controller Color")

        swatch_grid = QtWidgets.QGridLayout()
        swatch_grid.setSpacing(0)
        swatch_grid.setContentsMargins(0, 0, 0, 0)
        color_widget.setStyleSheet("background-color: #2A2A2A;")

        color_index = 0
        for row in range(4):
            for column in range(8):
                btn = QtWidgets.QPushButton()
                button_colour = colorList().get_color_by_index(color_index)
                btn.setStyleSheet(f"background-color: rgb{button_colour};")
                swatch_grid.addWidget(btn, row, column)

                btn.clicked.connect(lambda *args,idx=color_index: self.controller_color(idx))

                color_index += 1


        color_reset_btn = QtWidgets.QPushButton("Reset Color")
        color_reset_btn.clicked.connect(self.reset_color)
        color_reset_btn.setStyleSheet("background-color: gray;")
        color_layout.addLayout(swatch_grid)
        color_layout.addWidget(color_reset_btn)
        self.controller_main_layout.addWidget(color_widget)

        ############
        replace_shape_widget, replace_collapsible_button, replace_container = self._collapsible_button("Replace Shapes")

        to_replace_layout = QtWidgets.QHBoxLayout()
        to_replace_box = QtWidgets.QLineEdit()
        to_replace_box.setFixedWidth(200)
        to_replace_button = QtWidgets.QPushButton("Register Shape")
        to_replace_box.setReadOnly(True)


        to_replace_layout.addWidget(to_replace_box)
        to_replace_layout.addWidget(to_replace_button)

        shape_reference_layout = QtWidgets.QHBoxLayout()
        shape_reference_box = QtWidgets.QLineEdit()
        shape_reference_box.setReadOnly(True)
        shape_reference_box.setFixedWidth(200)
        shape_reference_button = QtWidgets.QPushButton("Reference Shape")

        shape_reference_layout.addWidget(shape_reference_box)
        shape_reference_layout.addWidget(shape_reference_button)

        replace_layout = QtWidgets.QHBoxLayout()
        mirror_checkbox = QtWidgets.QCheckBox("Mirror Shapes")
        replace_button = QtWidgets.QPushButton("Replace Shapes")
        replace_button.setFixedWidth(200)
        replace_layout.addWidget(mirror_checkbox)
        replace_layout.addWidget(replace_button)


        replace_container.addLayout(to_replace_layout)
        replace_container.addLayout(shape_reference_layout)
        replace_container.addLayout(replace_layout)

        self.controller_main_layout.addWidget(replace_shape_widget)

        #######
        lock_widget, lock_collapsible_button, lock_container = self._collapsible_button("Lock/Unlock Attributes")
        lock_hide_layout = QtWidgets.QHBoxLayout()
        lock_hide_label = QtWidgets.QLabel("Operations:")
        self.lock_checkboxes = QtWidgets.QCheckBox("Lock")
        self.hide_checkboxes = QtWidgets.QCheckBox("Hide")
        execute_lock_button = QtWidgets.QPushButton("Execute")

        execute_lock_button.clicked.connect(self.lock_execute)


        lock_hide_layout.addWidget(lock_hide_label)
        lock_hide_layout.addWidget(self.lock_checkboxes)
        lock_hide_layout.addWidget(self.hide_checkboxes)
        lock_hide_layout.addWidget(execute_lock_button)
        lock_container.addLayout(lock_hide_layout)
        lock_container.addWidget(self._separator())


        for attribute in ["Translate", "Rotate", "Scale"]:
            transform_layout = self._create_colored_checkboxes(attribute)
            lock_container.addLayout(transform_layout)


        visibility_layout = QtWidgets.QHBoxLayout()
        self.visibility_checkboxes = QtWidgets.QCheckBox("Visibility")

        lock_container.addLayout(visibility_layout)

        visibility_layout.addWidget(self.visibility_checkboxes)
        lock_container.addWidget(self._separator())


        lock_utilities_layout = QtWidgets.QHBoxLayout()
        unlock_button = QtWidgets.QPushButton("Unlock")
        reset_lock_button = QtWidgets.QPushButton("Reset")


        lock_utilities_layout.addWidget(unlock_button)
        lock_utilities_layout.addWidget(reset_lock_button)
        lock_container.addLayout(lock_utilities_layout)

        self.controller_main_layout.addWidget(lock_widget)


        #controller_collapsible_button.click()
        #color_collapsible_button.click()
        #attribute_collapsible_button.click()
        #replace_collapsible_button.click()
        #lock_collapsible_button.click()

        tab_widget.addTab(controller_scroll_area, "Controller")
        self.controller_scroll_content.setUpdatesEnabled(True)
        #tab_widget.setCurrentIndex(1)

        ##############################
        attribute_scroll_area = QtWidgets.QScrollArea()
        attribute_scroll_area.setWidgetResizable(True)
        attribute_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.attribute_scroll_content = QtWidgets.QWidget()

        self.attribute_main_layout = QtWidgets.QVBoxLayout(self.attribute_scroll_content)
        self.attribute_main_layout.setAlignment(QtCore.Qt.AlignTop)

        attribute_scroll_area.setWidget(self.attribute_scroll_content)
        main_layout.addWidget(attribute_scroll_area)
        tab_widget.addTab(attribute_scroll_area, "Attribute")


        ############
        add_attribute_widget, attribute_collapsible_button, attribute_container = self._collapsible_button("Add Attributes")


        self.attribute_main_layout.addWidget(add_attribute_widget)

        #######



        ###########
        shift_widget, shift_collapsible_button, shift_container = self._collapsible_button("Shift Attributes")
        shift_layout = QtWidgets.QHBoxLayout()

        shift_button_layout = QtWidgets.QVBoxLayout()
        shift_update_attribute = QtWidgets.QPushButton("o")
        shift_update_attribute.clicked.connect(lambda:self.update_attribute(True))
        shift_up_attribute = QtWidgets.QPushButton("^")
        shift_up_attribute.clicked.connect(lambda:self.shifting_attr(True))
        shift_down_attribute = QtWidgets.QPushButton("v")
        shift_down_attribute.clicked.connect(lambda:self.shifting_attr(False))

        shift_update_attribute.setFixedWidth(30)
        shift_up_attribute.setFixedWidth(30)
        shift_down_attribute.setFixedWidth(30)


        shift_button_layout.addWidget(shift_update_attribute,alignment=QtCore.Qt.AlignTop)
        shift_button_layout.addWidget(shift_up_attribute)
        shift_button_layout.addWidget(shift_down_attribute)
        shift_layout.addLayout(shift_button_layout)

        self.shift_attribute_list = QtWidgets.QListWidget()
        self.shift_attribute_list .setFixedSize(300, 200)
        shift_layout.addWidget(self.shift_attribute_list,alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        shift_container.addLayout(shift_layout)
        self.attribute_main_layout.addWidget(shift_widget)


        ###########

        connect_attribute_widget, connect_collapsible_button, connect_container = self._collapsible_button("Connect Attributes")

        row_object_layout = QtWidgets.QHBoxLayout()
        source_object =  QtWidgets.QLineEdit()
        label_object = QtWidgets.QLabel(">")
        target_object = QtWidgets.QLineEdit()

        row_object_layout.addWidget(source_object)
        row_object_layout.addWidget(label_object)
        row_object_layout.addWidget(target_object)
        connect_container.addLayout(row_object_layout)

        row_connect_layout = QtWidgets.QHBoxLayout()

        source_connect_list = QtWidgets.QListWidget()
        source_connect_list .setFixedSize(170, 200)
        target_connect_list = QtWidgets.QListWidget()
        target_connect_list .setFixedSize(170, 200)

        row_connect_layout.addWidget(source_connect_list,alignment=QtCore.Qt.AlignTop)
        row_connect_layout.addWidget(target_connect_list,alignment=QtCore.Qt.AlignTop)
        connect_container.addLayout(row_connect_layout)
        self.attribute_main_layout.addWidget(connect_attribute_widget)



    def _create_colored_checkboxes(self, attribute):
        transform_layout = QtWidgets.QHBoxLayout()
        transform_layout.setContentsMargins(0, 0, 0, 0)
        lock_checkboxes = QtWidgets.QCheckBox(attribute)
        transform_layout.addWidget(lock_checkboxes)


        axis_checkboxes = []
        for axis, color in zip(["X", "Y", "Z"], ["red", "green", "blue"]):
            axis_checkbox = QtWidgets.QCheckBox(axis)
            axis_checkboxes.append(axis_checkbox)

            icon_label = QtWidgets.QLabel()
            icon_label.setFixedSize(5, 12)
            icon_label.setStyleSheet(f"background-color: {color};")

            axis_layout = QtWidgets.QHBoxLayout()
            axis_layout.setSpacing(2)
            axis_layout.setContentsMargins(0, 0, 0, 0)
            axis_layout.addWidget(icon_label)
            axis_layout.addWidget(axis_checkbox)

            axis_widget = QtWidgets.QWidget()
            axis_widget.setLayout(axis_layout)
            transform_layout.addWidget(axis_widget)
            self.checkbox_dict[attribute[0].lower() + axis.lower()] = axis_checkbox

        lock_checkboxes.stateChanged.connect(lambda state, boxes=axis_checkboxes: self._toggle_axis_checkboxes(state, boxes))


        return transform_layout
    def _on_slider_change(self, value, field):
        new_value = value*0.1
        field.setText(f"{new_value:.2f}")
    def _collapsible_button(self, label_text):
        section_widget = QtWidgets.QWidget()
        section_layout = QtWidgets.QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        toggle_button = QtWidgets.QToolButton(checkable=True, checked=False)
        toggle_button.setText(label_text)
        toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        toggle_button.setArrowType(QtCore.Qt.DownArrow)
        toggle_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        toggle_button.setStyleSheet("""
            QToolButton {
                background-color:  #666666;   
                border: none;              
                padding: 5px;              
                border-radius: 5px;          
                color: white;               
            }
        """)

        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 0, 5, 5)

        section_layout.addWidget(toggle_button)
        section_layout.addWidget(content_widget)
        toggle_button.clicked.connect(lambda: self._collapsible_on_pressed(toggle_button, content_widget))
        return section_widget, toggle_button, content_layout
    def _collapsible_on_pressed(self, buttons, collapse_widget):
        checked = buttons.isChecked()
        buttons.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        collapse_widget.setVisible(not checked)
        return
    def _separator(self):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setStyleSheet("margin-top: 5px; margin-bottom: 5px;")
        return line
    def _toggle_axis_checkboxes(self, state, boxes):
        checked = state == QtCore.Qt.Checked
        for checkbox in boxes:
            checkbox.setChecked(checked)
            checkbox.setEnabled(not checked)
    def populate(self):
        self.ctrlListWidget.clear()
        self.data.find()
        for name, info in self.data.items():
            item =QtWidgets.QListWidgetItem(name)
            self.ctrlListWidget.addItem(item)

            screenshot = info.get('screenshot') if isinstance(info, dict) else None
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)
                item.setTextAlignment(QtCore.Qt.AlignHCenter)

    def import_controller(self, create =True):
        selection = cmds.ls(selection =True)
        current_item = self.ctrlListWidget.currentItem()
        if not current_item:
            return
        selected_item = self.ctrlListWidget.selectedItems()

        if create == True:
            if selected_item:
                name = current_item.text()
                original_ctrl = self.data.load(name)
                isOffset = self.offset_checkboxes.isChecked()
                if isOffset:
                    suffix = "_offset"
                    group_name = original_ctrl.replace("_ctrl", suffix)
                    cmds.group(original_ctrl, name=group_name)
                    to_duplicate = group_name
                else:
                    suffix = "_ctrl"
                    to_duplicate = original_ctrl

                if selection:
                    ctrl_map = {}
                    offset_map = {}
                    for selected in selection:
                        dup_name = selected + suffix
                        duplicated = cmds.duplicate(to_duplicate, name=dup_name)[0]
                        cmds.matchTransform(duplicated, selected)

                        if isOffset:
                            children = cmds.listRelatives(duplicated, children=True, type="transform", fullPath=True)
                            if children:
                                uuid = cmds.ls(children[0], uuid=True)[0]
                                real_child = cmds.ls(uuid, long=True)[0]
                                renamed_child = cmds.rename(real_child, selected + "_ctrl")
                                offset_map[selected] = duplicated
                                ctrl_map[selected] = renamed_child
                        else:
                            ctrl_map[selected] = duplicated

                    for selected in selection:
                        new_ctrl = ctrl_map[selected]
                        new_offset = offset_map[selected] if isOffset else None

                        original_parent = cmds.listRelatives(selected, parent=True, type="transform")
                        if original_parent:
                            parent_name = original_parent[0]
                            if parent_name in ctrl_map:
                                new_parent = ctrl_map[parent_name]
                                if isOffset:
                                    cmds.parent(new_offset, new_parent)
                                else:
                                    cmds.parent(new_ctrl, new_parent)

                    cmds.delete(to_duplicate)
            else:
                return

        elif not create and selection:
            if selected_item:
                name = current_item.text()
                original_ctrl = self.data.load(name)
                for selected in selection:
                    if cmds.listRelatives(selected, shapes=True, fullPath=True) != None:
                        dup = cmds.duplicate(original_ctrl, name = original_ctrl+"TMP")
                        original_shape = cmds.listRelatives(dup, s=True)
                        selection_shape = cmds.listRelatives(selected, s=True)
                        cmds.delete(selection_shape)
                        for shape in original_shape:
                            cmds.parent(shape, selected ,add=True, s=True)
                            new_name = f"{selected}Shape" if len(selection_shape)>1 else selection_shape
                            cmds.rename(shape, new_name)
                        cmds.delete(dup)

                cmds.delete(original_ctrl)


            else:
                return
                '''
                selection = cmds.ls(selected =True)[0]
                if len(selection)>1:
                    new_shape = cmds.listRelatives(selection[-1], s=True)
                    for selected in selection[:-1]:
                        original_shape = cmds.listRelatives(selected, s=True)
                        cmds.delete(original_shape)
                        cmds.parent(new_shape, selected, add=True, s=True)
                        cmds.rename(original_shape, new_shape)
                        
                



                else:
                    return
                '''


    def shape_thickness(self):
        value = float(self.thickness_box.value())
        selection = cmds.ls(selection=True)
        if selection:
            ctrl = cmds.listRelatives(selection, s=True)
            for selected in ctrl:
                cmds.setAttr(f"{selected}.overrideEnabled", 1)
                cmds.setAttr(f"{selected}.lineWidth", float(value))

    def shape_size(self, delta):
        selection = cmds.ls(selection=True)
        print(selection)
        if selection:
            for selected in selection:
                value = 1.0 + delta
                cmds.scale(value, value, value, selected + ".cv[*]", relative=True)




    def controller_color(self, color_index):
        selection = cmds.ls(selection=True, long=True)
        shapes = cmds.listRelatives(selection, shapes=True, fullPath=True) or []
        for shape in shapes:
            cmds.setAttr(f"{shape}.overrideEnabled", 1)
            cmds.setAttr(f"{shape}.overrideColor", color_index)

    def reset_color(self):
        selection = cmds.ls(selection=True, long=True)
        shapes = cmds.listRelatives(selection, shapes=True, fullPath=True) or []
        for shape in shapes:
            cmds.setAttr(f"{shape}.overrideEnabled", 0)
            cmds.setAttr(f"{shape}.overrideColor", 0)

    def lock_execute(self):
        selection = cmds.ls(selection=True)
        attribute_list = ["tx", "ty", "tz","rx", "ry", "rz","sx", "sy", "sz","v"]


        for attribute, checkbox in self.checkbox_dict.items():
            if not checkbox.isChecked():
                attribute_list.remove(attribute)

        attribute_list.remove("v")if not self.visibility_checkboxes.isChecked() else None


        is_lock = self.lock_checkboxes.isChecked()
        is_hide = self.hide_checkboxes.isChecked()

        if is_hide or is_lock:
            for selected in selection:
                for each in attribute_list:
                    name = f"{selected}.{each}"
                    is_locked = cmds.getAttr(name, lock=True)
                    is_visible =cmds.attributeQuery(each, node=selected, channelBox=True)
                    if not is_locked:
                        cmds.setAttr(name, lock=is_lock)

                    if not is_visible:
                        cmds.setAttr(name, channelBox=not is_hide, keyable=not is_hide)

    def update_attribute(self, first = True):
        self.shift_attribute_list.clear()
        self.user_attrs = None
        if first == True:
            self.selected_attribute = cmds.ls(selection=True)[0]
        else:
            cmds.select(clear=True)

        self.user_attrs = cmds.listAttr(self.selected_attribute, userDefined=True) or cmds.warning("No custom Attribute detected")

        if self.user_attrs:
            for each in self.user_attrs:
                self.shift_attribute_list.addItem(each)

    def shifting_attr(self, direction):
        index = self.shift_attribute_list.currentRow()
        length = self.shift_attribute_list.count()

        #direction True = Up
        if direction:
            if index <= 0:
                print("Cannot shift up the first item.")
                return
            dir = -1
        elif not direction:
            if index >= length:
                print("Cannot shift down the last item.")
                return
            dir = +1


        cmds.undoInfo(openChunk=True)
        value = index + dir
        test = self.user_attrs[value]
        cmds.setAttr(f"{self.selected_attribute}.{self.user_attrs[value]}", lock=False)
        cmds.deleteAttr(self.selected_attribute, at=self.user_attrs[value])
        print("deleted",self.user_attrs[value])



        if length +value != index:
            self.user_attrs.remove(self.user_attrs[value])
            self.user_attrs.append(test)
        else:
            print("Skipping")



        cmds.undoInfo(closeChunk=True)
        cmds.undo()

        if length +value == index:
            print("Last stuff, skipping")
        else:
            cmds.undoInfo(openChunk=True)
            for i in range(length-1, index-1, -1):
                if i == length-1 :
                    print("test")
                else:
                    cmds.setAttr(f"{self.selected_attribute}.{self.user_attrs[i]}", lock=False)
                    cmds.deleteAttr(self.selected_attribute, at=self.user_attrs[i])
                    print("deleted",self.user_attrs[i])

            cmds.undoInfo(closeChunk=True)
            cmds.undo()


        self.user_attrs = cmds.listAttr(self.selected_attribute, userDefined=True) or []
        self.update_attribute(False)
        self.shift_attribute_list.setCurrentRow(index + dir)


def createDirectory(directory=DIRECTORY):
    if not os.path.exists(directory):
        os.mkdir(directory)

class control_library(dict):
    def save(self, name, directory=DIRECTORY, screenshot=True, **info):
        if screenshot:
            selected = cmds.ls(selection=True)
            result = self.preview(name, directory=directory)
            if result:
                createDirectory(directory)
                path = os.path.join(directory, f"{name}.ma")
                info_file = os.path.join(directory, f"{name}.json")

                info['name'] = name
                info['path'] = path

                cmds.file(rename=path)
                if len(selected) == 1:
                    a = cmds.select(selected)
                    print(a)
                    cmds.file(force=True, type='mayaAscii',exportSelected=True)
                    info['screenshot'] = result
                    with open(info_file,'w') as f:
                        json.dump(info, f, indent=4)

                    self[name]=path
                else:
                    cmds.warning("Select ONE Nurbs Curve")
                    return

            else:
                return


    def find(self, directory=DIRECTORY):
        if not os.path.exists(directory):
            return

        files= os.listdir(directory)
        maya_files = [f for f in files if f.endswith('.ma')]

        for ma in maya_files:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)
            info_file = f"{name}.json"
            if info_file in files:
                info_file = os.path.join(directory, info_file)
                with open(info_file,'r') as f:
                    info = json.load(f)
            else:
                info = {}

            screenshot = f'{name}.jpg'
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, screenshot)

            info['name'] = name
            info['path'] = os.path.join(directory, ma)

            self[name]= info

    def load(self, name):
        path = self[name]['path']

        ref_node = cmds.file(path, reference=True, returnNewNodes=False, namespace="TMP")

        ref_nodes = cmds.referenceQuery(ref_node, nodes=True)
        top_nodes = cmds.ls(ref_nodes, assemblies=True)

        duplicated = cmds.duplicate(top_nodes,renameChildren=True)[0]
        duplicated = cmds.rename(duplicated, f"{duplicated}_ctrl")

        cmds.file(path, removeReference=True)

        return duplicated
    def preview(self, name, directory):
        camera_name, camera_shape = cmds.camera(orthographic=True)
        camera_name = cmds.rename(camera_name, "isoCam")

        cmds.setAttr(f"{camera_name}.translateX", 30)
        cmds.setAttr(f"{camera_name}.translateY", 30)
        cmds.setAttr(f"{camera_name}.translateZ", 30)
        cmds.setAttr(f"{camera_name}.rotateX", -35.264)
        cmds.setAttr(f"{camera_name}.rotateY", 45)
        cmds.setAttr(f"{camera_name}.rotateZ", 0)

        cmds.lookThru(camera_name)

        cmds.setAttr("defaultResolution.width", 200)
        cmds.setAttr("defaultResolution.height", 200)
        cmds.setAttr(f"{camera_name}.displayResolution", 1)
        cmds.setAttr(f"{camera_name}.displayGateMask", 1)


        panel = cmds.getPanel(withFocus=True)
        if cmds.getPanel(typeOf=panel) == "modelPanel":
            cmds.modelEditor(panel, edit=True, camera=camera_name)
            cmds.viewFit()


        #################

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Screenshot Preview")
        dialog.resize(400, 300)
        main_layout = QtWidgets.QVBoxLayout(dialog)

        translate_layout = QtWidgets.QHBoxLayout()
        tx_label = QtWidgets.QLabel('Translate X:')
        ty_label = QtWidgets.QLabel('Translate Y:')
        tz_label = QtWidgets.QLabel('Translate Z:')
        tx_spin = QtWidgets.QDoubleSpinBox()
        ty_spin = QtWidgets.QDoubleSpinBox()
        tz_spin = QtWidgets.QDoubleSpinBox()
        tx_spin.setValue(30)
        ty_spin.setValue(30)
        tz_spin.setValue(30)
        tx_spin.valueChanged.connect(lambda val: cmds.setAttr(f"{camera_name}.translateX", val))
        ty_spin.valueChanged.connect(lambda val: cmds.setAttr(f"{camera_name}.translateY", val) )
        tz_spin.valueChanged.connect(lambda val: cmds.setAttr(f"{camera_name}.translateZ", val) )
        translate_layout.addWidget(tx_label)
        translate_layout.addWidget(ty_label)
        translate_layout.addWidget(tz_label)
        translate_layout.addWidget(tx_spin)
        translate_layout.addWidget(ty_spin)
        translate_layout.addWidget(tz_spin)

        zoom_layout = QtWidgets.QHBoxLayout()
        zoom_label = QtWidgets.QLabel("Zoom Camera")
        zoom_line = QtWidgets.QLineEdit()
        zoom_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        zoom_slider.valueChanged.connect(lambda val: self.update_zoom(val, zoom_line, camera_name))

        zoom_slider.setRange(10,30)
        zoom_slider.setValue(20)

        zoom_layout.addWidget(zoom_label)
        zoom_layout.addWidget(zoom_line)
        zoom_layout.addWidget(zoom_slider)
        done_layout = QtWidgets.QHBoxLayout()
        done_button = QtWidgets.QPushButton("Done")
        done_layout.addWidget(done_button)
        done_button.clicked.connect(dialog.accept)



        main_layout.addLayout(translate_layout)
        main_layout.addLayout(zoom_layout)
        main_layout.addLayout(done_layout)
        result = dialog.exec_()


        if result == QtWidgets.QDialog.Accepted:
            cmds.setAttr(f"{camera_name}.displayResolution",0)
            cmds.setAttr(f"{camera_name}.displayGateMask", 0)
            path = self.save_screenshot(name,directory, camera_name)
            return path
        else:
            cmds.delete(camera_name)

    def update_zoom(self, val, zoom_line, camera_name):
        zoom = val / 10.0
        zoom_line.setText(str(zoom))
        cmds.setAttr(f"{camera_name}Shape.cameraScale", 3.2-zoom)

    def save_screenshot(self, name, directory, camera_name):
        path = os.path.join(directory, f"{name}.jpg")

        cmds.select(clear=True)
        cmds.setAttr('defaultRenderGlobals.imageFormat',8)
        cmds.cameraView(camera=camera_name)
        cmds.playblast(completeFilename=path, forceOverwrite=True, format = 'image', width=200, height = 200,
                       showOrnaments=False, startTime =1, endTime=1, viewer=False)
        cmds.delete(camera_name)

        return path


class colorList():
    def get_color_by_index(self, index):
        maya_colors = [
            (140, 140, 140),        # 0
            (0, 0, 0),         # 1
            (63, 63, 63),      # 2
            (127, 127, 127),   # 3
            (155, 0, 40),      # 4
            (0, 0, 255),       # 5
            (0, 4, 95),       # 6
            (0, 70, 24),       # 6
            (37, 0, 67),       # 7
            (199, 0, 199),     # 8
            (137, 71, 51),     # 9
            (62, 34, 31),      # 10
            (153, 36, 0),      # 11
            (255, 0, 0),       # 12
            (0, 255, 0),       # 13
            (0, 65, 153),      # 14
            (255, 255, 255),   # 15
            (255, 255, 0),     # 16
            (99, 220, 255),    # 17
            (67, 255, 162),    # 18
            (255, 175, 175),   # 19
            (227, 172, 121),   # 20
            (255, 255, 98),    # 21
            (0, 153, 83),      # 22
            (160, 105, 48),    # 23
            (158, 160, 48),    # 24
            (104, 160, 48),    # 25
            (48, 160, 93),     # 26
            (48, 160, 160),    # 27
            (48, 103, 160),    # 28
            (111, 48, 160),    # 29
            (160, 48, 111),    # 30
        ]
        return maya_colors[index]


def getWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def show_control_tool():
    global controller_UI

    try:
        controller_UI.close()
        controller_UI.deleteLater()
    except:
        pass

    parent = getWindow()
    controller_UI = ControllerLibrary_UI(parent)
    controller_UI.show()



