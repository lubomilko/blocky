:: Memorize current working dir and set it to the dir containing this bat file.
pushd "%~dp0"
:: Run tests using blocky source files (not binaries).
python.exe test_main.py
:: Set current working dir to the original memorized dir.
@popd
