from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QWidget, QTableWidget, QTableWidgetItem,
                            QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt

class WordListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = parent.db
        
        # 设置窗口属性
        self.setWindowTitle("单词列表")
        self.setMinimumSize(800, 600)
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "单词", "释义", "发音", "例句", "学习状态"])
        
        # 设置表格样式
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID列
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # 单词列
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # 释义列
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # 发音列
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # 例句列
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # 状态列
        
        # 创建按钮区域
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        self.refresh_btn = QPushButton("刷新")
        self.delete_btn = QPushButton("删除选中")
        self.export_btn = QPushButton("导出列表")
        self.close_btn = QPushButton("关闭")
        
        for btn in [self.refresh_btn, self.delete_btn, self.export_btn, self.close_btn]:
            button_layout.addWidget(btn)
            
        # 连接信号
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.export_btn.clicked.connect(self.export_words)
        self.close_btn.clicked.connect(self.close)
        
        # 添加到主布局
        layout.addWidget(self.table)
        layout.addWidget(button_widget)
        
        # 加载数据
        self.refresh_table()
        
    def refresh_table(self):
        """刷新表格数据"""
        try:
            words = self.db.get_all_words()
            self.table.setRowCount(len(words))
            
            for row, word in enumerate(words):
                # word结构: (id, word, meaning, pronunciation, example, category, learn_count, mastered)
                self.table.setItem(row, 0, QTableWidgetItem(str(word[0])))
                self.table.setItem(row, 1, QTableWidgetItem(word[1]))
                self.table.setItem(row, 2, QTableWidgetItem(word[2]))
                self.table.setItem(row, 3, QTableWidgetItem(word[3] or ""))
                self.table.setItem(row, 4, QTableWidgetItem(word[4] or ""))
                
                status = "已掌握" if word[7] else f"学习中 ({word[6]}次)"
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 5, status_item)
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载单词列表失败：{str(e)}")
            
    def delete_selected(self):
        """删除选中的单词"""
        selected_rows = set(item.row() for item in self.table.selectedItems())
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选择要删除的单词！")
            return
            
        confirm = QMessageBox.question(
            self, "确认删除",
            f"确定要删除选中的 {len(selected_rows)} 个单词吗？\n此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                for row in sorted(selected_rows, reverse=True):
                    word_id = int(self.table.item(row, 0).text())
                    self.db.delete_word(word_id)
                    self.table.removeRow(row)
                QMessageBox.information(self, "成功", "删除成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除单词失败：{str(e)}")
                
    def export_words(self):
        """导出单词列表"""
        try:
            from datetime import datetime
            filename = f"单词列表_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("单词列表\n")
                f.write("="*50 + "\n\n")
                
                for row in range(self.table.rowCount()):
                    word = self.table.item(row, 1).text()
                    meaning = self.table.item(row, 2).text()
                    pronunciation = self.table.item(row, 3).text()
                    example = self.table.item(row, 4).text()
                    status = self.table.item(row, 5).text()
                    
                    f.write(f"单词：{word}\n")
                    f.write(f"释义：{meaning}\n")
                    if pronunciation:
                        f.write(f"发音：{pronunciation}\n")
                    if example:
                        f.write(f"例句：{example}\n")
                    f.write(f"状态：{status}\n")
                    f.write("-"*50 + "\n\n")
                    
            QMessageBox.information(self, "成功", f"单词列表已导出到：{filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出单词列表失败：{str(e)}") 