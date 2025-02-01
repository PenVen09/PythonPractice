from maya import cmds
from functools import partial
import re

ops = {
    '0': 'error',
    1: lambda x, y: x + y,
    2: lambda x, y: x * y,
    3: lambda x, y: x / y,
}
class BaseWindow(object):

    windowName = "Multiple_Object_Transformation"

    def __init__(self):
        self.tranSize = []
        self.rotaSize = []
        self.scaSize = []
        self.finalValue = []
        self.TBC= "False"
        self.RBC= "False"
        self.SBC= "False"




    def show(self):
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()

        cmds.showWindow()


    def buildUI(self):
        column = cmds.columnLayout(adjustableColumn=True, columnAlign="center")

        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="                                  Enable:")
        cmds.checkBoxGrp("Grp", numberOfCheckBoxes=3, label1='Translation', label2='Rotation',
                         label3='Scale',  cc1 = self.Maintoggle, v1=True, cc2=self.Maintoggle, v2=True, cc3=self.Maintoggle, v3=True)

        cmds.setParent(column)
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="                          Operations:")
        cmds.radioButtonGrp("Radio_Grp", l1="+", l2="X", l3="/", numberOfRadioButtons=3, select=1, cc1="1", cc2="2", cc3="3")

        cmds.setParent(column)
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="                              Template:")
        cmds.radioButtonGrp("Radio_Template", l1="1", l2="5", l3="10", l4="50", numberOfRadioButtons=4, select=1)

        cmds.setParent(column)

        cmds.rowLayout(numberOfColumns=17)
        cmds.text(label='                              Translation', align="center")
        cmds.button("TranslationX<<",label="<<", command=partial(self.button, "TranslationX", "<<"))
        cmds.button("TranslationX<",label="<", command=partial(self.button, "TranslationX", "<"))
        cmds.floatField("TranslationX", value=0.0)
        cmds.button("TranslationX>",label=">", command=partial(self.button, "TranslationX", ">"))
        cmds.button("TranslationX>>",label=">>", command=partial(self.button, "TranslationX", ">>"))
        cmds.button("TranslationY<<",label="<<", command=partial(self.button, "TranslationY", "<<"))
        cmds.button("TranslationY<",label="<", command=partial(self.button, "TranslationY", "<"))
        cmds.floatField("TranslationY", value=0.0)
        cmds.button("TranslationY>",label=">", command=partial(self.button, "TranslationY", ">"))
        cmds.button("TranslationY>>",label=">>", command=partial(self.button, "TranslationY", ">>"))
        cmds.button("TranslationZ<<",label="<<", command=partial(self.button, "TranslationZ", "<<"))
        cmds.button("TranslationZ<",label="<", command=partial(self.button, "TranslationZ", "<"))
        cmds.floatField("TranslationZ", value=0.0)
        cmds.button("TranslationZ>",label=">", command=partial(self.button, "TranslationZ", ">"))
        cmds.button("TranslationZ>>",label=">>", command=partial(self.button, "TranslationZ", ">>"))
        cmds.button("TransApply", label="Apply", command = self.TranlateButtonC)


        cmds.setParent(column)
        cmds.rowLayout(numberOfColumns=17)
        cmds.text(label='                                     Rotate', align="center")
        cmds.button("RotationX<<",label="<<", command=partial(self.button, "RotationX", "<<"))
        cmds.button("RotationX<",label="<", command=partial(self.button, "RotationX", "<"))
        cmds.floatField("RotationX", value=0.0)
        cmds.button("RotationX>",label=">", command=partial(self.button, "RotationX", ">"))
        cmds.button("RotationX>>",label=">>", command=partial(self.button, "RotationX", ">>"))
        cmds.button("RotationY<<",label="<<", command=partial(self.button, "RotationY", "<<"))
        cmds.button("RotationY<",label="<", command=partial(self.button, "RotationY", "<"))
        cmds.floatField("RotationY", value=0.0)
        cmds.button("RotationY>",label=">", command=partial(self.button, "RotationY", ">"))
        cmds.button("RotationY>>",label=">>", command=partial(self.button, "RotationY", ">>"))
        cmds.button("RotationZ<<",label="<<", command=partial(self.button, "RotationZ", "<<"))
        cmds.button("RotationZ<",label="<", command=partial(self.button, "RotationZ", "<"))
        cmds.floatField("RotationZ", value=0.0)
        cmds.button("RotationZ>",label=">", command=partial(self.button, "RotationZ", ">"))
        cmds.button("RotationZ>>",label=">>", command=partial(self.button, "RotationZ", ">>"))
        cmds.button("RotApply", label="Apply", command=self.RotateButtonC)

        cmds.setParent(column)
        cmds.rowLayout(numberOfColumns=17)
        cmds.text(label='                                        Scale', align="center")
        cmds.button("ScaleX<<",label="<<", command=partial(self.button, "ScaleX", "<<"))
        cmds.button("ScaleX<",label="<", command=partial(self.button, "ScaleX", "<"))
        cmds.floatField("ScaleX", value=0.0)
        cmds.button("ScaleX>",label=">", command=partial(self.button, "ScaleX", ">"))
        cmds.button("ScaleX>>",label=">>", command=partial(self.button, "ScaleX", ">>"))
        cmds.button("ScaleY<<",label="<<", command=partial(self.button, "ScaleY", "<<"))
        cmds.button("ScaleY<",label="<", command=partial(self.button, "ScaleY", ">"))
        cmds.floatField("ScaleY", value=0.0)
        cmds.button("ScaleY>",label=">", command=partial(self.button, "ScaleY", ">"))
        cmds.button("ScaleY>>",label=">>", command=partial(self.button, "ScaleY", ">>"))
        cmds.button("ScaleZ<<",label="<<", command=partial(self.button, "ScaleZ", "<<"))
        cmds.button("ScaleZ<",label="<", command=partial(self.button, "ScaleZ", "<"))
        cmds.floatField("ScaleZ", value=0.0)
        cmds.button("ScaleZ>",label=">", command=partial(self.button, "ScaleZ", ">"))
        cmds.button("ScaleZ>>",label=">>", command=partial(self.button, "ScaleZ", ">>"))
        cmds.button("ScApply", label="Apply", command=self.ScaButtonC)

        cmds.setParent(column)
        #row = cmds.rowLayout(numberOfColumns=3)
        cmds.button("Main_Apply", label="Apply All Transformation", command=self.mainButton)
        cmds.button(label="Reset", command=self.reset)
        cmds.button(label="Close", command=self.close)

    def button(self, bName, value, *args):
        radio = cmds.radioButtonGrp("Radio_Template", q=True, select=True)
        FloatF = cmds.floatField(bName, q=True, v=True)
        Lib = {
            1 : 1,
            2 : 5,
            3: 10,
            4: 50,
        }
        tem = Lib[radio]
        if value == "<<":
            C = FloatF - (tem*2)

        elif value == "<":
            C= FloatF - tem

        elif value == ">>":
             C = FloatF + (tem*2)

        elif value == ">":
            C = FloatF + tem


        cmds.floatField(bName, edit=True, v=C)






    def TranlateButtonC(self, *args):
        self.TBC = "True"
        self.applyMain()

    def RotateButtonC(self, *args):
        self.RBC = "True"
        self.applyMain()

    def ScaButtonC(self, *args):
        self.SBC = "True"
        self.applyMain()

    def mainButton(self, *args):
        self.TBC = "True"
        self.RBC = "True"
        self.SBC = "True"
        self.applyMain()

    def Maintoggle(self, *args):
        translateValue = cmds.checkBoxGrp("Grp", q=True, v1=True)
        rotateValue = cmds.checkBoxGrp("Grp", q=True, v2=True)
        scaleValue = cmds.checkBoxGrp("Grp", q=True, v3=True)
        library= {
            "tValue": [["TranslationX","TranslationY", "TranslationZ"], "TransApply", translateValue],
            "rValue": [["RotationX","RotationY","RotationZ"], "RotApply", rotateValue],
            "sValue": [["ScaleX","ScaleY","ScaleZ"], "ScApply", scaleValue]
        }
        for i in library:
            cmds.floatField(library[i][0][0], edit=True, en=library[i][2])
            cmds.floatField(library[i][0][1], edit=True, en=library[i][2])
            cmds.floatField(library[i][0][2], edit=True, en=library[i][2])
            cmds.button(library[i][1], edit=True, en=library[i][2])


    def applyMain(self, *args):
        applyTr = cmds.button("TransApply", q=True, en=True)
        applyRo = cmds.button("RotApply", q=True, en=True)
        applySc = cmds.button("ScApply", q=True, en=True)

        translateValue = cmds.checkBoxGrp("Grp", q=True, v1=True)
        rotateValue = cmds.checkBoxGrp("Grp", q=True, v2=True)
        scaleValue = cmds.checkBoxGrp("Grp", q=True, v3=True)
        self.selection = cmds.ls(sl=True)
        self.tranSize=['TranslationX','TranslationY','TranslationZ']
        self.rotaSize=['RotationX','RotationY','RotationZ']
        self.scaSize=['ScaleX','ScaleY','ScaleZ']

        dict = {
            "tValue": ["translate", "t", applyTr, self.tranSize, translateValue],
            "rValue": ["rotate", "ro", applyRo, self.rotaSize, rotateValue],
            "sValue": ["scale", "s", applySc, self.scaSize, scaleValue],
        }

        if self.selection == []:
            cmds.warning("Please select the objects")
        else:
            for i in dict:
                if dict[i][2] != dict[i][4] or dict[i][2] == False or dict[i][4] == False:
                    print("You disabled this:")
                    print(dict[i][0])
                    pass
                else:
                    for a in self.selection:
                        S = cmds.getAttr('%s.%s' % (a, dict[i][0]))
                        self.finalValue =[]
                        for val in range(0,3):
                            valuess = cmds.floatField(dict[i][3][val], q=True, v=True)
                            h= self.finalValue
                            h.append(valuess)
                        operan = cmds.radioButtonGrp("Radio_Grp", q=True, select=True)

                        for az in S:
                            final = list(S[0]) + list(self.finalValue)
                            final1 = ops[operan](final[0],final[3])
                            final2 = ops[operan](final[1],final[4])
                            final3 = ops[operan](final[2],final[5])
                            fin = (final1, + final2, + final3,)


                            if i == "tValue" and self.TBC == "True":
                                cmds.xform(a, t= fin)


                            elif i == "rValue" and self.RBC == "True":
                                cmds.xform(a, ro= fin)


                            elif i == "sValue" and self.SBC == "True":
                                cmds.xform(a, s= fin)


                            else:
                                pass

        self.TBC = "False"
        self.RBC = "False"
        self.SBC = "False"



    def reset(self, *args):
        list = ["TranslationX","TranslationY", "TranslationZ", "TranslationY", "RotationX", "RotationY","RotationZ",
                "ScaleX","ScaleY","ScaleZ"]
        for a in list:
            cmds.floatField(a, edit=True, value=0.0)

    def close(self, *args):
        cmds.deleteUI(self.windowName)


lib = BaseWindow()
lib.show()

