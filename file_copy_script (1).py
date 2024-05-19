import os
import shutil
from tkinter import Tk, Label, Button, ttk, messagebox, StringVar
from tkinter import *


"""
List all Files in directory
===========================
"""
def get_filenames(directory):

  return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

"""-------------------------------------------------------------------------------------------------------------------
"""

"""
Copies all files from the source directory to the destination directory with progress bar update.
=================================================================================================
"""

def copy_all_files():

  total_files = len(os.listdir(source_dir)) 
  copied_files = 0
  for filename in os.listdir(source_dir):
    if os.path.isfile(os.path.join(source_dir, filename)):  
      source_path = os.path.join(source_dir, filename)
      dest_path = os.path.join(destination_dir, filename)
      try:
        
        copy_file_with_progress(source_path, dest_path, progress_bar, total_files, copied_files)
        copied_files += 1
      except Exception as e:
        print(f"Error copying file: {filename} - {e}")
  messagebox.showinfo("Success", f"Copied {copied_files} files out of {total_files}.")

"""
Handles the click event for the copy button.
============================================
"""  
def copy_file_button_click():

  source = os.path.join(source_dir, selected_file_var.get())

  if not source:
    print("Error: Please select a source file.")
    return
  if not destination_dir:
    print("Error: Destination directory not set.")
    return

  filename = os.path.basename(source)
  dest_path = os.path.join(destination_dir, filename)

  copy_file_with_progress(source, dest_path, progress_bar,1,1)
  update_file_list_list()

"""
Copies a file from source to destination with progress bar update.
===================================================================
"""  
def copy_file_with_progress(source, destination, progress_bar,total_files, copied_files):
  
  try:
    total_size = os.path.getsize(source)

    copied_size = 0
    with open(source, 'rb') as src, open(destination, 'wb') as dst:
      while True:

        chunk = src.read(1024)
        if not chunk:
          break
        dst.write(chunk)
        copied_size += len(chunk)
        percentage = int((copied_size / total_size) * 100)
        progress_bar['value'] = int((copied_files / total_files) * 100) + percentage  
        progress_caption.config(text=f"Copying: {percentage}% ({total_size} B)") 
        if copied_size % 10240 == 0:  
          root.update()  

    print(f"File copied: {source} -> {destination}")
  except Exception as e:
    print(f"Error copying file: {e}")
    messagebox.showerror("Error", f"Error copying file: {e}") 

"""-------------------------------------------------------------------------------------------------------------------
"""
def find_string_and_next_value( ):
  """
  Find output result of tested files
  """
  try:
    selected_index = dest_list.curselection()
    selected_file = dest_list.get(selected_index[0])
    search_string = f"{selected_file},"
    existvalue=0
    get_selected_file()
    with open(decision_file_path, 'r') as f:
      lines = f.readlines()
      for line in lines:
        if search_string in line:
          tokens = line.split()
          result=tokens[0]
          
          if result[-1]=="1":
            Result_value.config(text=f"{selected_file} is Normal",fg="green")
            existvalue=1
          if result[-1]=="0":
            Result_value.config(text=f"{selected_file} is Suspicious",fg="red")
            existvalue=2
          if len(tokens) > 1: 
            
            return tokens[1]  
      if existvalue==0:
          messagebox.showinfo("Warrning", f"File Not Exist ")  
          Result_value.config(text=f"Selected file: Not Exist",fg="red",bg="blue")
      if lines==-1:
          messagebox.showinfo("Find", "File is not exist")
  except Exception as e:
    print(f"Error reading file: {e}")
  return None


# Update list of test files in combo   
#========================================================================================  
def update_file_list():

  global file_combo, source_dir
  files = get_filenames(source_dir)
  file_combo['values'] = files
  update_selected_file_label(None)  
  
# Update list of test files in listbox   
#========================================================================================    
def update_file_list_list():
  """
  Updates the combo box with filenames from the source directory.
  """
  global dest_list
  dest_list.delete(0, END)
  files = get_filenames(destination_dir)
  for file1 in files:
    dest_list.insert(0,file1)
  

# Update caption of selected file from list  
#========================================================================================  
def update_selected_file_label(event):
  
  selected_file = selected_file_var.get()
  if selected_file:  
    progress_caption.config(text=f"You will copy: {os.path.basename(selected_file)}")

  else:
    progress_caption.config(text="")  # Clear label if no file selected

# Run train script  
#========================================================================================  
def run_script_button_click():
  
  try:
    with open(output_file_path, 'w') as output_file:
      output = os.popen(script_path).read()
      output_file.write(output)
      print(f"Script execution successful. Output saved to: {output_file_path}")
  except Exception as e:
    print(f"Error running script: {e}")
    
    
# Delete a seected file from list 
#========================================================================================  

def delete_selected_file():
  """
  Deletes the selected file from the destination directory and listbox.
  """
  selected_index = dest_list.curselection()
  if selected_index:
    selected_file = dest_list.get(selected_index[0])  
    file_path = os.path.join(destination_dir, selected_file)  

    try:
      os.remove(file_path)  # Delete file
      update_file_list_list()  # Update listbox after deletion
      messagebox.showinfo("Success", "File deleted successfully!")
    except Exception as e:
      print(f"Error deleting file: {e}")
      messagebox.showerror("Error", f"Error deleting file: {e}")  
  else:
    messagebox.showinfo("Attention", "Please select a file to delete.")

# Clear listbox  from all files (delete all) 
#========================================================================================  

def clear_destination_list():

  confirmation = messagebox.askquestion("Confirm", "Are you sure you want to clear all files?")
  if confirmation == 'yes':
    for filename in dest_list.get(0, END): 
      file_path = os.path.join(destination_dir, filename)
      try:
        os.remove(file_path)  # Delete file
      except Exception as e:
        print(f"Error deleting file: {e}")
        messagebox.showerror("Error", f"Error deleting file: {e}")  
    update_file_list_list()  
    messagebox.showinfo("Success", "All files deleted successfully!")

# Retrive selecteed files name from list  
#========================================================================================  
def get_selected_file():

  selected_index = dest_list.curselection()
  if selected_index:
    selected_index = selected_index[0] 

    selected_file = dest_list.get(selected_index)
    
    print(f"Selected file: {selected_file}")
  else:
    print("No file selected.")
    
# Create the main window
root = Tk()
root.geometry('1000x800') # x -y
root.title("Demo Presentation for project")
root.config(bg="white") 

# All reqired paths 
source_dir = "/Users/Omar/Desktop/dcase2023_task2_baseline_ae/Temp/test"
destination_dir = "/Users/Omar/Desktop/dcase2023_task2_baseline_ae/data/dcase2023t2/dev_data/raw/bearing/test/"


script_path = "/Users/Omar/Desktop/dcase2023_task2_baseline_ae/02a_test.sh"
output_file_path = "/Users/Omar/Desktop/dcase2023_task2_baseline_ae/script_output.txt"
decision_file_path = "/Users/Omar/Desktop/dcase2023_task2_baseline_ae/results/dev_data/baseline_MAHALA/decision_result_DCASE2023T2bearing_section_00_test_seed13711_id(0_).csv"

selected_file=""
#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
font = ('Arial', 12) 
#--------------------------------------------------------------------------------------

combo_caption = Label(root, text="Select test sound file:")
combo_caption.pack(padx=15,pady=15)
combo_caption.configure(font=font)
combo_caption.place(x=50, y=30)


selected_file_var = StringVar(root) 
file_combo = ttk.Combobox(root, textvariable=selected_file_var, state='readonly', width=60)
file_combo.pack()
file_combo.place(x=50, y=70)
file_combo.bind("<<ComboboxSelected>>", update_selected_file_label)

# Labels
progress_caption = Label(root, text="Selected File:")
progress_caption.pack(side = TOP,padx=15,pady=15)
progress_caption.place(x=100, y=100)
# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=300)
progress_bar.pack()
progress_bar.place(x=100, y=140)


list_caption = Label(root, text="Data Set test files:")
list_caption.pack(padx=15,pady=15)
list_caption.place(x=100, y=200)

dest_list = Listbox(root,width=60,height=30,bg="black",bd=2)
dest_list.pack(padx=15,pady=15)
dest_list.place(x=100, y=240)




exit_button = Button(root, text="Exit", command=root.destroy, compound=TOP,padx=0, pady=0,  width=25,height=2, fg="red")
exit_button.pack( )
exit_button.place(x=700, y=30)



run_script_button = Button(root, text="Run test script", command=run_script_button_click, width=25, heigh=2, fg="blue")
run_script_button.pack( padx=15)
run_script_button.place(x=280, y=200)

copy_button = Button(root, text="Copy File", command=copy_file_button_click, width=10, heigh=2, fg="green")
copy_button.pack(padx=15)
copy_button.place(x=350, y=20)

delete_button = Button(root, text="Delete Selected", command=delete_selected_file, width=15, heigh=2, fg="green")
delete_button.pack(padx=15,pady=15)  
delete_button.place(x=750, y=240)

clear_button = Button(root, text="Clear All", command=clear_destination_list, width=15, heigh=2, fg="green")
clear_button.pack(padx=15,pady=15)  
clear_button.place(x=750, y=340)

copyall_button = Button(root, text="Copy All", command=copy_all_files, width=15, heigh=2, fg="green")
copyall_button.pack(padx=15,pady=15)  
copyall_button.place(x=750, y=440)

readoutput_button = Button(root, text="Read Result File", command=find_string_and_next_value, width=15, heigh=2, fg="green")
readoutput_button.pack(padx=15,pady=15)  
readoutput_button.place(x=750, y=540)

Result_caption = Label(root, text="File Result of :",wraplength=300,width= 20, fg="blue",bg="yellow")
Result_caption.pack(padx=15,pady=15)
Result_caption.place(x=100, y=700)
font = ('Arial', 16)  
Result_caption.configure(font=font, justify="left")

Result_value = Label(root, text="Normal / Suspicious", wraplength=500,width= 60, fg="green")
Result_value.pack(padx=15,pady=15)
Result_value.place(x=300, y=700) 
Result_value.configure(font=font)
#==============================================================================================================

# Get Activity data list
update_file_list() # Combo list files (test file from temp folder)
update_file_list_list() # List files (test file from test folder)

# Run the main loop
# ************************************************************************************************************************8
root.mainloop()
# ************************************************************************************************************************8