@echo off
title C Drive Deep Clean
echo ================================================
echo  C Drive Deep Clean Tool
echo  RUN AS ADMINISTRATOR (right-click - Run as admin)
echo ================================================
echo.

echo [Step 1/4] Clean WinSxS component store (old versions)
echo This may take 5-10 minutes...
Dism /online /Cleanup-Image /StartComponentCleanup
echo.

echo [Step 2/4] Clean Windows Update superseded files
Dism /online /Cleanup-Image /SPSuperseded
echo.

echo [Step 3/4] List installed drivers - check which are old
echo Running...
pnputil /enum-drivers | findstr /i "Published Name Class Provider Date"
echo.
echo To delete an old driver, run:
echo   pnputil /delete-driver oemXX.inf
echo (replace oemXX.inf with the actual filename)
echo.

echo [Step 4/4] Run Windows Disk Cleanup
echo Press Win+R, type: cleanmgr
echo Select C: drive, click "Clean up system files"
echo Check ALL boxes, especially:
echo   - Windows Update Cleanup
echo   - Delivery Optimization Files
echo   - Temporary Windows Installation Files
echo   - Recycle Bin
echo Click OK
echo.

echo ================================================
echo EXTRA (if you want more space):
echo.
echo Disable hibernation (frees RAM-sized file):
echo   powercfg /h off
echo.
echo Reduce pagefile:
echo   System Properties - Advanced - Performance Settings
echo   Advanced - Virtual Memory - Change
echo   Set Custom size: 4096-8192 MB
echo ================================================
pause
