from platform import system

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QTabWidget, QGridLayout
from PySide6.QtCore import Qt

from ui.components.badges import badges
from ui.components.mini_badge import mini_badge
from services.pixmaps_manager import PixMapManager
from services.settings_manager import SettingsManager


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.settings= SettingsManager()
        self.pixmap_manager= PixMapManager(self.settings)

        title_layout = QVBoxLayout()
        title_label = QLabel("Acerca de")
        title_label.setProperty('class', 'content_title')
        title_description = QLabel("Información sobre la aplicación")
        title_description.setProperty('class', 'content_subtitle')
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_description)

        title = QWidget()
        title.setLayout(title_layout)
        title.setFixedHeight(70)

        header_layout = QVBoxLayout()
        header_title = QLabel('IDS/IPS')
        header_title.setProperty('class', 'content_title')
        header_subtitle = QLabel('Sistema de detección de anomalías')
        version_badge = badges('Versión 2.0.0 ','media')
        header_description =  QLabel('Aplicación desarrollada en Python con PySide6 para monitoreo de red y detección de actividades sospechosas en tiempo real.')

        header_layout.addWidget(header_title)
        header_layout.addWidget(header_subtitle)
        header_layout.addWidget(version_badge)
        header_layout.addWidget(header_description)

        header_tabs_layout = QHBoxLayout()

        header_tab1_layout = QHBoxLayout()

        self.code_icon = QLabel()
        self.pixmap1 = self.pixmap_manager.get('code')
        self.pixmap1.scaled(30,30,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.code_icon.setPixmap(self.pixmap1)

        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel('Desarrollado con'))
        tab1_layout.addWidget(QLabel('Python 3.14, PySide6'))
        tab1=QWidget()
        tab1.setLayout(tab1_layout)

        header_tab1_layout.addWidget(self.code_icon)
        header_tab1_layout.addWidget(tab1)

        header_tab1 = QWidget()
        header_tab1.setLayout(header_tab1_layout)


        header_tab2_layout = QHBoxLayout()

        self.shield_icon = QLabel()
        self.pixmap2 = self.pixmap_manager.get('shield-check')
        self.pixmap2.scaled(30,30,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.shield_icon.setPixmap(self.pixmap2)

        tabs2_layout = QVBoxLayout()
        tabs2_layout.addWidget(QLabel('Propósito'))
        tabs2_layout.addWidget(QLabel('Detección, prevención y monitoreo'))
        tabs2=QWidget()
        tabs2.setLayout(tabs2_layout)

        header_tab2_layout.addWidget(self.shield_icon)
        header_tab2_layout.addWidget(tabs2)

        header_tab2 = QWidget()
        header_tab2.setLayout(header_tab2_layout)

        header_tab3_layout = QHBoxLayout()

        self.terminal_icon = QLabel()
        self.pixmap3 = self.pixmap_manager.get('terminal')
        self.pixmap3.scaled(30,30,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.terminal_icon.setPixmap(self.pixmap3)

        tabs3_layout = QVBoxLayout()
        tabs3_layout.addWidget(QLabel('Plataforma'))
        tabs3_layout.addWidget(QLabel('Windows versiones 10 y 11'))
        tabs3=QWidget()
        tabs3.setLayout(tabs3_layout)

        header_tab3_layout.addWidget(self.terminal_icon)
        header_tab3_layout.addWidget(tabs3)

        header_tab3 = QWidget()
        header_tab3.setLayout(header_tab3_layout)


        header_tabs_layout.addWidget(header_tab1)
        header_tabs_layout.addWidget(header_tab2)
        header_tabs_layout.addWidget(header_tab3)
        header_tabs_layout.addStretch()

        header_tabs=QWidget()
        header_tabs.setLayout(header_tabs_layout)

        header_layout.addWidget(header_tabs)

        header = QWidget()
        header.setLayout(header_layout)
        header.setProperty('class', 'content_card')

        system_info_layout = QVBoxLayout()
        system_info_title = QLabel('Información del sistema')
        system_info_title.setProperty('class','content_title')

        system_content_layout = QGridLayout()
        system_content_layout.addWidget(QLabel('Aplicación'),0,0)
        system_content_layout.addWidget(QLabel('IDS/IPS'),0,1)
        system_content_layout.addWidget(QLabel('Versión'),1,0)
        system_content_layout.addWidget(QLabel('v2.0.0'),1,1)
        system_content_layout.addWidget(QLabel('Fecha de compilación'),2,0)
        system_content_layout.addWidget(QLabel('POR DEFINIR'),2,1)
        system_content_layout.addWidget(QLabel('Desarrollador'),3,0)
        system_content_layout.addWidget(QLabel('SyMEC2026🙀'),3,1)
        system_content_layout.addWidget(QLabel('Licencia'), 4, 0)
        system_content_layout.addWidget(QLabel(''), 4, 1)
        system_content_layout.addWidget(QLabel('Código fuente'), 5, 0)
        source_code = QLabel('<a href="https://github.com/Rendel05/IDS-IPS">https://github.com/Rendel05/IDS-IPS</a>')
        source_code.setOpenExternalLinks(True)
        system_content_layout.addWidget(source_code, 5, 1)

        system_content=QWidget()
        system_content.setLayout(system_content_layout)


        system_info_layout.addWidget(system_info_title)
        system_info_layout.addWidget(system_content)
        system_info = QWidget()
        system_info.setLayout(system_info_layout)
        system_info.setProperty('class','content_card')
        system_info.setMaximumWidth(500)




        credits_layout = QVBoxLayout()

        credits_title = QLabel('Créditos')
        credits_title.setProperty('class','content_title')
        credits_subtitle=QLabel('Este proyecto utiliza las siguientes tecnologías de código abierto')

        credits_tabs_layout = QHBoxLayout()

        credits_tabs1_layout = QHBoxLayout()
        python_icon = QLabel()
        pixmap_python = QPixmap('assets/python.svg')
        python_icon.setPixmap(pixmap_python)
        python_text=QLabel('Python 3.14')
        credits_tabs1_layout.addWidget(python_icon)
        credits_tabs1_layout.addWidget(python_text)
        credits_tabs1=QWidget()
        credits_tabs1.setLayout(credits_tabs1_layout)
        credits_tabs1.setProperty('class','content_card')

        credits_tabs2_layout = QHBoxLayout()
        qt_icon = QLabel()
        pixmap_qt = QPixmap('assets/Qt.svg')
        qt_icon.setPixmap(pixmap_qt)
        qt_text=QLabel('PySide6')
        credits_tabs2_layout.addWidget(qt_icon)
        credits_tabs2_layout.addWidget(qt_text)
        credits_tabs2=QWidget()
        credits_tabs2.setLayout(credits_tabs2_layout)
        credits_tabs2.setProperty('class','content_card')


        credits_tabs3_layout = QHBoxLayout()
        scapy_icon = QLabel()
        pixmap_scapy = QPixmap('assets/scapy.svg')
        scapy_icon.setPixmap(pixmap_scapy)
        scapy_text=QLabel('Scapy')
        credits_tabs3_layout.addWidget(scapy_icon)
        credits_tabs3_layout.addWidget(scapy_text)
        credits_tabs3=QWidget()
        credits_tabs3.setLayout(credits_tabs3_layout)
        credits_tabs3.setProperty('class','content_card')


        credits_tabs4_layout = QHBoxLayout()
        sqlite_icon = QLabel()
        pixmap_sqlite = QPixmap('assets/sqlite.svg')
        sqlite_icon.setPixmap(pixmap_sqlite)
        sqlite_text=QLabel('SQLite')
        credits_tabs4_layout.addWidget(sqlite_icon)
        credits_tabs4_layout.addWidget(sqlite_text)
        credits_tabs4=QWidget()
        credits_tabs4.setLayout(credits_tabs4_layout)
        credits_tabs4.setProperty('class','content_card')

        credits_tabs5_layout = QHBoxLayout()
        numpy_icon = QLabel()
        pixmap_numpy = QPixmap('assets/numpy.svg')
        numpy_icon.setPixmap(pixmap_numpy)
        numpy_text=QLabel('NumPy')
        credits_tabs5_layout.addWidget(numpy_icon)
        credits_tabs5_layout.addWidget(numpy_text)
        credits_tabs5=QWidget()
        credits_tabs5.setLayout(credits_tabs5_layout)
        credits_tabs5.setProperty('class','content_card')

        credits_tabs6_layout = QHBoxLayout()
        psutil_icon = QLabel()
        pixmap_psutil = QPixmap('assets/psutil.svg')
        psutil_icon.setPixmap(pixmap_psutil)
        psutil_text=QLabel('Psutil')
        credits_tabs6_layout.addWidget(psutil_icon)
        credits_tabs6_layout.addWidget(psutil_text)
        credits_tabs6=QWidget()
        credits_tabs6.setLayout(credits_tabs6_layout)
        credits_tabs6.setProperty('class','content_card')

        credits_tabs_layout.addWidget(credits_tabs1)
        credits_tabs_layout.addWidget(credits_tabs2)
        credits_tabs_layout.addWidget(credits_tabs3)
        credits_tabs_layout.addWidget(credits_tabs4)
        credits_tabs_layout.addWidget(credits_tabs5)
        credits_tabs_layout.addWidget(credits_tabs6)
        credits_tabs_layout.addStretch()
        credits_tabs=QWidget()
        credits_tabs.setLayout(credits_tabs_layout)


        credits_layout.addWidget(credits_title)
        credits_layout.addWidget(credits_subtitle)
        credits_layout.addWidget(credits_tabs)
        credits_layout.addWidget(QLabel('Agradecimientos a la comunidad de código abierto por sus herramientas y bibliotecas.'))



        credits_info = QWidget()
        credits_info.setLayout(credits_layout)
        credits_info.setProperty('class', 'content_card')


        layout.addWidget(title)
        layout.addWidget(header)
        layout.addWidget(system_info)
        layout.addWidget(credits_info)
        layout.addStretch()
        self.setLayout(layout)

    def change_theme(self):
        self.settings = SettingsManager()
        self.pixmap_manager = PixMapManager(self.settings)
        self.pixmap1 = self.pixmap_manager.get('code')
        self.code_icon.setPixmap(self.pixmap1)
        self.pixmap2 = self.pixmap_manager.get('shield-check')
        self.shield_icon.setPixmap(self.pixmap2)
        self.pixmap3 = self.pixmap_manager.get('terminal')
        self.terminal_icon  .setPixmap(self.pixmap3)