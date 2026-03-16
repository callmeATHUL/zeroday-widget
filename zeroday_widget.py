import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QFileSystemWatcher
from PyQt6.QtGui import QScreen, QGuiApplication

# Path to the TODO file on the desktop
TODO_PATH = os.path.expanduser("~/Desktop/TODO.md")
STYLE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/style.qss"

class TaskRow(QFrame):
    def __init__(self, text, delete_callback):
        super().__init__()
        self.setObjectName("TaskRow")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        dot = QFrame()
        dot.setObjectName("TaskDot")
        layout.addWidget(dot)

        label = QLabel(text)
        label.setObjectName("TaskLabel")
        label.setWordWrap(True)
        layout.addWidget(label, 1)

        del_btn = QPushButton("×")
        del_btn.setObjectName("DelBtn")
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.clicked.connect(lambda: delete_callback(text))
        layout.addWidget(del_btn)

class ZERODAYWidget(QWidget):
    def __init__(self, screen):
        super().__init__()
        self.screen_ptr = screen
        self.init_ui()
        self.load_tasks()
        
        # Watch for file changes
        self.watcher = QFileSystemWatcher([TODO_PATH])
        self.watcher.fileChanged.connect(self.load_tasks)

    def init_ui(self):
        self.setWindowTitle("ZERODAY")
        self.setObjectName("MainWidget")
        
        # Standard widget flags that allow WM management but feel like a widget
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnBottomHint
        )
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # Sticky note dimensions
        width = 300
        height = 400
        
        # Position at top-right of the assigned screen
        geom = self.screen_ptr.availableGeometry()
        margin = 20
        x = geom.x() + geom.width() - width - margin
        y = geom.y() + margin
        self.setGeometry(x, y, width, height)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setObjectName("Header")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        title = QLabel("ZERODAY")
        title.setObjectName("Title")
        header_layout.addWidget(title)
        
        subtitle = QLabel("notes")
        subtitle.setObjectName("Subtitle")
        header_layout.addWidget(subtitle)
        
        self.main_layout.addWidget(header)

        # Divider
        div1 = QFrame()
        div1.setObjectName("Divider")
        self.main_layout.addWidget(div1)

        # Task List Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("ScrollArea")
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ScrollContent")
        self.tasks_layout = QVBoxLayout(self.scroll_content)
        self.tasks_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tasks_layout.setContentsMargins(0, 5, 0, 5)
        self.tasks_layout.setSpacing(4)
        
        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll, 1)

        # Divider
        div2 = QFrame()
        div2.setObjectName("Divider")
        self.main_layout.addWidget(div2)

        # Input Area
        input_container = QWidget()
        input_container.setObjectName("InputRow")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 8, 0, 0)
        input_layout.setSpacing(6)

        self.input_field = QLineEdit()
        self.input_field.setObjectName("TaskInput")
        self.input_field.setPlaceholderText("New task...")
        self.input_field.returnPressed.connect(self.add_task)
        input_layout.addWidget(self.input_field)

        add_btn = QPushButton("+")
        add_btn.setObjectName("AddBtn")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(add_btn)

        self.main_layout.addWidget(input_container)

    def load_tasks(self):
        # Clear existing tasks
        while self.tasks_layout.count():
            item = self.tasks_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not os.path.exists(TODO_PATH):
            with open(TODO_PATH, 'a') as f: pass

        try:
            with open(TODO_PATH, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line: continue
                    task_text = line.lstrip('- [ ] ').lstrip('- ')
                    if task_text:
                        row = TaskRow(task_text, self.remove_task)
                        self.tasks_layout.addWidget(row)
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def add_task(self):
        text = self.input_field.text().strip()
        if text:
            try:
                with open(TODO_PATH, 'a') as f:
                    f.write(f"- [ ] {text}\n")
                self.input_field.clear()
                # File watcher might take a moment, so we reload manually too
                self.load_tasks()
            except Exception as e:
                print(f"Error adding task: {e}")

    def remove_task(self, text):
        try:
            with open(TODO_PATH, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            removed = False
            for line in lines:
                if not removed and text in line:
                    removed = True
                    continue
                new_lines.append(line)
                
            with open(TODO_PATH, 'w') as f:
                f.writelines(new_lines)
                
            self.load_tasks()
        except Exception as e:
            print(f"Error removing task: {e}")

def main():
    app = QApplication(sys.argv)
    
    # Set app_id for Wayland (matches Hyprland class)
    app.setDesktopFileName("zeroday")
    
    # Load QSS
    qss = ""
    if os.path.exists(STYLE_PATH):
        try:
            with open(STYLE_PATH, 'r') as f:
                qss = f.read()
                app.setStyleSheet(qss)
        except Exception as e:
            print(f"Error loading style: {e}")
            
    # Spawn a widget for each screen
    widgets = []
    for screen in QGuiApplication.screens():
        w = ZERODAYWidget(screen)
        w.show()
        widgets.append(w)
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
