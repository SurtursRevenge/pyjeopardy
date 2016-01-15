from PySide import QtGui
from pyjeopardy.game import Game
from .widgets import JeopardyControlWidget, JeopardyGameWidget

class JeopardyMain(QtGui.QMainWindow):
    def __init__(self):
        super(JeopardyMain, self).__init__()

        self._game = Game()

        self.initUI()

    def initUI(self):
        #
        # menu
        #
        menubar = self.menuBar()

        # menu -> game
        gameMenu = menubar.addMenu('&Game')

        # menu -> game -> abort game
        self.abortGameAction = QtGui.QAction('&Abort', self)
        self.abortGameAction.triggered.connect(self.stop_game)
        self.abortGameAction.setEnabled(False)
        gameMenu.addAction(self.abortGameAction)

        # menu -> game -> exit
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        gameMenu.addAction(exitAction)

        # menu -> config
        configMenu = menubar.addMenu('&Configuration')

        # menu -> config -> load
        loadConfigAction = QtGui.QAction('&Load', self)
        configMenu.addAction(loadConfigAction)

        # menu -> config -> save
        saveConfigAction = QtGui.QAction('&Save', self)
        configMenu.addAction(saveConfigAction)

        #
        # widgets
        #
        self.controlWidget = JeopardyControlWidget(game=self._game, main=self)

        # window content
        self.content = QtGui.QStackedWidget(self);
        self.content.addWidget(self.controlWidget)
        self.content.setCurrentWidget(self.controlWidget)

        self.setCentralWidget(self.content)

        # window title
        self.setWindowTitle('PyJeopardy')

        # show
        self.show()

    def start_game(self):
        # create widget
        gameWidget = JeopardyGameWidget(game=self._game)
        self.content.addWidget(gameWidget)
        self.content.setCurrentWidget(gameWidget)

        # update menu
        self.abortGameAction.setEnabled(True)

    def stop_game(self):
        # delete widgets
        self._close_all_widgets()

        # update menu
        self.abortGameAction.setEnabled(False)

    def _close_cur_widget(self):
        tmp = self.content.currentWidget()

        # do not delete control widget
        if tmp == self.controlWidget:
            return False

        self.content.removeWidget(tmp)
        return True

    def _close_all_widgets(self):
        while self._close_cur_widget():
            pass
