from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.widget import Widget
from random import random

class NortApp(App):
    def build(self):
        layout = BoxLayout(orientation = "vertical")
        lbl1 = Label(text="Shit happens...")
        lbl2 = Label(text="Worlds Collide...")
        btn = Button(text="Yet they survive")
        layout.add_widget(lbl1)
        layout.add_widget(lbl2)
        layout.add_widget(btn)
        
        return layout

class SoutApp(App):
    def build(self):
        layout = FloatLayout()
        lbl1 = Label(text="Shit happens...", size_hint=(0.5, 0.3), pos_hint={'center_x':0.3, 'center_y':0.9})
        lbl2 = Label(text="Worlds Collide...", size_hint=(0.3, 0.1), pos_hint={'center_x':0.6, 'center_y':0.9})
        btn = Button(text="Yet they survive", size_hint=(0.3, 0.3), pos_hint={'center_x':0.5, 'center_y':0.5})
        layout.add_widget(lbl1)
        layout.add_widget(lbl2)
        layout.add_widget(btn)
        
        return layout
    
class MyLayout(BoxLayout):
    def __init__(self):
        super().__init__()
        self.btn = Button(text = "Press me")
        self.btn.bind(on_press = self.NewLabel)
        
        self.add_widget(self.btn)
        
    def NewLabel(self, btn):
        self.lbl = Label(text = "New text biatch!")
        self.add_widget(self.lbl)
        self.remove_widget(btn)

class MyApp2(App):
    def build(self):
        return MyLayout()
    
class MyLabel(Label):
    def __init__(self, text):
        super().__init__()
        self.text = text
    
class MyApp3(App):
    def build(self):
        self.OwnLabel = MyLabel("Hi")
        return self.OwnLabel
    
class MyWidget(Widget):
    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

class MyApp4(App):
    def build(self):
        return MyWidget()
    
if __name__ == '__main__':
    MyApp4().run()