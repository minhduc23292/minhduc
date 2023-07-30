from tkinter import messagebox
from i18n import _

def shutdown_info():
    messagebox.showinfo("", _("OS IS BEING SHUTDDWN"))

def company_project_dont_exist_warning( ):
    if(messagebox.askyesno("Question", _("Company name and project code dont exist. Do you want to continue ?"))):
        return True
    else:
        return False
def company_project_shutdown_warning( ):
    if(messagebox.askyesno("Question", _("Do you want shutdown the device?"))):
        return True
    else:
        return False
def company_project_exist_error():
    if messagebox.showerror("Error", _("This project code is existed, please type another code")):
        return True
    else:
        return False
def company_or_project_existed_warning():
    if(messagebox.askyesno("Question", _("Company existed and project code dont exist. Do you want to continue ?"))):
        return True
    else:
        return False
def company_project_existed_warning():
    if(messagebox.askyesno("Question", _("Company and project existed. Do you want to continue ?"))):
        return True
    else:
        return False

def general_warning(state):
    if messagebox.askyesno("Question", f"{state}"):
        return True
    else:
        return False

def empty_entry_error(fiel):
    if messagebox.showerror("Error", _("Please entry the ") + f" {fiel}"):
        return True
    else:
        return False
def show_error(fiel):
    if messagebox.showerror("Error", f"{fiel}"):
        return True
    else:
        return False
