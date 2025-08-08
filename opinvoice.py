from reportlab.lib.units import inch
from reportlab.platypus import Image
from datetime import date
import sqlite3
import pandas as pd

import time
import datetime
from database_sync import selectTable


start_time = time.time()


def getPatientDetails(UHId):
    

    rowsWithUHId = selectTable('vw_getOPdetails', condition=f"UHId = '{UHId}'" )
    
    print(rowsWithUHId)
    return rowsWithUHId[0]

def my_temp(c):
    # Set A5 size dimensions
    a5_width, a5_height = 5.8 * inch, 8.3 * inch
    c.translate(a5_width - 0.05 * inch, 0.05 * inch)  # Adjust origin to top-left corner
    
    # define a smaller font for A5
    c.setFont("Helvetica", 10)
    
    # Other adjustments...
    c.setStrokeColorRGB(0, 1, 0)
    c.setFillColorRGB(0,0,1)
    c.rotate(90)
    c.drawImage('Images\Logo.jpg',  3.55 * inch, 4.8 * inch, width=60, height=60)
    
    c.setFont("Helvetica", 20)
    c.drawString(0.2*inch, 5.4 * inch, "Dr Preethi's")
    c.setFont("Helvetica", 12)
    c.drawString(0.2*inch, 5.2 * inch, "Skin Hair and Laser Clinic")
    c.drawString(0.2*inch, 5.0 * inch, f'Dr. C Madhu Preethi')
    
    c.setFont("Helvetica", 8)
    c.drawString(0.2*inch, 4.85 * inch, "MBBS, MDDVL - Dermatologist and Cosmetologist")
    c.drawString(0.2*inch, 4.7 * inch, "#25-684-15, TTD Road, Doctor's Lane")     
    c.drawString(0.2*inch, 4.55 * inch, "Nandyal, 518501")
    #c.drawString(0.4 * inch, 4.6 * inch, f'Dermatologist and Cosmetologist')

    c.setFont("Helvetica", 10)
    c.setStrokeColorRGB(0, 1, 0)  # line colour
    c.line(0.2, 4.5 * inch, 8.0 * inch, 4.5 * inch)
    
    
    #dt = date.today().strftime('30-05-%Y')
    
    
    
    # Other adjustments...
    
    c.setFillColorRGB(1, 0, 0)  # font colour
    c.setFont("Times-Bold", 16)
    c.drawString(3.5 * inch, 4.6 * inch, 'INVOICE')

    
    # Other adjustments...
    
    # Set vertical line color
    c.setStrokeColorCMYK(0, 0, 0, 1)
    
    # Other adjustments...
    
    # Set horizontal line total
    global ProductLine
    #global RateLine
    #global QtyLine
    global AmtLine
    global billYLine
    global PcodeLine
    global BatchLine
    global ExpDateLine

    PcodeLine = 1.5
    #ProductLine = PcodeLine + 0.9
    #RateLine = ProductLine + 2
    #BatchLine = RateLine + 1
    #ExpDateLine = BatchLine + 0.8
    #QtyLine = ExpDateLine+0.7
    AmtLine = PcodeLine+4
    
    billYLine = 1.9
    
    c.setFont("Times-Bold", 12)
    c.line(0*inch, 4.5 *inch,0 * inch, billYLine * inch)
    c.drawString(0.2 * inch, 4.3 * inch, 'Id')
    c.line(PcodeLine * inch,4.5* inch, PcodeLine * inch, billYLine * inch)    
    c.drawString((PcodeLine+0.05) * inch, 4.3 * inch, 'Item') 
    
    c.line(AmtLine * inch,4.5* inch, AmtLine * inch, billYLine * inch)
    c.drawString((AmtLine+.05) * inch, 4.3 * inch, 'Amount')
    
    c.line(8.0*inch, 4.5 *inch, 8.0 * inch, billYLine * inch)
    c.line(0.2, 4.2 * inch, 8.0 * inch, 4.2 * inch)
    c.line(0*inch, billYLine * inch, 8.0 * inch, billYLine * inch)
    
    
    
    
    c.drawString(0.5 * inch, -5.5 * inch, 'Discount')
    c.drawString(0.5 * inch, -6.2 * inch, 'Tax')
    
   
    
    c.setFont("Times-Bold", 12)
    c.drawString(1 * inch, -6.7 * inch, 'Total')
    
    # Other adjustments...
    
    c.setFont("Times-Roman", 12)
    c.drawString(3.5 * inch, -7.3 * inch, 'Signature')
    
    #Bottom Line color
    c.setStrokeColorRGB(0.1, 0.8, 0.1)
    c.line(0, -7.8 * inch, 5.5 * inch, -7.8 * inch)
    
    c.setFont("Helvetica", 6)  # font size
    c.setFillColorRGB(1, 0, 0)  # font colour
    c.drawString(0, -8 * inch, u"\u00A9" + " plus2net.com")
    
    return c


from reportlab.pdfgen import canvas
#$UHId = "PM2403404"

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A5
#from temp_invoice import my_temp # import the template
#from invoice_data import *  # get all data required for invoice
def printBill(UHId):
    
    my_prod = getPatientDetails(UHId)

    #print(my_prod)
    if my_prod[2]:
        ptName = my_prod[2]
    else:
        ptName = "   "
    my_path=r'Invoices\OP\{}.pdf'.format(UHId + "_" + ptName) 
    c = canvas.Canvas(my_path,pagesize=A5)
    c=my_temp(c) # run the template
    
    #print(ProductLine, QtyLine, AmtLine, RateLine)
    c.setFillColorRGB(0,0,0) # font colour

    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 1)
    c.drawString(6.2 * inch, 5.0 * inch, f'Invoice No: {UHId}')
    row_gap=0.15 # gap between each row
    line_y=4.05 # location of fist Y position

    currAmount = str(my_prod[8])
    currSex = my_prod[4]
    currAge = str(my_prod[5])

    c.setFont("Helvetica", 8) 
    c.drawString(6.2 * inch, 4.85 * inch, f'To: {ptName}')
    c.drawString(6.2 * inch, 4.7 * inch, f'Sex: {currSex}')
    c.drawString(6.2 * inch, 4.55 * inch, f'Age: {currAge}')
    c.drawString((PcodeLine+0.05) * inch, line_y * inch, 'OP Consultation Fees') 
    c.drawString((AmtLine+.05) * inch, line_y * inch, f'{currAmount}')
        
    #date_object = datetime.datetime.strptime(my_prod[0][1], '%d/%m/%Y, %H:%M:%S')
    billDate = my_prod[1]
    c.setFont("Times-Bold", 10)
    c.setFillColorRGB(0,0,1)
    c.drawString(6.8 * inch, 5.25 * inch, billDate)
    c.setFillColorRGB(0,0,0)
    
    c.drawRightString((AmtLine -0.05)*inch, (billYLine-row_gap) * inch, 'Gross Amount: ')
    c.drawString((AmtLine+0.05)*inch,(billYLine-row_gap)*inch,currAmount) # Total
    c.drawRightString((AmtLine -0.05)*inch, (billYLine-row_gap*2) * inch, 'Discount: ')
    c.drawRightString((AmtLine -0.05)*inch, (billYLine-row_gap*3) * inch, 'Net Amount: ')
    c.drawString((AmtLine+0.05)*inch,(billYLine-row_gap*3)*inch,currAmount)
     
    c.setFont("Times-Bold", 22)
    c.setFillColorRGB(1,0,0) # font colour
   
    c.rotate(90)
    c.showPage()
    c.save()




UHId = '2501A026'
#ptName = 'Arshiya'
#billData = getPatientDetails(UHId)
printBill(UHId)

