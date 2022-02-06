###########################################################
#######           CONTROL SYSTEMS SIMULATOR         #######
#######              SIMULATION TOOL GUI            #######
#######      EDUARDO VILLALOBOS UGALDE - B37571     #######
###########################################################

# Libraries.
import time as sp
from datetime import datetime
from PIL import ImageTk, Image
import numpy as np
from scipy import integrate
import control as co
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure

#################################################
#######       BASIC WINDOW SETTINGS       #######
#################################################
mainWindow = tk.Tk()
width= mainWindow.winfo_screenwidth() 
height= mainWindow.winfo_screenheight()
mainWindow.geometry("%dx%d" % (width, height))
mainWindow.title('Control Systems Simulator')

######################################################
#######      VARIABLES AND INITIAL VALUES      #######
######################################################

# Slider values
plantValue = tk.DoubleVar()
pValue = tk.DoubleVar()
iValue = tk.DoubleVar()
dValue = tk.DoubleVar()

# ReRun Prevention
changeP = False
changeI = False
changeD = False

# Sector A.
plantNum = tk.StringVar(mainWindow,'[1,2,3,...]')  # Hint text.
plantDen = tk.StringVar(mainWindow,'[1,2,3,...]')
deadTime = tk.DoubleVar()
contNum = tk.StringVar(mainWindow,'[1,2,3,...]')
contDen = tk.StringVar(mainWindow,'[1,2,3,...]')
eqP = tk.StringVar()
exp = tk.StringVar()
eqC = tk.StringVar()
eqP.set('');exp.set('');eqC.set('')  # No functions shown.
# Sector B.
simTime = tk.DoubleVar()
options = ('s', 'min', 'h')
opt = options[0]
timeUnits = tk.StringVar(value=opt)
inTime = tk.DoubleVar()
magS = tk.DoubleVar()
magR = tk.DoubleVar()
check = tk.IntVar()
checkType = tk.IntVar()
# Sector C.
graphics = tk.IntVar()
# Sector E.
position = tk.IntVar()

#################################################
#######            FUNCTIONS              #######
#################################################

#############################
## Menu/Hotkeys functions. ##
#############################
def close():
   mainWindow.quit()
   mainWindow.destroy()

def about(*args):
   aboutTitle = 'Control Systems Simulation Tool'
   aboutVersion = 'v3.0'
   aboutContent = """The Control Systems Simulator is an open-source tool designed for simulating closed-loop P, PI, PID controllers, the primary goal
of this tool is to help undergraduate students of the University of Costa Rica with a better understanding of control systems.
   
The Control Systems Simulator utilizes Python libraries to manage transfer functions and calculate the system response to step
and ramp inputs both in Servo-Control and Regulatory Control modes, while also calculating the IAE, ISE and ITAE performance
indexes, the control effort and the maximum sensitivity as a measure of robustness.

Developed by Eduardo Villalobos Ugalde.
Contact: eduardo.villalobosugalde@ucr.ac.cr
"""
   aboutW = tk.Toplevel(mainWindow)
   aboutW.geometry('900x290')
   aboutW.title('About')
   aboutW.resizable(False,False)
   aboutL1 = tk.Label(aboutW,text=aboutTitle,font=('Calibri',40))
   aboutL1.pack()
   aboutL2 = tk.Label(aboutW,text=aboutVersion,font=('Calibri',17))
   aboutL2.pack()
   aboutL3 = tk.Label(aboutW,text=aboutContent,font=('Calibri',11),justify=tk.LEFT)
   aboutL3.pack()

def help(*args):
   helpTitle = 'Welcome to the Control Systems Simulator User Guide'
   helpContent = """INTRODUCTION.

The simulation tool is divided into five main sections of data collection and display. These guide
describes the proper way to enter and retrieve data from the simulator. Do notice that every entry
used to collect numerical data works with real numbers and uses the decimal point as separator.

GENERAL DATA.

On this section both the Process model and the Controller Transfer Functions (TF) data are collec-
ted, as well as the dead time of the Process. It is required to enter the TF numerator and denomi-
nator coefficients using the format [a,b,c,...,n]. The coefficients "a,b,c,...,n" are real numbers
and "a" is the coefficient of the highest power of s, so "n" is the coefficient of s^0. The Process
dead time entered must be a positive value.

Below the "P(s) Transfer Function" label the Transfer Function of P(s) will be displayed. Also, the
controller Transfer Funtion will be displayed below the "C(s) Transfer Function" label. Lastly,there
are two "Reset Values" buttons: the one on the left resets all of the Process information, while the
one on the right resets the Controller information.

Finally, clicking on the question mark button will show you the closed loop configuration used for
this tool.

SIMULATION DATA.

On this section all the information necessary to compute the system response is collected. First, it
is necesary to select the type of input for the system: if the "Step" option is selected, the entry 
box called "Step magnitude" will be available to input the desired magnitude. On the other hand, if
the "Ramp" input is selected then the "Ramp slope" entry will be available for data entry. 

A positive value must be entered on the "Simulation time" box. On the "Time units" the user is able
to select among three different time units for the simulations: seconds, minutes and hours. There's
also a "Reset Values" button to restore to default values all the entry boxes of this section.

GRAPHICS.

On this section, the transfer function used for the simulations is determined. There are up to four
transfer functions to select from: the Reaction Curve P(s), Servo-Control (Myr), Regulatory Control 
(Myd) and both Myr and Myd control modes. If the "Reaction Curve" option is selected the response 
of P(s) to the desired input is simulated, if either the "Myr" or "Myd" option is selected both the
system response and the control signal response (ur or ud) to the desired input are simulated and if
the "Myr and Myd" option is selected the simulator will compute both Myr and Myd responses and both
control signal responses.

Finally, the "Run" button will begin the simulation and the "Reset ALL" button will reset to default
all the input data on the "General Data", "Simulation Data" and "Graphics" sections.

RESPONSE PARAMETERS

On this section the performance and robustness indicators computed for the system are shown. Those 
indicators are the following:

-IAE performance index.
-ISE performance index.
-ITAE performance index.
-Control effort, TVu.
-Maximum sensitivity, Ms.

SIMULATION RESULTS

This section contains all the plots generated with the computed system and control signal responses.
Depending on the option chosen in the "Graphics" section, the number of plots generated varies from 
only one plot (when the "Reaction Curve" option is chosen) and a maximum of four plots (when "both 
Myr and Myd" option is chosen). Each plot generated counts with a "View" button that shows the res-
pective plot on a new window and offers a more detailed view of the data. New options are available
for the figure on this new window, including: zoom, pan, save and more.
"""
   helpW = tk.Toplevel(mainWindow)
   helpW.geometry('935x900')
   helpW.title('Help')
   helpW.resizable(False,False)
   
   aboutH1 = tk.Label(helpW,text=helpTitle,font=('Calibri',30))
   aboutH1.grid(row=0,column=0,columnspan=2,ipadx=20)
   scrollbarH = tk.Scrollbar(helpW)
   scrollbarH.grid(row=1,column=1,sticky='ns')
   helpText = tk.Text(helpW,yscrollcommand=scrollbarH.set,height=40,width=100)
   helpText.grid(row=1,column=0,padx=28,pady=10)
   helpText.insert(tk.END,helpContent)
   helpText.configure(state='disabled')
   scrollbarH.config(command=helpText.yview)

##############################
## Widget-related functions ##
##############################
def get_current_value():
    return '{: .2f}'.format(current_value.get())

def pSlider_changed(event):
    changeP = True;
    
def iSlider_changed(event):
    changeI = True;
    
def dSlider_changed(event):
    changeD = True;
    
def plantSlider_changed(event):
    print("Cambio planta")

def checkRealtime(*args):
    realtimeExecute = True
    if(checkType.get() == 1):
        simulator()
    else:
        simulatorRealtime()
        # while(1):
            # simulatorRealtime()
            # # Rerun protection
            # if(changeP or changeI or changeD):
                # realtimeExecute = True
            # else:
                

def closedLoop():
   cl = tk.Toplevel(mainWindow)
   cl.title('Implemented Closed Loop')
   cl.resizable(False,False)

   panel = tk.Label(cl,image=new_image)
   panel.pack()
   
def pNumHintText(*args):
   pnumEntry.configure(fg='black')
   pnumEntry.delete(0,'end')
   pnumEntry.unbind('<Button-1>',pnumBind)

def pDenHintText(*args):
   pdenEntry.configure(fg='black')
   pdenEntry.delete(0,'end')
   pdenEntry.unbind('<Button-1>',pdenBind)

def delayHintText(*args):
   plantDelay.configure(fg='black')
   plantDelay.delete(0,'end')
   plantDelay.unbind('<Button-1>',delayBind)

def cNumHintText(*args):
   cnumEntry.configure(fg='black')
   cnumEntry.delete(0,'end')
   cnumEntry.unbind('<Button-1>',cnumBind)

def cDenHintText(*args):
   cdenEntry.configure(fg='black')
   cdenEntry.delete(0,'end')
   cdenEntry.unbind('<Button-1>',cdenBind)

def intimeHintText(*args):
   tinEntry.configure(fg='black')
   tinEntry.delete(0,'end')
   tinEntry.unbind('<Button-1>',tinBind)

def timeHintText(*args):
   timeEntry.configure(fg='black')
   timeEntry.delete(0,'end')
   timeEntry.unbind('<Button-1>',timeBind)

def stepHintText(*args):
   stepEntry.configure(fg='black')
   stepEntry.delete(0,'end')
   stepEntry.unbind('<Button-1>',stepBind)

def rampHintText(*args):
   rampEntry.configure(fg='black')
   rampEntry.delete(0,'end')
   rampEntry.unbind('<Button-1>',rampBind)

def stepOptionLock(*args):
   stepEntry.configure(state='normal')
   rampEntry.configure(state='disabled') 

def rampOptionLock(*args):
   stepEntry.configure(state='disabled')
   rampEntry.configure(state='normal') 

def resetProcess():
   pResetButton.focus()
   pnumEntry.delete(0,'end')
   pdenEntry.delete(0,'end')
   plantDelay.delete(0,'end')
   exp.set('')
   eqP.set('')

def resetController():
   cResetButton.focus()
   cnumEntry.delete(0,'end')
   cdenEntry.delete(0,'end')
   eqC.set('')

def resetInputs():
   inputResetButton.focus()
   timeUnits.set(options[0])
   tinEntry.delete(0,'end')
   timeEntry.delete(0,'end')
   stepEntry.configure(state='normal')
   stepEntry.delete(0,'end')
   rampEntry.configure(state='normal')
   rampEntry.delete(0,'end')
   stepOption.select()
   stepEntry.configure(state='normal')
   rampEntry.configure(state='disabled')

def masterReset(*args):
   allResetButton.focus()
   pnumEntry.delete(0,'end');pdenEntry.delete(0,'end')
   cnumEntry.delete(0,'end');cdenEntry.delete(0,'end')
   plantDelay.delete(0,'end');timeEntry.delete(0,'end')
   tinEntry.delete(0,'end');timeUnits.set(options[0])
   stepEntry.configure(state='normal');stepEntry.delete(0,'end')
   rampEntry.configure(state='normal');rampEntry.delete(0,'end')
   stepEntry.configure(state='normal')
   rampEntry.configure(state='disabled')
   stepOption.select();servoOption.select()
   exp.set('');eqP.set('');eqC.set('')
   param.configure(state='normal')
   param.delete(1.0,'end')
   param.insert('end','')
   param.configure(state='disabled')
   buttonNW.pack_forget();buttonNE.pack_forget()
   buttonSW.pack_forget();buttonSE.pack_forget()
   canvas1.get_tk_widget().pack_forget()
   canvas2.get_tk_widget().pack_forget()
   canvas3.get_tk_widget().pack_forget()
   canvas4.get_tk_widget().pack_forget()

def masterButton():
   axI.clear();axII.clear();axIII.clear();axIV.clear()
   # Shortened version of simulator code.
   units = timeUnits.get()
   time = simTime.get()
   t = np.linspace(0,time,5001)
   magStep = magS.get()
   magRamp = magR.get()
   timeIn = inTime.get()
   state = check.get()
   if state == 1: In = 'step'
   else: In = 'ramp'
   transfer = graphics.get()
   if transfer == 1: mode = 'servo'
   elif transfer == 2: mode = 'reg'
   elif transfer == 3: mode = 'both'
   else: mode = 'process'
   numeratorP = plantNum.get()
   numP = conversion(numeratorP)
   denominatorP = plantDen.get()
   denP = conversion(denominatorP)
   A = co.tf(numP,denP)
   dT = deadTime.get()
   L = float(dT)
   numPade,denPade = co.pade(L,n=10)
   Pade = co.tf(numPade,denPade)
   P = A*Pade
   if mode == 'process':
      if In == 'step':
         tP,yP,inP = response(P,magStep,timeIn,t,In)
      elif In == 'ramp':
         tP,yP,inP = response(P,magRamp,timeIn,t,In) 
      axI.plot(tP,inP,':m',label='r(t)')
      axI.plot(tP,yP,'-b',label='y(t)');axI.legend()
      axI.set_xlabel('Time ({})'.format(units));axI.set_ylabel('Amplitude')
   else:
      numeratorC = contNum.get()
      numC = conversion(numeratorC)
      denominatorC = contDen.get()
      denC = conversion(denominatorC)
      C = co.tf(numC,denC)
      MYR = (C*P)/(1+C*P)
      MYD = P/(1+C*P)
      UR = C/(1+C*P)
      UD = (-C*P)/(1+C*P)
      if mode == 'servo':
         if In == 'step':
            tServo,yServo,inServo = response(MYR,magStep,timeIn,t,In)
            tUR,yUR,inUR = response(UR,magStep,timeIn,t,In)
         elif In == 'ramp':
            tServo,yServo,inServo = response(MYR,magRamp,timeIn,t,In)
            tUR,yUR,inUR = response(UR,magRamp,timeIn,t,In)
         axI.plot(tServo,inServo,':m',label='r(t)')
         axI.plot(tServo,yServo,'-b',label='yr(t)');axI.legend()
         axI.set_xlabel('Time ({})'.format(units));axI.set_ylabel('Amplitude')
         axII.plot(tServo,inServo,':m',label='r(t)')
         axII.plot(tUR,yUR,'-b',label='ur(t)');axII.legend()
         axII.set_xlabel('Time ({})'.format(units));axII.set_ylabel('Amplitude')
      elif mode == 'reg':
         if In == 'step':
            tReg,yReg,inReg = response(MYD,magStep,timeIn,t,In)
            tUD,yUD,inUD = response(UD,magStep,timeIn,t,In)
         elif In == 'ramp':
            tReg,yReg,inReg = response(MYD,magRamp,timeIn,t,In)
            tUD,yUD,inUD = response(UD,magRamp,timeIn,t,In)
         axI.plot(tReg,inReg,':m',label='d(t)')
         axI.plot(tReg,yReg,'-b',label='yd(t)');axI.legend()
         axI.set_xlabel('Time ({})'.format(units));axI.set_ylabel('Amplitude')
         axII.plot(tReg,inReg,':m',label='d(t)')
         axII.plot(tUD,yUD,'-b',label='ud(t)');axII.legend()
         axII.set_xlabel('Time ({})'.format(units));axII.set_ylabel('Amplitude')
      elif mode == 'both':
         if In == 'step':
            tServo,yServo,inServo = response(MYR,magStep,timeIn,t,In)
            tUR,yUR,inUR = response(UR,magStep,timeIn,t,In)
            tReg,yReg,inReg = response(MYD,magStep,timeIn,t,In)
            tUD,yUD,inUD = response(UD,magStep,timeIn,t,In)
         elif In == 'ramp':
            tServo,yServo,inServo = response(MYR,magRamp,timeIn,t,In)
            tUR,yUR,inUR = response(UR,magRamp,timeIn,t,In)
            tReg,yReg,inReg = response(MYD,magRamp,timeIn,t,In)
            tUD,yUD,inUD = response(UD,magRamp,timeIn,t,In)
         axI.plot(tServo,inServo,':m',label='r(t)')
         axI.plot(tServo,yServo,'-b',label='yr(t)');axI.legend()
         axI.set_xlabel('Time ({})'.format(units));axI.set_ylabel('Amplitude')
         axII.plot(tServo,inServo,':m',label='r(t)')
         axII.plot(tUR,yUR,'-b',label='ur(t)');axII.legend()
         axII.set_xlabel('Time ({})'.format(units));axII.set_ylabel('Amplitude')
         axIII.plot(tServo,inServo,':m',label='d(t)')
         axIII.plot(tReg,yReg,'-b',label='yd(t)');axIII.legend()
         axIII.set_xlabel('Time ({})'.format(units));axIII.set_ylabel('Amplitude')
         axIV.plot(tServo,inServo,':m',label='d(t)')
         axIV.plot(tUD,yUD,'-b',label='ud(t)');axIV.legend()
         axIV.set_xlabel('Time ({})'.format(units));axIV.set_ylabel('Amplitude')
   var = position.get()
   if var == 1: F = figI
   elif var == 2: F = figII
   elif var == 3: F = figIII
   else: F = figIV

   # Pop-up window.
   figWindow1 = tk.Toplevel(mainWindow)
   figWindow1.geometry('700x550')
   figWindow1.resizable(False,False)
   canvasI = FigureCanvasTkAgg(F,master=figWindow1)
   canvasI.get_tk_widget()
   toolbarI = NavigationToolbar2Tk(canvasI,figWindow1)
   toolbarI.update()
   canvasI.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

def figViewNW():
   position.set(1)
   masterButton()

def figViewNE():
   position.set(2)
   masterButton()

def figViewSW():
   position.set(3)
   masterButton()

def figViewSE():
   position.set(4)
   masterButton()

###############################
## Simulator core functions. ##
###############################
def conversion(input): 
   # Converts the input from string to a float array.
   # Returns: final float array.
   input = str(input)
   caracters = "[]"
   string = input.replace(caracters[0],"").replace(caracters[1],"")  # Remove '[]' from string.
   list = string.split(',')  # List created from the string. String-type values.
   final = [float(x) for x in list]  # List of floats created using the first list.
   return final

def response(tf,ku,tin,time,signal):
   # Computes the desired step or ramp input of magnitude ku and applied on t=tin.
    # Computes the system response to the desired input.
    # Returns: ta,ya,ua: time and response values and the input computed.
    # Returns: None
    ntp = len(time)
    u = np.zeros(ntp)
    if signal == 'step':
    # Step with amplitude ku applied on t=tin.
        for k in range(ntp):
            u[k] = 0. if time[k] < tin else ku
        ta,ya = co.forced_response (tf,time,u)
    elif signal == 'ramp':
        # Ramp with slope ku aaplied on t=tin.
        for k in range(ntp):
            u[k] = 0. if time[k] < tin else ku*time[k]
        ta,ya = co.forced_response (tf,time,u)
    return ta,ya,u

def indexes(FT,inputName,yinput,y,t,ua):
   # Computes de IAE, ISE and ITAE of a given system response.
   # Also computes de control effort TVu of a given control signal.
   # Returns: None
   if FT == 'MYD': error = -y
   else: error = yinput-y
   iae = integrate.trapezoid(np.abs(error),t)
   ise = integrate.trapezoid(error**2,t)
   itae = integrate.trapezoid(np.abs(error)*t,t)
   if FT != 'P': TV = np.sum(np.abs(np.diff(ua)));TV = round(TV,7)
   iae = round(iae,7);ise = round(ise,7);itae = round(itae,7)
   inputName = str(inputName).upper()

   if FT == 'MYR': 
     C = """SERVO CONTROL
{} INPUT""".format(inputName)
     T = 'TVur'
   elif FT == 'MYD':
     C = """REGULATORY CONTROL
{} INPUT""".format(inputName)
     T = 'TVud'
   else:
     C = 'REACTION CURVE'
   if FT != 'P':
      TV = np.sum(np.abs(np.diff(ua)))
      TV = round(TV,7)
      results = """
{}

{} = {}
IAE = {}
ISE = {}
ITAE = {}
""".format(C,T,TV,iae,ise,itae)
   else:
      results = """
{}
""".format(C)

   param.configure(state='normal')
   param.insert(tk.END,results)
   param.configure(state='disabled')

def graph(etq,uin,t1,y1,t2=0,y2=0,t3=0,y3=0,t4=0,y4=0):
   # Plots the system simulations using Matplotlib.
   # Automatically sets the corresponding labels according to the control mode used.
   # Plots the system response (or reaction curve) and control signals in separate Figures.
   # Returns: None      
   if etq == 'Process':
      lab1 = 'y(t)'; labIn1 = 'r(t)'
      ax1.plot(t1,uin,':m',label=labIn1)
      ax1.plot(t1,y1,'-b',label=lab1)
      ax1.legend()
      canvas1.draw();canvas1.get_tk_widget().pack(padx=15)
      buttonNW.pack(side=tk.BOTTOM)
   elif etq == 'both': 
      lab1 = 'yr(t)'; lab2 = 'ur(t)'
      lab3 = 'yd(t)'; lab4 = 'ud(t)'
      labIn1 = 'r(t)'; labIn2 = 'd(t)'
      ax1.plot(t1,uin,':m',label=labIn1)
      ax1.plot(t1,y1,'-b',label=lab1);ax1.legend()
      ax2.plot(t1,uin,':m',label=labIn1)
      ax2.plot(t2,y2,'-b',label=lab2);ax2.legend()
      ax3.plot(t1,uin,':m',label=labIn2)
      ax3.plot(t3,y3,'-b',label=lab3);ax3.legend()
      ax4.plot(t1,uin,':m',label=labIn2)
      ax4.plot(t4,y4,'-b',label=lab4);ax4.legend()
      canvas1.draw();canvas1.get_tk_widget().pack(padx=15)
      canvas2.draw();canvas2.get_tk_widget().pack()
      canvas3.draw();canvas3.get_tk_widget().pack(padx=15)
      canvas4.draw();canvas4.get_tk_widget().pack()
      buttonNW.pack(side=tk.BOTTOM);buttonNE.pack(side=tk.BOTTOM)
      buttonSW.pack(side=tk.BOTTOM);buttonSE.pack(side=tk.BOTTOM)
   else: 
      if etq == 'servo': lab1='yr(t)';lab2='ur(t)';labIn1='r(t)'
      else: lab1='yd(t)';lab2='ud(t)';labIn1='d(t)'
      ax1.plot(t1,uin,':m',label=labIn1)
      ax1.plot(t1,y1,'-b',label=lab1);ax1.legend()
      ax2.plot(t1,uin,':m',label=labIn1)
      ax2.plot(t2,y2,'-b',label=lab2);ax2.legend()
      canvas1.draw();canvas1.get_tk_widget().pack(padx=15)
      canvas2.draw();canvas2.get_tk_widget().pack()
      buttonNW.pack(side=tk.BOTTOM);buttonNE.pack(side=tk.BOTTOM)

def simulator(*args):
   # GUI settings.
   runButton.focus()
   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # dd/mm/YY H:M:S
   param.configure(state='normal')
   param.insert(tk.END,'\n'+dt_string)
   param.configure(state='disabled')
   ax1.clear();ax2.clear();ax3.clear();ax4.clear()
   buttonNW.pack_forget();buttonNE.pack_forget()
   buttonSW.pack_forget();buttonSE.pack_forget()
   canvas1.get_tk_widget().pack_forget();canvas2.get_tk_widget().pack_forget()
   canvas3.get_tk_widget().pack_forget();canvas4.get_tk_widget().pack_forget()

   # Simulation time.
   try:
      time = simTime.get()
      t = np.linspace(0,time,5001)
   except tkinter.TclError:
      timeEntry.focus()
      tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid simulation time value.
Please enter valid numerical data.""")
   
   # Step magnitude.
   try:
      magStep = magS.get()
   except tkinter.TclError:
      stepEntry.focus()
      tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid step input value.
Please enter valid numerical data.""")
   
   # Ramp magnitude.
   try:
      magRamp = magR.get()
   except tkinter.TclError:
      rampEntry.focus()
      tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid ramp slope value.
Please enter valid numerical data.""")
   
   # Input time.
   try:
      timeIn = inTime.get()
   except tkinter.TclError:
      tinEntry.focus()
      tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid input time value.
Please enter valid numerical data.""")

   # Input selection.
   state = check.get()
   if state == 1: In = 'step'
   else: In = 'ramp'

   # Control mode selection.
   transfer = graphics.get()
   if transfer == 1: mode = 'servo'
   elif transfer == 2: mode = 'reg'
   elif transfer == 3: mode = 'both'
   else: mode = 'process'

   # Process data.
   try:
      numeratorP = plantNum.get()
      numP = conversion(numeratorP)
   except ValueError:
      pnumEntry.focus()
      tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid P(s) numerator values.
Please enter valid numerical data using the format [a,b,c].""")

   try:
      denominatorP = plantDen.get()
      denP = conversion(denominatorP)
      A = co.tf(numP,denP)
   except ValueError:
      pdenEntry.focus()
      tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid P(s) denominator values.
Please enter valid numerical data using the format [a,b,c].""")
   
   try:
      dT = deadTime.get()
      L = float(dT)
      numPade,denPade = co.pade(L,n=10)
      Pade = co.tf(numPade,denPade)
      P = A*Pade
   except tkinter.TclError:
      plantDelay.focus()
      tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid dead time value.
Please enter valid numerical data.""")
   eqP.set(str(A))
   if L == 0: exp.set('*e^0')
   else: exp.set('*e^-{} s'.format(dT))
   
   if mode == 'process':
      lab = 'Process'
      if In == 'step':
         tP,yP,inP = response(P,magStep,timeIn,t,In)
         indexes('P',In,inP,yP,tP,0)
         graph(lab,inP,tP,yP)
      elif In == 'ramp':
         tP,yP,inP = response(P,magRamp,timeIn,t,In)
         indexes('P',In,inP,yP,tP,0)
         graph(lab,inP,tP,yP)
      ending = '------------------------------'
   
   else:
      # Controller data.
      try:
         numeratorC = contNum.get()
         numC = conversion(numeratorC)
      except ValueError:
         cnumEntry.focus()
         tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid C(s) numerator values.
Please enter valid numerical data using the format [a,b,c].""")
      
      try:   
         denominatorC = contDen.get()
         denC = conversion(denominatorC)
         C = co.tf(numC,denC)
      except ValueError:
         cdenEntry.focus()
         tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid C(s) denominator values.
Please enter valid numerical data using the format [a,b,c].""") 
      eqC.set(str(C))

      # Calculated transfer functions.
      MYR = (C*P)/(1+C*P)
      MYD = P/(1+C*P)
      S = 1/(1+C*P)
      UR = C/(1+C*P)
      UD = (-C*P)/(1+C*P)

      # System response and performance indexes computation.
      try:
         if mode == 'servo':
            lab = 'servo'
            if In == 'step':
               tServo,yServo,inServo = response(MYR,magStep,timeIn,t,In)
               tUR,yUR,inUR = response(UR,magStep,timeIn,t,In)
               indexes('MYR',In,inServo,yServo,tServo,yUR)
               graph(lab,inServo,tServo,yServo,tUR,yUR)
            elif In == 'ramp':
               tServo,yServo,inServo = response(MYR,magRamp,timeIn,t,In)
               tUR,yUR,inUR = response(UR,magRamp,timeIn,t,In)
               indexes('MYR',In,inServo,yServo,tServo,yUR)
               graph(lab,inServo,tServo,yServo,tUR,yUR)
         elif mode == 'reg':
            lab = 'reg'
            if In == 'step':
               tReg,yReg,inReg = response(MYD,magStep,timeIn,t,In)
               tUD,yUD,inUD = response(UD,magStep,timeIn,t,In)
               indexes('MYD',In,inReg,yReg,tReg,yUD)
               graph(lab,inReg,tReg,yReg,tUD,yUD)
            elif In == 'ramp':
               tReg,yReg,inReg = response(MYD,magRamp,timeIn,t,In)
               tUD,yUD,inUD = response(UD,magRamp,timeIn,t,In)
               indexes('MYD',In,inReg,yReg,tReg,yUD)
               graph(lab,inReg,tReg,yReg,tUD,yUD)
         elif mode == 'both':
            lab = 'both'
            if In == 'step':
               tServo,yServo,inServo = response(MYR,magStep,timeIn,t,In)
               tUR,yUR,inUR = response(UR,magStep,timeIn,t,In)
               tReg,yReg,inReg = response(MYD,magStep,timeIn,t,In)
               tUD,yUD,inUD = response(UD,magStep,timeIn,t,In)
               indexes('MYR',In,inServo,yServo,tServo,yUR)
               indexes('MYD',In,inReg,yReg,tReg,yUD)
               graph(lab,inServo,tServo,yServo,tUR,yUR,tReg,yReg,tUD,yUD)
            elif In == 'ramp':
               tServo,yServo,inServo = response(MYR,magRamp,timeIn,t,In)
               tUR,yUR,inUR = response(UR,magRamp,timeIn,t,In)
               tReg,yReg,inReg = response(MYD,magRamp,timeIn,t,In)
               tUD,yUD,inUD = response(UD,magRamp,timeIn,t,In)
               indexes('MYR',In,inServo,yServo,tServo,yUR)
               indexes('MYD',In,inReg,yReg,tReg,yUD)
               graph(lab,inServo,tServo,yServo,tUR,yUR,tReg,yReg,tUD,yUD)
      except ValueError:
      # Add context to error eg. Numerator degree greater than denominator degree
         tkinter.messagebox.showerror('Simulation Error', """SIMULATION ERROR: A non-proper transfer function.
has been entered.""")
      # Closed Loop maximum sensitivity Ms.
      m,p,w = co.bode_plot(S,plot=False)  # This bode function is used to obtain the magnitude of S.
      Ms = max(m)  # Ms is the maximum value of the magnitude array.
      Ms = round(Ms,7)
      ending = """
MAXIMUM SENSITIVITY
Ms = {}
------------------------------
""".format(Ms)
   param.configure(state='normal')
   param.insert(tk.END,ending)
   param.see('end')
   param.configure(state='disabled')

def simulatorRealtime(*args):
       # GUI settings.
       runButton.focus()
       now = datetime.now()
       dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # dd/mm/YY H:M:S
       param.configure(state='normal')
       param.insert(tk.END,'\n'+dt_string)
       param.configure(state='disabled')
       ax1.clear();ax2.clear();ax3.clear();ax4.clear()
       buttonNW.pack_forget();buttonNE.pack_forget()
       buttonSW.pack_forget();buttonSE.pack_forget()
       canvas1.get_tk_widget().pack_forget();canvas2.get_tk_widget().pack_forget()
       canvas3.get_tk_widget().pack_forget();canvas4.get_tk_widget().pack_forget()

       # Simulation time.
       try:
          time = simTime.get()
          t = np.linspace(0,time,5001)
       except tkinter.TclError:
          timeEntry.focus()
          tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid simulation time value.
    Please enter valid numerical data.""")
       
       # Step magnitude.
       try:
          magStep = magS.get()
       except tkinter.TclError:
          stepEntry.focus()
          tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid step input value.
    Please enter valid numerical data.""")
       
       # Ramp magnitude.
       try:
          magRamp = magR.get()
       except tkinter.TclError:
          rampEntry.focus()
          tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid ramp slope value.
    Please enter valid numerical data.""")
       
       # Input time.
       try:
          timeIn = inTime.get()
       except tkinter.TclError:
          tinEntry.focus()
          tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid input time value.
    Please enter valid numerical data.""")

       # Input selection.
       state = check.get()
       if state == 1: In = 'step'
       else: In = 'ramp'

       # Control mode selection.
       transfer = graphics.get()
       if transfer == 1: mode = 'servo'
       elif transfer == 2: mode = 'reg'
       elif transfer == 3: mode = 'both'
       else: mode = 'process'

       # Process data.
       try:
          numeratorP = plantNum.get()
          numP = conversion(numeratorP)
       except ValueError:
          pnumEntry.focus()
          tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid P(s) numerator values.
    Please enter valid numerical data using the format [a,b,c].""")

       try:
          #denominatorP = plantDen.get()
          #denP = conversion(denominatorP)
          A = co.tf(numP,1)
       except ValueError:
          pdenEntry.focus()
          tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid P(s) denominator values.
    Please enter valid numerical data using the format [a,b,c].""")
       
       try:
          dT = deadTime.get()
          L = float(dT)
          numPade,denPade = co.pade(L,n=10)
          Pade = co.tf(numPade,denPade)
          P = A*Pade
       except tkinter.TclError:
          plantDelay.focus()
          tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid dead time value.
    Please enter valid numerical data.""")
       eqP.set(str(A))
       if L == 0: exp.set('*e^0')
       else: exp.set('*e^-{} s'.format(dT))
       
       if mode == 'process':
          lab = 'Process'
          if In == 'step':
             tP,yP,inP = response(P,magStep,timeIn,t,In)
             indexes('P',In,inP,yP,tP,0)
             graph(lab,inP,tP,yP)
          elif In == 'ramp':
             tP,yP,inP = response(P,magRamp,timeIn,t,In)
             indexes('P',In,inP,yP,tP,0)
             graph(lab,inP,tP,yP)
          ending = '------------------------------'
       
       else:
          # Controller data.
          try:
             #numeratorC = contNum.get()
             numeratorC = [dValue.get(),pValue.get(),iValue.get()]
             numC = [float(x) for x in numeratorC]
             #numC = conversion(numeratorC)
          except ValueError:
             cnumEntry.focus()
             tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid C(s) numerator values.
    Please enter valid numerical data using the format [a,b,c].""")
          
          try:   
             denominatorC = contDen.get()
             #denC = conversion(denominatorC)
             denC = [1,0]
             C = co.tf(numC,denC)
          except ValueError:
             cdenEntry.focus()
             tkinter.messagebox.showerror('Value Error', """VALUE ERROR: Invalid C(s) denominator values.
    Please enter valid numerical data using the format [a,b,c].""") 
          eqC.set(str(C))

          # Calculated transfer functions.
          MYR = (C*P)/(1+C*P)
          MYD = P/(1+C*P)
          S = 1/(1+C*P)
          UR = C/(1+C*P)
          UD = (-C*P)/(1+C*P)

          # System response and performance indexes computation.
          try:
             if mode == 'servo':
                lab = 'servo'
                if In == 'step':
                   tServo,yServo,inServo = response(MYR,magStep,timeIn,t,In)
                   tUR,yUR,inUR = response(UR,magStep,timeIn,t,In)
                   indexes('MYR',In,inServo,yServo,tServo,yUR)
                   graph(lab,inServo,tServo,yServo,tUR,yUR)
                elif In == 'ramp':
                   tServo,yServo,inServo = response(MYR,magRamp,timeIn,t,In)
                   tUR,yUR,inUR = response(UR,magRamp,timeIn,t,In)
                   indexes('MYR',In,inServo,yServo,tServo,yUR)
                   graph(lab,inServo,tServo,yServo,tUR,yUR)
             elif mode == 'reg':
                lab = 'reg'
                if In == 'step':
                   tReg,yReg,inReg = response(MYD,magStep,timeIn,t,In)
                   tUD,yUD,inUD = response(UD,magStep,timeIn,t,In)
                   indexes('MYD',In,inReg,yReg,tReg,yUD)
                   graph(lab,inReg,tReg,yReg,tUD,yUD)
                elif In == 'ramp':
                   tReg,yReg,inReg = response(MYD,magRamp,timeIn,t,In)
                   tUD,yUD,inUD = response(UD,magRamp,timeIn,t,In)
                   indexes('MYD',In,inReg,yReg,tReg,yUD)
                   graph(lab,inReg,tReg,yReg,tUD,yUD)
             elif mode == 'both':
                lab = 'both'
                if In == 'step':
                   tServo,yServo,inServo = response(MYR,magStep,timeIn,t,In)
                   tUR,yUR,inUR = response(UR,magStep,timeIn,t,In)
                   tReg,yReg,inReg = response(MYD,magStep,timeIn,t,In)
                   tUD,yUD,inUD = response(UD,magStep,timeIn,t,In)
                   indexes('MYR',In,inServo,yServo,tServo,yUR)
                   indexes('MYD',In,inReg,yReg,tReg,yUD)
                   graph(lab,inServo,tServo,yServo,tUR,yUR,tReg,yReg,tUD,yUD)
                elif In == 'ramp':
                   tServo,yServo,inServo = response(MYR,magRamp,timeIn,t,In)
                   tUR,yUR,inUR = response(UR,magRamp,timeIn,t,In)
                   tReg,yReg,inReg = response(MYD,magRamp,timeIn,t,In)
                   tUD,yUD,inUD = response(UD,magRamp,timeIn,t,In)
                   indexes('MYR',In,inServo,yServo,tServo,yUR)
                   indexes('MYD',In,inReg,yReg,tReg,yUD)
                   graph(lab,inServo,tServo,yServo,tUR,yUR,tReg,yReg,tUD,yUD)
             #sectorE.after(100, simulatorRealtime())
          except ValueError:
          # Add context to error eg. Numerator degree greater than denominator degree
             tkinter.messagebox.showerror('Simulation Error', """SIMULATION ERROR: A non-proper transfer function.
    has been entered.""")
          # Closed Loop maximum sensitivity Ms.
          m,p,w = co.bode_plot(S,plot=False)  # This bode function is used to obtain the magnitude of S.
          Ms = max(m)  # Ms is the maximum value of the magnitude array.
          Ms = round(Ms,7)
          ending = """
    MAXIMUM SENSITIVITY
    Ms = {}
    ------------------------------
    """.format(Ms)
       param.configure(state='normal')
       param.insert(tk.END,ending)
       param.see('end')
       param.configure(state='disabled')

#################################################
#######          GUI LAYOUT CODE          #######
#################################################

# Main menu.   
menubar = tk.Menu(mainWindow)
systemenu = tk.Menu(menubar,tearoff=0)
systemenu.add_command(label='Run',command=simulator,accelerator="F5")
systemenu.add_command(label='Reset all values',command=masterReset,accelerator="Ctrl+L")
systemenu.add_separator()
systemenu.add_command(label='Exit',command=close,accelerator="Alt+F4")
menubar.add_cascade(label='Simulation',menu=systemenu)
helpmenu = tk.Menu(menubar,tearoff=0)
helpmenu.add_command(label='Help Index',command=help,accelerator="F1")
helpmenu.add_command(label='About...',command=about,accelerator="F10")
menubar.add_cascade(label='Help',menu=helpmenu)

# Main window LabelFrames.
sectorA = ttk.LabelFrame(mainWindow,text='General Data')
sectorA.place(x=15,y=5,width=605)
sectorB = ttk.LabelFrame(mainWindow,text='Simulation Data')
sectorB.place(x=15,y=430) #,height=208
sectorC = ttk.LabelFrame(mainWindow,text='Graphics')
sectorC.place(x=15,y=710)
sectorD = ttk.LabelFrame(mainWindow,text='Response Parameters')
sectorD.place(x=335,y=460)
sectorE = ttk.LabelFrame(mainWindow,text='Simulation Results')
sectorE.place(x=625,y=5,width=795,height=708)

# Sector A widgets.
# Labels.
tk.Label(sectorA,text='Process Data:').grid(row=1,column=1,padx=10,sticky=tk.W)
tk.Label(sectorA,text='Numerator:').grid(row=2,column=1,padx=10,sticky=tk.W)
tk.Label(sectorA,text='Denominator:').grid(row=3,column=1,padx=10,sticky=tk.W)
tk.Label(sectorA,text='Dead time:').grid(row=4,column=1,padx=10,sticky=tk.W)
tk.Label(sectorA,text='P(s) Transfer Function:').grid(row=6,column=1,columnspan=2,padx=10,sticky='nsew')
tk.Label(sectorA,text='Controller Data:').grid(row=1,column=3,padx=10,sticky=tk.W)
tk.Label(sectorA,text='Numerator:').grid(row=2,column=3,padx=10,sticky=tk.W)
tk.Label(sectorA,text='Denominator:').grid(row=3,column=3,padx=10,sticky=tk.W)
tk.Label(sectorA,text='C(s) Transfer Function:').grid(row=7,column=3,columnspan=2,padx=10,sticky='nsew')
tk.Label(sectorA,text='Valor Planta:').grid(row=5,column=1,columnspan=1,padx=0,sticky='nsew')
tk.Label(sectorA,text='Valor P:').grid(row=4,column=3,columnspan=1,padx=0,sticky='nsew')
tk.Label(sectorA,text='Valor I:').grid(row=5,column=3,columnspan=1,padx=0,sticky='nsew')
tk.Label(sectorA,text='Valor D:').grid(row=6,column=3,columnspan=1,padx=0,sticky='nsew')
# Entries.
pnumEntry = tk.Entry(sectorA,textvariable=plantNum)
pnumEntry.grid(row=2,column=2,padx=10,pady=5)
pdenEntry = tk.Entry(sectorA,textvariable=plantDen)
pdenEntry.grid(row=3,column=2)
plantDelay = tk.Entry(sectorA,textvariable=deadTime)
plantDelay.grid(row=4,column=2,pady=5)
cnumEntry = tk.Entry(sectorA,textvariable=contNum)
cnumEntry.grid(row=2,column=4,padx=10)
cdenEntry = tk.Entry(sectorA,textvariable=contDen)
cdenEntry.grid(row=3,column=4)
# Sliders
barraPlant = tk.Scale(sectorA, from_=0, to=100, orient='horizontal',command=plantSlider_changed, variable=plantValue)
barraPlant.grid(row=5,column=2,pady=2)
barraP = tk.Scale(sectorA, from_=0, to=1000, orient='horizontal',command=pSlider_changed, variable=pValue)
barraP.grid(row=4,column=4,pady=3)
barraI = tk.Scale(sectorA, from_=0, to=100, orient='horizontal',command=iSlider_changed, variable=iValue)
barraI.grid(row=5,column=4,pady=3)
barraD = tk.Scale(sectorA, from_=0, to=100, orient='horizontal',command=dSlider_changed, variable=dValue)
barraD.grid(row=6,column=4,pady=2)
# Frames.
frameA = tk.Frame(sectorA)  # Frame containing the TF of P(s).
frameA.grid(row=8,column=1,columnspan=2,sticky='nsew',padx=100)
tk.Label(frameA,textvariable=eqP).grid(row=0,column=0)  # Label for P(s) TF.
tk.Label(frameA,textvariable=exp).grid(row=0,column=1)
frameB = tk.Frame(sectorA)  # Frame containing the TF of C(s).
frameB.grid(row=8,column=3,columnspan=2,sticky='nsew',padx=100)
tk.Label(frameB,textvariable=eqC,anchor='center').pack()  # Label for C(s) TF.
# Frames.
info = tk.Frame(mainWindow)
info.place(x=540,y=55)
sign = tk.Button(info,bitmap="question",command=closedLoop)
sign.pack(side="top",expand=1,fill='both')
# Buttons.
pResetButton = tk.Button(sectorA,text='Reset Values',bg='#829ce3',command=resetProcess)
pResetButton.grid(row=9,column=1,columnspan=2,pady=10)
cResetButton = tk.Button(sectorA,text='Reset Values',bg='#829ce3',command=resetController)
cResetButton.grid(row=9,column=3,columnspan=2,pady=10)
#Images.
img = Image.open('./resources/help.png')
resized_image= img.resize((570,250), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)


# Sector B widgets.
# Labels.
tk.Label(sectorB,text='Simulation time:').grid(row=1,column=1,padx=10,sticky=tk.W)
tk.Label(sectorB,text='Time units:').grid(row=2,column=1,padx=10,sticky=tk.W)
tk.Label(sectorB,text='Input time:').grid(row=3,column=1,padx=10,sticky=tk.W)
tk.Label(sectorB,text='Step magnitude:').grid(row=4,column=1,padx=10,sticky=tk.W)
tk.Label(sectorB,text='Ramp slope:').grid(row=5,column=1,padx=10,sticky=tk.W)
tk.Label(sectorB,text='Input type:').grid(row=6,column=1,padx=10,pady=11,sticky=tk.W)
tk.Label(sectorB,text='Simulation type:').grid(row=7,column=1,padx=10,pady=11,sticky=tk.W)
# Entries.
timeEntry = tk.Entry(sectorB,textvariable=simTime)
timeEntry.grid(row=1,column=2,pady=5)
tUnits = tk.Spinbox(sectorB,values=options,textvariable=timeUnits,width=18)
tUnits.grid(row=2,column=2,padx=10)
tinEntry = tk.Entry(sectorB,textvariable=inTime)
tinEntry.grid(row=3,column=2,padx=10,pady=5)
stepEntry = tk.Entry(sectorB,textvariable=magS)
stepEntry.grid(row=4,column=2)
rampEntry = tk.Entry(sectorB,textvariable=magR)
rampEntry.grid(row=5,column=2,pady=5)
# Radiobuttons.
stepOption = tk.Radiobutton(sectorB, text='Step',variable=check,value=1)
stepOption.grid(row=6,column=2,sticky='w')
stepOption.select()
rampOption = tk.Radiobutton(sectorB, text='Ramp',variable=check,value=2)
rampOption.grid(row=6,column=2,padx=5,sticky='e')
discreteOption = tk.Radiobutton(sectorB, text='Discrete',variable=checkType,value=1)
discreteOption.grid(row=7,column=2,sticky='w')
discreteOption.select()
realtimeOption = tk.Radiobutton(sectorB, text='Realtime',variable=checkType,value=2)
realtimeOption.grid(row=7,column=2,padx=5,sticky='e')

# Buttons.
inputResetButton = tk.Button(sectorB,text='Reset Values',bg='#829ce3',command=resetInputs)
inputResetButton.grid(row=8,column=1,columnspan=2,pady=9)

# Sector C widgets.
# Radiobuttons.
servoOption = tk.Radiobutton(sectorC, text='Servo Control',variable=graphics,value=1)
servoOption.grid(row=1,column=1,pady=10,sticky='w')
servoOption.select()
regOption = tk.Radiobutton(sectorC, text='Regulatory Control',variable=graphics,value=2)
regOption.grid(row=1,column=2,padx=5,sticky='w')
bothOption = tk.Radiobutton(sectorC, text='Servo and Regulatory',variable=graphics,value=3)
bothOption.grid(row=2,column=1,pady=5,sticky='w')
processOption = tk.Radiobutton(sectorC, text='Reaction Curve',variable=graphics,value=4)
processOption.grid(row=2,column=2,padx=5,sticky='w')
# Buttons.
allResetButton = tk.Button(sectorC,text='Reset ALL',bg='#829ce3',width=10,command=masterReset)
allResetButton.grid(row=3,column=1,pady=21,padx=10,ipady=5)
runButton = tk.Button(sectorC,text='RUN', bg='#e1e311', width=10, command=checkRealtime)
runButton.grid(row=3,column=2,padx=10,ipady=5)

# Sector D widgets.
# Scrollbars.
scrollbar = tk.Scrollbar(sectorD)
scrollbar.grid(row=1,column=2,sticky='ns')
# Text.
param = tk.Text(sectorD,yscrollcommand=scrollbar.set,height=24,width=30)
param.grid(row=1,column=1,padx=10,pady=10)
scrollbar.config(command=param.yview)

# Sector E widgets.
# Frames.
frameNW = tk.Frame(sectorE)
frameNW.grid(row=0,column=0,pady=5)
frameSW = tk.Frame(sectorE)
frameSW.grid(row=1,column=0)
frameNE = tk.Frame(sectorE)
frameNE.grid(row=0,column=1,padx=5)
frameSE = tk.Frame(sectorE)
frameSE.grid(row=1,column=1)
# Buttons.
buttonNW = tk.Button(master=frameNW,text='View',command=figViewNW)
buttonNE = tk.Button(master=frameNE, text='View',command=figViewNE)
buttonSW = tk.Button(master=frameSW, text='View',command=figViewSW)
buttonSE = tk.Button(master=frameSE, text='View',command=figViewSE)
# Figures.
fig1 = Figure(figsize=(5,5),dpi=100)
fig1, ax1 = plt.subplots()
fig2 = Figure(figsize=(5,5),dpi=100)
fig2, ax2 = plt.subplots()
fig3 = Figure(figsize=(5,5),dpi=100)
fig3, ax3 = plt.subplots()
fig4 = Figure(figsize=(5,5),dpi=100)
fig4, ax4 = plt.subplots()
# FigureCanvas.
canvas1 = FigureCanvasTkAgg(fig1,master=frameNW)
canvas1.get_tk_widget().config(width=370,height=310)
canvas2 = FigureCanvasTkAgg(fig2,master=frameNE)
canvas2.get_tk_widget().config(width=370,height=310)
canvas3 = FigureCanvasTkAgg(fig3,master=frameSW)
canvas3.get_tk_widget().config(width=370,height=310)
canvas4 = FigureCanvasTkAgg(fig4,master=frameSE)
canvas4.get_tk_widget().config(width=370,height=310)
# Pop-up window Figures.
figI = Figure(figsize=(5,5),dpi=100)
figI, axI = plt.subplots()
axI.set_xlabel('Time (s)');axI.set_ylabel('Amplitude')
figII = Figure(figsize=(5,5),dpi=100)
figII, axII = plt.subplots()
axII.set_xlabel('Time (s)');axII.set_ylabel('Amplitude')
figIII = Figure(figsize=(5,5),dpi=100)
figIII, axIII = plt.subplots()
axIII.set_xlabel('Time (s)');axIII.set_ylabel('Amplitude')
figIV = Figure(figsize=(5,5),dpi=100)
figIV, axIV = plt.subplots()
axIV.set_xlabel('Time (s)');axIV.set_ylabel('Amplitude')

##########################################
#####        GUI MAIN SETTINGS       #####
##########################################
# Main Window Hotkeys.
mainWindow.bind("<F1>",help)
mainWindow.bind("<F5>",simulator)
mainWindow.bind("<F10>",about)
mainWindow.bind("<Control_L><l>",masterReset)
# Hint text event for Entries.
# Sector A.
pnumEntry.configure(fg='gray')
pdenEntry.configure(fg='gray')
plantDelay.configure(fg='gray')
cnumEntry.configure(fg='gray')
cdenEntry.configure(fg='gray')
pnumBind = pnumEntry.bind("<FocusIn>",pNumHintText)
pdenBind = pdenEntry.bind("<FocusIn>",pDenHintText)
delayBind = plantDelay.bind("<FocusIn>",delayHintText)
cnumBind = cnumEntry.bind("<FocusIn>",cNumHintText)
cdenBind = cdenEntry.bind("<FocusIn>",cDenHintText)
# Sector B.
timeEntry.configure(fg='gray')
tinEntry.configure(fg='gray')
stepEntry.configure(fg='gray')
rampEntry.configure(fg='gray')
timeBind = timeEntry.bind("<FocusIn>",timeHintText)
tinBind = tinEntry.bind("<FocusIn>",intimeHintText)
stepBind = stepEntry.bind("<FocusIn>",stepHintText)
rampBind = rampEntry.bind("<FocusIn>",rampHintText)
# Sector B RadioButtons settings.
stepEntry.configure(state='normal')
rampEntry.configure(state='disabled')
stepOption.bind("<Button-1>",stepOptionLock)
rampOption.bind("<Button-1>",rampOptionLock)
# Sector D TextBox settings.
param.insert(tk.END,"""Welcome to the Control Systems
Simulator!\n""")
param.configure(state='disabled')

mainWindow.config(menu=menubar)
mainWindow.mainloop()