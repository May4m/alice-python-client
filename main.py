
from kivy.app import App
from kivy.factory import Factory
from kivy.logger import Logger
from kivy.uix.screenmanager import FadeTransition


import widgets
import screens
import endpoint

try:
    import Android
    from Android import Intent
    from Android import Dialogs
    from Android import Activity
    from Android import Connection
    from Android import RecognizerIntent
except:
    Android = None
    Logger.warning("Application not running on android")


class AliceScreenManager(Factory.ScreenManager):
    pass


class Alice(App):

    def check_native_requirements(self):
        """
        checks whether the required packages are available on the android version

        """
        if not Android:
            return
        pm = Activity.getPackageManager()
        self.stt_mods = pm.queryIntentActivities(
            Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH), 0)
        if self.stt_mods.size() == 0:
            Logger.warning("Android Speech to Text packages not found")

    def build(self):
        """
        starting point of the application life cycle
        """
        manager = AliceScreenManager(transition=FadeTransition())
        Factory.register('ViewManager', cls=manager)
        return manager

    def on_start(self):
        endpoint.start_alice()
        self.check_native_requirements()

    def on_pause(self):
        return True


if __name__ == "__main__":
	Alice().run()