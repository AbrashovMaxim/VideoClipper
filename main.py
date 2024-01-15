from PyQt5 import QtCore
from moviepy.editor import *
import textwrap as tw
import os

from PyQt5.QtWidgets import QApplication, QWidget, QLayout, QFileDialog, QLabel, QCheckBox, QSpinBox, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QFormLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QAbstractItemView

class TimeVideo:
    seconds = 0
    minutes = 0
    hours = 0
    def __init__(self, time):
        print(time)
        try:
            time = int(time)
            self.hours = time//3600
            self.seconds = time
            while self.seconds > 60:
                self.minutes = 1 if self.minutes == 60 else self.minutes+1
                self.seconds -=60
        except:
            time = time.split(':')
            self.seconds = int(time[2])
            self.minutes = int(time[1])
            self.hours = int(time[0])
    
    def _get_totalSeconds(self):
        return self.seconds + (self.minutes * 60) + (self.hours * 3600)
    
    def _plus_Time(self, hour: int = 0, minute: int = 0, second: int = 0):
        self.hours += hour
        self.minutes += minute
        self.seconds += second

class Window(QWidget):

    lastVideo = ''
    lastIMG = ''
    time_line_from = None

    tL_to_HH = 0
    tL_to_MM = 0
    tL_to_SS = 0
    tL_from_HH = 0
    tL_from_MM = 0
    tL_from_SS = 0

    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self._init_add())
        self.layout.addWidget(self._init_table())
    
    def _init_add(self) -> QWidget:
        GroupBox = QGroupBox(title = "Добавление")
        FormLayout = QFormLayout()
        FormLayout.setVerticalSpacing(10)

        # ============================= Открыть видео =============================
        
        self.ButtonVideo = QPushButton("Открыть видео")
        self.ButtonVideo.clicked.connect(self._openFileVideo)
        FormLayout.addRow(QLabel("Видео"), self.ButtonVideo)
        
        # =========================================================================
        # =============================== Обрезать ================================
        
        self.CheckBox = QCheckBox(self)
        self.CheckBox.setEnabled(False)
        self.CheckBox.stateChanged.connect(self._change_cut)
        FormLayout.addRow(QLabel("Обрезать"), self.CheckBox)
        
        # =========================================================================
        # ========================== Обрезать QSpinBox's ==========================
        
        HorBoxLayout = QHBoxLayout()
        temp_Form1 = QFormLayout()
        temp_Form2 = QFormLayout()
        
        HorBoxLayout_to = QHBoxLayout()
        temp_Form1_temp1 = QFormLayout()
        self.timeLine_to_HH = QSpinBox()
        self.timeLine_to_HH.setValue(0)
        self.timeLine_to_HH.setEnabled(False)
        self.timeLine_to_HH.valueChanged.connect(lambda x: self._slotTo_valueChanged(x, 'to_HH'))
        temp_Form1_temp1.addRow(QLabel("  :  "), self.timeLine_to_HH)

        temp_Form1_temp2 = QFormLayout()
        self.timeLine_to_MM = QSpinBox()
        self.timeLine_to_MM.setValue(0)
        self.timeLine_to_MM.setEnabled(False)
        self.timeLine_to_MM.valueChanged.connect(lambda x: self._slotTo_valueChanged(x, 'to_MM'))
        temp_Form1_temp2.addRow(QLabel("  :  "), self.timeLine_to_MM)
        temp_Form1_temp3 = QFormLayout()

        self.timeLine_to_SS = QSpinBox()
        self.timeLine_to_SS.setValue(0)
        self.timeLine_to_SS.setEnabled(False)
        self.timeLine_to_SS.valueChanged.connect(lambda x: self._slotTo_valueChanged(x, 'to_SS'))
        temp_Form1_temp3.addRow(QLabel("  :  "), self.timeLine_to_SS)
        HorBoxLayout_to.addLayout(temp_Form1_temp1)
        HorBoxLayout_to.addLayout(temp_Form1_temp2)
        HorBoxLayout_to.addLayout(temp_Form1_temp3)

        HorBoxLayout_from = QHBoxLayout()
        temp_Form2_temp1 = QFormLayout()
        self.timeLine_from_HH = QSpinBox()
        self.timeLine_from_HH.setValue(0)
        self.timeLine_from_HH.setEnabled(False)
        self.timeLine_from_HH.valueChanged.connect(lambda x: self._slotFrom_valueChanged(x, 'from_HH'))
        temp_Form2_temp1.addRow(QLabel("  :  "), self.timeLine_from_HH)

        temp_Form2_temp2 = QFormLayout()
        self.timeLine_from_MM = QSpinBox()
        self.timeLine_from_MM.setValue(0)
        self.timeLine_from_MM.setEnabled(False)
        self.timeLine_from_MM.valueChanged.connect(lambda x: self._slotFrom_valueChanged(x, 'from_MM'))
        temp_Form2_temp2.addRow(QLabel("  :  "), self.timeLine_from_MM)

        temp_Form2_temp3 = QFormLayout()
        self.timeLine_from_SS = QSpinBox()
        self.timeLine_from_SS.setValue(0)
        self.timeLine_from_SS.setEnabled(False)
        self.timeLine_from_SS.valueChanged.connect(lambda x: self._slotFrom_valueChanged(x, 'from_SS'))
        temp_Form2_temp3.addRow(QLabel("  :  "), self.timeLine_from_SS)

        HorBoxLayout_from.addLayout(temp_Form2_temp1)
        HorBoxLayout_from.addLayout(temp_Form2_temp2)
        HorBoxLayout_from.addLayout(temp_Form2_temp3)

        temp_Form1.addRow(QLabel("  С  "), HorBoxLayout_to)
        temp_Form2.addRow(QLabel("  До  "), HorBoxLayout_from)

        HorBoxLayout.addLayout(temp_Form1)
        HorBoxLayout.addLayout(temp_Form2)

        FormLayout.addRow(HorBoxLayout)
        
        # =========================================================================
        # ======================== Добавить водяной знак ==========================

        self.ButtonImg = QPushButton("Открыть водяной знак")
        self.ButtonImg.clicked.connect(self._openFileIMG)
        FormLayout.addRow(QLabel("Водяной знак:"), self.ButtonImg)

        # =========================================================================
        # ================================ Текст ==================================

        self.Text = QTextEdit()
        FormLayout.addRow(QLabel("Текст:"), self.Text)

        # =========================================================================
        # =============================== Кнопки ==================================

        VerBoxLayout = QVBoxLayout()

        self.Save = QPushButton("Сохранить")
        self.Save.setEnabled(False)
        self.Save.clicked.connect(self._save)
        VerBoxLayout.addWidget(self.Save)

        self.Sbros = QPushButton("Сброс")
        self.Sbros.clicked.connect(self._sbros)
        VerBoxLayout.addWidget(self.Sbros)
        FormLayout.addRow(VerBoxLayout)

        # =========================================================================
        GroupBox.setLayout(FormLayout)
        return GroupBox
    
    def _init_table(self) -> QWidget:
        GroupBox = QGroupBox(title = "Добавление")
        VerBoxLayout = QVBoxLayout()
        self.TableWidget = QTableWidget(0, 5)
        self.TableWidget.setHorizontalHeaderLabels(["Имя файла", "Текст", "Водяной знак", "Обрезать", "Статус"])
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        VerBoxLayout.addWidget(self.TableWidget)

        HorBoxLayout = QHBoxLayout()
        Start = QPushButton("Начать")
        Start.clicked.connect(self._start_Table)
        HorBoxLayout.addWidget(Start)
        Delete = QPushButton("Удалить")
        Delete.clicked.connect(self._remove_Table)
        HorBoxLayout.addWidget(Delete)
        SbrosTable = QPushButton("Сброс")
        SbrosTable.clicked.connect(self._sbros_Table)
        HorBoxLayout.addWidget(SbrosTable)
        VerBoxLayout.addLayout(HorBoxLayout)

        GroupBox.setLayout(VerBoxLayout)
        return GroupBox

    def _save(self):
        if self.lastVideo == '': return
        rowCount = self.TableWidget.rowCount()
        self.TableWidget.insertRow(rowCount)
        self.TableWidget.setItem(rowCount, 0, QTableWidgetItem(self.lastVideo))
        self.TableWidget.setItem(rowCount, 1, QTableWidgetItem(self.Text.toPlainText()))
        self.TableWidget.setItem(rowCount, 2, QTableWidgetItem(self.lastIMG))
        if self.CheckBox.checkState() == QtCore.Qt.CheckState.Checked: item = f'{self.timeLine_to_HH.value()}:{self.timeLine_to_MM.value()}:{self.timeLine_to_SS.value()}|{self.timeLine_from_HH.value()}:{self.timeLine_from_MM.value()}:{self.timeLine_from_SS.value()}'
        else: item = ''
        self.TableWidget.setItem(rowCount, 3, QTableWidgetItem(item))
        self.TableWidget.setItem(rowCount, 4, QTableWidgetItem('Добавлен'))
        self._sbros("Save")

    def _sbros(self, typ="Sbros"):
        if typ == "Sbros": 
            self.ButtonImg.setText("Открыть водяной знак")
            self.lastIMG = ''
        
        self.ButtonVideo.setText("Открыть видео")
        self.lastVideo = ''
        self.CheckBox.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.CheckBox.setEnabled(False)
        self.Save.setEnabled(False)
        
        self.timeLine_to_HH.setValue(0)
        self.timeLine_to_MM.setValue(0)
        self.timeLine_to_SS.setValue(0)

        self.timeLine_from_HH.setValue(0)
        self.timeLine_from_MM.setValue(0)
        self.timeLine_from_SS.setValue(0)

        self.time_line_from = None
    
    def _openFileVideo(self):
        FileVideo = QFileDialog.getOpenFileName(self, 'Открыть видео', self.lastVideo, "Video Files (*.mp4 *.avi)")
        if FileVideo[0] != '':
            clip = VideoFileClip(FileVideo[0])
            temp_Video = TimeVideo(int(clip.duration))
            self._sbros('OpenFile')
            self.time_line_from = temp_Video

            self.timeLine_from_HH.setValue(temp_Video.hours)
            self.timeLine_from_MM.setValue(temp_Video.minutes)
            self.timeLine_from_SS.setValue(temp_Video.seconds)

            self.CheckBox.setEnabled(True)

            self.Save.setEnabled(True)

            self.lastVideo = FileVideo[0]
            fileName = FileVideo[0].split('/')[-1]
            self.ButtonVideo.setText(fileName)
    
    def _openFileIMG(self):
        FileIMG = QFileDialog.getOpenFileName(self, 'Открыть водяной знак', self.lastIMG, "PNG Files (*.png)")
        if FileIMG[0] != '':
            self.lastIMG = FileIMG[0]
            fileName = FileIMG[0].split('/')[-1]
            self.ButtonImg.setText(fileName)

    def _change_cut(self, state):
        self.timeLine_to_HH.setEnabled(state)
        self.timeLine_to_MM.setEnabled(state)
        self.timeLine_to_SS.setEnabled(state)
        self.timeLine_from_HH.setEnabled(state)
        self.timeLine_from_MM.setEnabled(state)
        self.timeLine_from_SS.setEnabled(state)

    def _start_Table(self):
        rowCount = self.TableWidget.rowCount()
        for i in range(rowCount): self.TableWidget.setItem(i, 4, QTableWidgetItem("Загрузка"))

        for i in range(self.TableWidget.rowCount()):
            self.TableWidget.setItem(i, 4, QTableWidgetItem("Монтирование..."))
            
            fileName = self.TableWidget.item(i, 0).text()
            text = self.TableWidget.item(i, 1).text()
            znak = self.TableWidget.item(i, 2).text()
            obrez = self.TableWidget.item(i, 3).text()
            
            compose = []

            clip = VideoFileClip(fileName)

            if obrez != '':
                obrez = obrez.split('|')
                to_time = TimeVideo(obrez[0])
                from_time = TimeVideo(obrez[1])
                clip = clip.subclip(to_time._get_totalSeconds(), from_time._get_totalSeconds())


            clip = vfx.resize(clip, height=660, width=1080)

            black_image = (ImageClip("blackscreen.png")
                        .set_duration(clip.duration))
            compose.append(black_image)
            compose.append(clip.set_pos(("center", "center")))
            if znak != '':
                znak_image = (ImageClip(znak)
                            .set_duration(clip.duration)
                            .resize(height=500)
                            .set_pos(("right", "bottom"))
                            .set_opacity(0.14)
                            .rotate(15)
                            .margin(bottom=20, left=50))
                compose.append(znak_image)
            if text != '':
                text_clip = TextClip(tw.fill(text, width=15), fontsize=100, color='white').set_pos(("center", "top")).set_duration(clip.duration).margin(top=150)
                compose.append(text_clip)

            final = CompositeVideoClip(compose)

            final.write_videofile(f"result/{fileName.split('/')[-1]}_9x16.mp4", fps=30)
            # ==================================================
            compose = []

            clip = VideoFileClip(fileName)
            if obrez != '':
                obrez = obrez.split('|')
                to_time = TimeVideo(obrez[0])
                from_time = TimeVideo(obrez[1])
                clip = clip.subclip(to_time._get_totalSeconds(), from_time._get_totalSeconds())

            compose.append(clip.set_pos(("center", "center")))

            if znak != '':
                znak_image = (ImageClip(znak)
                            .set_duration(clip.duration)
                            .resize(height=500)
                            .set_pos(("right", "bottom"))
                            .set_opacity(0.13)
                            .rotate(15)
                            .margin(bottom=20, left=25))
                compose.append(znak_image)
            if len(compose) == 1: final = compose[0]
            else: final = CompositeVideoClip(compose)

            final.write_videofile(f"result/{fileName.split('/')[-1]}_16x9.mp4", fps=30)
            self.TableWidget.setItem(i, 4, QTableWidgetItem("Выполнен"))

    def _remove_Table(self):
        self.TableWidget.removeRow(self.TableWidget.currentRow())

    def _sbros_Table(self):
        rowCount = self.TableWidget.rowCount()
        while rowCount > 0:
            self.TableWidget.removeRow(rowCount-1)
            rowCount -= 1

    def _slotFrom_valueChanged(self, a: int, typ: str):
        type_slot = typ.split('_')

        new_Time = TimeVideo(f'{self.timeLine_from_HH.value()}:{self.timeLine_from_MM.value()}:{self.timeLine_from_SS.value()}')
        new_Time2 = TimeVideo(f'{self.timeLine_to_HH.value()}:{self.timeLine_to_MM.value()}:{self.timeLine_to_SS.value()}')
        if self.time_line_from == None: return
        if self.time_line_from._get_totalSeconds() < new_Time._get_totalSeconds() or new_Time._get_totalSeconds() < new_Time2._get_totalSeconds():
            if type_slot[1] == 'HH': self.timeLine_from_HH.setValue(self.tL_from_HH.text)
            elif type_slot[1] == 'MM': self.timeLine_from_MM.setValue(self.tL_from_MM)
            elif type_slot[1] == 'SS': self.timeLine_from_SS.setValue(self.tL_from_SS)
            return

        if type_slot[1] == 'HH': self.tL_from_HH = a
        elif type_slot[1] == 'MM': self.tL_from_MM = a
        elif type_slot[1] == 'SS': self.tL_from_SS = a


    def _slotTo_valueChanged(self, a: int, typ: str):
        type_slot = typ.split('_')

        new_Time = TimeVideo(f'{self.timeLine_to_HH.value()}:{self.timeLine_to_MM.value()}:{self.timeLine_to_SS.value()}')
        if self.time_line_from == None: return
        if self.time_line_from._get_totalSeconds() <= new_Time._get_totalSeconds():
            if type_slot[1] == 'HH': self.timeLine_to_HH.setValue(self.tL_to_HH)
            elif type_slot[1] == 'MM': self.timeLine_to_MM.setValue(self.tL_to_MM)
            elif type_slot[1] == 'SS': self.timeLine_to_SS.setValue(self.tL_to_SS)
            return

        if type_slot[1] == 'HH': self.tL_to_HH = a
        elif type_slot[1] == 'MM': self.tL_to_MM = a
        elif type_slot[1] == 'SS': self.tL_to_SS = a

if __name__ == '__main__':

    App = QApplication([])

    Win = Window()

    Win.show()

    App.exec_()

