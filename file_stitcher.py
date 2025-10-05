import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from plyer import filechooser

class Stitcher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.selected_files = []
        self.stitched_text = ""

        # File selector
        select_btn = Button(text='Select Text Files', size_hint_y=None, height=40)
        select_btn.bind(on_press=self.open_file_chooser)
        self.add_widget(select_btn)

        # File paths display
        self.file_list_display = TextInput(
            hint_text="Selected file paths will show here...",
            readonly=True,
            size_hint_y=0.2
        )
        self.add_widget(self.file_list_display)

        # Output name
        self.output_name = TextInput(
            hint_text='Enter output file name (no extension)',
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.output_name)
        
        # Merged content display
        self.result_display = TextInput(
            hint_text='Merged file content...',
            size_hint_y=0.4
        )
        self.add_widget(self.result_display)

        # Export button
        btn_export = Button(text='Export as .txt', size_hint_y=None, height=40)
        btn_export.bind(on_press=self.export_result)
        self.add_widget(btn_export)

    def show_popup(self, message):
        popup = Popup(
            title="",
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 150)
        )
        popup.open()

    def open_file_chooser(self, instance):
        def got_selection(selection):
            if selection:
                self.selected_files = selection
                self.file_list_display.text = "\n".join(selection)
                self.merge_selected_files()
        filechooser.open_file(filters=["*.txt"], multiple=True, on_selection=got_selection)

    def merge_selected_files(self):
        try:
            contents = []
            for path in self.selected_files:
                with open(path, 'r', encoding='utf-8') as f:
                    contents.append(f.read().strip())

            merged = contents[0]
            for i in range(1, len(contents)):
                merged = self.merge_files(merged, contents[i])

            self.stitched_text = merged
            self.result_display.text = merged
        except Exception as e:
            self.result_display.text = f"Error: {e}"

    def merge_files(self, a, b):
        a = a.strip()
        b = b.strip()
        if a in b:
            return b
        elif b in a:
            return a
        return a + "\n\n" + b

    def export_result(self, instance):
        filename = self.output_name.text.strip()
        if not filename:
            self.result_display.text = "Please enter a filename."
            return

        # Save to same directory as first selected file
        if self.selected_files:
            directory = os.path.dirname(self.selected_files[0])
            full_path = os.path.join(directory, filename + ".txt")
        else:
            full_path = filename + ".txt"

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(self.stitched_text)
            self.result_display.text = f"Exported to: {full_path}"
            self.show_popup("Note has been exported!")
        except Exception as e:
            self.result_display.text = f"Export failed: {e}"
