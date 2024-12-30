from customtkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
from database import loadDatabase
from CTkScrollableDropdown import *
import pandas as pd
from CTkTable import CTkTable
from time import strftime
import ttkbootstrap as ttb
from autocomplete import AutoComplete
from database import selectTable

medDB = selectTable()

print(medDB)