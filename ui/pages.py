from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea, 
                            QPushButton, QLineEdit, QTextEdit, QHBoxLayout,
                            QMessageBox)
from PyQt6.QtCore import Qt
from models.database import Database  # 导入数据库模块
from .study_dialog import StudyDialog  # 导入学习对话框

class BasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 创建内容窗口
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        
        scroll.setWidget(content)
        self.layout.addWidget(scroll)

class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        title = QLabel("背单词程序用户指南")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: #2196F3; margin: 20px;")
        self.content_layout.addWidget(title)
        
        welcome = QLabel("欢迎使用背单词程序！\n\n请点击左侧导航栏查看详细内容。")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("font-size: 16px; margin: 20px;")
        self.content_layout.addWidget(welcome)
        
        self.content_layout.addStretch()

class IntroPage(BasePage):
    def __init__(self):
        super().__init__()
        title = QLabel("程序简介")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: #2196F3; margin: 20px;")
        self.content_layout.addWidget(title)
        
        intro = QLabel("这是一个基于Python开发的私人背单词程序，它可以帮助你管理和学习单词，"
                      "跟踪学习进度，并提供科学的复习计划。")
        intro.setWordWrap(True)
        intro.setStyleSheet("font-size: 16px; margin: 20px;")
        self.content_layout.addWidget(intro)
        
        self.content_layout.addStretch()

class FeaturesPage(BasePage):
    def __init__(self):
        super().__init__()
        title = QLabel("主要功能")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: #2196F3; margin: 20px;")
        self.content_layout.addWidget(title)
        
        features = [
            "1. 顺序背诵：按照添加顺序学习单词",
            "2. 随机背诵：随机顺序学习单词",
            "3. 添加单词：可以添加预设示例单词或手动添加新单词",
            "4. 查看统计：显示学习进度和统计信息",
            "5. 查看所有单词：查看数据库中的所有单词",
            "6. 清理重复单词：清理数据库中的重复单词"
        ]
        
        for feature in features:
            label = QLabel(feature)
            label.setStyleSheet("font-size: 16px; margin: 10px;")
            self.content_layout.addWidget(label)
        
        self.content_layout.addStretch()

class InstructionsPage(BasePage):
    def __init__(self):
        super().__init__()
        title = QLabel("使用说明")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: #2196F3; margin: 20px;")
        self.content_layout.addWidget(title)
        
        instructions = [
            ("添加单词", "• 选择主菜单中的'3. 添加单词'\n• 可以选择添加预设示例单词或手动添加新单词"),
            ("背诵单词", "• 可以选择'1. 顺序背诵'或'2. 随机背诵'\n• 按回车查看释义\n• 输入 y/n 表示是否记住"),
            ("查看统计", "• 可以看到总单词数、已掌握单词数和掌握率"),
            ("清理重复", "• 自动检测和清理重复的单词")
        ]
        
        for section, content in instructions:
            section_label = QLabel(section)
            section_label.setStyleSheet("font-size: 18px; color: #1976D2; margin: 10px;")
            self.content_layout.addWidget(section_label)
            
            content_label = QLabel(content)
            content_label.setStyleSheet("font-size: 16px; margin: 10px;")
            content_label.setWordWrap(True)
            self.content_layout.addWidget(content_label)
        
        self.content_layout.addStretch()

class TipsPage(BasePage):
    def __init__(self):
        super().__init__()
        title = QLabel("学习建议")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: #2196F3; margin: 20px;")
        self.content_layout.addWidget(title)
        
        tips = [
            "• 建议每天固定时间学习",
            "• 新添加的单词建议当天多复习几次",
            "• 定期查看统计信息，了解学习进度",
            "• 发现重复单词时及时清理"
        ]
        
        for tip in tips:
            label = QLabel(tip)
            label.setStyleSheet("font-size: 16px; margin: 10px;")
            self.content_layout.addWidget(label)
        
        self.content_layout.addStretch()

class NotesPage(BasePage):
    def __init__(self):
        super().__init__()
        title = QLabel("注意事项")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: #2196F3; margin: 20px;")
        self.content_layout.addWidget(title)
        
        notes = [
            "• 添加单词时请确保必填项不为空",
            "• 背诵过程中可随时退出",
            "• 程序会自动保存学习进度",
            "• 重复单词清理后无法恢复，请谨慎操作"
        ]
        
        for note in notes:
            label = QLabel(note)
            label.setStyleSheet("font-size: 16px; margin: 10px;")
            self.content_layout.addWidget(label)
        
        self.content_layout.addStretch()

class FAQPage(BasePage):
    def __init__(self):
        super().__init__()
        title = QLabel("常见问题")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: #2196F3; margin: 20px;")
        self.content_layout.addWidget(title)
        
        faqs = [
            ("如何退出背诵模式？", "在背诵过程中输入 'q' 即可退出"),
            ("如何删除单词？", "当前版本暂不支持删除单词功能"),
            ("学习记录会保存吗？", "是的，所有学习记录都会自动保存到数据库中"),
            ("重复单词怎么处理？", "使用'清理重复单词'功能可以自动处理重复单词")
        ]
        
        for question, answer in faqs:
            q_label = QLabel(f"Q: {question}")
            q_label.setStyleSheet("font-size: 16px; color: #1976D2; margin: 10px;")
            self.content_layout.addWidget(q_label)
            
            a_label = QLabel(f"A: {answer}")
            a_label.setStyleSheet("font-size: 16px; margin: 10px;")
            self.content_layout.addWidget(a_label)
        
        self.content_layout.addStretch()

class MainFunctionPage(BasePage):
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        # 创建功能区域
        functions_layout = QHBoxLayout()
        
        # 左侧：单词学习区
        study_widget = QWidget()
        study_layout = QVBoxLayout(study_widget)
        
        # 添加学习功能按钮
        study_title = QLabel("单词学习")
        study_title.setStyleSheet("font-size: 18px; color: #2196F3; margin: 10px;")
        study_layout.addWidget(study_title)
        
        # 添加学习按钮
        sequence_btn = QPushButton("顺序背诵")
        random_btn = QPushButton("随机背诵")
        sequence_btn.clicked.connect(self.start_sequence_study)
        random_btn.clicked.connect(self.start_random_study)
        
        study_layout.addWidget(sequence_btn)
        study_layout.addWidget(random_btn)
        study_layout.addStretch()
        
        # 右侧：单词管理区
        manage_widget = QWidget()
        manage_layout = QVBoxLayout(manage_widget)
        
        # 添加单词管理标题
        manage_title = QLabel("单词管理")
        manage_title.setStyleSheet("font-size: 18px; color: #2196F3; margin: 10px;")
        manage_layout.addWidget(manage_title)
        
        # 添加单词输入区域
        word_label = QLabel("单词:")
        self.word_input = QLineEdit()
        meaning_label = QLabel("释义:")
        self.meaning_input = QLineEdit()
        pronunciation_label = QLabel("发音(可选):")
        self.pronunciation_input = QLineEdit()
        example_label = QLabel("例句(可选):")
        self.example_input = QTextEdit()
        self.example_input.setMaximumHeight(100)
        
        manage_layout.addWidget(word_label)
        manage_layout.addWidget(self.word_input)
        manage_layout.addWidget(meaning_label)
        manage_layout.addWidget(self.meaning_input)
        manage_layout.addWidget(pronunciation_label)
        manage_layout.addWidget(self.pronunciation_input)
        manage_layout.addWidget(example_label)
        manage_layout.addWidget(self.example_input)
        
        # 添加按钮
        add_btn = QPushButton("添加单词")
        add_btn.clicked.connect(self.add_word)
        manage_layout.addWidget(add_btn)
        
        # 添加单词列表按钮
        word_list_btn = QPushButton("查看单词列表")
        word_list_btn.clicked.connect(self.show_word_list)
        manage_layout.addWidget(word_list_btn)
        
        # 将左右两侧添加到主布局
        functions_layout.addWidget(study_widget)
        functions_layout.addWidget(manage_widget)
        
        self.content_layout.addLayout(functions_layout)
        
    def add_word(self):
        """添加单词"""
        word = self.word_input.text().strip()
        meaning = self.meaning_input.text().strip()
        pronunciation = self.pronunciation_input.text().strip()
        example = self.example_input.toPlainText().strip()
        
        if not word or not meaning:
            QMessageBox.warning(self, "提示", "单词和释义不能为空！")
            return
            
        try:
            if self.db.add_word(word, meaning, pronunciation, example):
                QMessageBox.information(self, "成功", f"单词 '{word}' 添加成功！")
                self.clear_inputs()
            else:
                QMessageBox.warning(self, "提示", f"单词 '{word}' 已存在！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"添加单词失败：{str(e)}")
    
    def clear_inputs(self):
        """清空输入框"""
        self.word_input.clear()
        self.meaning_input.clear()
        self.pronunciation_input.clear()
        self.example_input.clear()
    
    def start_sequence_study(self):
        """开始顺序背诵"""
        try:
            words = self.db.get_words_to_review()
            if not words:
                QMessageBox.information(self, "提示", "当前没有需要复习的单词！")
                return
            
            dialog = StudyDialog(words, "sequence", self)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动背诵模式失败：{str(e)}")
    
    def start_random_study(self):
        """开始随机背诵"""
        try:
            words = self.db.get_words_to_review()
            if not words:
                QMessageBox.information(self, "提示", "当前没有需要复习的单词！")
                return
            
            # 随机打乱单词顺序
            import random
            word_list = list(words)
            random.shuffle(word_list)
            
            dialog = StudyDialog(word_list, "random", self)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动背诵模式失败：{str(e)}")

    def show_word_list(self):
        """显示单词列表对话框"""
        try:
            from .word_list_dialog import WordListDialog
            dialog = WordListDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开单词列表失败：{str(e)}")

# 其他页面类似，这里先展示一部分代码 