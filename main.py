import sys
import os
import argparse
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QFileDialog, QSizePolicy
)
from PyQt6.QtGui import QImage, QPixmap, QKeyEvent, QAction, QIcon

def resource_path(relative_path):
    """ Obtener la ruta del recurso para que funcione con el empaquetado de PyInstaller """
    try:
        # PyInstaller extrae los archivos a una carpeta temporal
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

from PyQt6.QtCore import Qt, QTimer, QTime

class PresentationWindow(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Presentation View")
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("background-color: black;")
        self.setCentralWidget(self.label)
        self.cached_pixmap = None
        
    def update_slide(self, pixmap):
        self.cached_pixmap = pixmap
        self.refresh_pixmap()
            
    def refresh_pixmap(self):
        if self.cached_pixmap:
            scaled_pixmap = self.cached_pixmap.scaled(
                self.label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)
        else:
            self.label.clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh_pixmap()
        
    def keyPressEvent(self, event):
        self.main_app.handle_key_event(event)

    def closeEvent(self, event):
        QApplication.quit()


class PresenterWindow(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Presenter View")
        self.resize(1000, 700)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Top panel: controls and timer
        top_layout = QHBoxLayout()
        self.btn_load = QPushButton("Load PDF")
        self.btn_load.clicked.connect(self.main_app.load_pdf)
        
        self.lbl_time = QLabel("00:00:00")
        self.lbl_time.setStyleSheet("font-size: 32px; font-weight: bold; color: #d32f2f;")
        
        self.lbl_slide_info = QLabel("No PDF loaded")
        self.lbl_slide_info.setStyleSheet("font-size: 18px;")
        
        control_sublayout = QHBoxLayout()
        self.btn_prev = QPushButton("<< Prev")
        self.btn_next = QPushButton("Next >>")
        self.btn_prev.clicked.connect(self.main_app.prev_slide)
        self.btn_next.clicked.connect(self.main_app.next_slide)
        control_sublayout.addWidget(self.btn_prev)
        control_sublayout.addWidget(self.btn_next)
        
        top_layout.addWidget(self.btn_load)
        top_layout.addStretch()
        top_layout.addWidget(self.lbl_slide_info)
        top_layout.addStretch()
        top_layout.addLayout(control_sublayout)
        top_layout.addSpacing(20)
        top_layout.addWidget(self.lbl_time)
        
        layout.addLayout(top_layout)
        
        # Slides view
        self.slides_layout = QHBoxLayout()
        
        # Current slide (large)
        current_layout = QVBoxLayout()
        title_curr = QLabel("Current Slide:")
        title_curr.setStyleSheet("font-weight: bold; font-size: 16px;")
        current_layout.addWidget(title_curr)
        self.lbl_current = QLabel()
        self.lbl_current.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_current.setStyleSheet("background-color: #222;")
        self.lbl_current.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        current_layout.addWidget(self.lbl_current, stretch=1)
        
        # Next slide (smaller)
        next_layout = QVBoxLayout()
        title_next = QLabel("Next Slide:")
        title_next.setStyleSheet("font-weight: bold; font-size: 16px;")
        next_layout.addWidget(title_next)
        self.lbl_next = QLabel()
        self.lbl_next.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_next.setStyleSheet("background-color: #222;")
        self.lbl_next.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        next_layout.addWidget(self.lbl_next, stretch=1)
        
        self.slides_layout.addLayout(current_layout, stretch=2)
        self.slides_layout.addLayout(next_layout, stretch=1)
        
        layout.addLayout(self.slides_layout)
        
        self.cached_curr = None
        self.cached_next = None
        
    def update_slides(self, current_pixmap, next_pixmap):
        self.cached_curr = current_pixmap
        self.cached_next = next_pixmap
        self.refresh_pixmaps()
            
    def refresh_pixmaps(self):
        if self.cached_curr:
            scaled_curr = self.cached_curr.scaled(
                self.lbl_current.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.lbl_current.setPixmap(scaled_curr)
        else:
            self.lbl_current.clear()
            
        if self.cached_next:
            scaled_next = self.cached_next.scaled(
                self.lbl_next.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.lbl_next.setPixmap(scaled_next)
        else:
            self.lbl_next.clear()
            
    def update_info(self, current, total):
        self.lbl_slide_info.setText(f"Slide {current} of {total}")
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh_pixmaps()
        
    def keyPressEvent(self, event):
        self.main_app.handle_key_event(event)

    def closeEvent(self, event):
        QApplication.quit()


class PDFPresenterApp:
    def __init__(self):
        self.doc = None
        self.current_page = 0
        self.total_pages = 0
        
        self.presentation_win = PresentationWindow(self)
        self.presenter_win = PresenterWindow(self)
        
        # Set Application Icon
        icon_path = resource_path("lambdito.png")
        if not os.path.exists(icon_path):
            icon_path = resource_path("lambdito.ico")
            
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            # Imponer el icono en la misma instancia de la app completa (Mejora en Linux)
            QApplication.instance().setWindowIcon(app_icon)
            self.presentation_win.setWindowIcon(app_icon)
            self.presenter_win.setWindowIcon(app_icon)
        
        # Positioning Logic: try to move presentation to secondary screen if available
        screens = QApplication.screens()
        if len(screens) > 1:
            # Secondary screen for presentation
            self.presentation_win.move(screens[1].geometry().topLeft())
            self.presentation_win.showFullScreen()
            self.presenter_win.move(screens[0].geometry().topLeft())
            self.presenter_win.showMaximized()
        else:
            self.presentation_win.showNormal()
            self.presentation_win.resize(600, 400)
            self.presenter_win.show()
            
        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = QTime(0, 0, 0)
        self.timer_running = False
        
    def load_pdf(self, filepath=None):
        if not isinstance(filepath, str):
            filepath, _ = QFileDialog.getOpenFileName(
                self.presenter_win,
                "Open PDF File",
                "",
                "PDF Files (*.pdf)"
            )
        if filepath:
            if self.doc:
                self.doc.close()
            self.doc = fitz.open(filepath)
            self.total_pages = len(self.doc)
            self.current_page = 0
            
            # Reset timer on new presentation
            self.reset_timer()
            
            self.refresh_views()

    def get_pixmap(self, page_num):
        if not self.doc or page_num < 0 or page_num >= self.total_pages:
            return None
        page = self.doc.load_page(page_num)
        
        # Use high resolution for rendering (4.0 is extremely sharp)
        zoom = 4.0
        mat = fitz.Matrix(zoom, zoom)
        # alpha=False optimizes generation making rendering a bit faster
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # Convert to QImage and then QPixmap
        fmt = QImage.Format.Format_RGB888
        qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
        return QPixmap.fromImage(qimg)

    def refresh_views(self):
        if self.doc:
            curr_pix = self.get_pixmap(self.current_page)
            next_pix = self.get_pixmap(self.current_page + 1)
            
            self.presentation_win.update_slide(curr_pix)
            self.presenter_win.update_slides(curr_pix, next_pix)
            self.presenter_win.update_info(self.current_page + 1, self.total_pages)

    def next_slide(self):
        if self.doc and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.refresh_views()

    def prev_slide(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.refresh_views()
            
    def restart_presentation(self):
        if self.doc:
            self.current_page = 0
            self.refresh_views()

    def toggle_timer(self):
        if self.timer_running:
            self.timer.stop()
        else:
            self.timer.start(1000)
        self.timer_running = not self.timer_running

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.elapsed_time = QTime(0, 0, 0)
        self.presenter_win.lbl_time.setText(self.elapsed_time.toString("hh:mm:ss"))

    def update_timer(self):
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.presenter_win.lbl_time.setText(self.elapsed_time.toString("hh:mm:ss"))

    def handle_key_event(self, event: QKeyEvent):
        key = event.key()
        if key in (Qt.Key.Key_Right, Qt.Key.Key_Down, Qt.Key.Key_PageDown):
            self.next_slide()
        elif key in (Qt.Key.Key_Left, Qt.Key.Key_Up, Qt.Key.Key_PageUp):
            self.prev_slide()
        elif key in (Qt.Key.Key_Space, Qt.Key.Key_P):
            self.toggle_timer()
        elif key == Qt.Key.Key_R:
            self.reset_timer()
        elif key == Qt.Key.Key_Home:
            self.restart_presentation()
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Lector de Presentaciones PDF Dual.\nPermite abrir presentaciones PDF separando la vista del público y la del presentador.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'pdf_file', 
        nargs='?', 
        help="Ruta opcional al archivo PDF que se desea abrir automáticamente al iniciar.",
        default=None
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    pdf_app = PDFPresenterApp()
    
    if args.pdf_file:
        pdf_app.load_pdf(args.pdf_file)
        
    sys.exit(app.exec())
