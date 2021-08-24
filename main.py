"""
BJTpy (Bipolar Junction Transistor in Python)
----------------------------------------------
This class computes a software for circuit analysis of BJT Amplifiers

**authors**: Paola Castro *University of Francisco de Paula Santander*
             Sebastian Rojas *University of Francisco de Paula Santander*

..note::
    This class makes inherits from `tkinter`, from `PIL`, from `os`, from `random` and from `sympy`
    Check the corresponding documentation below
    <https://docs.python.org/3/library/tk.html>
    <https://pillow.readthedocs.io/en/stable/>
    <https://docs.python.org/3/library/os.html>
    <https://docs.python.org/3/library/random.html>
    <https://docs.sympy.org/latest/index.html>
"""

from tkinter import * #The main controller for this Software
from PIL import ImageTk, Image #Used to implement images in Tkinter
import os #Used to open the corresponding PDF's files in the software
import random #Used to generate a few random numbers in functions
from sympy import symbols, solve #Used to solve equations in many functions

#This is where all the functions starts, beggining with root() which is the main one
def root ():
    """
    Starts the program, it is defined as the main function

    Parameters
    ----------
    menu: Tk
        The main screen controller
    menuImage: ImageTk
        The background image

    Return
    -------
    Void
        
    """

    global menu
    menu = Tk()
    menu.geometry("720x480")
    menu.title("BJTpy - Menú")
    menu.resizable(False,False)
    menu.iconbitmap("Images/BJTpy_ICO.ico")
    #Background Menu Image
    menuImage = ImageTk.PhotoImage(Image.open("Images/Menu.jpg"))
    Label(image = menuImage).place(x=0,y=0)
    #Some useful buttons such as Help
    Button(text = "Ingresar", height = "2", width = "30", cursor = "hand2", command = appAccess).place(x = 468, y = 250)
    Button(text = "Ayuda", height = "2", width = "30", cursor = "hand2", command = apphelp).place(x = 468, y = 300)
    #The loop where everything starts to work in this function, it is needed so the window stays in the screen, otherwise it would dissapear
    menu.mainloop()

def appAccess ():
    """
    Starts the second window, it allows to modificate transistors characteristics

    Parameters
    ----------
    menuAccess: Tk
        The second screen controller
    menuAccessImage: ImageTk
        The second background image
    gain: DoubleVar
        Value of transistor gain
    gainEntry: Entry
        Where is written the transistor gain
    beta: DobleVar
        Value of transistor beta
    betaEntry: Entry
        Where is written the transistor beta
    vcc: DobleVar
        Value of transistor voltage Vcc
    vccEntry: Entry
        Where is written the transistor voltage Vcc
    follower: IntVar
        It is a check botton to add a follower transistor in the design if needed

    Return
    -------
    Void
        
    """
    
    menu.destroy()
    global menuAccess
    menuAccess = Tk()
    menuAccess.geometry("320x440")
    menuAccess.title("BJTpy - Ingreso de Datos")
    menuAccess.resizable(False,False)
    menuAccess.iconbitmap("Images/BJTpy_ICO.ico")
    #Background Menu Image
    menuAccessImage = ImageTk.PhotoImage(Image.open("Images/MenuIngreso.jpg"))
    Label(menuAccess, image = menuAccessImage).place(x=0,y=0)
    #Main content of the page 
    Label(menuAccess, text = "En este espacio se van a introducir algunos datos para\nel respectivo diseño de un amplificador BJT en su con-\nfiguración inversora.",justify = "left").place(x=15,y=40)
    #Circuit main variables
    Label(menuAccess, text = "Ganancia (Av): [2-125]*").place(x=20,y=100)
    global gain
    global gainEntry
    gain = DoubleVar()
    gainEntry = Entry(menuAccess, textvariable = gain, width = "30")
    gainEntry.place(x=20,y=120)
    Label(menuAccess, text = "Beta (β): [80-150]*").place(x=20,y=160)
    global beta
    global betaEntry
    beta = DoubleVar()
    betaEntry = Entry(menuAccess, textvariable = beta, width = "30")
    betaEntry.place(x=20,y=180)
    Label(menuAccess, text = "Vcc: [10-20]*").place(x=20,y=220)
    global vcc
    global vccEntry
    vcc = DoubleVar()
    vccEntry = Entry(menuAccess, textvariable = vcc, width = "30")
    vccEntry.place(x=20,y=240)
    global follower
    follower = IntVar()
    Checkbutton(menuAccess, text = "Deseo añadir una etapa seguidora", variable = follower, cursor = "hand2", onvalue = 1, offvalue = 0).place(x=20,y=280)
    Button(menuAccess, text = "Crear Amplificador", height = "2", width = "30", cursor = "hand2", command = makeAmp).place(x=50,y=340)
    Button(menuAccess, text = "?", height = "1", width = "2", cursor = "hand2", command = apphelp).place(x=280,y=380)
    #The loop where everything starts to work in this function, it is needed so the window stays in the screen, otherwise it would dissapear
    menuAccess.mainloop()

def makeAmp ():
    """
    This function stores the main three variables of the Amplifier

    Parameters
    ----------
    gainValue: DoubleVar
        The gain value in the amplifier
    betaValue: DoubleVar
        The beta value in the amplifier
    vccValue: DoubleVar
        The vcc value in the amplifier

    Return
    -------
    Void
        
    """
    
    #Takes the values written by the user
    global gainValue
    gainValue = gain.get()
    gainEntry.delete(0,END)
    global betaValue
    betaValue = beta.get()
    betaEntry.delete(0,END)
    global vccValue
    vccValue = vcc.get()
    vccEntry.delete(0,END)
    #Set values for correct functionality
    if 2<=gainValue<=125 and 80<=betaValue<=150 and 10<=vccValue<=20:
        makeCircuit()
    else:
        errorWindow()

def errorWindow():
    """
    Shows an error window if parameters aren't in set values

    Parameters
    ----------
    errorWin: Tk
        The screen that shows an error window
        
    Return
    -------
    Void
        
    """
    
    errorWin = Tk()
    errorWin.geometry("350x80")
    errorWin.title("BJTpy - Error")
    errorWin.resizable(False,False)
    errorWin.iconbitmap("Images/BJTpy_ICO.ico")
    Label(errorWin, text = "ERROR: Verifique los datos ingresados.").place(x=70,y=25)

def apphelp ():
    """
    Shows help manual

    Parameters
    ----------
    Void
        
    Return
    -------
    Help manual
        
    """
    os.startfile("Help\Manual.pdf")

def makeCircuit():
    """
    The graffic controller to build every possible amplifier in the software

    Parameters
    ----------
    menuCircuit: Tk
        The Third screen controller
    menuAmplifier: ImageTk
        Background image in this window
    followerCheck: IntVar
        Carries the information to check if a follower is needed in the final stage

    Return
    -------
    Void
        
    """
    
    menuAccess.destroy()
    global menuCircuit
    menuCircuit = Tk()
    menuCircuit.geometry("920x518")
    menuCircuit.title("BJTpy - Circuito Amplificador")
    menuCircuit.resizable(False,False)
    menuCircuit.iconbitmap("Images/BJTpy_ICO.ico")
    #Background Image
    menuAmplifier = ImageTk.PhotoImage(Image.open("Images/MenuAmplificador.jpg"))
    Label(menuCircuit, image = menuAmplifier).place(x=0,y=0)
    #Process to build the schematic and organize all the variables
    followerCheck = follower.get()
    if followerCheck == 1:
        if 2<=gainValue<=5:
            imageCircuit = ImageTk.PhotoImage(Image.open("Images/Casos/UnaEtapaSeguidor.jpg"))
            Label(menuCircuit, image = imageCircuit).place(x=175,y=100)
            Label(menuCircuit, text = "Amplificador de una etapa con seguidor", justify = "center", font=("Times New Roman", 20)).place(x=250,y=45)
            calculateOneStageF()
            #Labels for the Follower Stage
            Label(menuCircuit, text = str(RB_S)+" Ω", bg = "white").place(x=580,y=210)
            Label(menuCircuit, text = str(RE_S)+" Ω", bg = "white").place(x=680,y=360)
            Label(menuCircuit, text = str(vccValue)+" V", bg = "white").place(x=570,y=150)
            #Labels for Stage 1
            Label(menuCircuit, text = str(RC)+" Ω", bg = "white").place(x=470,y=210)
            Label(menuCircuit, text = str(RE)+" Ω", bg = "white").place(x=470,y=360)
            Label(menuCircuit, text = str(R1)+" Ω", bg = "white").place(x=350,y=210)
            Label(menuCircuit, text = str(R2)+" Ω", bg = "white").place(x=350,y=360)
        elif 6<=gainValue<=25:
            imageCircuit = ImageTk.PhotoImage(Image.open("Images/Casos/DosEtapasSeguidor.jpg"))
            Label(menuCircuit, image = imageCircuit).place(x=60,y=100)
            Label(menuCircuit, text = "Amplificador de dos etapas con seguidor", justify = "center", font=("Times New Roman", 20)).place(x=250,y=45)
            calculateTwoStagesF()
            #Labels for the Follower Stage
            Label(menuCircuit, text = str(RB_S)+" Ω", bg = "white").place(x=690,y=205)
            Label(menuCircuit, text = str(RE_S)+" Ω", bg = "white").place(x=790,y=355)
            Label(menuCircuit, text = str(vccValue)+" V", bg = "white").place(x=465,y=145)
            #Labels for Stage 2
            Label(menuCircuit, text = str(RC_2)+" Ω", bg = "white").place(x=595,y=205)
            Label(menuCircuit, text = str(RE_2)+" Ω", bg = "white").place(x=595,y=355)
            Label(menuCircuit, text = str(R1_2)+" Ω", bg = "white").place(x=475,y=205)
            Label(menuCircuit, text = str(R2_2)+" Ω", bg = "white").place(x=475,y=355)
            #Labels for Stage 1
            Label(menuCircuit, text = str(RC_1)+" Ω", bg = "white").place(x=360,y=205)
            Label(menuCircuit, text = str(RE_1)+" Ω", bg = "white").place(x=360,y=355)
            Label(menuCircuit, text = str(R1_1)+" Ω", bg = "white").place(x=245,y=205)
            Label(menuCircuit, text = str(R2_1)+" Ω", bg = "white").place(x=245,y=355)
        else:
            imageCircuit = ImageTk.PhotoImage(Image.open("Images/Casos/TresEtapasSeguidor.jpg"))
            Label(menuCircuit, image = imageCircuit).place(x=17,y=120) 
            Label(menuCircuit, text = "Amplificador de tres etapas con seguidor", justify = "center", font=("Times New Roman", 20)).place(x=250,y=45)
            calculateThreeStagesF()
            #Labels for the Follower Stage
            Label(menuCircuit, text = str(RB_S)+" Ω", bg = "white").place(x=775,y=210)
            Label(menuCircuit, text = str(RE_S)+" Ω", bg = "white").place(x=850,y=335)
            Label(menuCircuit, text = str(vccValue)+" V", bg = "white").place(x=510,y=155)
            #Labels for Stage 3
            Label(menuCircuit, text = str(RC_3)+" Ω", bg = "white").place(x=685,y=210)
            Label(menuCircuit, text = str(RE_3)+" Ω", bg = "white").place(x=685,y=335)
            Label(menuCircuit, text = str(R1_3)+" Ω", bg = "white").place(x=580,y=210)
            Label(menuCircuit, text = str(R2_3)+" Ω", bg = "white").place(x=580,y=335)
            #Labels for Stage 2
            Label(menuCircuit, text = str(RC_2)+" Ω", bg = "white").place(x=485,y=210)
            Label(menuCircuit, text = str(RE_2)+" Ω", bg = "white").place(x=485,y=335)
            Label(menuCircuit, text = str(R1_2)+" Ω", bg = "white").place(x=380,y=210)
            Label(menuCircuit, text = str(R2_2)+" Ω", bg = "white").place(x=380,y=335)
            #Labels for Stage 1
            Label(menuCircuit, text = str(RC_1)+" Ω", bg = "white").place(x=280,y=210)
            Label(menuCircuit, text = str(RE_1)+" Ω", bg = "white").place(x=280,y=335)
            Label(menuCircuit, text = str(R1_1)+" Ω", bg = "white").place(x=175,y=210)
            Label(menuCircuit, text = str(R2_1)+" Ω", bg = "white").place(x=175,y=335)
    else:
        if 2<=gainValue<=5:
            imageCircuit = ImageTk.PhotoImage(Image.open("Images/Casos/UnaEtapa.jpg"))
            Label(menuCircuit, image = imageCircuit).place(x=300,y=100)
            Label(menuCircuit, text = "Amplificador de una etapa", justify = "center", font=("Times New Roman", 20)).place(x=320,y=45)
            calculateOneStage()
            Label(menuCircuit, text = str(RC)+" Ω", bg = "white").place(x=600,y=210)
            Label(menuCircuit, text = str(RE)+" Ω", bg = "white").place(x=600,y=320)
            Label(menuCircuit, text = str(R1)+" Ω", bg = "white").place(x=480,y=210)
            Label(menuCircuit, text = str(R2)+" Ω", bg = "white").place(x=480,y=320)
            Label(menuCircuit, text = str(vccValue)+" V", bg = "white").place(x=580,y=150)
        elif 6<=gainValue<=25:
            imageCircuit = ImageTk.PhotoImage(Image.open("Images/Casos/DosEtapas.jpg"))
            Label(menuCircuit, image = imageCircuit).place(x=150,y=100)
            Label(menuCircuit, text = "Amplificador de dos etapas", justify = "center", font=("Times New Roman", 20)).place(x=320,y=45)
            calculateTwoStages()
            #Labels for Stage 2
            Label(menuCircuit, text = str(RC_2)+" Ω", bg = "white").place(x=690,y=210)
            Label(menuCircuit, text = str(RE_2)+" Ω", bg = "white").place(x=690,y=350)
            Label(menuCircuit, text = str(R1_2)+" Ω", bg = "white").place(x=570,y=210)
            Label(menuCircuit, text = str(R2_2)+" Ω", bg = "white").place(x=570,y=350)
            Label(menuCircuit, text = str(vccValue)+" V", bg = "white").place(x=530,y=145)
            #Labels for Stage 1
            Label(menuCircuit, text = str(RC_1)+" Ω", bg = "white").place(x=450,y=210)
            Label(menuCircuit, text = str(RE_1)+" Ω", bg = "white").place(x=450,y=350)
            Label(menuCircuit, text = str(R1_1)+" Ω", bg = "white").place(x=330,y=210)
            Label(menuCircuit, text = str(R2_1)+" Ω", bg = "white").place(x=330,y=350)
        else:
            imageCircuit = ImageTk.PhotoImage(Image.open("Images/Casos/TresEtapas.jpg"))
            Label(menuCircuit, image = imageCircuit).place(x=45,y=110) 
            Label(menuCircuit, text = "Amplificador de tres etapas", justify = "center", font=("Times New Roman", 20)).place(x=320,y=45)
            calculateThreeStages()
            #Labels for Stage 3
            Label(menuCircuit, text = str(RC_3)+" Ω", bg = "white").place(x=820,y=210)
            Label(menuCircuit, text = str(RE_3)+" Ω", bg = "white").place(x=820,y=355)
            Label(menuCircuit, text = str(R1_3)+" Ω", bg = "white").place(x=700,y=210)
            Label(menuCircuit, text = str(R2_3)+" Ω", bg = "white").place(x=700,y=355)
            Label(menuCircuit, text = str(vccValue)+" V", bg = "white").place(x=630,y=155)
            #Labels for Stage 2
            Label(menuCircuit, text = str(RC_2)+" Ω", bg = "white").place(x=580,y=210)
            Label(menuCircuit, text = str(RE_2)+" Ω", bg = "white").place(x=580,y=355)
            Label(menuCircuit, text = str(R1_2)+" Ω", bg = "white").place(x=460,y=210)
            Label(menuCircuit, text = str(R2_2)+" Ω", bg = "white").place(x=460,y=355)
            #Labels for Stage 1
            Label(menuCircuit, text = str(RC_1)+" Ω", bg = "white").place(x=345,y=210)
            Label(menuCircuit, text = str(RE_1)+" Ω", bg = "white").place(x=345,y=355)
            Label(menuCircuit, text = str(R1_1)+" Ω", bg = "white").place(x=225,y=210)
            Label(menuCircuit, text = str(R2_1)+" Ω", bg = "white").place(x=225,y=355)
    Button(menuCircuit, text = "Ver paso a paso", height = "2", width = "30", cursor = "hand2", command = StepByStep).place(x=660,y=450)
    Button(menuCircuit, text = "←", height = "1", width = "2", cursor = "hand2", command = Reset).place(x=50,y=50)
    #The loop where everything starts to work in this function, it is needed so the window stays in the screen, otherwise it would dissapear
    menuCircuit.mainloop()

def Reset():
    """
    Destroys final window and comes back to the first one

    Parameters
    ----------
    Void
        
    Return
    -------
    root
        
    """
    
    menuCircuit.destroy()
    root()

def StepByStep():
    """
    Shows an document to check the design step by step 

    Parameters
    ----------
    Void
        
    Return
    -------
    Document to view a step by step
        
    """

    os.startfile("Help\PasoaPaso.pdf")


def calculateOneStageF():
    """
    Calculates the values of the variables needed in the first stage in the amplifier, including the follower stage.

    Parameters
    ----------
    RC: Int
        Stores the value of RC in the first stage
    RE: Int
        Stores the value of RE in the first stage
    R1: Int
        Stores the value of R1 in the first stage
    R2: Int
        Stores the value of R2 in the first stage
    RB_S: Int
        Stores the value of RB in the follower stage
    RE_S: Int
        Stores the value of RE in the follower stage
    rand: randint
        Stores a random number between one and three
    vce: Int
        Stores the value of vce
    RL: Int
        Stores the value of RL in the first stage
    expr: expression
        Stores the expression temporarily
    solTemp: solve
        It is the solution for the temporal expression
    IC: Int
        Stores the value of IC in the first stage
    VB: Int
        Stores the value of VB in the first stage
    
    Return
    -------
    The values of the resistors in each stage
        
    """
    global RC, RE, R1, R2, RB_S, RE_S
    #FOLLOWER STAGE
    vce=(vccValue)/2
    rand = random.randint(1,3)
    if rand == 1:
        RE_S = 1000
    elif rand == 2:
        RE_S = 1500
    else:
        RE_S = 2000
    RB_S=round((0.7+vce)/((vce/RE_S)/betaValue),2)
    #FIRST INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC = 10500
    elif rand == 2:
        RC = 15500
    else:
        RC = 19500
    RL = (1/RB_S+1/(((betaValue*0.025)/(vce/RE_S))+(betaValue+1)*RE_S))**-1
    RE = symbols('RE')
    expr = ((betaValue*(1/RC+1/RL)**-1)/((betaValue+1)*RE+((betaValue*0.025)/(vce/(RE+RC)))))-gainValue
    solTemp = solve(expr)
    RE = round(solTemp[0],2)
    IC=vce/(RE+RC)
    R2=round((betaValue)*RE/10,2)
    VB=0.7+(IC*RE)
    R1=round((vccValue*R2/VB)-R2,2)

def calculateTwoStagesF():
    """
    Calculates the values of the variables needed in the two stages in the amplifier, including the follower stage.
        
    Parameters
    ----------
    RC_1: Int
        Stores the value of RC in the first stage
    RE_1: Int
        Stores the value of RE in the first stage
    R1_1: Int
        Stores the value of R1 in the first stage
    R2_1: Int
        Stores the value of R2 in the first stage
    RC_2: Int
        Stores the value of RC in the second stage
    RE_2: Int
        Stores the value of RE in the second stage
    R1_2: Int
        Stores the value of R1 in the second stage
    R2_2: Int
        Stores the value of R2 in the second stage
    RB_S: Int
        Stores the value of RB in the follower stage
    RE_S: Int
        Stores the value of RE in the follower stage
    vce: Int
        Stores the value of vce
    rand: randint
        Stores a random number between one and three
    RL_2: Int
        Stores the value of RL in the second stage
    RL_1: Int
        Stores the value of RL in the first stage
    expr: expression
        Stores the expression temporarily
    solTemp: solve
        It is the solution for the temporal expression
    IC_2: Int
        Stores the value of IC in the second stage
    VB_2: Int
        Stores the value of VB in the second stage
    IC_1: Int
        Stores the value of IC in the first stage
    VB_1: Int
        Stores the value of VB in the first stage
    
    Return
    -------
    The values of the resistors in each stage
        
    """
    
    global RC_1, RE_1, R1_1, R2_1, RC_2, RE_2, R1_2, R2_2, RB_S, RE_S
    #FOLLOWER STAGE
    vce=(vccValue)/2
    rand = random.randint(1,3)
    if rand == 1:
        RE_S = 1000
    elif rand == 2:
        RE_S = 1500
    else:
        RE_S = 2000
    RB_S=round((0.7+vce)/((vce/RE_S)/betaValue),2)
    #SECOND INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC_2 = 10500
    elif rand == 2:
        RC_2 = 13500
    else:
        RC_2 = 15500
    RL_2 = (1/RB_S+1/(((betaValue*0.025)/(vce/RE_S))+(betaValue+1)*RE_S))**-1
    RE_2 = symbols('RE_2')
    expr = ((betaValue*(1/RC_2+1/RL_2)**-1)/((betaValue+1)*RE_2+((betaValue*0.025)/(vce/(RE_2+RC_2)))))-((gainValue)**(1/2))
    solTemp = solve(expr)
    RE_2 = round(solTemp[0],2)
    IC_2=vce/(RE_2+RC_2)
    R2_2=round((betaValue)*RE_2/10,2)
    VB_2=0.7+(IC_2*RE_2)
    R1_2=round((vccValue*R2_2/VB_2)-R2_2,2)
    #FIRST INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC_1 = 17500
    elif rand == 2:
        RC_1 = 18500
    else:
        RC_1 = 19500
    RL_1 = (1/R1_2+1/R2_2+1/(((betaValue*0.025)/(vce/(RE_2+RC_2)))+(betaValue+1)*RE_2))**-1
    RE_1 = symbols('RE_1')
    expr = ((betaValue*(1/RC_1+1/RL_1)**-1)/((betaValue+1)*RE_1+((betaValue*0.025)/(vce/(RE_1+RC_1)))))-((gainValue)**(1/2))
    solTemp = solve(expr)
    RE_1 = round(solTemp[0],2)
    IC_1=vce/(RE_1+RC_1)
    R2_1=round(((betaValue)*RE_1/10),2)
    VB_1=0.7+(IC_1*RE_1)
    R1_1=round((vccValue*R2_1/VB_1)-R2_1,2)

def calculateThreeStagesF():
    """
    Calculates the values of the variables needed in the three stages in the amplifier, including the follower stage.

    Parameters
    ----------
    RC_1: Int
        Stores the value of RC in the first stage
    RE_1: Int
        Stores the value of RE in the first stage
    R1_1: Int
        Stores the value of R1 in the first stage
    R2_1: Int
        Stores the value of R2 in the first stage
    RC_2: Int
        Stores the value of RC in the second stage
    RE_2: Int
        Stores the value of RE in the second stage
    R1_2: Int
        Stores the value of R1 in the second stage
    R2_2: Int
        Stores the value of R2 in the second stage
    RC_3: Int
        Stores the value of RC in the third stage
    RE_3: Int
        Stores the value of RE in the third stage
    R1_3: Int
        Stores the value of R1 in the third stage
    R2_3: Int
        Stores the value of R2 in the third stage
    RB_S: Int
        Stores the value of RB in the follower stage
    RE_S: Int
        Stores the value of RE in the follower stage
    vce: Int
        Stores the value of vce
    rand: randint
        Stores a random number between one and three
    RL_3: Int
        Stores the value of RL in the third stage
    RL_2: Int
        Stores the value of RL in the second stage
    RL_1: Int
        Stores the value of RL in the first stage
    expr: expression
        Stores the expression temporarily
    solTemp: solve
        It is the solution for the temporal expression
    IC_3: Int
        Stores the value of IC in the third stage
    VB_3: Int
        Stores the value of VB in the third stage
    IC_2: Int
        Stores the value of IC in the second stage
    VB_2: Int
        Stores the value of VB in the second stage
    IC_1: Int
        Stores the value of IC in the first stage
    VB_1: Int
        Stores the value of VB in the first stage
    
    Return
    -------
    The values of the resistors in each stage
        
    """
    
    global RC_1, RE_1, R1_1, R2_1, RC_2, RE_2, R1_2, R2_2, RC_3, RE_3, R1_3, R2_3, RB_S, RE_S
    #FOLLOWER STAGE
    vce=(vccValue)/2
    rand = random.randint(1,3)
    if rand == 1:
        RE_S = 1000
    elif rand == 2:
        RE_S = 1500
    else:
        RE_S = 2000
    RB_S=round((0.7+vce)/((vce/RE_S)/betaValue),2)
    #THIRD INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC_3 = 10500
    elif rand == 2:
        RC_3 = 13500
    else:
        RC_3 = 15500
    RL_3 = (1/RB_S+1/(((betaValue*0.025)/(vce/RE_S))+(betaValue+1)*RE_S))**-1
    RE_3 = symbols('RE_3')
    expr = ((betaValue*(1/RC_3+1/RL_3)**-1)/((betaValue+1)*RE_3+((betaValue*0.025)/(vce/(RE_3+RC_3)))))-((gainValue)**(1/3))
    solTemp = solve(expr)
    RE_3 = round(solTemp[0],2)
    IC_3=vce/(RE_3+RC_3)
    R2_3=round((betaValue)*RE_3/10,2)
    VB_3=0.7+(IC_3*RE_3)
    R1_3=round((vccValue*R2_3/VB_3)-R2_3,2)
    #SECOND INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC_2 = 17500
    elif rand == 2:
        RC_2 = 18500
    else:
        RC_2 = 19500
    RL_2 = (1/R1_3+1/R2_3+1/(((betaValue*0.025)/(vce/(RE_3+RC_3)))+(betaValue+1)*RE_3))**-1
    RE_2 = symbols('RE_2')
    expr = ((betaValue*(1/RC_2+1/RL_2)**-1)/((betaValue+1)*RE_2+((betaValue*0.025)/(vce/(RE_2+RC_2)))))-((gainValue)**(1/3))
    solTemp = solve(expr)
    RE_2 = round(solTemp[0],2)
    IC_2=vce/(RE_2+RC_2)
    R2_2=round((betaValue)*RE_2/10,2)
    VB_2=0.7+(IC_2*RE_2)
    R1_2=round((vccValue*R2_2/VB_2)-R2_2,2)
    #FIRST INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC_1 = 21500
    elif rand == 2:
        RC_1 = 23500
    else:
        RC_1 = 25500
    RL_1 = (1/R1_2+1/R2_2+1/(((betaValue*0.025)/(vce/(RE_2+RC_2)))+(betaValue+1)*RE_2))**-1
    RE_1 = symbols('RE_1')
    expr = ((betaValue*(1/RC_1+1/RL_1)**-1)/((betaValue+1)*RE_1+((betaValue*0.025)/(vce/(RE_1+RC_1)))))-((gainValue)**(1/3))
    solTemp = solve(expr)
    RE_1 = round(solTemp[0],2)
    IC_1=vce/(RE_1+RC_1)
    R2_1=round(((betaValue)*RE_1/10),2)
    VB_1=0.7+(IC_1*RE_1)
    R1_1=round((vccValue*R2_1/VB_1)-R2_1,2)

def calculateOneStage():
    """
    Calculates the values of the variables needed in the first stage of the amplifier.

    Parameters
    ----------
    RC: Int
        Stores the value of RC in the first stage
    RE: Int
        Stores the value of RE in the first stage
    R1: Int
        Stores the value of R1 in the first stage
    R2: Int
        Stores the value of R2 in the first stage
    vce: Int
        Stores the value of vce
    rand: randint
        Stores a random number between one and three
    expr: expression
        Stores the expression temporarily
    solTemp: solve
        It is the solution for the temporal expression
    IC: Int
        Stores the value of IC in the first stage
    VB: Int
        Stores the value of VB in the first stage
    
    Return
    -------
    The values of the resistors in each stage
        
    """
    
    global RC, RE, R1, R2
    rand = random.randint(1,3)
    if rand == 1:
        RC = 10500
    elif rand == 2:
        RC = 15500
    else:
        RC = 19500
    vce=(vccValue)/2
    RE = symbols('RE')
    expr = ((betaValue*RC)/(((betaValue*0.025)/(vce/(RE+RC)))+((betaValue+1)*RE)))-gainValue
    solTemp = solve(expr)
    RE = round(solTemp[0],2)
    IC=vce/(RE+RC)
    R2=round((betaValue)*RE/10,2)
    VB=0.7+(IC*RE)
    R1=round((vccValue*R2/VB)-R2,2)

def calculateTwoStages():
    """
    Calculates the values of the variables needed in the two stages in the amplifier.

    Parameters
    ----------
    RC_1: Int
        Stores the value of RC in the first stage
    RE_1: Int
        Stores the value of RE in the first stage
    R1_1: Int
        Stores the value of R1 in the first stage
    R2_1: Int
        Stores the value of R2 in the first stage
    RC_2: Int
        Stores the value of RC in the second stage
    RE_2: Int
        Stores the value of RE in the second stage
    R1_2: Int
        Stores the value of R1 in the second stage
    R2_2: Int
        Stores the value of R2 in the second stage
    vce: Int
        Stores the value of vce
    rand: randint
        Stores a random number between one and three
    RL: Int
        Stores the value of RL in the first stage
    expr: expression
        Stores the expression temporarily
    solTemp: solve
        It is the solution for the temporal expression
    IC_2: Int
        Stores the value of IC in the second stage
    VB_2: Int
        Stores the value of VB in the second stage
    IC_1: Int
        Stores the value of IC in the first stage
    VB_1: Int
        Stores the value of VB in the first stage
    
    Return
    -------
    The values of the resistors in each stage
        
    """
    
    global RC_1, RE_1, R1_1, R2_1, RC_2, RE_2, R1_2, R2_2
    #SECOND INVERSOR STAGE
    RC_2 = 10500
    vce=(vccValue)/2
    RE_2 = symbols('RE_2')
    expr = ((betaValue*RC_2)/(((betaValue*0.025)/(vce/(RE_2+RC_2)))+((betaValue+1)*RE_2)))-((gainValue)**(1/2))
    solTemp = solve(expr)
    RE_2 = round(solTemp[0],2)
    IC_2=vce/(RE_2+RC_2)
    R2_2=round((betaValue)*RE_2/10,2)
    VB_2=0.7+(IC_2*RE_2)
    R1_2=round((vccValue*R2_2/VB_2)-R2_2,2)
    #FIRST INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC_1 = 12500
    elif rand == 2:
        RC_1 = 15500
    else:
        RC_1 = 19500
    RL=(1/R1_2+1/R2_2+1/(((betaValue*0.025)/(vce/(RE_2+RC_2)))+(betaValue+1)*RE_2))**-1
    RE_1 = symbols('RE_1')
    expr = ((betaValue*(1/RC_1+1/RL)**-1)/((betaValue+1)*RE_1+((betaValue*0.025)/(vce/(RE_1+RC_1)))))-((gainValue)**(1/2))
    solTemp = solve(expr)
    RE_1 = round(solTemp[0],2)
    IC_1=vce/(RE_1+RC_1)
    R2_1=round((betaValue)*RE_1/10,2)
    VB_1=0.7+(IC_1*RE_1)
    R1_1=round((vccValue*R2_1/VB_1)-R2_1,2)

def calculateThreeStages():
    """
    Calculates the values of the variables needed in the three stages in the amplifier.

    Parameters
    ----------
    RC_1: Int
        Stores the value of RC in the first stage
    RE_1: Int
        Stores the value of RE in the first stage
    R1_1: Int
        Stores the value of R1 in the first stage
    R2_1: Int
        Stores the value of R2 in the first stage
    RC_2: Int
        Stores the value of RC in the second stage
    RE_2: Int
        Stores the value of RE in the second stage
    R1_2: Int
        Stores the value of R1 in the second stage
    R2_2: Int
        Stores the value of R2 in the second stage
    RC_3: Int
        Stores the value of RC in the third stage
    RE_3: Int
        Stores the value of RE in the third stage
    R1_3: Int
        Stores the value of R1 in the third stage
    R2_3: Int
        Stores the value of R2 in the third stage
    vce: Int
        Stores the value of vce
    rand: randint
        Stores a random number between one and three
    RL_2: Int
        Stores the value of RL in the second stage
    RL_1: Int
        Stores the value of RL in the first stage
    expr: expression
        Stores the expression temporarily
    solTemp: solve
        It is the solution for the temporal expression
    IC_3: Int
        Stores the value of IC in the third stage
    VB_3: Int
        Stores the value of VB in the third stage
    IC_2: Int
        Stores the value of IC in the second stage
    VB_2: Int
        Stores the value of VB in the second stage
    IC_1: Int
        Stores the value of IC in the first stage
    VB_1: Int
        Stores the value of VB in the first stage
    
    Return
    -------
    The values of the resistors in each stage
        
    """
    
    global RC_1, RE_1, R1_1, R2_1, RC_2, RE_2, R1_2, R2_2, RC_3, RE_3, R1_3, R2_3
    #THIRD INVERSOR STAGE
    RC_3 = 15500
    vce=(vccValue)/2
    RE_3 = symbols('RE_3')
    expr = ((betaValue*RC_3)/(((betaValue*0.025)/(vce/(RE_3+RC_3)))+((betaValue+1)*RE_3)))-((gainValue)**(1/3))
    solTemp = solve(expr)
    RE_3 = round(solTemp[0],2)
    IC_3=vce/(RE_3+RC_3)
    R2_3=round((betaValue)*RE_3/10,2)
    VB_3=0.7+(IC_3*RE_3)
    R1_3=round((vccValue*R2_3/VB_3)-R2_3,2)
    #SECOND INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC_2 = 17500
    elif rand == 2:
        RC_2 = 18500
    else:
        RC_2 = 19500
    RL_2 = (1/R1_3+1/R2_3+1/(((betaValue*0.025)/(vce/(RE_3+RC_3)))+(betaValue+1)*RE_3))**-1
    RE_2 = symbols('RE_2')
    expr = ((betaValue*(1/RC_2+1/RL_2)**-1)/((betaValue+1)*RE_2+((betaValue*0.025)/(vce/(RE_2+RC_2)))))-((gainValue)**(1/3))
    solTemp = solve(expr)
    RE_2 = round(solTemp[0],2)
    IC_2=vce/(RE_2+RC_2)
    R2_2=round(((betaValue)*RE_2/10),2)
    VB_2=0.7+(IC_2*RE_2)
    R1_2=round((vccValue*R2_2/VB_2)-R2_2,2)
    #FIRST INVERSOR STAGE
    rand = random.randint(1,3)
    if rand == 1:
        RC_1 = 22500
    elif rand == 2:
        RC_1 = 25500
    else:
        RC_1 = 28500
    RL_1 = (1/R1_2+1/R2_2+1/(((betaValue*0.025)/(vce/(RE_2+RC_2)))+(betaValue+1)*RE_2))**-1
    RE_1 = symbols('RE_1')
    expr = ((betaValue*(1/RC_1+1/RL_1)**-1)/((betaValue+1)*RE_1+((betaValue*0.025)/(vce/(RE_1+RC_1)))))-((gainValue)**(1/3))
    solTemp = solve(expr)
    RE_1 = round(solTemp[0],2)
    IC_1=vce/(RE_1+RC_1)
    R2_1=round((betaValue)*RE_1/10,2)
    VB_1=0.7+(IC_1*RE_1)
    R1_1=round((vccValue*R2_1/VB_1)-R2_1,2)

#This is the call to the main function, where everthing starts
if __name__ == "__main__":
    root()