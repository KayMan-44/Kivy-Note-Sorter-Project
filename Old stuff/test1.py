from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label

class testWidget(Widget):
    pass

class testApp(App):
    def build(self):
        lbl = Label(text = "What do you want?")
        return lbl

appy = testApp()
appy.run()