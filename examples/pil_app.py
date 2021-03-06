"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import time
import io

import PIL.Image

import remi.gui as gui
from remi import start, App


class PILImageViewverWidget(gui.Image):
    def __init__(self, width, height, pil_image=None):
        super(PILImageViewverWidget, self).__init__(width, height, "/res/logo.png")
        self._buf = None
    
    def load(self, file_path_name):
        pil_image = PIL.Image.open(file_path_name)
        self._buf = io.BytesIO()
        pil_image.save(self._buf, format='png')
        self.refresh()
    
    def refresh(self):
        i = int(time.time()*1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self),i)
        
    def get_image_data(self,update_index):
        if self._buf is None:
            return None
        self._buf.seek(0)
        headers = {'Content-type':'image/png'}
        return [self._buf.read(),headers]


class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        # the arguments are	width - height - layoutOrientationOrizontal
        wid = gui.Widget(640, 270, False, 10)
        self.image_widget = PILImageViewverWidget(200, 200)

        self.menu = gui.Menu(620, 30)
        m1 = gui.MenuItem(100, 30, 'File')
        m11 = gui.MenuItem(100, 30, 'Save')
        m12 = gui.MenuItem(100, 30, 'Open')
        m12.set_on_click_listener(self, 'menu_open_clicked')
        m111 = gui.MenuItem(100, 30, 'Save')
        m111.set_on_click_listener(self, 'menu_save_clicked')
        m112 = gui.MenuItem(100, 30, 'Save as')
        m112.set_on_click_listener(self, 'menu_saveas_clicked')

        self.menu.append('1',m1)
        m1.append('11',m11)
        m1.append('12',m12)
        m11.append('111',m111)
        m11.append('112',m112)
        
        wid.append('0', self.menu)
        wid.append('1', self.image_widget)
        
        # returning the root widget
        return wid

    def menu_open_clicked(self):
        self.fileselectionDialog = gui.FileSelectionDialog( 600, 310, 
            'File Selection Dialog', 'Select an image file',False,'.')
        self.fileselectionDialog.set_on_confirm_value_listener(
            self, 'on_image_file_selected')
        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialog.show(self)

    def on_image_file_selected(self,file_list):
        if len(file_list)<1:
            return
        self.image_widget.load(file_list[0])


if __name__ == "__main__":
    start(MyApp)
