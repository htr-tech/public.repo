
taskkill /f /im explorer.exe

set iconcache=%localappdata%\IconCache.db
TAKEOWN /f "%iconcache%" && ICACLS "%iconcache%" /grant:r "%username%":F /T && ICACLS "%iconcache%" /grant:r "administrators":F /T
del "%iconcache%"/A
cd %userprofile%\AppData\Local\Microsoft\Windows\Explorer
attrib -H iconcache_*.db
del iconcache_*.db
cd %userprofile%\AppData\Local\Microsoft\Windows\Explorer
attrib -H thumbcache_*.db
del thumbcache_*.db
set thumbcache=C:\Users\%username%\AppData\Local\Microsoft\Windows\Explorer\*.db*
TAKEOWN /f "C:\Users\%username%\AppData\Local\Microsoft\Windows\Explorer" /r /d y && ICACLS "C:\Users\%username%\AppData\Local\Microsoft\Windows\Explorer" /grant:r "%username%":F /T && ICACLS "C:\Users\%username%\AppData\Local\Microsoft\Windows\Explorer" /grant:r "administrators":F /T
del "%thumbcache%"/A
del /F /Q "%SystemDrive%\Users\%username%\AppData\Local\Microsoft\Windows\Explorer\*.db"
del /F /Q /A:H "%SystemDrive%\Users\%username%\AppData\Local\Microsoft\Windows\Explorer\*.db"
del /F /Q /A:R "%SystemDrive%\Users\%username%\AppData\Local\Microsoft\Windows\Explorer\*.db"
del /F /S /Q /A "%LocalAppData%\Microsoft\Windows\Explorer\*.db"
DEL /F /S /Q /A %LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db
DEL /F /S /Q /A %LocalAppData%\Microsoft\Windows\Explorer\iconcache_*.db
explorer.exe