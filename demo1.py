import kivy
import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from file_stitcher import Stitcher

Window.clearcolor = (0.1, 0.1, 0.2, 1) #R G B A

kivy.require('2.1.0')
notes_DB = sqlite3.connect("notes4sorter.db")
cursor = notes_DB.cursor()

#D2 nakalagay ung ui (This will be called in the build function)
class NoteRoot(BoxLayout):
    pass

#GUI ng program
kv_code = '''
<NoteRoot>:
    orientation: "vertical"
    spacing: 10
    padding: 10

    TextInput:
        id: note_name
        hint_text: "Note Name"
        size_hint_y: None
        height: 40

    TextInput:
        id: note_subject
        hint_text: "Subject"
        size_hint_y: None
        height: 40

    TextInput:
        id: note_content
        hint_text: "Write..."
        size_hint_y: None
        height: 100

    Button:
        text: "SAVE"
        color: 0, 0, 0, 1
        size_hint_y: None
        height: 40
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.save_Note()

    Button:
        text: "STITCH FILES"
        color: 0, 0, 0, 1
        size_hint_y: None
        height: 40
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.open_stitch_popup()
    
    Button:
        text: "EXPORT"
        color: 0, 0, 0, 1
        size_hint_y: None
        height: 40
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.export_As_txt()
    
    Button:
        text: "SORT"
        color: 0, 0, 0, 1
        size_hint_y: None
        height: 40
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: 

    Button:
        text: "NEW"
        color: 0, 0, 0, 1
        size_hint_y: None
        height: 40
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.new_Note()

    Label:
        text: "Saved Notes:"
        font_size: 25
        size_hint_y: None
        height: 30

    ScrollView:
        size_hint: (1, 1)

        GridLayout:
            id: notes_list
            cols: 1
            spacing: 10
            size_hint_y: None
            height: self.minimum_height

    Button:
        text: "DELETE"
        size_hint_y: None
        height: 40
        background_color: 5.0, 0, 0, 1 
        background_normal: "" 
        on_press: app.confirm_delete_note()
'''

#Main program
class NoteSorter(App):
    def build(self):
        Builder.load_string(kv_code)
        self.selected_ID = None
        self.root = NoteRoot()
        self.refresh_notes_list()
        return self.root
    
    def get_widget(self, name):
        return self.root.ids[name]

    def save_Note(self):
        try:
            notes_DB.execute(
                'INSERT INTO Notes (note_Content, note_Name, note_Subject) VALUES (?, ?, ?)',
                (
                    self.get_widget("note_content").text,
                    self.get_widget("note_name").text,
                    self.get_widget("note_subject").text
                )
            )
            notes_DB.commit()
            self.refresh_notes_list()
        except Exception as e:
            print(f"Error: {e}")

    def new_Note(self):
        self.selected_ID = None
        self.get_widget("note_name").text = ""
        self.get_widget("note_subject").text = ""
        self.get_widget("note_content").text = ""

    def load_Note(self, ID):
        self.selected_ID = ID
        cursor = notes_DB.cursor()
        cursor.execute('SELECT note_Name, note_Content, note_Subject FROM Notes WHERE ID = ?', (ID,))
        note = cursor.fetchone()

        if note:
            name, content, subject = note
            self.get_widget("note_name").text = name
            self.get_widget("note_content").text = content
            self.get_widget("note_subject").text = subject

    def export_As_txt(self):
        filename = f"{self.get_widget('note_name').text}.txt"
        with open(filename, 'w') as file:
            file.write(self.get_widget("note_subject").text + "\n")
            file.write(self.get_widget("note_content").text)
        print(f"Exported to {filename}")

    def confirm_delete_note(self):
        if self.selected_ID is None:
            print("No note selected.")
            return

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Are you sure you want to delete this note?"))

        btn_layout = BoxLayout(spacing=10, size_hint_y=0.3)
        yes_btn = Button(text="Yes")
        no_btn = Button(text="Cancel")
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)

        content.add_widget(btn_layout)

        popup = Popup(title="Confirm Delete", content=content, size_hint=(None, None), size=(350, 200), auto_dismiss=False)
        yes_btn.bind(on_press=lambda x: (self.delete_note(), popup.dismiss()))
        no_btn.bind(on_press=popup.dismiss)
        popup.open()

    def delete_note(self):
        if self.selected_ID is not None:
            cursor = notes_DB.cursor()
            cursor.execute('DELETE FROM Notes WHERE ID = ?', (self.selected_ID,))
            notes_DB.commit()
            self.selected_ID = None
            self.new_Note()
            self.refresh_notes_list()

    def refresh_notes_list(self):
        if not self.root:
            return
        list_layout = self.get_widget("notes_list")
        list_layout.clear_widgets()

        cursor = notes_DB.cursor()
        cursor.execute('SELECT ID, note_Name, note_Subject FROM Notes')
        notes = cursor.fetchall()

        for ID, name, subject in notes:
            btn = Button(text=f"Name: {name} | Subject: {subject}", size_hint_y=None, height=100, background_normal="", background_color=(0.6, 0.6, 4, 5 ), color=(0, 0, 0, 1), font_size=20)
            btn.bind(on_press=lambda instance, ID=ID: self.load_Note(ID))
            list_layout.add_widget(btn)

    def open_stitch_popup(self):
        stitch_widget = Stitcher()
        popup = Popup(title="Stitch Files", content=stitch_widget, size_hint=(0.9, 0.9))
        popup.open()

if __name__ == '__main__':
    NoteSorter().run()
