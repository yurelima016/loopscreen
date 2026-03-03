import os
import sys
import json
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QLabel, QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtGui import QPixmap

class TotemWindow(QMainWindow):
    def __init__(self, playlist):
        super().__init__()
        
        self.setWindowTitle("LoopScreen")
        self.showFullScreen()
        self.setCursor(Qt.CursorShape.BlankCursor)
        self.raise_()
        self.activateWindow()
        self.setFocus()

        self.playlist = playlist
        self.current_index = 0

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 1. Navegador (URL)
        self.browser = QWebEngineView()
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        self.browser.page().fullScreenRequested.connect(self.acceptFullScreen)
        self.stack.addWidget(self.browser)

        # 2. Vídeo
        self.video_widget = QVideoWidget()
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        self.player.mediaStatusChanged.connect(self.check_video_status)
        self.stack.addWidget(self.video_widget)

        # 3. Imagem
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #242424;")
        self.stack.addWidget(self.image_label)

        # Timer Principal
        self.master_timer = QTimer(self)
        self.master_timer.timeout.connect(self.next_item)

        # Inicia o loop automaticamente se a playlist não estiver vazia
        if self.playlist:
            self.next_item()

    def acceptFullScreen(self, request):
        request.accept()

    def next_item(self):
        # Para os processos atuais antes de trocar a tela
        self.master_timer.stop()
        self.player.stop()

        # Pega o item atual da lista
        item = self.playlist[self.current_index]
        
        # Prepara o índice para a próxima rodada (volta pro 0 se chegar no fim)
        self.current_index = (self.current_index + 1) % len(self.playlist)

        media_type = item.get('type')
        media_value = item.get('value')
        duration_ms = int(item.get('duration', 10)) * 1000

        print(f"Exibindo [{media_type}]: {media_value}")

        if media_type == 'url':
            self.browser.load(QUrl(media_value))
            self.stack.setCurrentWidget(self.browser)
            self.master_timer.start(duration_ms)

        elif media_type == 'file':
            # Descobre se o arquivo é vídeo ou foto olhando a extensão
            file_ext = os.path.splitext(media_value)[1].lower()
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.webm']
            
            if file_ext in video_extensions:
                self.player.setSource(QUrl.fromLocalFile(media_value))
                self.stack.setCurrentWidget(self.video_widget)
                self.player.play()
            else:
                # Se não é vídeo, tratamos como imagem
                pixmap = QPixmap(media_value)
                self.image_label.setPixmap(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                self.stack.setCurrentWidget(self.image_label)
                self.master_timer.start(duration_ms)

    def check_video_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_item()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.master_timer.stop()
            self.player.stop()            
            QApplication.quit()