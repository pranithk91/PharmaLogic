from customtkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
from database_sync import selectTable, runQuery
#from CTkScrollableDropdown import *
import pandas as pd
#from CTkTable import CTkTable
from time import strftime
#from new_client import ClientMainViewFrame
import ttkbootstrap as ttb
#from autocomplete import AutoComplete
import sqlite3
from datetime import date
from printinvoice import printBill

medData = selectTable('MedicineList', column_names="MId, MName,  CurrentStock, MType, MRP,  GST, Weight")
medicineDf=pd.DataFrame(medData, columns=['MId', 'MName',  'CurrentStock', 'MType', 'MRP',  'GST', 'Weight'])
medSuggestionList = [med[1] for med in medData]


class PriceUpdateFrame(ttk.Frame):
    def __init__(self, master=NONE):
        super().__init__(master,  width=1050, height=850, relief=tk.GROOVE)
        self.pack_propagate(0)
        self.grid(column=1, row=0, pady = (10,10), padx=(25,25))
        today = date.today().strftime("%Y-%m-%d")
       
        def clearBillTable():
            
            numRows = self.billTable.rows
            self.billTable.delete_rows(range(1,numRows))
            self.billTotalLabel.configure(text = "Bill Total: 0")
        
        # Title Section     
        padx_values = (35,35)
        gridPadding = 30
        self.titleFrame = ttk.Frame(master=self)
        self.titleFrame.pack(anchor="w", pady=(29, 0), padx=27)
        
        self.titleLabel = ttk.Label(master=self.titleFrame, text="New Bill", 
                                   font=("Calibri", 25, "bold"), style="success.TLabel" )
        self.titleLabel.grid(row=0, column=0, sticky="w", padx = padx_values)


        self.timeLabel = ttk.Label(master=self.titleFrame, font=("Calibri", 17, "bold"), style="success.TLabel" )
        self.timeLabel.grid(row=0, column=1, sticky="e",padx = (520,0))
        def get_time():
            string = strftime('%I:%M:%S %p')
            self.timeLabel.configure(text=string)
            self.timeLabel.after(1000, get_time)
        get_time()

        # Search Section
        self.searchGrid = ttk.Frame(master=self, bootstyle="default")
        self.searchGrid.pack(fill="both", padx=gridPadding, pady=(31, 0))

        self.itemNameLabel = ttk.Label(master=self.searchGrid, 
                                      text="Item Name", font=("Calibri", 15, "bold"), 
                                      style="success.TLabel")
        self.itemNameLabel.grid(row=0, column=0, sticky="w", padx = padx_values)

        self.itemNameLabel = ttk.Label(master=self.searchGrid, 
                                      text="Updated Price", font=("Calibri", 15, "bold"), 
                                      style="success.TLabel")
        self.itemNameLabel.grid(row=0, column=1, sticky="w", padx = padx_values)


        #Update Quantity Label on medicine option select
        def onMedNameSelect(event):
            global currentMedQty
            global currentMedPrice
            global currentMedType
            global currentMedId
            global currentMedWeight
            global currentMedName

            currentMedName = self.itemNameEntry.get()
            #print(medicineDf.loc[medicineDf["MName"] == currentMedName])
            currentMedQty = int(medicineDf.loc[medicineDf["MName"] == currentMedName]["CurrentStock"].iloc[0])
            currentMedPrice = float(medicineDf.loc[medicineDf["MName"] == currentMedName]["MRP"].iloc[0])
            currentMedType = str(medicineDf.loc[medicineDf["MName"] == currentMedName]["MType"].iloc[0])
            currentMedWeight = str(medicineDf.loc[medicineDf["MName"] == currentMedName]["Weight"].iloc[0])
            currentMedId = str(medicineDf.loc[medicineDf["MName"] == currentMedName]["MId"].iloc[0])
            
            
            self.qtyInStockLabel.configure(text="Quantity in Stock:"+ str(currentMedQty))  
            self.currentPriceLabel.configure(text="Current Price:"+ str(currentMedPrice))
            self.currentWeightLabel.configure(text="Current Price:"+ str(currentMedWeight)) 
            self.currentTypeLabel.configure(text="Type: " + currentMedType )
        
        def autofillMeds(event):
            currChar = self.itemNameEntry.get()
            updatedList=[med for med in medSuggestionList if med.lower().startswith(currChar.lower())]
            self.itemNameEntry.configure(values=updatedList)

        style = ttk.Style()
        style.configure(
            "success.TButton",
            font=("Helvetica", 14),  # Set a larger font size
        )

        def priceUpdate():
            updatedPrice = self.updatedPriceEntry.get()
            query = f'Update MedicineList Set MRP = {updatedPrice}'
            condition = f"MId = '{currentMedId}' and MName = '{currentMedName}'"
            runQuery(query, condition)

            self.itemNameEntry.set("")
            self.updatedPriceEntry.delete(0,END)
            
        
        #style.configure("custom.TCombobox", font=("Helvetica", 18))

        self.itemNameEntry = ttk.Combobox(master=self.searchGrid, values=medSuggestionList,
                                          style='success.TCombobox',
                                          justify=LEFT, 
                                          font=("calibri", 12, "bold"), 
                                             cursor='hand2')
        self.itemNameEntry.grid(row=1, column=0, sticky='w', padx = padx_values)

        self.itemNameEntry.bind('<<ComboboxSelected>>', onMedNameSelect)
        self.itemNameEntry.bind("<KeyRelease>", autofillMeds)

        self.updatedPriceEntry = ttk.Entry(master=self.searchGrid, #placeholder_text=0,
                                       style="success.TEntry", font=("Arial Black", 16),
                                       width=5
                                        )
        self.updatedPriceEntry.grid(row=1, column=1, sticky='w', padx = padx_values)


        self.currentTypeLabel = ttk.Label(master=self.searchGrid, text = "Quantity in Stock: 0",
                                        font=("Calibri", 15, "bold"), 
                                        style="success.TLabel",
                                        )
        self.currentTypeLabel.grid(row=2, column=0, sticky="w", padx = padx_values, pady=30)
        
        self.qtyInStockLabel = ttk.Label(master=self.searchGrid, text = "Quantity in Stock: 0",
                                        font=("Calibri", 15, "bold"), 
                                        style="success.TLabel",
                                        )
        self.qtyInStockLabel.grid(row=2, column=1, sticky="w", padx = padx_values, pady=30)

        self.currentPriceLabel = ttk.Label(master=self.searchGrid, text = "Current Price: 0",
                                        font=("Calibri", 15, "bold"), 
                                        style="success.TLabel",
                                        )
        
        self.currentPriceLabel.grid(row=2, column=2, sticky="w", padx = padx_values, pady=30)
        
        self.currentWeightLabel = ttk.Label(master=self.searchGrid, text = "Current Weight: 0",
                                        font=("Calibri", 15, "bold"), 
                                        style="success.TLabel",
                                        )
        
        self.currentWeightLabel.grid(row=2, column=3, sticky="w", padx = padx_values, pady=30)
        
        
        

        self.confirmPriceUpdateButton = ttk.Button(master=self.searchGrid, text="Confirm New Price", 
                                            width=15, style="success.TButton",
                                            command=priceUpdate
                                            )
        self.confirmPriceUpdateButton.grid(row=1, column=3, sticky="w", padx = padx_values, pady=30)


if __name__ == "__main__":
    app = tk.Tk()
    PriceUpdateFrame(app)
    app.mainloop()
