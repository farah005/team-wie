@echo off
REM Script pour télécharger les JAR Jakarta EE manquants

setlocal enabledelayedexpansion

set "LIB_DIR=c:\Users\Admin\Desktop\jee\rendezVousDentaire\src\main\webapp\WEB-INF\lib"

echo Création du répertoire lib...
if not exist "%LIB_DIR%" mkdir "%LIB_DIR%"

echo.
echo Téléchargement des JAR Jakarta EE...
echo.

REM Liste des JAR à télécharger
set "JARS[0]=jakarta.servlet-api-6.0.0.jar|https://repo1.maven.org/maven2/jakarta/servlet/jakarta.servlet-api/6.0.0/jakarta.servlet-api-6.0.0.jar"
set "JARS[1]=jakarta.ejb-api-4.0.0.jar|https://repo1.maven.org/maven2/jakarta/ejb/jakarta.ejb-api/4.0.0/jakarta.ejb-api-4.0.0.jar"
set "JARS[2]=jakarta.persistence-api-3.1.0.jar|https://repo1.maven.org/maven2/jakarta/persistence/jakarta.persistence-api/3.1.0/jakarta.persistence-api-3.1.0.jar"
set "JARS[3]=jakarta.activation-api-2.1.0.jar|https://repo1.maven.org/maven2/jakarta/activation/jakarta.activation-api/2.1.0/jakarta.activation-api-2.1.0.jar"
set "JARS[4]=jakarta.xml.bind-api-4.0.0.jar|https://repo1.maven.org/maven2/jakarta/xml/bind/jakarta.xml.bind-api/4.0.0/jakarta.xml.bind-api-4.0.0.jar"

for /L %%i in (0,1,4) do (
    for /f "tokens=1,2 delims=|" %%a in ("!JARS[%%i]!") do (
        set "FILE=%%a"
        set "URL=%%b"
        
        if exist "%LIB_DIR%\!FILE!" (
            echo [✓] !FILE! existe déjà
        ) else (
            echo [→] Téléchargement de !FILE!...
            powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '!URL!' -OutFile '%LIB_DIR%\!FILE!'"
            if exist "%LIB_DIR%\!FILE!" (
                echo [✓] !FILE! téléchargé avec succès
            ) else (
                echo [✗] Erreur lors du téléchargement de !FILE!
            )
        )
    )
)

echo.
echo Téléchargement terminé!
echo.
pause
