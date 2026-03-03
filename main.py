import webview
import sys
from PyQt6.QtWidgets import QApplication
from core import TotemWindow

class API:
    def __init__(self):
        self._window = None
        self.configs = None
        self._is_maximized = False

    def start_system(self, data):
        print(f"Playlist recebida do Frontend: {data}")
        self.configs = data
        self._window.destroy()

    def choose_file(self):
        tipos_permitidos = ('Arquivos de Mídia (*.mp4;*.avi;*.mov;*.mkv;*.jpg;*.jpeg;*.png)', 'Todos os arquivos (*.*)')
        
        caminho = self._window.create_file_dialog(
            webview.OPEN_DIALOG, 
            allow_multiple=False, 
            file_types=tipos_permitidos
        )
        
        if caminho:
            return caminho[0]
        return ""
    
    def minimize_window(self):
        self._window.minimize()

    def maximize_window(self):
            if self._is_maximized:
                self._window.restore()
                self._is_maximized = False
            else:
                self._window.maximize()
                self._is_maximized = True
            
            return self._is_maximized

    def close_window(self):
        self._window.destroy()

if __name__ == '__main__':
    api = API()
    
    # 1. Abre a interface HTML do LoopScreen
    window = webview.create_window(
        title="Configuração - LoopScreen",
        url="index.html",
        js_api=api,
        width=800,
        height=800,
        resizable=True,
        frameless=True
    )
    api._window = window
    webview.start()

    # 2. Inicia o Totem com a Playlist
    if api.configs:
        print("Iniciando o LoopScreen em tela cheia...")
        app = QApplication(sys.argv)
        
        # Passamos a lista inteira de mídia (playlist) para o TotemWindow
        totem_app = TotemWindow(playlist=api.configs)
        totem_app.show()
        
        sys.exit(app.exec())