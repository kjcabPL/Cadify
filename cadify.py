import math
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
from lib.converter import Converter

currencyOptions = ["CAD","PHP","USD","YEN","EUR","GBP"]
separator = ","
targetList = separator.join([item for item in currencyOptions])
conv = Converter("CAD",targetList)
baseText = f"1 CAD"
targetText = f"42 PHP"

labelFont1 = ("Arial", 20, "normal")

# build tkinter and components
main = tk.Tk()
main.title("Cadify")

grpFields = Frame(padx = 10, pady = 10)
grpButtons = Frame(padx = 10, pady = 10)

txtConv1 = Entry(grpFields, width = 15)
txtConv2 = Entry(grpFields, width = 15)

lblBase = Label(grpFields, text = baseText, width = 8, font = labelFont1)
lblTarget = Label(grpFields, text = targetText, width = 8, font = labelFont1)
lblEquals = Label(grpFields, text = "=", width = 1, font = labelFont1)

lbBase = Combobox(grpButtons, values = currencyOptions, state = "readonly", width = 13)
lbRates = Combobox(grpButtons, values = [val for val in conv.rates.keys()], state = "readonly", width = 13)
lblTo = Label(grpButtons, text = "TO", width = 5)
choices = [val for val in conv.rates.keys()]

# Arrange components and prep values
grpFields.grid(row = 0, column = 0, padx = 10, pady = 10)
grpButtons.grid(row = 1, column = 0, padx = 10, pady = 10)

txtConv1.grid(row = 0, column = 0, padx = 5, pady = 5 )
txtConv2.grid(row = 0, column = 2, padx = 5, pady = 5 )

lblBase.grid(row = 1, column = 0, padx = 5, pady = 5)
lblEquals.grid(row = 1, column = 1, padx = 10, pady = 5)
lblTarget.grid(row = 1, column = 2, padx = 5, pady = 5)

lbBase.grid(row = 1, column = 0, padx = 5, pady = 5)
lblTo.grid(row = 1, column = 1, padx = 10, pady = 5)
lbRates.grid(row = 1, column = 2, padx = 5, pady = 5)


txtConv1.insert(0, "1")
lbBase.set(currencyOptions[0])
if len(choices) > 0:
    lbRates.set(choices[0])
    txtConv2.insert(0, f"{conv.rates[choices[0]]:.2f}")

# Button Actions and Behavior

def doConversion(amount, targetRate, isReverse = False):
    return conv.convert(amount, targetRate, isReverse)

def onTBUpdate(event):
    global conv
    tbSrc = event.widget
    tbDest = txtConv2
    isReverse = False
    if tbSrc == txtConv2:
        tbDest = txtConv1
        isReverse = True
    text = tbSrc.get()
    try:
        amount = float(text)
        targetRate = lbRates.get()
        result = doConversion(amount, targetRate, isReverse)
        res = f"{result:.2f}"
        tbDest.delete(0, tk.END)
        tbDest.insert(0, res)
    except:
        pass

# Update value when target listbox value is changed
def onTargetSelected(event):
    val = txtConv1.get()
    try:
        amount = float(val)
        targetRate = lbRates.get()
        result = doConversion(amount, targetRate)
        updateUI(result, txtConv2)
    except:
        pass

# Update base and conversion
def onBaseSelected(event):
    newBase = lbBase.get()
    conv.updateFactors(newBase, targetList)
    currentTarget = lbRates.get()
    choices = [val for val in conv.rates.keys()]
    lbRates["values"] = choices
    if currentTarget in choices:
        lbRates.set(currentTarget)
    else:
        lbRates.set(choices[0])
    val = txtConv2.get()
    try:
        amount = float(val)
        targetRate = lbRates.get()
        result = doConversion(amount, targetRate)
        updateUI(result, txtConv1)
    except:
        pass

# update the UI data
def updateUI(result, tbTarget):
    baseRate = lbBase.get()
    targetRate = lbRates.get()

    rateText = conv.rates[targetRate]
    baseText = f"1 {baseRate}"
    targetText = f"{rateText:.2f} {targetRate}"
    lblBase["text"] = baseText
    lblTarget["text"] = targetText

    res = f"{result:.2f}"
    tbTarget.delete(0, tk.END)
    tbTarget.insert(0, res)

# Add actions to components
txtConv1.bind("<KeyRelease>", onTBUpdate)
txtConv2.bind("<KeyRelease>", onTBUpdate)

lbBase.bind("<<ComboboxSelected>>", onBaseSelected)
lbRates.bind("<<ComboboxSelected>>", onTargetSelected)

# Final Actions before running
updateUI(1, txtConv2)

# run main window
main.mainloop()

