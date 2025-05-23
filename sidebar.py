#from customtkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
#from database import loadDatabase, getClientid
from Pharmacy_view import pharmacyViewFrame
from new_client import ClientMainViewFrame
from new_sale import MainViewFrame
from price_update import PriceUpdateFrame
from returns import returnsViewFrame

import ttkbootstrap as tkb

 


class MedicineApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #self.pack_propagate(0)
        self.sidebarFrame=ttk.Frame(master,width=300, height=950, relief = tk.GROOVE)
        self.sidebarFrame.grid(column=0, row=0, padx=(25,0))
        #self.pack(fill="y", anchor="w", side="left")

        # Logo
        oImg = Image.open("Images/logo.jpg")
        res_img = oImg.resize((77, 85), Image.LANCZOS)
        
        img= ImageTk.PhotoImage(res_img)        
        self.logoLabel = ttk.Label(master=self.sidebarFrame,  image=img)
        self.logoLabel.pack(pady=(38, 0), anchor="center")
        
        # Buttons
        self.opButton = self.create_button("OP Register", "Images/plus_icon.png", command=self.client_frame)
        self.opButton.pack(anchor="center", ipady=5, pady=(16, 0),padx=(25,25) )
         
        self.ordersListButton = self.create_button("Pharmacy", "Images/list_icon.png", command=self.main_frame)
        self.ordersListButton.pack(anchor="center", ipady=5, pady=(16, 0),padx=(25,25) )

        self.viewSalesButton = self.create_button("View Sales", "Images/settings_icon.png", command=self.viewSale_frame) 
        self.viewSalesButton.pack(anchor="center", ipady=5, pady=(16, 0) ,padx=(25,25))

        self.returnsButton = self.create_button("Returns", "Images/returns_icon.png", command=self.returns_frame)
        self.returnsButton.pack(anchor="center", ipady=5, pady=(16, 0),padx=(25,25) )
        
        self.priceUpdateButton = self.create_button("Price Update", "Images/settings_icon.png", command=self.priceUpdate_frame) 
        self.priceUpdateButton.pack(anchor="center", ipady=5, pady=(16, 0) ,padx=(25,25))

        self.accountButton = self.create_button("Account", "Images/person_icon.png")
        self.accountButton.pack(anchor="center", ipady=5, pady=(160, 80),padx=(25,25) )

        #self.frames = 
        
        self.main_view = ClientMainViewFrame(master)


    def main_frame(self):

        self.main_view   = MainViewFrame(self.master)
        self.main_view.tkraise()

    def client_frame(self):

        self.main_view = ClientMainViewFrame(self.master)
        self.main_view.tkraise()

    def viewSale_frame(self):
        self.main_view = pharmacyViewFrame(self.master)
        self.main_view.tkraise()

    def priceUpdate_frame(self):
        self.main_view = PriceUpdateFrame(self.master)
        self.main_view.tkraise()

    def returns_frame(self):
        self.main_view = returnsViewFrame(self.master)
        self.main_view.tkraise()


    def create_button(self, text, image_filename,  command = None):
        img_data = Image.open(f"{image_filename}")
        img = ImageTk.PhotoImage(img_data)
        return ttk.Button(master=self.sidebarFrame, image=img, text=text, width=20,  style="success.TButton" , command = command)

    # Main View Frame
    



    @property
    def logoImg(self):
        oImg = Image.open("Images/logo.jpg")
        res_img = oImg.resize((77, 85), Image.ANTIALIAS)
        
        return ImageTk.PhotoImage(res_img)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('IMS 2024')
        self.geometry('1410x900')
        #self.resizable(False, False)


"""class SidebarFrame(tkb.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=176, height=650)
        self.pack_propagate(0)

        # Logo
        self.logoLabel = tkb.Label(master=self, text="", image=self.logoImg)
        self.logoLabel.pack(pady=(38, 0), anchor="center")

        # Buttons
        self.opButton = self.create_button("OP Register", "plus_icon.png")
        self.ordersButton = self.create_button("Procedures", "package_icon.png")
        self.ordersListButton = self.create_button("Pharmacy", "list_icon.png")
        self.returnsButton = self.create_button("Returns", "returns_icon.png")
        self.priceUpdateButton = self.create_button("Settings", "settings_icon.png")
        self.accountButton = self.create_button("Account", "person_icon.png", pady=(160, 0))





        #image = im = Image.open("/path/to/your/image.ext")
    def create_button(self, text, image_filename, pady=(16, 0)):
        img_data = Image.open(f"main_ttk/{image_filename}")
        img = ImageTk.PhotoImage(img_data)
        return tkb.Button(master=self, image=img, text=text,bootstyle="success").pack(anchor="center", ipady=5, pady=pady)

    @property
    def logoImg(self):
        logoImgData=Image.open("main_ttk/logo.png")
        img = ImageTk.PhotoImage(logoImgData, size=(77.68, 85.42))
        return img"""

if __name__ == "__main__":
    app = App()
    MedicineApp(app)
    app.mainloop()
