import kivy
import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from datetime import datetime

kivy.require('2.1.0')

# List to store notes 
notes_DB = sqlite3.connect("notes4sorter.db")
notes = []

class NoteSorterApp(App):
    
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title input
        self.title_input = TextInput(hint_text="Title", size_hint_y=None, height=40)
        self.layout.add_widget(self.title_input)
        
        # Content input
        self.content_input = TextInput(hint_text="Content", size_hint_y=None, height=100, multiline=True)
        self.layout.add_widget(self.content_input)
        
        # Add button
        add_button = Button(text="Add Note", size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_note)
        self.layout.add_widget(add_button)
        
        # Notes display section
        self.notes_layout = GridLayout(cols=1, size_hint_y=None)
        self.notes_layout.bind(minimum_height=self.notes_layout.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 200))
        scroll_view.add_widget(self.notes_layout)
        
        self.layout.add_widget(scroll_view)
        
        # Delete button
        delete_button = Button(text="Delete Note", size_hint_y=None, height=50)
        delete_button.bind(on_press=self.delete_note)
        self.layout.add_widget(delete_button)
        
        return self.layout

    def add_note(self, instance):
        title = self.title_input.text
        content = self.content_input.text
        timestamp = datetime.now().isoformat()
        
        if title and content:
            note = {
                'title': title,
                'content': content,
                'timestamp': timestamp
            }
            notes.append(note)
            self.update_notes_display()
            self.title_input.text = ""
            self.content_input.text = ""
        else:
            self.show_popup("Error", "Title and Content are required.")

    def update_notes_display(self):
        self.notes_layout.clear_widgets()
        for idx, note in enumerate(notes):
            note_button = Button(text=f"{note['title']} - {note['timestamp']}", size_hint_y=None, height=40)
            note_button.bind(on_press=lambda btn, idx=idx: self.show_note_details(idx))
            self.notes_layout.add_widget(note_button)

    def show_note_details(self, idx):
        note = notes[idx]
        content_popup = Popup(title=note['title'], content=Label(text=note['content']), size_hint=(0.8, 0.8))
        content_popup.open()

    def delete_note(self, instance):
        if len(notes) > 0:
            note_to_delete = notes.pop()
            self.update_notes_display()
            self.show_popup("Success", f"Deleted note: {note_to_delete['title']}")
        else:
            self.show_popup("Error", "No notes to delete.")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    NoteSorterApp().run()
