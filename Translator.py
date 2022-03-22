import os
import re
import time
# pip install googletrans==4.0.0rc1
from googletrans import Translator
import tkinter as tk
from tkinter import font as tkFont  # for convenience
from tkinter import filedialog
from tkinter import ttk



#Local variable
opt=0


#function

def save_file_at_dir(dir_path, filename, file_content, mode='w'):
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, filename), mode, encoding='utf-8') as f:
        f.write(file_content)

def is_text_line(line):
    pattern = '[0-9]'
    return not ((1 if re.match(pattern, line[0]) else 0) and ( 1 if re.match(pattern, line[len(line)-2]) else 0))

def main_path(path):
    return path.strip("\n")

def name_file_after_translate(main_path, suffix='.vi'):
    name_file_after_translate_arr = main_path.split('\/').pop()
    name_file_after_translate_arr = name_file_after_translate_arr.split('.')
    name_file_after_translate_arr[len(name_file_after_translate_arr)-2] += suffix
    name_file_after_translate = ''
    for i in range(0,len(name_file_after_translate_arr)):
        if i == len(name_file_after_translate_arr) -1:
            name_file_after_translate += name_file_after_translate_arr[i]
        else:
            name_file_after_translate += name_file_after_translate_arr[i] + '.'
    return name_file_after_translate

def clear_content(component):
    component.delete('1.0', 'end')

def get_content(component):
    return component.get('1.0', 'end-1c')

def show_content(component, content):
    clear_content(component)
    component.insert('1.0', content)
    
def parent_path(main_path):
    main_path_arr = main_path.split('/')
    main_path_arr.pop()
    parent_path = ''
    for i in range(0,len(main_path_arr)):
        if i == len(main_path_arr) -1:
            parent_path += main_path_arr[i]
        else:
            parent_path += main_path_arr[i] + '/'
    return  parent_path
    

def open_file():
    clear_content(inputText)
    clear_content(outputText)
    
    filepath = filedialog.askopenfile().name
    show_content(inputText, filepath)
    trans_button.config(state='active')

    
def translate_file():
    show_content(outputText, 'Wait a minute')
    # num = get_content(num_button)
    path = inputText.get('1.0', 'end')
    print(path)
    if path != '' and path != '\n':
         # mainPath = 'D:\text.srt'
        mainPath = main_path(path)
        num= int(get_content(num_button))
        ### Suffix file after trans
        suffix_file = '.' + get_content(src_button)
        # mainPath = 'D:\text.srt'
        # parentPath = 'D:\'
        parentPath = parent_path(mainPath)
        # nameFileAterTrans = 'text.vi.srt'
        nameFileAterTrans = name_file_after_translate(mainPath , suffix=suffix_file)
        
        translator = Translator()
        content =list()
        file= open(mainPath, 'r', encoding='utf-8')
        text=file.readlines()
        
        content=''
        tem=''
        i=0
        try:
            for line in text:
                if( is_text_line(line) and (line != '\n')):
                    tem += line
                if i% num == 0 and i != 0:
                    content += translator.translate(tem, dest='vi').text
                    content += '\n'
                    tem=''
                i+=1
            show_content(outputText, 'Loading: 50%')

            content += translator.translate(tem, dest='vi').text
        except:
            show_content(outputText, 'Network disconnected! Please try again')
            return None
        tem = content.split('\n')
        

        length_tem= len(tem)

        i=0
        result=''
        try:
            for line in text:
                if i == length_tem:
                    break
                if( is_text_line(line) and (line != '\n')):
                    result += tem[i] + '\n'
                    i+=1
                else:
                    result += line
            os.makedirs(os.path.abspath(parentPath), exist_ok=True)
            with open(os.path.join(os.path.abspath(parentPath), nameFileAterTrans),  mode='w', encoding='utf-8') as f:
                f.write(result)
        except:
            show_content(outputText, 'OOPS! Something was wrong - Please try again')
            return None
        
        show_content(outputText,'SUCCESS! Enjoy your susbtitle')
    else:
        show_content(outputText, 'Path is empty')

def translate_text():
    content = get_content(inputText)
    translator= Translator()
    show_content(outputText,translator.translate(content, dest=get_content(src_button)).text)
    
def translate_text(e):
    content = get_content(inputText)
    translator= Translator()
    show_content(outputText,translator.translate(content, dest=get_content(src_button)).text)
    

def clear():
    global opt
    clear_content(inputText)
    clear_content(outputText)
    if opt:
        show_content(src_button, 'vi')
        show_content(num_button, 300)
    inputText.focus_set()
    
def clear(e):
    global opt
    clear_content(inputText)
    clear_content(outputText)
    if opt:
        show_content(src_button, 'vi')
        show_content(num_button, 300)
    inputText.focus_set()
    
def swap_opt():
    global  opt
    if opt == 1:
        opt = 0
        opt_button.configure(text='Text')
        trans_button.configure(command=translate_text)
        inputBox.configure(text='Translate your text')
        
        clear_content(num_button)
        num_button.configure(state='disable')
        open_file_button.configure(state='disable')
    else:
        opt = 1
        opt_button.configure(text='File')
        trans_button.configure(command=translate_file)
        inputBox.configure(text='Translate your file')
        
        num_button.configure(state='normal')
        show_content(num_button,  300)
        open_file_button.configure(state='normal')
        
        
def change_theme():
    # NOTE: The theme's real name is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")
    

###################

root = tk.Tk()
root.geometry("500x150")
root.title("Translate subtitle")
root.attributes('-topmost', 'true')

root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")

#####
tool = tk.Frame(root, height=30, bd=0) 
tool.pack(fill='both')

opt_button = tk.Button(tool,text='Text',font=("ROBOTO", 10),command=swap_opt, borderwidth=0, cursor='hand2')

frame_src_button=tk.Frame(tool, height=25, width=100)
src_button = tk.Text(frame_src_button, font=("ROBOTO", 10), width=5, borderwidth=1, state='normal')
label_button= tk.Label(frame_src_button, text='To:',font=("ROBOTO", 10))


src_button.place(x=25,y=2)
label_button.place(x=0,y=0)

#init value
show_content(src_button, 'vi')


frame_num_button=tk.Frame(tool, height=25, width=80)
label_num_button= tk.Label(frame_num_button, text='Num:',font=("ROBOTO", 10))
num_button = tk.Text(frame_num_button, font=("ROBOTO", 10),width=4, borderwidth=1, state='disable')

label_num_button.place(x=0, y =0)
num_button.place(x=40,y=2)


trans_button = tk.Button(tool,text='Translate',font=("ROBOTO", 10),command=translate_text, borderwidth=0, cursor='hand2')
clear_button = tk.Button(tool,text='Reset', font=("ROBOTO", 10),command=clear, borderwidth=0, cursor='hand2', state='normal')
open_file_button = tk.Button(tool,text='Open', font=("ROBOTO", 10),command=open_file, borderwidth=0, cursor='hand2',state='disable')

switch_button = ttk.Checkbutton(tool,text="Dark mode", style="Switch.TCheckbutton", command=change_theme)
switch_button.place(x=370,y=2)


opt_button.place(x=10,y=5)
open_file_button.place(x=50, y=5)
trans_button.place(x=100, y=5)
clear_button.place(x=170,  y=5)

frame_src_button.place(x=220,y=6)
frame_num_button.place(x=290,y=6)


#######

content=tk.Frame(root)
content.pack(expand='True', fill='both')

content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)

content.rowconfigure(0, weight=1)

#inputFrame = tk.LabelFrame(root, background="#2C2E43")
inputBox = tk.LabelFrame(content, text='Translate your text',font=("ROBOTO", 10))
#inputBox.pack()
inputBox.columnconfigure(0, weight=1)
inputBox.rowconfigure(0, weight=1)

inputText = tk.Text(inputBox,font=("ROBOTO", 10), bd=0)
inputText.grid(column=0, row=0, padx=0, pady=0, sticky='NSEW')
inputBox.grid(column=0, row=0, padx=10, pady=10,sticky='NSEW')



outputBox = tk.LabelFrame(content, text='Result',font=("ROBOTO", 10))
#inputBox.pack()
outputBox.columnconfigure(0, weight=1)
outputBox.rowconfigure(0, weight=1)

outputText = tk.Text(outputBox,font=("ROBOTO", 10), bd=0)
outputText.grid(column=0, row=0, padx=0, pady=0, sticky='NSEW')
outputBox.grid(column=1, row=0, padx=10,pady=10, sticky='NSEW')



#init value
show_content(src_button, 'vi')
show_content(num_button, 300)

# short cut keyboar
root.bind('<Control-space>', translate_text)
root.bind('<Control-d>', clear)
root.mainloop()