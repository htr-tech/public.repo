@echo off
mode 20, 12
:: Temporary PHP Server

title  PHP SERVER
SET ADDR=127.0.0.1:8081

cls
echo:                                                         
echo: [1] PHP 5
echo: [2] PHP 7
echo: [3] PHP 8
echo: [4] Exit                                        
choice /C:1234 /N /M "Option: "
set _erl=%errorlevel%
if %_erl%==4 exit /b
if %_erl%==1 goto php5
if %_erl%==2 goto php7
if %_erl%==3 goto php8

:php5
cls
echo %ADDR% | clip
:: start http://%ADDR%
"C:/Software/php5/php.exe" -S %ADDR%

:php7
cls
echo %ADDR% | clip
:: start http://%ADDR%
"C:/Software/php7/php.exe" -S %ADDR%

:php8
cls
echo %ADDR% | clip
:: start http://%ADDR%
"C:/Software/php8/php.exe" -S %ADDR%
