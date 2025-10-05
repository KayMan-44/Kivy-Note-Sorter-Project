from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Color
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
       

class note_Taking(App):
    def build(self):
        self.layout = BoxLayout()
        self.text = Label(text = "Hello there")
        self.user_Input = TextInput(hint_text = "Write...")
        
        self.save_Button = Button(text ="Save")
        
        self.layout.add_widget(self.text)
        self.layout.add_widget(self.user_Input)
        self.layout.add_widget(self.save_Button)
        
        return self.layout
    
    def on_touch_down(self, touch):
            self.user_Input = TextInput(text = "")
        
if __name__ == '__main__':
    note_Taking().run()