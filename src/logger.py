"""記錄器模組，用於處理應用程式的日誌記錄功能。"""

from logging import FileHandler, Formatter, getLogger, DEBUG

# 記錄器設定
logger = getLogger(__name__)  # 設定記錄器
logger.setLevel(DEBUG)  # 設定記錄等級

file_handler = FileHandler("log.txt")  # 設定檔案處理器
file_handler.setLevel(DEBUG)  # 設定檔案處理器的記錄等級

# 設定格式器
formatter = Formatter("%(asctime)s - %(name)s - %(message)s")
file_handler.setFormatter(formatter)  # 為檔案處理器設定格式器

logger.addHandler(file_handler)  # 為記錄器添加檔案處理器

# 輸出記錄
logger.debug("除錯記錄")
logger.info("資訊記錄")
logger.warning("警告記錄")
logger.error("錯誤記錄")
logger.critical("嚴重錯誤記錄")
