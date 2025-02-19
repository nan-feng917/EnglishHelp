import sqlite3
import os
from datetime import datetime
from utils.review_scheduler import ReviewScheduler

class Database:
    def __init__(self, db_file="database/words.db"):
        try:
            self.db_file = db_file
            # 确保数据库目录存在
            db_dir = os.path.dirname(db_file)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
                
            # 检查数据库文件是否存在
            db_exists = os.path.exists(db_file)
            
            # 连接数据库（如果不存在会自动创建）
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            
            # 如果是新数据库，创建表结构
            if not db_exists:
                self.init_database()
                
            self.scheduler = ReviewScheduler()
            
        except Exception as e:
            print(f"初始化数据库时出错: {str(e)}")
            if hasattr(self, 'conn'):
                self.conn.close()
            raise

    def init_database(self):
        """初始化数据库表结构"""
        try:
            # 创建单词表
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL UNIQUE,  # 添加 UNIQUE 约束
                meaning TEXT NOT NULL,
                pronunciation TEXT,
                example TEXT,
                category TEXT
            )
            ''')
            
            # 创建学习记录表
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id INTEGER,
                learn_count INTEGER DEFAULT 0,
                mastered INTEGER DEFAULT 0,
                last_review_time TIMESTAMP,
                next_review_time TIMESTAMP,
                FOREIGN KEY (word_id) REFERENCES words (id)
            )
            ''')
            
            self.conn.commit()
            
        except Exception as e:
            print(f"创建数据库表时出错: {str(e)}")
            raise

    def __del__(self):
        """确保数据库连接在对象销毁时正确关闭"""
        if hasattr(self, 'conn'):
            try:
                self.conn.commit()
                self.conn.close()
            except Exception as e:
                print(f"关闭数据库连接时出错: {str(e)}")

    def add_word(self, word, meaning, pronunciation="", example="", category=""):
        try:
            # 检查单词是否已存在
            self.cursor.execute('SELECT id FROM words WHERE word = ?', (word,))
            existing_word = self.cursor.fetchone()
            if existing_word:
                print(f"单词 '{word}' 已存在，跳过添加")
                return False

            # 添加新单词
            self.cursor.execute('''
            INSERT INTO words (word, meaning, pronunciation, example, category)
            VALUES (?, ?, ?, ?, ?)
            ''', (word, meaning, pronunciation, example, category))
            
            word_id = self.cursor.lastrowid
            self.cursor.execute('''
            INSERT INTO learning_records (word_id, learn_count)
            VALUES (?, 0)
            ''', (word_id,))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"添加单词时出错: {str(e)}")
            return False

    def get_words_to_review(self):
        try:
            self.cursor.execute('''
            SELECT w.*, lr.learn_count, lr.mastered
            FROM words w
            JOIN learning_records lr ON w.id = lr.word_id
            WHERE lr.next_review_time <= datetime('now') OR lr.next_review_time IS NULL
            ''')
            
            words = self.cursor.fetchall()
            
            # 如果没有需要复习的单词，返回所有单词
            if not words:
                self.cursor.execute('''
                SELECT w.*, lr.learn_count, lr.mastered
                FROM words w
                JOIN learning_records lr ON w.id = lr.word_id
                ''')
                words = self.cursor.fetchall()
            
            return words
            
        except Exception as e:
            print(f"获取复习单词时出错: {str(e)}")
            return []

    def update_learning_record(self, word_id, mastered):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # 获取当前学习次数
            cursor.execute('SELECT learn_count FROM learning_records WHERE word_id = ?', (word_id,))
            current_learn_count = cursor.fetchone()[0]
            
            # 使用 ReviewScheduler 计算下次复习时间
            next_review_time = self.scheduler.calculate_next_review_time(current_learn_count)
            
            cursor.execute('''
            UPDATE learning_records
            SET learn_count = learn_count + 1,
                mastered = ?,
                last_review_time = ?,
                next_review_time = ?
            WHERE word_id = ?
            ''', (mastered, datetime.now(), next_review_time, word_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"更新学习记录时出错: {str(e)}")
            if 'conn' in locals() and conn:
                conn.close()

    def get_all_words(self):
        """获取所有单词及其学习状态"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT w.*, lr.learn_count, lr.mastered
            FROM words w
            JOIN learning_records lr ON w.id = lr.word_id
            ORDER BY w.word
            ''')
            
            words = cursor.fetchall()
            conn.close()
            return words
            
        except Exception as e:
            print(f"获取单词列表时出错: {str(e)}")
            if 'conn' in locals() and conn:
                conn.close()
            return []

    def clean_duplicate_words(self):
        """清理重复的单词"""
        try:
            print("\n开始清理重复单词...")
            
            # 找出所有重复的单词
            self.cursor.execute('''
            SELECT word, COUNT(*) as count, GROUP_CONCAT(id) as ids
            FROM words
            GROUP BY word
            HAVING count > 1
            ''')
            
            duplicates = self.cursor.fetchall()
            if not duplicates:
                print("没有发现重复单词。")
                return
            
            for dup in duplicates:
                word, count, ids = dup
                id_list = [int(id) for id in ids.split(',')]
                keep_id = id_list[0]  # 保留第一个ID
                delete_ids = id_list[1:]  # 其他ID将被删除
                
                # 删除重复单词的学习记录
                self.cursor.execute('''
                DELETE FROM learning_records
                WHERE word_id IN ({})
                '''.format(','.join('?' * len(delete_ids))), delete_ids)
                
                # 删除重复的单词
                self.cursor.execute('''
                DELETE FROM words
                WHERE id IN ({})
                '''.format(','.join('?' * len(delete_ids))), delete_ids)
                
                print(f"清理单词 '{word}' 的 {count-1} 个重复项")
            
            self.conn.commit()
            print("\n清理完成！")
            
        except Exception as e:
            print(f"清理重复单词时出错: {str(e)}")
            self.conn.rollback() 