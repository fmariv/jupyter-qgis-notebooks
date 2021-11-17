# -*- coding: utf-8 -*-
"""
/***************************************************************************
 JupyterQGISNotebook
                                 A QGIS plugin
 Jupyter Notebook in QGIS environment
                             -------------------
        begin                : 2021-11-10
        copyright            : (C) 2021 by Fran Martín
        email                : fmartinrivas2@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load JupyterQGIS class from file JupyterQGIS.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .jupyter_qgis_notebook import JupyterQGISNotebook
    return JupyterQGISNotebook(iface)
