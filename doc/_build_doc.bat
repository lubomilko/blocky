@ECHO OFF

:: Store the current working directory and move into the directory containing this bat file.
pushd %~dp0

:: Remove the entire build directory for Sphinx build files and create a new empty one.
if exist build\ (
    rmdir /s /q build
)

:: Build HTML documentation and save it into the "html" dir in doc root dir.
sphinx-build -M html src build %O%

:: Move back to the original current working directory.
popd
