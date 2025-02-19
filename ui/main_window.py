from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QStackedWidget, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from .pages import (HomePage, IntroPage, FeaturesPage, InstructionsPage, 
                   TipsPage, NotesPage, FAQPage, MainFunctionPage)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("背单词程序")
        self.setMinimumSize(800, 600)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QHBoxLayout(main_widget)
        
        # 创建导航栏
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_widget.setMaximumWidth(200)
        nav_widget.setMinimumWidth(150)
        
        # 创建导航按钮
        self.create_nav_buttons(nav_layout)
        
        # 创建内容区域
        self.content_stack = QStackedWidget()
        
        # 添加各个页面
        self.add_pages()
        
        # 将导航栏和内容区域添加到主布局
        layout.addWidget(nav_widget)
        layout.addWidget(self.content_stack)
        
        # 设置初始页面
        self.content_stack.setCurrentIndex(0)

    def create_nav_buttons(self, layout):
        """创建导航按钮"""
        buttons = [
            ("首页", 0),
            ("开始背单词", 1),
            ("程序简介", 2),
            ("主要功能", 3),
            ("使用说明", 4),
            ("学习建议", 5),
            ("注意事项", 6),
            ("常见问题", 7)
        ]
        
        for text, index in buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=index: self.change_page(idx))
            if text == "开始背单词":
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        padding: 8px;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
            layout.addWidget(btn)
        
        layout.addStretch()

    def add_pages(self):
        """添加所有页面到堆栈窗口"""
        pages = [
            HomePage(),
            MainFunctionPage(),
            IntroPage(),
            FeaturesPage(),
            InstructionsPage(),
            TipsPage(),
            NotesPage(),
            FAQPage()
        ]
        
        for page in pages:
            self.content_stack.addWidget(page)

    def change_page(self, index):
        """切换页面"""
        self.content_stack.setCurrentIndex(index) 