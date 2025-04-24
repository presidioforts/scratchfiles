
@echo off
setlocal

REM Create and activate virtual environment
python -m venv env
call env\Scripts\activate.bat

REM Upgrade pip and tools
pip install --upgrade pip setuptools wheel build

REM Download and build tokenizers from source
pip download tokenizers==0.13.3 --no-binary=:all:
tar -xvf tokenizers-0.13.3.tar.gz
cd tokenizers-0.13.3
python -m build

REM Copy the built wheel to workspace for archiving
copy dist\tokenizers-0.13.3-*.whl %WORKSPACE%

endlocal
