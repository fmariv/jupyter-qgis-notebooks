@echo off
call "%~dp0\o4w_env.bat"
call "%OSGEO4W_ROOT%\apps\grass\grass76\etc\env.bat"
call qt5_env.bat
call py3_env.bat
@echo off
path %OSGEO4W_ROOT%\apps\qgis\bin;%OSGEO4W_ROOT%\apps\grass\grass76\lib;%OSGEO4W_ROOT%\apps\grass\grass76\bin;%PATH%
PATH %OSGEO4W_ROOT%\apps\qgis\python;%PATH%
PATH %OSGEO4W_ROOT%\apps\qgis\bin;%PATH%
PATH %OSGEO4W_ROOT%\apps\Qt5\bin;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python37;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python37\Scripts;%PATH%
PATH %OSGEO4W_ROOT%\apps\qgis\python\plugins;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python37\DLLs;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python37\lib;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python37\lib\site\packages;%PATH%

set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python

@echo off
call jupyter notebook