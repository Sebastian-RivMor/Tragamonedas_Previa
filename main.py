from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.lang import Builder
from kivy.uix.widget import Widget


class LoginScreen(GridLayout):
    def slide_it(self, *args):
        self.slide_text.text = str(int(args[1]))
    def spinner_clicked(self, value):
        self.ids.click_label.text = f'{value}'


class Tercon(Button):
    pass

class Edad(Slider):
    pass

class Selcard(Widget):
    pass

class HelloApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    myApp = HelloApp()
    myApp.run()
