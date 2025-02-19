from datetime import datetime, timedelta

class ReviewScheduler:
    @staticmethod
    def calculate_next_review_time(learn_count):
        """基于艾宾浩斯遗忘曲线计算下次复习时间"""
        intervals = [
            timedelta(minutes=5),    # 第1次复习
            timedelta(hours=1),      # 第2次复习
            timedelta(days=1),       # 第3次复习
            timedelta(days=2),       # 第4次复习
            timedelta(days=4),       # 第5次复习
            timedelta(days=7),       # 第6次复习
            timedelta(days=15),      # 第7次复习
            timedelta(days=30)       # 第8次复习
        ]
        
        if learn_count >= len(intervals):
            return datetime.now() + intervals[-1]
        return datetime.now() + intervals[learn_count] 