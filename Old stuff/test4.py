from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from random import random


class ScreenOne(Button):
    def __init__(self):
        super().__init__()
        self.text = "hello"
        self.bind(on_press = self.switch_Item)
        
    def switch_Item(self, item):
        run_App.screen_Manager.transition = SlideTransition(direction = "left")
        run_App.screen_Manager.current = "Second"

class ScreenTwo(Button):
    def __init__(self):
        super().__init__()
        self.text = "Hi there!"
        self.bind(on_press = self.switch_Item)
        
    def switch_Item(self, item):
        run_App.screen_Manager.transition = SlideTransition(direction = "right")
        run_App.screen_Manager.current = "First"

class MyApp(App):
    def build(self):
        self.screen_Manager = ScreenManager()
        
        self.first_Screen = ScreenOne()
        screen = Screen(name="First")
        screen.add_widget(self.first_Screen)
        self.screen_Manager.add_widget(screen)
        
        self.second_Screen = ScreenTwo()
        screen = Screen(name="Second")
        screen.add_widget(self.second_Screen)
        self.screen_Manager.add_widget(screen)
        
        return self.screen_Manager
    
run_App = MyApp()
run_App.run()
