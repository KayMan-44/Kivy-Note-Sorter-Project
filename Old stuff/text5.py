from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Color # type: ignore


class MyBox(Widget):
    myInput = ObjectProperty(None)
    
    def print_Out(self):
        print(self.myInput.text)

class test5App(App):
    def build(self):
        return MyBox()
    
run_App = test5App()
run_App.run()