import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QListWidget, QFileDialog, QMessageBox,
    QSplitter, QFrame, QLabel, QAction, QMenu, QFontDialog, QInputDialog
)
from PyQt5.QtGui import QFont, QColor, QPainter, QPixmap, QSyntaxHighlighter, QTextCharFormat, QTextCursor
from PyQt5.QtCore import Qt, QTimer, QRegExp


def create_dark_site_structure(base_path='DARK SITE'):
    """Create the folder hierarchy used by the project."""
    os.makedirs(base_path, exist_ok=True)
    mosc = os.path.join(base_path, 'MOSCÚ PANDA XL.BDK')
    for sub, files in {
        'VS-1': ['GPT_BDK_1.BDK', 'GPT_BDK_2.BDK'],
        'M1': ['GEMINI_BDK_1.BDK', 'GEMINI_BDK_2.BDK'],
        'CY1': ['GROK_BDK_1.BDK', 'GROK_BDK_2.BDK'],
    }.items():
        sub_path = os.path.join(mosc, sub)
        os.makedirs(sub_path, exist_ok=True)
        for fname in files:
            open(os.path.join(sub_path, fname), 'a', encoding='utf-8').close()
    misifus = os.path.join(base_path, 'MISIFÚS FUMADOX.VTHA')
    for sub, files in {
        'VS00-1': [
            'PANGETYUM.VTHA',
            'MEMORIA ETERNA.VTHA',
            ('LOGS_DIARIOS', ['LOG_GPT_DIARIO.VTHA']),
            ('DIRECTRICES_Y_REGLAS_OPERATIVAS', ['REGLAS_GPT.VTHA']),
        ],
        'M1': [
            'PANGETYUM.VTHA',
            'MEMORIA ETERNA.VTHA',
            ('LOGS_DIARIOS', ['LOG_GEMINI_DIARIO.VTHA']),
            ('DIRECTRICES_Y_REGLAS_OPERATIVAS', ['REGLAS_GEMINI.VTHA']),
        ],
        'CY1': [
            'PANGETYUM.VTHA',
            'MEMORIA ETERNA.VTHA',
            ('LOGS_DIARIOS', ['LOG_GROK_DIARIO.VTHA']),
            ('DIRECTRICES_Y_REGLAS_OPERATIVAS', ['REGLAS_GROK.VTHA']),
        ],
    }.items():
        sub_path = os.path.join(misifus, sub)
        os.makedirs(sub_path, exist_ok=True)
        for item in files:
            if isinstance(item, tuple):
                folder, f_list = item
                folder_path = os.path.join(sub_path, folder)
                os.makedirs(folder_path, exist_ok=True)
                for fname in f_list:
                    open(os.path.join(folder_path, fname), 'a', encoding='utf-8').close()
            else:
                open(os.path.join(sub_path, item), 'a', encoding='utf-8').close()
    fairy = os.path.join(base_path, 'FAIRY BLACK')
    for sub in ['IMAGENES_DE_FONDO','CONFIGURACIONES_GENERALES','RUTAS_LINKS','GALERIAS','DOCS_GENERALES']:
        os.makedirs(os.path.join(fairy, sub), exist_ok=True)

SETTINGS_FILE = 'config.vtha'
MEMORY_FILE = 'pangetyum.vtha'

class SettingsManager:
    def __init__(self, path=SETTINGS_FILE):
        self.path = path
        self.settings = {
            'fondos_dir': 'fondos',
            'bg_scale_mode': 'expand',
            'bg_custom_scale': 1.0
        }
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                self.settings.update(json.load(f))
        else:
            self.save()

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

class SimpleHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []
        kw_format = QTextCharFormat()
        kw_format.setForeground(QColor('#ff66cc'))
        keywords = ['def','class','import','from','return','if','else','while','for']
        for kw in keywords:
            self.rules.append((QRegExp(r'\b'+kw+r'\b'), kw_format))
        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor('#660066'))
        self.rules.append((QRegExp('".*"'), str_fmt))
        self.rules.append((QRegExp("'.*'"), str_fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

class TarantulaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('🕷 Torre de Marfil IDE')
        self.resize(1200,800)
        self.settings = SettingsManager()
        self.memory_file = MEMORY_FILE

        self.backgrounds = []
        self.bg_index = 0
        self.load_backgrounds()
        create_dark_site_structure()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)
        self.editor = QTextEdit()
        layout.addWidget(self.editor)
        self.slogan_label = QLabel('🕷🕸👁‍🗨¡HOY CONSTRUIMOS EL IMPERIO!💜🖤🔥🚀')
        self.slogan_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.slogan_label)
        self.editor.setFont(QFont('Old English', 14))
        self.highlighter = SimpleHighlighter(self.editor.document())

        self.create_menu()
        self.load_memory()
        self.color_hue = 0
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.cycle_slogan_color)
        self.color_timer.start(200)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_background)
        if self.backgrounds:
            self.timer.start(20000)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Archivo')
        open_act = QAction('Abrir', self)
        open_act.triggered.connect(self.open_file)
        file_menu.addAction(open_act)
        save_act = QAction('Guardar', self)
        save_act.triggered.connect(self.save_file)
        file_menu.addAction(save_act)
        run_act = QAction('Run GPT4 Prompt', self)
        run_act.triggered.connect(self.run_gpt_prompt)
        file_menu.addAction(run_act)
        bg_menu = menubar.addMenu('Fondo')
        fill = QAction('Rellenar', self)
        fill.triggered.connect(lambda: self.set_scale_mode('fill'))
        bg_menu.addAction(fill)
        fit = QAction('Ajustar', self)
        fit.triggered.connect(lambda: self.set_scale_mode('fit'))
        bg_menu.addAction(fit)
        exp = QAction('Expandir', self)
        exp.triggered.connect(lambda: self.set_scale_mode('expand'))
        bg_menu.addAction(exp)
        custom = QAction('Personalizado', self)
        custom.triggered.connect(self.set_custom_scale)
        bg_menu.addAction(custom)

    def load_backgrounds(self):
        folder = self.settings.get('fondos_dir','fondos')
        if os.path.isdir(folder):
            for f in os.listdir(folder):
                if f.lower().endswith(('.png','.jpg','.jpeg')):
                    self.backgrounds.append(os.path.join(folder,f))

    def rotate_background(self):
        if not self.backgrounds:
            return
        self.bg_index = (self.bg_index + 1) % len(self.backgrounds)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.backgrounds:
            pix = QPixmap(self.backgrounds[self.bg_index])
            mode = self.settings.get('bg_scale_mode','expand')
            factor = self.settings.get('bg_custom_scale',1.0)
            target = self.size()
            if mode == 'fill':
                scaled = pix.scaled(target, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            elif mode == 'fit':
                scaled = pix.scaled(target, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            elif mode == 'custom':
                scaled = pix.scaled(pix.size()*factor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                scaled = pix.scaled(target, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            x = (self.width()-scaled.width())/2
            y = (self.height()-scaled.height())/2
            painter.drawPixmap(int(x),int(y),scaled)
        else:
            painter.fillRect(self.rect(), QColor(0,0,0))

    def open_file(self):
        path,_ = QFileDialog.getOpenFileName(self,'Abrir archivo','', 'Text Files (*.txt *.py *.bdk *.vtha)')
        if path:
            with open(path,'r',encoding='utf-8') as f:
                self.editor.setPlainText(f.read())

    def save_file(self):
        path,_ = QFileDialog.getSaveFileName(self,'Guardar archivo','', 'Text Files (*.txt *.py *.bdk *.vtha)')
        if path:
            with open(path,'w',encoding='utf-8') as f:
                f.write(self.editor.toPlainText())

    def run_gpt_prompt(self):
        prompt = self.editor.toPlainText()
        self.editor.append('\n🧠 GPT-4: Ejecutando análisis simbólico... (respuesta simulada)')
        self.store_memory(prompt)

    def set_scale_mode(self, mode):
        self.settings.set('bg_scale_mode', mode)
        self.update()

    def set_custom_scale(self):
        factor, ok = QInputDialog.getDouble(self,'Escala Personalizada','Factor de escala:',self.settings.get('bg_custom_scale',1.0),0.1,10.0,1)
        if ok:
            self.settings.set('bg_scale_mode','custom')
            self.settings.set('bg_custom_scale',factor)
            self.update()

    def store_memory(self,data):
        with open(self.memory_file,'a',encoding='utf-8') as f:
            f.write('\n[RECUERDO] '+data+'\n')

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file,'r',encoding='utf-8') as f:
                cont=f.read()
                if cont:
                    self.editor.append('\n🧬 RECUERDOS CARGADOS:\n'+cont)


    def cycle_slogan_color(self):
        color = QColor.fromHsv(self.color_hue % 360, 255, 255)
        self.slogan_label.setStyleSheet(f'color: {color.name()};')
        self.color_hue += 5

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TarantulaWindow()
    win.show()
    sys.exit(app.exec_())
