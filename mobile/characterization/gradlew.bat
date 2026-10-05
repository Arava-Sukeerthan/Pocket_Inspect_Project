@rem
@rem  Gradle startup script for Windows
@rem
@if "%DEBUG%"=="" @echo off
@if "%%OS%%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
set CMD_LINE_ARGS=%*

@rem Find gradle-wrapper.jar
set WRAPPER_JAR="%DIRNAME%gradle\wrapper\gradle-wrapper.jar"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto execute

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE="%JAVA_HOME%\bin\java.exe"

if exist %JAVA_EXE% goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
goto fail

:execute
if exist %WRAPPER_JAR% goto runWrapper
echo.
echo ERROR: Gradle wrapper JAR not found: %WRAPPER_JAR%
echo.
goto fail

:runWrapper
%JAVA_EXE% -jar %WRAPPER_JAR% %CMD_LINE_ARGS%
if "%ERRORLEVEL%" == "0" goto mainEnd

:fail
rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "%GRADLE_EXIT_CONSOLE%" == "" [exit %ERRORLEVEL%]
exit /b %ERRORLEVEL%

:mainEnd
if "%OS%"=="Windows_NT" endlocal
