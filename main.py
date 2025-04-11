import sys
import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLabel, QFileDialog, QComboBox,
                            QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt
from send2trash import send2trash
from dateutil import parser

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organizador de Arquivos")
        self.setGeometry(100, 100, 600, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Seleção de pasta
        self.folder_label = QLabel("Pasta selecionada: Nenhuma")
        layout.addWidget(self.folder_label)
        
        select_button = QPushButton("Selecionar Pasta")
        select_button.clicked.connect(self.select_folder)
        layout.addWidget(select_button)
        
        # Opções de organização
        self.organize_by = QComboBox()
        self.organize_by.addItems(["Tipo de Arquivo", "Data"])
        layout.addWidget(QLabel("Organizar por:"))
        layout.addWidget(self.organize_by)
        
        # Barra de progresso
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Botão de organização
        organize_button = QPushButton("Organizar Arquivos")
        organize_button.clicked.connect(self.organize_files)
        layout.addWidget(organize_button)
        
        self.selected_folder = None
        
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if folder:
            self.selected_folder = folder
            self.folder_label.setText(f"Pasta selecionada: {folder}")
    
    def organize_files(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione uma pasta primeiro!")
            return
        
        try:
            files = os.listdir(self.selected_folder)
            self.progress.setMaximum(len(files))
            self.progress.setValue(0)
            
            for i, file in enumerate(files):
                file_path = os.path.join(self.selected_folder, file)
                
                if os.path.isfile(file_path):
                    if self.organize_by.currentText() == "Tipo de Arquivo":
                        self.organize_by_type(file_path)
                    else:
                        self.organize_by_date(file_path)
                
                self.progress.setValue(i + 1)
                QApplication.processEvents()
            
            QMessageBox.information(self, "Sucesso", "Arquivos organizados com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {str(e)}")
    
    def organize_by_type(self, file_path):
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # Mapeamento de extensões para pastas
        type_folders = {
            # Documentos
            '.pdf': 'Documentos',
            '.doc': 'Documentos',
            '.docx': 'Documentos',
            '.txt': 'Documentos',
            '.rtf': 'Documentos',
            '.odt': 'Documentos',
            '.pages': 'Documentos',
            
            # Planilhas
            '.xlsx': 'Planilhas',
            '.xls': 'Planilhas',
            '.csv': 'Planilhas',
            '.numbers': 'Planilhas',
            '.ods': 'Planilhas',
            
            # Apresentações
            '.ppt': 'Apresentações',
            '.pptx': 'Apresentações',
            '.key': 'Apresentações',
            '.odp': 'Apresentações',
            
            # Imagens
            '.jpg': 'Imagens',
            '.jpeg': 'Imagens',
            '.png': 'Imagens',
            '.gif': 'Imagens',
            '.bmp': 'Imagens',
            '.tiff': 'Imagens',
            '.svg': 'Imagens',
            '.webp': 'Imagens',
            '.heic': 'Imagens',
            
            # Vídeos
            '.mp4': 'Videos',
            '.avi': 'Videos',
            '.mov': 'Videos',
            '.wmv': 'Videos',
            '.flv': 'Videos',
            '.mkv': 'Videos',
            '.webm': 'Videos',
            
            # Áudio
            '.mp3': 'Musicas',
            '.wav': 'Musicas',
            '.wma': 'Musicas',
            '.aac': 'Musicas',
            '.flac': 'Musicas',
            '.m4a': 'Musicas',
            '.ogg': 'Musicas',
            
            # Compactados
            '.zip': 'Compactados',
            '.rar': 'Compactados',
            '.7z': 'Compactados',
            '.tar': 'Compactados',
            '.gz': 'Compactados',
            
            # Notas Fiscais
            '.xml': 'Notas Fiscais',
            '.nfe': 'Notas Fiscais',
            '.nfce': 'Notas Fiscais',
            
            # Executáveis
            '.exe': 'Executáveis',
            '.msi': 'Executáveis',
            '.app': 'Executáveis',
            
            # Fontes
            '.ttf': 'Fontes',
            '.otf': 'Fontes',
            '.woff': 'Fontes',
            '.woff2': 'Fontes',
            
            # Código
            '.py': 'Código',
            '.js': 'Código',
            '.html': 'Código',
            '.css': 'Código',
            '.java': 'Código',
            '.cpp': 'Código',
            '.c': 'Código',
            '.php': 'Código',
            '.json': 'Código',
            
            # Power BI e SQL
            '.pbix': 'Power BI e SQL',
            '.pbit': 'Power BI e SQL',
            '.sql': 'Power BI e SQL',
            '.m': 'Power BI e SQL',
            '.dax': 'Power BI e SQL',
            '.bim': 'Power BI e SQL'
        }
        
        if file_ext in type_folders:
            folder_name = type_folders[file_ext]
            new_folder = os.path.join(self.selected_folder, folder_name)
            
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            
            new_path = os.path.join(new_folder, file_name)
            if os.path.exists(new_path):
                base, ext = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(new_path):
                    new_path = os.path.join(new_folder, f"{base}_{counter}{ext}")
                    counter += 1
            
            shutil.move(file_path, new_path)
    
    def organize_by_date(self, file_path):
        try:
            # Tenta obter a data de modificação do arquivo
            timestamp = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(timestamp)
            folder_name = date.strftime("%Y-%m")
            
            new_folder = os.path.join(self.selected_folder, folder_name)
            
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            
            file_name = os.path.basename(file_path)
            new_path = os.path.join(new_folder, file_name)
            
            if os.path.exists(new_path):
                base, ext = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(new_path):
                    new_path = os.path.join(new_folder, f"{base}_{counter}{ext}")
                    counter += 1
            
            shutil.move(file_path, new_path)
            
        except Exception as e:
            print(f"Erro ao organizar arquivo por data: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec()) 