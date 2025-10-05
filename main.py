import kivy
import sqlite3
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from plyer import filechooser
from file_stitcher import Stitcher

Window.clearcolor = (0.1, 0.1, 0.2, 1)
kivy.require('2.1.0')

# Use platform-safe SQLite path
if platform == "android":
    db_path = App.get_running_app().user_data_dir + "/notes4sorter.db"
else:
    db_path = "notes4sorter.db"

notes_DB = sqlite3.connect(db_path)
cursor = notes_DB.cursor()

class NoteRoot(BoxLayout):
    pass

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
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.save_Note()

    Button:
        text: "STITCH FILES"
        color: 0, 0, 0, 1
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.open_stitch_popup()

    Button:
        text: "SHOW NOTES"
        color: 0, 0, 0, 1
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.show_merged_notes()

    Button:
        text: "EXPORT"
        color: 0, 0, 0, 1
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.export_As_txt()

    Button:
        text: "NEW"
        color: 0, 0, 0, 1
        background_color: 0.2, 0.6, 1, 1 
        background_normal: "" 
        on_press: app.new_Note()

    Button:
        text: "DELETE"
        background_color: 5.0, 0, 0, 1 
        background_normal: "" 
        on_press: app.confirm_delete_note()
'''

class NoteSorter(App):
    def build(self):
        Builder.load_string(kv_code)
        self.selected_ID = None
        self.notes_popup = None
        self.root = NoteRoot()
        return self.root

    def get_widget(self, name):
        return self.root.ids[name]

    def show_popup(self, message):
        popup = Popup(title="", content=Label(text=message), size_hint=(None, None), size=(300, 150))
        popup.open()

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
            self.show_popup("Note has been saved!")
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
        self.show_popup("Note has been exported!")

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
            self.show_popup("Note has been deleted!")

    def show_merged_notes(self, sort_mode="id"):
        if hasattr(self, "notes_popup") and self.notes_popup:
            self.notes_popup.dismiss()
            
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Sort options
        sort_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        sort_layout.add_widget(Button(text="Sort A-Z", on_press=lambda x: (self.notes_popup.dismiss(), self.show_merged_notes("alpha"))))
        sort_layout.add_widget(Button(text="Sort by ID", on_press=lambda x: (self.notes_popup.dismiss(), self.show_merged_notes("id"))))
        layout.add_widget(sort_layout)

        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Database notes
        cursor = notes_DB.cursor()
        if sort_mode == "alpha":
            cursor.execute('SELECT ID, note_Name, note_Subject FROM Notes ORDER BY note_Name COLLATE NOCASE')
        else:
            cursor.execute('SELECT ID, note_Name, note_Subject FROM Notes ORDER BY ID')

        for ID, name, subject in cursor.fetchall():
            row = BoxLayout(size_hint_y=None, height=40)
            btn = Button(text=f"DB: {name} | {subject}")
            btn.bind(on_press=lambda inst, ID=ID: (self.load_Note(ID), self.notes_popup.dismiss()))
            del_btn = Button(text="X", size_hint_x=0.15, background_color=(1,0,0,1))
            del_btn.bind(on_press=lambda inst, ID=ID: (self.notes_popup.dismiss(), self._delete_and_refresh(ID, lambda: self.show_merged_notes(sort_mode))))
            row.add_widget(btn)
            row.add_widget(del_btn)
            grid.add_widget(row)

        # Exported text files (sorted alphabetically)
        for fname in sorted([f for f in os.listdir('.') if f.endswith('.txt')]):
            row = BoxLayout(size_hint_y=None, height=40)
            btn = Button(text=f"FILE: {fname}")
            btn.bind(on_press=lambda inst, f=fname: (self.load_txt_file(f), self.notes_popup.dismiss()))
            del_btn = Button(text="X", size_hint_x=0.15, background_color=(1,0,0,1))
            del_btn.bind(on_press=lambda inst, f=fname: (self.notes_popup.dismiss(), self._delete_file_and_refresh(f, lambda: self.show_merged_notes(sort_mode))))
            row.add_widget(btn)
            row.add_widget(del_btn)
            grid.add_widget(row)

        scroll.add_widget(grid)
        layout.add_widget(scroll)

        self.notes_popup = Popup(title="All Notes (Sorted)", content=layout, size_hint=(0.95, 0.95))
        self.notes_popup.open()

    def _delete_and_refresh(self, ID, refresh_callback):
        cursor = notes_DB.cursor()
        cursor.execute('DELETE FROM Notes WHERE ID = ?', (ID,))
        notes_DB.commit()
        refresh_callback()
        self.show_popup("Note has been deleted!")

    def _delete_file_and_refresh(self, filename, refresh_callback):
        try:
            os.remove(filename)
        except Exception as e:
            print(f"Error deleting {filename}: {e}")
        refresh_callback()
        self.show_popup("Note has been deleted!")

    def load_txt_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                self.get_widget("note_name").text = filename.replace('.txt', '')
                self.get_widget("note_subject").text = lines[0] if lines else ''
                self.get_widget("note_content").text = '\n'.join(lines[1:]) if len(lines) > 1 else ''
        except Exception as e:
            print(f"Failed to load {filename}: {e}")

    def open_stitch_popup(self):
        stitch_widget = Stitcher()
        popup = Popup(title="Stitch Files", content=stitch_widget, size_hint=(0.9, 0.9))
        popup.open()
        
    def open_file_chooser(self):
        # Example function to use plyer's filechooser
        def got_selection(selection):
            if selection:
                print("Selected:", selection[0])  # Or handle file opening here

        filechooser.open_file(on_selection=got_selection)

if __name__ == '__main__':
    NoteSorter().run()

