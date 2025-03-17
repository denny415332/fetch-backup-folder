from pathlib import Path
import shutil


def get_progress(copied_files: int, total_files: int) -> float:
    """計算複製進度百分比

    Args:
        copied_files (int): 複製的檔案數量
        total_files (int): 總檔案數量

    Returns:
        float: 複製進度百分比
    """
    return (copied_files / total_files) * 100


def copy_folder(src: str, dst: str):
    """複製資料夾及其內容到目標位置，若檔案已存在且相同則跳過，並顯示進度百分比

    Args:
        src (str): 來源資料夾路徑
        dst (str): 目標資料夾路徑
    """
    src_path = Path(src)  # 來源路徑
    dst_path = Path(dst)  # 目標路徑

    # 如果目標資料夾不存在，則建立
    if not dst_path.exists():
        dst_path.mkdir(parents=True, exist_ok=True)
        print(f"建立資料夾: '{dst_path}'")

    # 計算所有要複製的檔案數量（包含子目錄內的檔案）
    files_to_copy = [p for p in src_path.rglob("*") if p.is_file()]  # 遞迴取得所有檔案
    total_files = len(files_to_copy)  # 總檔案數量
    if total_files == 0:
        print("沒有檔案需要複製。")
        return

    copied_files = 0  # 複製的檔案數量

    def recursive_copy(current_src: Path, current_dst: Path):
        """遞迴複製資料夾及其內容到目標位置

        Args:
            current_src (Path): 當前來源路徑
            current_dst (Path): 當前目標路徑
        """
        nonlocal copied_files
        if current_src.is_dir():
            # 如果目標資料夾不存在，則建立
            if not current_dst.exists():
                current_dst.mkdir(parents=True, exist_ok=True)
                print(f"建立資料夾: '{current_dst}'")

            # 遞迴複製子目錄
            for item in current_src.iterdir():
                target = current_dst / item.name  # 目標路徑

                # 遞迴複製子目錄
                if item.is_dir():
                    print(f"複製資料夾: '{item}'")
                    recursive_copy(item, target)
                # 當 current_src 為檔案時
                else:
                    # 檢查目標檔案是否存在且相同（比對檔案大小與修改時間）
                    if target.exists():
                        src_stat = item.stat()  # 來源檔案的統計資訊
                        dst_stat = target.stat()
                        if src_stat.st_size == dst_stat.st_size and int(
                            src_stat.st_mtime
                        ) == int(dst_stat.st_mtime):
                            # print(f"跳過: {target} 已存在且相同")
                            copied_files += 1
                            progress = get_progress(copied_files, total_files)

                            # 每隔 5% 顯示一次進度
                            if progress % 5 < progress - get_progress(
                                copied_files - 1, total_files
                            ):
                                print(f"進度: {progress:.2f}%")

                            continue

                    # 複製檔案
                    shutil.copy2(item, target)
                    copied_files += 1
                    progress = get_progress(copied_files, total_files)
                    if progress % 5 < progress - get_progress(
                        copied_files - 1, total_files
                    ):
                        print(f"進度: {progress:.2f}%")
        else:
            # 當 current_src 為檔案時，先檢查目標檔案是否存在且相同
            if current_dst.exists():
                src_stat = current_src.stat()  # 來源檔案的統計資訊
                dst_stat = current_dst.stat()  # 目標檔案的統計資訊

                # 如果檔案大小和修改時間相同，則跳過複製
                if src_stat.st_size == dst_stat.st_size and int(
                    src_stat.st_mtime
                ) == int(dst_stat.st_mtime):
                    print(f"跳過: {current_dst} 已存在且相同")
                    copied_files += 1
                    progress = (copied_files / total_files) * 100
                    print(f"進度: {progress:.2f}%")
                    return

            # 複製檔案
            shutil.copy2(current_src, current_dst)
            copied_files += 1
            progress = (copied_files / total_files) * 100
            print(f"進度: {progress:.2f}%")

    recursive_copy(src_path, dst_path)
    print("複製完成！")
