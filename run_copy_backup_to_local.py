"""主程式，用於執行資料夾備份功能。"""

from src.backup import copy_folder
from src.logger import logger

REMOTE_PATH = r"T:\資料交換一天\1568"
"""遠端資料夾路徑"""
BACKUP_PATH = r"D:\1568"
"""備份資料夾路徑"""

if __name__ == "__main__":
    logger.info("")
    logger.info("正在複製備份到本機...")
    copy_folder(REMOTE_PATH, BACKUP_PATH)
    logger.info("複製備份到本機完成")
    # input("按下 Enter 鍵離開...")
    logger.info("")
