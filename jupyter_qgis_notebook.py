# -*- coding: utf-8 -*-
"""
/***************************************************************************
 JupyterQGISNotebook
                                 A QGIS plugin
 Jupyter Notebook in QGIS environment
                              -------------------
        begin                : 2021-11-10
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Fran Martín
        email                : fmartinrivas2@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# Import base libraries
import os.path
from subprocess import call
import pkg_resources
import platform
import sys

try:
    # Import QGIS libraries
    from qgis.core import Qgis, QgsMessageLog
    # Import PyQt5 libraries
    from PyQt5.QtCore import QSettings, QTranslator, QCoreApplication
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QAction
except:
    from qgis.core import QGis as Qgis, QgsMessagelog
    from PyQt4.QtCore import QSettings, QTranslator, QCoreApplication
    from PyQt4.QtGui import QIcon
    from PyQt4.QtWidgets import QAction


PLATFORM = platform.system()

# TODO test in Linux
# TODO test in MacOS
# TODO what to do when the OSGEO4W_ROOT environment variable is not defined


class JupyterQGISNotebook:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'JupyterQGIS_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Jupyter QGIS Notebook')

        # #######################
        # Paths
        # ###########
        # OSGeo4W Shell
        self.osgeo_shell_path = os.path.join(os.environ['OSGEO4W_ROOT'], 'OSGEO4W.bat')
        # Installers
        self.windows_installer_path = os.path.join(self.plugin_dir, 'scripts/windows/install-notebook.sh')
        self.linux_installer_path = os.path.join(self.plugin_dir, 'scripts/linux/install-notebook.sh')
        # Launchers
        self.windows_launcher_path = os.path.join(self.plugin_dir, 'scripts/windows/run-notebook.bat')
        self.linux_launcher_path = os.path.join(self.plugin_dir, 'scripts/linux/run-notebook.sh')

        # #######################
        # Calls
        # ###########
        # Installer command calls
        if PLATFORM.startswith('Windows'):
            self.installer_call = [self.osgeo_shell_path, self.windows_installer_path]
        elif PLATFORM.startswith('Linux'):
            self.installer_call = [self.linux_installer_path]
        # Launcher command calls
        if PLATFORM.startswith('Windows'):
            self.run_call = [self.windows_launcher_path]
        elif PLATFORM.startswith('Linux'):
            self.run_call = [self.linux_launcher_path]

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('JupyterQGIS', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """ Create the menu entries and toolbar icons inside the QGIS GUI """

        icon_path = os.path.join(os.path.join(os.path.dirname(__file__), 'icon.png'))
        self.add_action(
            icon_path,
            text=self.tr(u'Jupyter QGIS Notebook'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """ Removes the plugin menu item and icon from QGIS GUI """
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Jupyter QGIS Notebook'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """ Run method that performs all the real work """
        # Check if the Jupyter package is already installed in the python environment or not. If not,
        # run the installer. If it is, run the notebook
        installed_packages = pkg_resources.working_set
        installed_packages_list = sorted([i.key for i in installed_packages])

        if 'jupyter' in installed_packages_list:
            # Jupyter is installed
            try:
                call(self.run_call)   # FIXME QGIS crashes when run, not working when OSGEO4W_ROOT not defined
            except Exception as e:
                self.show_error_message('There has been an error during the Jupyter Notebook launching process. '
                                        'See the QGIS log for further information')
                QgsMessageLog.logMessage(e)
        else:
            # Jupyter is not installed
            try:
                call(self.installer_call)
                self.show_success_message('Jupyter Notebook environment correctly installed')
                # Restart QGIS to reload the environment's intalled packages
                # os.execl(sys.executable, sys.executable, *sys.argv)   # FIXME not working
            except Exception as e:
                self.show_error_message('There has been an error during the Jupyter Notebook installing process. '
                                        'See the QGIS log for further information')
                QgsMessageLog.logMessage(e)

    # #################################################
    # QGIS Messages
    def show_success_message(self, text):
        """ Show a QGIS success message """
        self.iface.messageBar().pushMessage('OK', text, level=Qgis.Success)

    def show_error_message(self, text):
        """ Show a QGIS error message """
        self.iface.messageBar().pushMessage('Error', text, level=Qgis.Critical)

    def show_warning_message(self, text):
        """ Show a QGIS warning message """
        self.iface.messageBar().pushMessage('Warning', text, level=Qgis.Warning)


if __name__ == '__main__':
    pass
