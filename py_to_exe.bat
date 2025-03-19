@ECHO OFF

@REM 設定命令提示字元使用 UTF-8 編碼，避免中文亂碼
CHCP 65001
@REM 啟用延遲環境變數擴充功能，讓變數可以在執行時期動態改變
SETLOCAL ENABLEDELAYEDEXPANSION

@REM 設定輸出路徑
SET distpath=dist
SET buildpath=build

@REM 刪除輸出路徑
IF EXIST "%distpath%" RMDIR /S /Q "%distpath%"
IF EXIST "%buildpath%" RMDIR /S /Q "%buildpath%"

@REM 建立輸出路徑
mkdir "%distpath%"
ECHO 正在建立輸出路徑 "%distpath%"
mkdir "%buildpath%"
ECHO 正在建立輸出路徑 "%buildpath%"

@REM 轉換為 exe 檔案
pyinstaller -F run_copy_backup_to_local.py ^
            --workpath "%buildpath%" ^
            --distpath "%distpath%" ^
            --clean ^
            -y

DEL "*.spec"
ECHO 刪除 *.spec 檔案

RMDIR /S /Q "%buildpath%"
ECHO 刪除建置資料夾

ECHO 轉換完成
PAUSE
