from src.backup import copy_folder

REMOTE_PATH = r"T:\資料交換一天\1568"
"""遠端資料夾路徑"""
BACKUP_PATH = r"D:\1568"
"""備份資料夾路徑"""

if __name__ == "__main__":
    print("正在複製備份到本機...")
    copy_folder(REMOTE_PATH, BACKUP_PATH)
    print("複製備份到本機完成")
    input("按下 Enter 鍵離開...")
