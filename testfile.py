from kivy.app import App
from kivy.lang import Builder

kv = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    Label:
        text: "If you see this, Kivy is working!"

    Button:
        text: "Click me"
        on_press: print("Button clicked!")
'''

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    TestApp().run()