import os
import Tkinter  as tk
import Image, ImageTk
from   util import renderMachine


class PreviewWindow(object):
    TEMP_FILENAME  = 'temp/fsm.png'
    ERROR_FILENAME = 'data/preview_error.png'
    INVALID_FILENAME = 'data/preview_invalid.png'
    
    def __init__(self, master, fsm, showrefresh=True):
        self._window = tk.Toplevel(master)
        self._window.title('Preview')
        self._window.transient(master)
        self._window.resizable(0,0)

        self._fsm    = fsm
        
        self._panel = tk.Label(self._window)
        self._panel.pack(side='top', fill='both', expand='yes')
        
        self._button = tk.Button(self._window, text='Refresh', command=self.refresh)
        self._button.lift()
        
        if showrefresh:
            self._button.place(y=0)
        else:
            self._button.place(y=-50)
        
        self.refresh()

    def refresh(self, fsm=None):
        if fsm: self._fsm = fsm
        
        if not self._fsm.isValid():
            filename = self.INVALID_FILENAME
        else:
            if os.path.exists(self.TEMP_FILENAME):
                os.unlink(self.TEMP_FILENAME)
            try:
                res = self._window.winfo_fpixels('1i')
                y_margin = 60 #Shell GUI (eg taskbar)
                size = (self._window.winfo_screenwidth() / res,
                        (self._window.winfo_screenheight()-y_margin) / res)

                renderMachine(self._fsm, outfile=self.TEMP_FILENAME, size=size)
                
                if os.path.exists(self.TEMP_FILENAME):
                    filename = self.TEMP_FILENAME
                else:
                    raise SystemError, 'No output rendered.'
            except:
                open('err.gv','w').write(self._fsm.toGraphViz(size))
                filename = self.ERROR_FILENAME
        
        self._image = ImageTk.PhotoImage(Image.open(filename))

        self._panel.configure(image=self._image)

        self.reposition()
        
    def reposition(self, y=None):
        w = self._image.width()
        h = self._image.height()

        x = (self._window.winfo_screenwidth() - w) / 2

        if y:
            self._window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        else:
            self._window.geometry("%dx%d+%d+%d" % (w, h, x, self._window.winfo_y()))

        x_offset = w-self._button.winfo_reqwidth()
        self._button.place(x=x_offset)
