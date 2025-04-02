"""備份模組，提供資料夾複製和進度追蹤功能。"""

from pathlib import Path
import shutil

from src.logger import logger


def get_progress(copied_files: int, total_files: int) -> float:
    """計算複製進度百分比

    Args:
        copied_files (int): 複製的檔案數量
        total_files (int): 總檔案數量

    Returns:
        float: 複製進度百分比
    """
    return (copied_files / total_files) * 100


def copy_file_with_progress(
    src: Path,
    dst: Path,
    copied_files: int,
    total_files: int,
) -> int:
    """複製單個檔案並更新進度

    Args:
        src (Path): 來源檔案路徑
        dst (Path): 目標檔案路徑
        copied_files (int): 已複製的檔案數
        total_files (int): 總檔案數

    Returns:
        int: 更新後的已複製檔案數
    """
    if dst.exists():
        src_stat = src.stat()
        dst_stat = dst.stat()
        if src_stat.st_size == dst_stat.st_size and int(src_stat.st_mtime) == int(
            dst_stat.st_mtime
        ):
            copied_files += 1
            progress = get_progress(copied_files, total_files)
            if progress % 5 < progress - get_progress(copied_files - 1, total_files):
                logger.info(f"進度: {progress:.2f}%")
            return copied_files

    shutil.copy2(src, dst)
    copied_files += 1
    progress = get_progress(copied_files, total_files)
    if progress % 5 < progress - get_progress(copied_files - 1, total_files):
        logger.info(f"進度: {progress:.2f}%")
    return copied_files


def copy_folder(src: str, dst: str):
    """複製資料夾及其內容到目標位置，若檔案已存在且相同則跳過，並顯示進度百分比

    Args:
        src (str): 來源資料夾路徑
        dst (str): 目標資料夾路徑
    """
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        logger.error(f"來源資料夾不存在: '{src_path}'")
        return

    if not dst_path.exists():
        dst_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"建立資料夾: '{dst_path}'")

    files_to_copy = [p for p in src_path.rglob("*") if p.is_file()]
    total_files = len(files_to_copy)
    logger.info(f"需要複製的檔案數量: {total_files}")
    if total_files == 0:
        logger.info("沒有檔案需要複製。")
        return

    copied_files = 0

    def recursive_copy(current_src: Path, current_dst: Path):
        """遞迴複製資料夾及其內容到目標位置

        Args:
            current_src (Path): 當前來源路徑
            current_dst (Path): 當前目標路徑
        """
        nonlocal copied_files

        if not current_src.is_dir():
            copied_files = copy_file_with_progress(
                current_src, current_dst, copied_files, total_files
            )
            return

        if not current_dst.exists():
            current_dst.mkdir(parents=True, exist_ok=True)
            logger.info(f"建立資料夾: '{current_dst}'")

        for item in current_src.iterdir():
            target = current_dst / item.name
            if item.is_dir():
                logger.info(f"複製資料夾: '{item}'")
                recursive_copy(item, target)
            else:
                copied_files = copy_file_with_progress(
                    item, target, copied_files, total_files
                )

    recursive_copy(src_path, dst_path)
    logger.info("複製完成！")
