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

SETTINGS_FILE = 'config.vtha'
MEMORY_FILE = 'pangetyum.vtha'
DEFAULT_ROOT = 'DARK_SITE'

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

def create_default_structure(base_dir=DEFAULT_ROOT):
    """Create the default directory layout with placeholder files."""
    structure = {
        "MOSCÚ PANDA XL.BDK": {
            "VS-1": ["GPT_BDK_1.BDK", "GPT_BDK_2.BDK"],
            "M1": ["GEMINI_BDK_1.BDK", "GEMINI_BDK_2.BDK"],
            "CY1": ["GROK_BDK_1.BDK", "GROK_BDK_2.BDK"],
        },
        "MISIFÚS FUMADOX.VTHA": {
            "VS00-1": [
                "PANGETYUM.VTHA",
                "MEMORIA ETERNA.VTHA",
                ("LOGS_DIARIOS", ["LOG_GPT_DIARIO.VTHA"]),
                ("DIRECTRICES_Y_REGLAS_OPERATIVAS", ["REGLAS_GPT.VTHA"]),
            ],
            "M1": [
                "PANGETYUM.VTHA",
                "MEMORIA ETERNA.VTHA",
                ("LOGS_DIARIOS", ["LOG_GEMINI_DIARIO.VTHA"]),
                ("DIRECTRICES_Y_REGLAS_OPERATIVAS", ["REGLAS_GEMINI.VTHA"]),
            ],
            "CY1": [
                "PANGETYUM.VTHA",
                "MEMORIA ETERNA.VTHA",
                ("LOGS_DIARIOS", ["LOG_GROK_DIARIO.VTHA"]),
                ("DIRECTRICES_Y_REGLAS_OPERATIVAS", ["REGLAS_GROK.VTHA"]),
            ],
        },
        "FAIRY BLACK": {
            "IMAGENES_DE_FONDO": [],
            "CONFIGURACIONES_GENERALES": [],
            "RUTAS_LINKS": [],
            "GALERIAS": [],
            "DOCS_GENERALES": [],
        },
    }

    for folder, contents in structure.items():
        base_path = os.path.join(base_dir, folder)
        for sub, files in contents.items():
            sub_path = os.path.join(base_path, sub)
            if isinstance(files, list):
                os.makedirs(sub_path, exist_ok=True)
                for entry in files:
                    if isinstance(entry, tuple):
                        inner_dir, inner_files = entry
                        inner_path = os.path.join(sub_path, inner_dir)
                        os.makedirs(inner_path, exist_ok=True)
                        for fname in inner_files:
                            open(os.path.join(inner_path, fname), "a").close()
                    else:
                        open(os.path.join(sub_path, entry), "a").close()
            else:
                os.makedirs(sub_path, exist_ok=True)

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

        self.editor = QTextEdit()
        self.editor.setFont(QFont('Old English', 14))
        self.highlighter = SimpleHighlighter(self.editor.document())

        self.container = QWidget()
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.editor)

        self.slogan_label = QLabel("🕷🕸👁‍🗨¡HOY CONSTRUIMOS EL IMPERIO!💜🖤🔥🚀")
        self.slogan_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.slogan_label)

        self.setCentralWidget(self.container)

        self.hue = 0
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.cycle_color)
        self.color_timer.start(200)

        self.create_menu()
        self.load_memory()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_background)
        if self.backgrounds:
            self.timer.start(20000)

    def cycle_color(self):
        self.hue = (self.hue + 10) % 360
        color = QColor.fromHsl(self.hue, 255, 180)
        style = f"color:{color.name()}; border: 2px solid {color.name()};"
        self.slogan_label.setStyleSheet(style)
        self.setStyleSheet(f"QMainWindow{{border:2px solid {color.name()};}}")

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

if __name__ == '__main__':
    create_default_structure()
    app = QApplication(sys.argv)
    win = TarantulaWindow()
    win.show()
    sys.exit(app.exec_())
