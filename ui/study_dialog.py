from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QWidget, QMessageBox)
from PyQt6.QtCore import Qt, QTimer

class StudyDialog(QDialog):
    def __init__(self, words, mode="sequence", parent=None):
        super().__init__(parent)
        self.words = words
        self.current_index = 0
        self.mode = mode
        
        # 设置窗口属性
        self.setWindowTitle("单词背诵")
        self.setMinimumSize(500, 400)
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建进度标签
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.progress_label.setStyleSheet("color: #666;")
        layout.addWidget(self.progress_label)
        
        # 创建单词显示区域
        self.word_area = QWidget()
        word_layout = QVBoxLayout(self.word_area)
        
        # 单词显示标签
        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setStyleSheet("font-size: 24px; margin: 20px;")
        word_layout.addWidget(self.word_label)
        
        # 释义和详细信息区域（初始隐藏）
        self.detail_widget = QWidget()
        detail_layout = QVBoxLayout(self.detail_widget)
        
        self.meaning_label = QLabel()
        self.pronunciation_label = QLabel()
        self.example_label = QLabel()
        
        for label in [self.meaning_label, self.pronunciation_label, self.example_label]:
            label.setStyleSheet("font-size: 16px; margin: 10px;")
            label.setWordWrap(True)
            detail_layout.addWidget(label)
        
        self.detail_widget.hide()
        word_layout.addWidget(self.detail_widget)
        
        # 添加状态提示标签
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 16px;
            padding: 5px;
            border-radius: 5px;
            background-color: transparent;
        """)
        word_layout.addWidget(self.status_label)
        
        # 添加按钮区域
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        self.show_btn = QPushButton("显示释义")
        self.know_btn = QPushButton("认识")
        self.unknown_btn = QPushButton("不认识")
        self.quit_btn = QPushButton("退出")
        
        self.know_btn.hide()
        self.unknown_btn.hide()
        
        for btn in [self.show_btn, self.know_btn, self.unknown_btn, self.quit_btn]:
            button_layout.addWidget(btn)
            
        # 连接信号
        self.show_btn.clicked.connect(self.show_details)
        self.know_btn.clicked.connect(lambda: self.process_answer(True))
        self.unknown_btn.clicked.connect(lambda: self.process_answer(False))
        self.quit_btn.clicked.connect(self.close)
        
        # 添加到主布局
        layout.addWidget(self.word_area)
        layout.addWidget(button_widget)
        
        # 显示第一个单词
        self.show_current_word()
        
    def show_current_word(self):
        """显示当前单词"""
        if self.current_index >= len(self.words):
            QMessageBox.information(self, "完成", "本轮背诵完成！")
            self.close()
            return
            
        word = self.words[self.current_index]
        self.word_label.setText(word[1])  # 显示单词
        self.meaning_label.setText(f"释义：{word[2]}")
        self.pronunciation_label.setText(f"发音：{word[3]}" if word[3] else "")
        self.example_label.setText(f"例句：{word[4]}" if word[4] else "")
        
        # 更新进度
        self.progress_label.setText(f"进度：{self.current_index + 1}/{len(self.words)}")
        
        # 重置界面状态
        self.detail_widget.hide()
        self.show_btn.show()
        self.know_btn.hide()
        self.unknown_btn.hide()
        self.status_label.clear()
        self.status_label.setStyleSheet("background-color: transparent;")
        
    def show_details(self):
        """显示单词详细信息"""
        self.detail_widget.show()
        self.show_btn.hide()
        self.know_btn.show()
        self.unknown_btn.show()
        
    def show_status(self, known):
        """显示状态提示"""
        if known:
            self.status_label.setText("✓ 已掌握")
            self.status_label.setStyleSheet("""
                color: #4CAF50;
                font-size: 16px;
                padding: 5px;
                border-radius: 5px;
                background-color: #E8F5E9;
            """)
        else:
            self.status_label.setText("继续努力")
            self.status_label.setStyleSheet("""
                color: #F44336;
                font-size: 16px;
                padding: 5px;
                border-radius: 5px;
                background-color: #FFEBEE;
            """)
        
        # 使用定时器在1秒后自动显示下一个单词
        QTimer.singleShot(800, self.next_word)
        
    def next_word(self):
        """显示下一个单词"""
        self.current_index += 1
        self.show_current_word()
        
    def process_answer(self, known):
        """处理用户回答"""
        word = self.words[self.current_index]
        try:
            # 更新学习记录
            self.parent().db.update_learning_record(word[0], 1 if known else 0)
            
            # 显示简洁的状态提示
            self.show_status(known)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"更新学习记录失败：{str(e)}") 