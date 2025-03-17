@ECHO OFF

@REM 設定輸出路徑
SET distpath=dist
SET buildpath=build

@REM 刪除輸出路徑
IF EXIST "%distpath%" RMDIR /S /Q "%distpath%"
IF EXIST "%buildpath%" RMDIR /S /Q "%buildpath%"

@REM 建立輸出路徑
mkdir "%distpath%"
ECHO Creating output path "%distpath%"
mkdir "%buildpath%"
ECHO Creating output path "%buildpath%"

@REM 轉換為 exe 檔案
pyinstaller -F run_copy_backup_to_local.py ^
--workpath "%buildpath%" ^
--distpath "%distpath%" ^
--clean ^
-y

DEL "*.spec"
ECHO Delete *.spec file

RMDIR /S /Q "%buildpath%"
ECHO Delete build folder

ECHO Conversion completed
PAUSE
