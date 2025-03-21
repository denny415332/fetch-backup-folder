"""日誌記錄模組，提供日誌記錄管理器"""

import inspect
from pathlib import Path
from datetime import datetime
from logging import FileHandler, Formatter, Logger, StreamHandler, getLogger, DEBUG


class LogManager:
    """日誌記錄管理器，負責管理日誌記錄器、處理器和格式器"""

    _logger: Logger = None
    """記錄器"""
    _console_handler: StreamHandler = None
    """主控台處理器"""
    _file_handler: FileHandler = None
    """檔案處理器"""

    def __init__(self, name: str):
        """初始化日誌記錄器

        Args:
            name (str): 記錄器名稱
        """

        # 建立日誌路徑
        now = datetime.now()
        log_path = (
            Path("log")
            / f"{now.strftime('%Y')}"
            / f"{now.strftime('%Y-%m')}"
            / f"{now.strftime('%Y-%m-%d')}.txt"
        )

        # 設定記錄器
        self._logger = getLogger(name)
        self._logger.setLevel(DEBUG)

        # 如果資料夾不存在，則建立資料夾
        if not log_path.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)

        # 設定主控台處理器
        self._console_handler = StreamHandler()
        self._console_handler.setLevel(DEBUG)

        # 設定檔案處理器
        self._file_handler = FileHandler(log_path)
        self._file_handler.setLevel(DEBUG)

        # 設定格式器
        self.fmt = Formatter("%(asctime)s - %(message)s")
        self._console_handler.setFormatter(self.fmt)
        self._file_handler.setFormatter(self.fmt)

        # 添加處理器
        self._logger.addHandler(self._console_handler)
        self._logger.addHandler(self._file_handler)

    def _update_log_format_with_caller(self):
        """更新日誌格式字串，包含呼叫者模組名稱"""

        ##### 更新呼叫者模組名稱 #####
        frame = inspect.currentframe().f_back.f_back  # 取得呼叫者的呼叫者框架
        module = inspect.getmodule(frame) if frame else None  # 取得呼叫者模組
        caller_module = module.__name__ if module else "__unknown__"  # 呼叫者模組名稱

        ##### 更新格式字串 #####
        fmt = Formatter(f"%(asctime)s - {caller_module} - %(message)s")  # 更新格式字串
        self._console_handler.setFormatter(fmt)  # 更新主控台處理器
        self._file_handler.setFormatter(fmt)  # 更新檔案處理器

    ##### 記錄訊息 #####

    def debug(self, message: str):
        """記錄除錯訊息

        Args:
            message (str): 要記錄的訊息
        """
        self._update_log_format_with_caller()
        self._logger.debug(message)

    def info(self, message: str):
        """記錄一般資訊

        Args:
            message (str): 要記錄的訊息
        """
        self._update_log_format_with_caller()
        self._logger.info(message)

    def warning(self, message: str):
        """記錄警告訊息

        Args:
            message (str): 要記錄的訊息
        """
        self._update_log_format_with_caller()
        self._logger.warning(message)

    def error(self, message: str):
        """記錄錯誤訊息

        Args:
            message (str): 要記錄的訊息
        """
        self._update_log_format_with_caller()
        self._logger.error(message)

    def critical(self, message: str):
        """記錄嚴重錯誤訊息

        Args:
            message (str): 要記錄的訊息
        """
        self._update_log_format_with_caller()
        self._logger.critical(message)


logger = LogManager(__name__)
"""日誌記錄管理器"""
