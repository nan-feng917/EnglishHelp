from models.database import Database
from utils.review_scheduler import ReviewScheduler
import random
import os

class WordMemorizer:
    def __init__(self):
        # 确保数据库目录存在
        os.makedirs('database', exist_ok=True)
        self.db = Database()
        self.scheduler = ReviewScheduler()

    def add_sample_words(self):
        """添加单词到数据库"""
        try:
            while True:
                print("\n" + "="*50)
                print("添加单词模式")
                print("1. 添加预设示例单词")
                print("2. 手动添加新单词")
                print("3. 返回主菜单")
                
                choice = input("\n请选择 (1-3): ").strip()
                
                if choice == "1":
                    sample_words = [
                        ("hello", "你好", "həˈləʊ", "Hello, how are you?", "基础词汇"),
                        ("world", "世界", "wɜːld", "Hello world!", "基础词汇"),
                        ("python", "蟒蛇；Python编程语言", "ˈpaɪθɑːn", "Python is easy to learn.", "编程"),
                    ]
                    
                    print("\n开始添加示例单词...")
                    for word in sample_words:
                        try:
                            self.db.add_word(*word)
                            print(f"成功添加单词: {word[0]}")
                        except Exception as e:
                            print(f"添加单词 {word[0]} 失败: {str(e)}")
                    print("\n示例单词添加完成！")
                    input("\n按回车键继续...")
                    
                elif choice == "2":
                    while True:
                        print("\n请输入单词信息（每项按回车确认，直接按回车返回上级菜单）：")
                        word = input("单词: ").strip()
                        if not word:
                            break
                        
                        meaning = input("释义: ").strip()
                        if not meaning:
                            print("释义不能为空！")
                            continue
                        
                        pronunciation = input("发音（可选）: ").strip()
                        example = input("例句（可选）: ").strip()
                        category = input("分类（可选）: ").strip()
                        
                        try:
                            self.db.add_word(word, meaning, pronunciation, example, category)
                            print(f"\n成功添加单词: {word}")
                            
                            if input("\n是否继续添加单词？(y/n): ").lower() != 'y':
                                break
                            
                        except Exception as e:
                            print(f"\n添加单词失败: {str(e)}")
                            if input("\n是否重试？(y/n): ").lower() != 'y':
                                break
                
                elif choice == "3":
                    print("\n返回主菜单...")
                    break
                else:
                    print("\n无效的选择，请重试。")
                    input("\n按回车键继续...")
                    
        except Exception as e:
            print(f"\n添加单词时出错: {str(e)}")
            input("\n按回车键继续...")

    def start_learning(self, mode="sequence"):
        """开始学习模式"""
        words = self.db.get_words_to_review()
        if not words:
            print("\n当前没有可学习的单词。请先添加一些单词！")
            return
        
        if mode == "random":
            random.shuffle(words)
        
        print(f"\n开始{mode=='random' and '随机' or '顺序'}背诵，共 {len(words)} 个单词")
        print("提示：输入 'q' 可以随时退出背诵")
        
        for word in words:
            if not self.show_word(word):  # 如果返回 False，表示用户想要退出
                print("\n已退出背诵！")
                return
            if not self.check_answer(word):  # 如果返回 False，表示用户想要退出
                print("\n已退出背诵！")
                return

        print("\n本轮学习完成！")

    def show_word(self, word):
        """显示单词信息"""
        print("\n" + "="*50)
        print(f"单词: {word[1]}")
        response = input("按回车查看释义...(输入 'q' 退出): ")
        if response.lower() == 'q':
            return False
        
        print(f"释义: {word[2]}")
        print(f"发音: {word[3]}")
        print(f"例句: {word[4]}")
        print(f"分类: {word[5]}")
        return True

    def check_answer(self, word):
        """检查用户答案"""
        try:
            while True:
                know = input("\n你记住这个单词了吗？(y/n/q 退出): ").lower()
                if know == 'q':
                    return False
                if know in ['y', 'n']:
                    try:
                        mastered = 1 if know == 'y' else 0
                        self.db.update_learning_record(word[0], mastered)
                        return True
                    except Exception as e:
                        print(f"更新学习记录失败: {str(e)}")
                        return False
                print("无效的输入，请输入 y/n/q")
        except Exception as e:
            print(f"处理答案时出错: {str(e)}")
            return False

    def show_statistics(self):
        """显示学习统计信息"""
        try:
            print("\n" + "="*50)
            print("学习统计信息")
            print("="*50)
            
            # 获取所有单词
            words = self.db.get_all_words()
            if not words:
                print("\n当前没有任何单词！")
                return
            
            total_words = len(words)
            # 修正索引：words中每个元素的结构是 (id, word, meaning, pronunciation, example, category, learn_count, mastered)
            mastered_words = sum(1 for word in words if word[-1])  # mastered 是最后一个字段
            
            print(f"\n总单词数：{total_words}")
            print(f"已掌握单词数：{mastered_words}")
            if total_words > 0:
                print(f"掌握率：{(mastered_words/total_words*100):.1f}%")
            
            print("\n单词列表：")
            print("-"*50)
            print(f"{'单词':<15}{'释义':<20}{'掌握状态':<10}{'学习次数':<10}")
            print("-"*50)
            
            for word in words:
                status = "已掌握" if word[-1] else "学习中"  # mastered 是最后一个字段
                learn_count = word[-2]  # learn_count 是倒数第二个字段
                print(f"{word[1]:<15}{word[2]:<20}{status:<10}{learn_count:<10}")
            
        except Exception as e:
            print(f"\n显示统计信息时出错: {str(e)}")
            print(f"错误详情: {str(e)}")

    def show_all_words(self):
        """显示所有单词列表"""
        try:
            print("\n" + "="*50)
            print("单词列表")
            print("="*50)
            
            words = self.db.get_all_words()
            if not words:
                print("\n当前没有任何单词！")
                return
            
            print(f"\n{'序号':<6}{'单词':<15}{'释义':<30}{'发音':<15}{'分类':<10}")
            print("-"*76)
            
            for i, word in enumerate(words, 1):
                # word结构: (id, word, meaning, pronunciation, example, category, learn_count, mastered)
                print(f"{i:<6}{word[1]:<15}{word[2]:<30}{word[3]:<15}{word[5]:<10}")
                
                if word[4]:  # 如果有例句
                    print(f"例句: {word[4]}")
                    print("-"*76)
            
        except Exception as e:
            print(f"\n显示单词列表时出错: {str(e)}")

    def clean_duplicates(self):
        """清理重复单词"""
        try:
            self.db.clean_duplicate_words()
        except Exception as e:
            print(f"清理重复单词时出错: {str(e)}")

def main():
    try:
        memorizer = WordMemorizer()
        
        while True:
            print("\n" + "="*50)
            print("欢迎使用背单词程序")
            print("1. 顺序背诵")
            print("2. 随机背诵")
            print("3. 添加单词")
            print("4. 查看统计")
            print("5. 查看所有单词")
            print("6. 清理重复单词")
            print("7. 退出")
            
            choice = input("\n请选择功能 (1-7): ").strip()
            
            if choice == "1":
                memorizer.start_learning("sequence")
                input("\n按回车键返回主菜单...")
            elif choice == "2":
                memorizer.start_learning("random")
                input("\n按回车键返回主菜单...")
            elif choice == "3":
                memorizer.add_sample_words()
                input("\n按回车键返回主菜单...")
            elif choice == "4":
                memorizer.show_statistics()
                input("\n按回车键返回主菜单...")
            elif choice == "5":
                memorizer.show_all_words()
                input("\n按回车键返回主菜单...")
            elif choice == "6":
                memorizer.clean_duplicates()
                input("\n按回车键返回主菜单...")
            elif choice == "7":
                print("\n感谢使用，再见！")
                break
            else:
                print("\n无效的选择，请重试。")
                input("\n按回车键继续...")

    except Exception as e:
        print(f"\n程序运行出错: {str(e)}")
        input("\n按回车键退出...")

if __name__ == "__main__":
    main() 