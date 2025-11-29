import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import themed_tk
from tkinter import filedialog, messagebox
import os

filename = None

def newFile():
    global filename
    if text.get(0.0, tk.END).strip():
        if not messagebox.askyesno("New File", "Do you want to discard unsaved changes?"):
            return
    
    filename = "Untitled"
    root.title("Lim - Untitled")
    text.delete(0.0, tk.END)

def saveFile():
    global filename

    if filename is None or filename == "Untitled":
        saveAs()
        return
    
    t = text.get(0.0, tk.END).strip()
    
    try:
        f = open(filename, 'w')
        f.write(t)
        f.close()
    except Exception as e:
        messagebox.showerror("Unable to Save", f"We cannot save your file. Try again.\nError: {e}")

def saveAs():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")

    if f is None:
        return
    
    t = text.get(0.0, tk.END).rstrip()
    
    try:
        f.write(t)
        global filename
        filename = f.name
        base_filename = os.path.basename(filename)
        root.title(f"Lim - {base_filename}")
        f.close()
    except Exception as e:
        messagebox.showerror("Unable to Save", f"We cannot save your file. Try again.\nError: {e}")

def openFile():
    global filename
    f = filedialog.askopenfile(mode='r', defaultextension=".txt")
    if f is not None:
        try:
            t = f.read()
            text.delete(0.0, tk.END)
            text.insert(0.0, t)
            
            filename = f.name
            base_filename = os.path.basename(filename)
            root.title(f"Lim - {base_filename}")
            
            f.close()
        except Exception as e:
            messagebox.showerror("Unable to Open", f"Could not read file.\nError: {e}")


root = themed_tk.ThemedTk(theme="arc")

try:
    icon_image = tk.PhotoImage(file=r'C:\Users\Main\Documents\dev\PythonVSCode\Lim\icon.png')
    root.wm_iconphoto(True, icon_image)
except tk.TclError:
    pass

root.title("Lim - Untitled")
root.minsize(width=400, height=400)

text_frame = ttk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) 

scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text = tk.Text(text_frame, 
               font=("Helvetica", 11), 
               wrap=tk.WORD, 
               relief=tk.FLAT, 
               yscrollcommand=scrollbar.set)

text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=text.yview)

menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator="Ctrl+N", command=newFile)
filemenu.add_command(label="Open...", accelerator="Ctrl+O", command=openFile)
filemenu.add_command(label="Save", accelerator="Ctrl+S", command=saveFile)
filemenu.add_command(label="Save As...", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)

root.bind('<Control-n>', lambda event: newFile())
root.bind('<Control-o>', lambda event: openFile())
root.bind('<Control-s>', lambda event: saveFile())

root.mainloop()