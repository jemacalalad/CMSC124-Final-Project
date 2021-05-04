import re
import os.path
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as sd
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename

# DICTIONARIES
# Error logs
errorcode = {
    "noHAI":            "Error 01: Program has no HAI code delimiter.\n",
    "noKTHXBYE":        "Error 02: Program has no KTHXBYE code delimiter.\n",
    "nopairTLDR":       "Error 03: Missing OBTW.\n",
    "dblHAI":           "Error 04: Double HAI keyword.\n",
    "dblKTHXBYE":       "Error 05: Double KTHXBYE keyword.\n",
    "wrongvarname":     "Error 06: Invalid variable name ",
    "invalidvalue":     "Error 07: Invalid value/expression for variable: ",
    "novalue":          'Error 08: No value given to variable ',
    "unknownref":       "Error 09: Unknown/Undeclared variable reference ",
    "missingvisible":   "Error 10: Missing statement after VISIBLE.\n",
    "missinggimmeh":    "Error 11: Missing statement after GIMMEH.\n",
    "multiplegimmeh":   "Error 12: Multiple arguments after GIMMEH is not allowed.\n",
    "notsubscript":     "Error 13: Unpermitted data type for ",
    "unknownop":        "Error 14: Unidentified operation: ",
    "quotedoperand":    "Error 15: Quoted operand is not of type NUMBR/NUMBAR.\n",
    "min2args":         "Error 16: Expression must have at least 2 operands.\n",
    "max2args":         "Error 17: Expression must have at most 2 operands.\n",
    "missingarg":       "Error 18: Missing operand on expression.\n",
    "noRleft":          "Error 19: Missing variable before R.\n",
    "noRRight":         "Error 20: Missing literal/variable/expression after R.\n",
    "manyRleft":        "Error 21: Multiple variables before R is not allowed.\n",
    "manyRright":       "Error 22: Multiple statements after R is not allowed.\n",
    "unpairedquotes":   "Error 23: Unpaired double quotes.\n",
    "boolrecursive":    "Error 24: ALL OF/ANY OF cannot be called recursively.\n",
    "noMKAY":           "Error 25: ALL OF/ANY OF must be terminated in MKAY.\n",
    "dblMKAY":          "Error 26: Double MKAY found.\n",
    "missingoperand":   "Error 27: Lacking operand/s. Please check the expression again.\n",
    "noOIC":            "Error 26: If-else/Switch blocks must be terminated by OIC\n",
    "loneOIC":          "Error 27: If-else blocks must be preceded by O RLY?/Switch blocks must be preceded by WTF?\n",
    "noYARLY":          "Error 28: O RLY? must be succeeded by YA RLY\n",
    "noNOWAI":          "Error 29: Missing NO WAI.\n",
    "conditionerror":   "Error 30: Preceding expression of If-else blocks must result to the type \"TROOF\"\n",
    "missingcasevalue": "Error 31: The succeeding expression after OMG is missing.\n",
    "multicasevalue":   "Error 32: Only one succeeding expression after OMG is allowed.\n",
    "missingdefault":   "Error 33: Missing OMGWTF statement.\n",
    "itemptyerror":     "Error 34: The Implicit Variable does not contain any value.\n",
    "nowtf":            "Error 35: Switch blocks must be preceded by WTF?\n",
    "noomg":            "Error 36: WTF? must be succeeded by a proper OMG statement.\n",
    "missingquote":     "Error 37: YARN literals must start and end with quotation marks.\n",
    "invalidcase":      "Error 38: This case value is invalid: ",
    "multiYARLY":       "Error 39: Only one YA RLY is allowed per block.\n",
    "multiNOWAI":       "Error 40: Only one NO WAI is allowed per block.\n",
    "multiOMGWTF":      "Error 41: Only one OMGWTF is allowed per block.\n",
    "noORLY":           "Error 42: Missing O RLY? statement.\n",
    "unreqcomm":        "Error 43: Unrecognizable command.\n",
    "invalidliteral":   "Error 44: Invalid literal: ",
    "noinput":          "Error 45: Please add an input.\n",
    "notvardec":        "Error 46: Variable declaration is not allowed inside If-Else/Switch blocks.\n",
    "multiorly":        "Error 47: Only one ORLY? is allowed per block.\n",
    "multiwtf":         "Error 48: Only one WTF? is allowed per block.\n"
}

# Literals
literals = {
    "numbr":    "\-?[0-9]+",
    "numbar":   "\-?[0-9]*\.[0-9]+",
    "yarn":     "\"[^\"]*\"\s*",
    "troof":    "(WIN)|(FAIL)"
}

# Arithmetic and Logic Lexemes
logic = {
    "add":          "^\s*SUM OF\s",
    "sub":          "^\s*DIFF OF\s",
    "mul":          "^\s*PRODUKT OF\s",
    "div":          "^\s*QUOSHUNT OF\s",
    "mod":          "^\s*MOD OF\s",
    "mor":          "^\s*BIGGR OF\s",
    "les":          "^\s*SMALLR OF\s",
    "equ":          "^\s*BOTH SAEM\s",
    "neq":          "^\s*DIFFRINT\s",
    "not":          "^\s*NOT\s",
    "xor":          "^\s*WON OF\s",
    "any":          "^\s*ANY OF\s",
    "all":          "^\s*ALL OF\s",
    "and":          "^\s*BOTH OF\s",
    "or_":          "^\s*EITHER OF\s",
    "mkay":         "\sMKAY\s*$",
    "smoosh":       "(^\s*|\s)SMOOSH\s",
    "operandid":    "\sAN\s"
}

# LOLCODE Lexemes
regexlist = {
    "varname":      "^[a-zA-Z][a-zA-Z0-9\_]*$",
    "spaces":       "^\s*$",
    "hai":          "^HAI\s*",
    "kthxbye":      "^\s*KTHXBYE$",
    "btw":          "\s*BTW\s",
    "obtw":         "^\s*OBTW\s*",
    "tldr":         "\s*TLDR$",
    "ihasa":        "^\s*I HAS A\s",
    "itz":          "\sITZ\s",
    "visible":      "\s*VISIBLE\s",
    "gimmeh":       "\s*GIMMEH\s",
    "var_assign":   "\s+R\s+",
    "ifblock":      "^\s*O RLY\?\s*$",
    "if":           "^\s*YA RLY\s*$",
    "else":         "^\s*NO WAI\s*$",
    "switchblock":  "^\s*WTF\?\s*$",
    "case":         "^\s*OMG\s+",
    "default":      "^\s*OMGWTF\s*$",
    "break":        "^\s*GTFO\s*$",
    "blockend":     "^\s*OIC\s*$",
    # following entries are for ease of identification for expressions
    "math":         "^(" + logic["add"] + "|" + logic["sub"] + "|" + logic["mul"] + "|" + logic["div"] + "|" + logic["mod"] + "|" + logic["mor"] + "|" + logic["les"] + ")",
    "bool":         "^(" + logic["not"] + "|" + logic["and"] + "|" + logic["or_"] + "|" + logic["xor"] + "|" + logic["all"] + "|" + logic["any"] + ")",
    "bool_spec":    "^(" + logic["all"] + "|" + logic["any"] + ")",
    "bool_xspec":   logic["all"][1:len(logic["all"])] + "|" + logic["any"][1:len(logic["any"])], 
    "comp":         "^(" + logic["equ"] + "|" + logic["neq"] + ")"
}

# modified string regex for general expression
expressionregex = "^(" + regexlist["math"][2:len(regexlist["math"]) - 1] + "|" + regexlist["comp"][2:len(regexlist["comp"]) - 1] + "|" + regexlist["bool"][2:len(regexlist["bool"]) - 1] + "|" + logic["smoosh"] + ")"


# window + header initalizations
projectwindow = tk.Tk()
projectwindow.title("CMSC 124 Project")
projectwindow.configure(background="black")
projectwindow.geometry('970x675')
prjlogo = tk.PhotoImage(file="prjsrc/lolcodelogo.gif")
codelog = tk.PhotoImage(file="prjsrc/codelogo.png")
lexmlog = tk.PhotoImage(file="prjsrc/lexemelogo.png")
symblog = tk.PhotoImage(file="prjsrc/symbollogo.png")
outplog = tk.PhotoImage(file="prjsrc/outputlogo.png")
open_bt = tk.PhotoImage(file="prjsrc/openbutton.png")
exec_bt = tk.PhotoImage(file="prjsrc/executeactive.png")
open_ac = tk.PhotoImage(file="prjsrc/openactive.png")
exec_ac = tk.PhotoImage(file="prjsrc/executebutton.png")
header = tk.Canvas(projectwindow, bd=-2, bg="black", width=prjlogo.width(), height=prjlogo.height())
filhead = tk.Canvas(projectwindow, bd=-2, bg="black", width=codelog.width(), height=codelog.height())
lexhead = tk.Canvas(projectwindow, bd=-2, bg="black", width=lexmlog.width(), height=lexmlog.height())
symhead = tk.Canvas(projectwindow, bd=-2, bg="black", width=symblog.width(), height=symblog.height())
outhead = tk.Canvas(projectwindow, bd=-2, bg="black", width=outplog.width(), height=25)
header.create_image(125, 45, anchor="center", image=prjlogo)
filhead.create_image(-4, 40, anchor="w", image=codelog)
lexhead.create_image(-11, 40, anchor="w", image=lexmlog)
symhead.create_image(-6, 40, anchor="w", image=symblog)
outhead.create_image(-4, 20, anchor="w", image=outplog)

# code reading/editing container
codedisplay = scrolledtext.ScrolledText(projectwindow, width=45, height=15, background="black", foreground="#4DEEEA", insertbackground='#4DEEEA',font=('Courier New Bold', 11))
codedisplay.focus()
# file path input (beside open button)
# input receiving: https://www.javatpoint.com/python-tkinter-entry
# read with specifc file formats: https://stackoverflow.com/questions/47176470/how-to-open-file-with-tkfiledialog-and-read-the-content-with-notepad
# file path checking: https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
# content erasing: https://stackoverflow.com/questions/27966626/how-to-clear-delete-the-contents-of-a-tkinter-text-widget
rawfilepathinput = tk.StringVar()
def fileread():
    prevcontent = codedisplay.get('1.0', tk.END)        # to get recent contents before opening a new file
    codedisplay.delete('1.0', tk.END)
    custominput = rawfilepathinput.get()
    filetemp = "***\nentered filename/path is invalid\n(absolute path required)\n***"       # fixed string for invalid paths
    if len(custominput) == 0:
        filetemp = askopenfilename(initialdir="./", filetypes=(("LOLCODE Files", "*.lol"),("All Files", "*.*")))
        if len(filetemp) != 0:
            filetemp = open(filetemp, "r").read()
        else:
            filetemp = prevcontent                      # if no file selected, previous contents are brought back
    elif os.path.isfile(custominput):
        filetemp = open(custominput, "r").read()
    codedisplay.insert(tk.INSERT, filetemp)
# file name / file path input container
filenamerawinput = tk.Entry(projectwindow, width=56, textvariable=rawfilepathinput)

# button customization:
# https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change
fileuploadbutton = tk.Button(projectwindow, image=open_bt, height=20, borderwidth=0, bg="#4DEEEA", activebackground="#F000FF",command=fileread)
def file_enter(e):
    fileuploadbutton['background'] = "#0400FE"
    fileuploadbutton['image'] = open_ac
def file_leave(e):
    fileuploadbutton['background'] = "#4DEEEA"
    fileuploadbutton['image'] = open_bt
fileuploadbutton.bind("<Enter>", file_enter)
fileuploadbutton.bind("<Leave>", file_leave)

# Style modification (for Treeview/listings): 
# https://riptutorial.com/tkinter/example/31885/customize-a-treeview
# https://www.youtube.com/watch?v=ewxT3ZEGKAA
datastyle = ttk.Style(projectwindow)
datastyle.theme_use("default")
datastyle.configure("Treeview.Heading", background="#FFE700", foreground="black", font=("Calibri", 13, 'bold'))
datastyle.configure("Treeview", background="black", foreground="#FFE700", fieldbackground="black")
datastyle.map("Treeview", background=[('selected', '#FFE700')], foreground=[('selected', 'black')])
# lexeme Treeview setup
lexemedisplay = ttk.Treeview(projectwindow, columns=("Classification"))
lexemedisplay.heading('#0', text="Lexeme")
lexemedisplay.heading('#1', text="Classification")
lexemedisplay.column("#0", width=85)
lexemedisplay.column("#1", width=170)
# symbol table Treeview setup
symboldisplay = ttk.Treeview(projectwindow, columns=("Value"))
symboldisplay.heading('#0', text="Identifier")
symboldisplay.heading('#1', text="Value")
symboldisplay.column("#0", width=85)
symboldisplay.column("#1", width=150)
# uneditable display: https://www.geeksforgeeks.org/python-tkinter-scrolledtext-widget/
executedisplay = scrolledtext.ScrolledText(projectwindow, width=100, height=10, background="black", foreground="#F000FF", insertbackground='#F000FF', highlightbackground='#F000FF', font=('Courier New Bold', 11))
executedisplay.configure(state='disabled')


# FUNCTIONS
# Functions were placed in this section because all the succeeding functions are needed to be declared before the execute button
# and these functions needed inputs from the widgets that were declared above.


# for quoted literals in arithmetics
def quotedoperand(string):
    if re.search(literals["numbar"], string):
        return [float(string), "NUMBAR"]
    elif re.search(literals["numbr"], string):
        return [int(string), "NUMBR"]
    return errorcode["quotedoperand"]

# operand evaluator for both arithmetic and logic operations
def operandevaulator(evaluate, currentsymbols, mode, operation):
    # for quoted values in arithmetic
    if mode == "mathmode" and re.search(literals["yarn"], evaluate):
        evaluate = quotedoperand(re.sub("\"", "", evaluate))
        if isinstance(evaluate, str):
            return evaluate
        return [evaluate, [["\"", '"String Delimiter"'], [evaluate[0], "Literal"], ["\"", '"String Delimiter"']]]
    # variable references
    elif re.search(regexlist["varname"], evaluate) and evaluate in currentsymbols:
        # and follows their repsective type limits (equalities and inequalities take any TYPE)
        if (mode == "mathmode" and ((currentsymbols[evaluate][1] == "NUMBR" or currentsymbols[evaluate][1] == "NUMBAR") or operation == "equ" or operation == "neq")) or (mode == "boolmode" and currentsymbols[evaluate][1] == "TROOF"):
            return [currentsymbols[evaluate], [[evaluate, '"Variable Reference"']]]
        elif mode == "boolmode" and (currentsymbols[evaluate][1] == "NUMBR" or currentsymbols[evaluate][1] == "NUMBAR"):    # --|
            # print(currentsymbols[evaluate]) # DEBUG LINE                                                                  #   |
            if currentsymbols[evaluate][0] == 0:                                                                            #   |--> logic expressions accepts integers, WIN if not 0, FAIL otherwise
                return [["FAIL", '"TROOF"'], [[evaluate, '"Variable Reference"']]]                                          #   |
            return [["WIN", '"TROOF"'], [[evaluate, '"Variable Reference"']]]                                               # --|
        errorstring = evaluate + " is of type " + currentsymbols[evaluate][1] + ".\n"   # --|
        if mode == "mathmode":                                                          #   |
            mode = "arithmetics"                                                        #   |--> error
        else:                                                                           #   |--> display
            mode = "boolean"                                                            #   |
        return errorcode["notsubscript"] + mode + ": " + errorstring                    # --|
    elif re.search(literals["numbr"], evaluate):                                    # --|
        if mode == "mathmode":                                                      #   |
            if re.search(literals["numbar"], evaluate):                             #   |
                if re.search("^\-?[0-9]*\.[0-9]+$", evaluate):                      #   |
                    return [[float(evaluate), "NUMBAR"], [[evaluate, '"Literal"']]] #   |
                else:                                                               #   |
                    return errorcode["invalidliteral"] + evaluate                   #   |
            else:                                                                   #   |
                if re.search("^\-?[0-9]+$", evaluate):                              #   |
                    return [[int(evaluate), "NUMBR"], [[evaluate, '"Literal"']]]    #   |--> numbr/numbar operand
                else:                                                               #   |
                    return errorcode["invalidliteral"] + evaluate                   #   |
        return errorcode["invalidliteral"] + evaluate                               #   |
        if mode == "boolmode":                                                      #   |
            if evaluate == 0:                                                       #   |
                return [["FAIL", '"TROOF"'], [[evaluate, '"Literal"']]]             #   |
            return [["WIN", '"TROOF"'], [[evaluate, '"Literal"']]]                  # --|
    elif mode == "boolmode" and re.search(literals["troof"], evaluate):     # Raw boolean
        if re.search("^((WIN)|(FAIL))$", evaluate):
            return [[evaluate, '"TROOF"'], [[evaluate, '"Literal"']]]       # operand
        else:
            return errorcode["invalidliteral"] + evaluate
    return errorcode["unknownref"] + evaluate + ".\n"       # Main error display

# grouping algorithm for nested expressions for both arithmetic and logic operations
def groupingalgo(datasplit, mode):
    index = 0
    needs = 0
    teststring = ""
    # tests if list index exists: https://stackoverflow.com/questions/11786157/if-list-index-exists-do-x
    while True:
        try:
            teststring = datasplit[index]
        except IndexError:
            if needs != 0:
                return errorcode["missingoperand"]
            else:
                break
        if len(datasplit[index]) == 0:
            return errorcode["missingarg"]
        if ((mode == "any" or mode == "all") and re.search(regexlist["bool_xspec"], teststring)):   # Error for recursive
            return errorcode["boolrecursive"]                                                       # ALL OF/ANY FOR
        elif re.search(regexlist["bool_spec"], teststring):                             # --|
            try:                                                                        #   |
                datasplit[index] = datasplit[index] + " AN " + datasplit[index + 1]     #   |
            except IndexError:                                                          #   |--> if ALL OF/ANY OF is nested by non-ALL OF/ANY OF expressions
                return errorcode["noMKAY"]                                              #   |
            if re.search(logic["mkay"], datasplit.pop(index + 1)):                      #   |
                index += 1                                                              # --|
        # general grouping for expression as operands
        elif re.search(expressionregex, teststring) and not re.search(logic["not"], teststring):
            while re.search(expressionregex, teststring):
                # identify operand count
                teststring = (re.split(expressionregex, teststring))[-1]
                needs += 2
                # if found a liteaal/variable, decrease operand count
                if re.search(regexlist["varname"], teststring) or re.search("^" + literals["yarn"], teststring) or re.search("^" + literals["numbr"], teststring) or re.search("^" + literals["troof"], teststring):
                    needs -= 1
                    index += 1
                    break
        # if found a literal/variable and needed operands is not 0
        elif (re.search(regexlist["varname"], teststring) or re.search(literals["yarn"], teststring) or re.search(literals["numbr"], teststring) or re.search(literals["troof"], teststring)) and needs != 0:
            needs -= 1                                                                          # --|
            datasplit[index - 1] = datasplit[index - 1] + " AN " + datasplit[index]             #   |
            datasplit.pop(index)                                                                #   |--> current item will be added to the previous group
            if needs != 0:                                                                      #   |--> a deduction will occur if still there are operands needed
                needs -= 1                                                                      #   |--> ( to compensate for the paired operations )
                if needs == 0:                                                                  #   |--> if "perfect pair", move to previous group
                    index -= 1                                                                  #   |--> and join it to the group before it
                    datasplit[index - 1] = datasplit[index - 1] + " AN " + datasplit[index]     #   |
                    datasplit.pop(index)                                                        # --|
        else:           # lone operand
            index += 1  # no need for grouping
    # operand count check
    if mode == "not" and len(datasplit) > 1:
        return errorcode["manyNOT"]
    elif mode != "not" and len(datasplit) < 2:
        return errorcode["min2args"]
    elif mode != "all" and mode != "any" and len(datasplit) > 2:
        return errorcode["max2args"]
    return datasplit

# general string splitter for arithmetic and logic operations
def exlex(lineparse, operation):
    return (re.split(regexlist["spaces"][1:len(regexlist["spaces"])], re.split(logic[operation], lineparse)[-1]))[0]

def arithmetics(lineparse, currentsymbols):
    mode = ""
    datasplit = []
    evaluated = []  # will hold the result of the arithmetic/comparison operation
    inoperand = []  # will hold the 2 operands with their corresponding types
    lex = []
    if re.search(logic["mor"], lineparse):                      # --|   A
        mode = "mor"                                            #   |   R
        lex.append(['BIGGR OF', '"Arithmetic Identifier"'])     #   |   I
    elif re.search(logic["les"], lineparse):                    #   |   T
        mode = "les"                                            #   |   H
        lex.append(['SMALLR OF', '"Arithmetic Identifier"'])    #   |   M
    elif re.search(logic["equ"], lineparse):                    #   |   E
        mode = "equ"                                            #   |   T
        lex.append(['BOTH SAEM', '"Comparison Identifier"'])    #   |   I
    elif re.search(logic["neq"], lineparse):                    #   |   C
        mode = "neq"                                            #   |   -
        lex.append(['DIFFRINT', '"Comparison Identifier"'])     #   |   C
    elif re.search(logic["add"], lineparse):                    #   |   O
        mode = "add"                                            #   |   M
        lex.append(['SUM OF', '"Arithmetic Identifier"'])       #   |   P
    elif re.search(logic["sub"], lineparse):                    #   |   A
        mode = "sub"                                            #   |   R
        lex.append(['DIFF OF', '"Arithmetic Identifier"'])      #   |   I
    elif re.search(logic["mul"], lineparse):                    #   |   S
        mode = "mul"                                            #   |   O
        lex.append(['PRODUKT OF', '"Arithmetic Identifier"'])   #   |   N
    elif re.search(logic["div"], lineparse):                    #   |    
        mode = "div"                                            #   |   F
        lex.append(['QUOSHUNT OF', '"Arithmetic Identifier"'])  #   |   I
    elif re.search(logic["mod"], lineparse):                    #   |   L
        mode = "mod"                                            #   |   T
        lex.append(['MOD OF', '"Arithmetic Identifier"'])       #   |   E
    else:                                                       #   |   R
        return errorcode["unknownop"] + lineparse + ".\n"       # --|   S
    
    # split using AN, regroup for nested expressions
    datasplit = groupingalgo(re.split(logic["operandid"], exlex(lineparse, mode)), mode)
    if isinstance(datasplit, str):
        return datasplit

    # operand 1 evaluation
    if re.search(regexlist["math"], datasplit[0]) or re.search(regexlist["comp"], datasplit[0]):
        result = arithmetics(datasplit[0], currentsymbols)
    else:
        result = operandevaulator(datasplit[0], currentsymbols, "mathmode", mode)
    if isinstance(result, str):
        return result
    inoperand.append(result[0])
    for item in result[1]:
        lex.append(item)

    lex.append(["AN", '"Operands Identifier"'])

    if re.search(regexlist["math"], datasplit[1]) or re.search(regexlist["comp"], datasplit[1]):
        result = arithmetics(datasplit[1], currentsymbols)
    else:
        result = operandevaulator(datasplit[1], currentsymbols, "mathmode", mode)
    if isinstance(result, str):
        return result
    inoperand.append(result[0])
    for item in result[1]:
        lex.append(item)
    
    a = inoperand[0][0]                                                 # --|
    b = inoperand[1][0]                                                 #   |
    if mode == "add":                                                   #   |
        evaluated.append(a + b)                                         #   |
    elif mode == "sub":                                                 #   |
        evaluated.append(a - b)                                         #   |
    elif mode == "mul":                                                 #   |
        evaluated.append(a * b)                                         #   |
    elif mode == "div":                                                 #   |--> Actual
        evaluated.append(a / b)                                         #   |--> arithmetic
    elif mode == "mod":                                                 #   |--> computation /
        evaluated.append(a % b)                                         #   |--> comparison
    elif mode == "mor":                                                 #   |--> evaluation
        evaluated.append(max(a,b))                                      #   |
    elif mode == "les":                                                 #   |
        evaluated.append(min(a,b))                                      #   |
    else:                                                               #   |
        if (mode == "equ" and a == b) or (mode == "neq" and a != b):    #   |
            evaluated.append("WIN")                                     #   |
        else:                                                           #   |
            evaluated.append("FAIL")                                    # --|

    # Result type assignment
    if re.search(literals["troof"], str(evaluated[0])):
        evaluated.append("TROOF")
    elif inoperand[0][1] == "NUMBAR" or inoperand[1][1] == "NUMBAR":
        evaluated.append("NUMBAR")
    else:
        evaluated.append("NUMBR")
        if mode == "div":
            evaluated[0] = int(evaluated[0])
    return [evaluated, lex]

def booleans(lineparse, currentsymbols):
    mode = ""
    lex = []
    if re.search(logic["not"], lineparse):
        mode = "not"                                        # --|
        lex.append(['NOT', '"Boolean Identifier"'])         #   |
    elif re.search (logic["and"], lineparse):               #   |
        mode = "and"                                        #   |   L
        lex.append(['BOTH OF', '"Boolean Identifier"'])     #   |   O
    elif re.search (logic["or_"], lineparse):               #   |   G
        mode = "or_"                                        #   |   I
        lex.append(['EITHER OF', '"Boolean Identifier"'])   #   |   C
    elif re.search (logic["xor"], lineparse):               #   |    
        mode = "xor"                                        #   |   F
        lex.append(['WON OF', '"Boolean Identifier"'])      #   |   I
    elif re.search (logic["all"], lineparse):               #   |   L
        mode = "all"                                        #   |   T
        lex.append(['ALL OF', '"Boolean Identifier"'])      #   |   E
    elif re.search (logic["any"], lineparse):               #   |   R
        mode = "any"                                        #   |   S
        lex.append(['ANY OF', '"Boolean Identifier"'])      #   |
    else:                                                   #   |
        return errorcode["unknownop"] + lineparse + ".\n"   # --|
    
    datasplit = exlex(lineparse, mode)
    if mode != "not":
        if mode == "all" or mode == "any":                          # --|
            if re.search(logic["mkay"], datasplit):                 #   |
                datasplit = (re.split(logic["mkay"], datasplit))[0] #   |
                if re.search(logic["mkay"], datasplit):             #   |--> MKAY Search
                    return errorcode["dblMKAY"]                     #   |
            else:                                                   #   |
                return errorcode["noMKAY"]                          # --|
    datasplit = groupingalgo(re.split(logic["operandid"], datasplit), mode) # --|
    if isinstance(datasplit, str):                                          #   |--> deconstruct and group
        return datasplit                                                    # --|

    # iteratte for all operands
    for item in range(0, len(datasplit)):
        result = ""
        if re.search(regexlist["bool"], datasplit[item]):           # --|
            result = booleans(datasplit[item], currentsymbols)      #   |--> recursive call
            if isinstance(result, str):                             #   |--> for nested expressions
                return result                                       # --|
        else:                                                                               # --|
            result = operandevaulator(datasplit[item], currentsymbols, "boolmode", mode)    #   |--> lone operand
            if isinstance(result, str):                                                     #   |--> evaluate immediately
                return result                                                               # --|
        datasplit[item] = result[0]     # --|
        for lexentry in result[1]:      #   |--> result and lexeme entry collector
            lex.append(lexentry)        # --|
        if ((mode == "any" or mode == "or_") and result[0][0] == "WIN") or ((mode == "all" or mode == "and") and result[0][0] == "FAIL"):   # --|
            # print(mode, "short circuit----------------") # DEBUG LINE                                                                     #   |
            if mode == "any" or mode == "all":                                                                                              #   |
                lex.append(["MKAY", '"Expession Delimiter"'])                                                                               #   |--> "short-circuiting" and/all and or/any operations
            if mode == "any" or mode == "or_":                                                                                              #   |
                return [["WIN", '"TROOF"'], lex]                                                                                            #   |
            return [["FAIL", '"TROOF"'], lex]                                                                                               # --|
        if item != len(datasplit) - 1:
            lex.append(["AN", '"Operands Identifier"'])
        # Actual logic operation execution
        else:
            if mode == "not":                           # --|
                if datasplit[item][0] == "WIN":         #   |--> NOT
                    return [["FAIL", '"TROOF"'], lex]   #   |--> OPERATION
                return [["WIN", '"TROOF"'], lex]        # --|
            elif mode == "xor":                                 # --|
                if datasplit[item][0] != datasplit[0][0]:       #   |--> XOR OPERATION
                    return [["WIN", '"TROOF"'], lex]            # --|
                return [["FAIL", '"TROOF"'], lex]
            elif ((mode == "any" or mode == "or_") and datasplit[-1][0] == "FAIL") or ((mode == "all" or mode == "and") and datasplit[-1][0] == "WIN"): # --|
                if mode == "any" or mode == "all":                                                                                                      #   |
                    lex.append(["MKAY", '"Expession Delimiter"'])                                                                                       #   |--> and/all/or/any
                if mode == "any" or mode == "or_":                                                                                                      #   |--> "short circuit"
                    return [["FAIL", '"TROOF"'], lex]                                                                                                   #   |
                return [["WIN", '"TROOF"'], lex]                                                                                                        # --|
            if mode == "any" or mode == "all":                  # --|
                lex.append(["MKAY", '"Expession Delimiter"'])   #   |
            if mode == "any" or mode == "or_":                  #   |--> last item conflict for any/all/or/and
                return [["WIN", '"TROOF"'], lex]                #   |
            return [["FAIL", '"TROOF"'], lex]                   # --|

# for string concatenations
def stringsconcat(lineparse, currentsymbols):
    lex = [["SMOOSH", '"Function Identifier"']]
    result = re.split(logic["operandid"], exlex(lineparse, "smoosh"))
    outputstr = ""
    if len(result) < 2:                 # No arguments followed the
        return errorcode["min2args"]    # smoosh keyword
    for item in range(0, len(result)):                                                          # --|
        if len(result[item]) == 0:                          # an argument                       #   |
            return errorcode["missingarg"]                  # is missing                        #   |
        if re.search(literals["yarn"], result[item]):                                           #   |
            outputstr += re.sub("\"", "", result[item])                                         #   |
            lex.append([result[item], '"Literal"'])                                             #   |
        elif re.search(literals["troof"], result[item]):                                        #   |
            outputstr += result[item]                                                           #   |
            lex.append([result[item], '"Literal"'])                                             #   |
        elif re.search(regexlist["varname"], result[item]) and result[item] in currentsymbols:  #   |--> argument
            if currentsymbols[result[item]][1] == "YARN":                                       #   |--> evaluation
                if re.search("\\\\\\\"", currentsymbols[result[item]][0]):                      #   |
                    dissect = re.split("\\\\\\\"", currentsymbols[result[item]][0])             #   |
                    for words in range(0, len(dissect)):                                        #   |
                        outputstr += dissect[words]                                             #   |
                        if words != len(dissect) - 1:                                           #   |
                            outputstr += "\\\""                                                 #   |
                else:                                                                           #   |
                    outputstr += re.sub("\"", "", currentsymbols[result[item]][0])              #   |
            else:                                                                               #   |
                outputstr += str(currentsymbols[result[item]][0])                               #   |
            lex.append([result[item], '"Variable Reference"'])                                  #   |
        elif re.search(literals["numbr"], result[item]):                                        #   |
            outputstr += str(result[item])                                                      #   |
            lex.append([result[item], '"Literal"'])                                             #   |
        else:                                                                                   #   |
            return errorcode["unknownref"] + result[item] + ".\n"                               # --|
        if item != len(result) - 1:                         # Lexeme
            lex.append(["AN", '"Operands Identifier"'])     # Collector
    return [[outputstr, '"YARN"'], lex]

# expressions designator for arithmetics, logics, and string concatenations
def expressionanalyzer(lineparse, currentsymbols):
    if re.search(regexlist["math"], lineparse) or re.search(regexlist["comp"], lineparse):
        return arithmetics(lineparse, currentsymbols)
    elif re.search(logic["smoosh"], lineparse):
        return stringsconcat(lineparse, currentsymbols)
    else:
        return booleans(lineparse, currentsymbols)

# getting input from user
def gimmeh(lineparse, currentsymbols):
    lex = []
    sym = {}
    readdata = (re.split(regexlist["gimmeh"], lineparse))[-1]
    readdata = readdata.strip(" ")
    readdata = readdata.split(" ")
    if len(readdata) > 1:
        return errorcode["multiplegimmeh"]
    elif readdata[0] == "":  # no variable provided
        return errorcode["missinggimmeh"]
    elif re.search(regexlist["varname"], readdata[0]) and readdata[0] in currentsymbols:
        readdata = readdata[0]
        # Input request via new window: https://stackoverflow.com/questions/51394482/is-it-possible-to-display-python-input-statements-in-tkinter
        codedisplay.configure(state='disabled')     # To avoid editing anything while asking for input
        executedisplay.configure(state='disabled')  # To avoid editing anything while asking for input
        liveInput = sd.askstring("User Input", "Enter value for " + readdata + ":")             # --|
        if liveInput == None:                                                                   #   |
            codedisplay.configure(state='normal')       # Enable fields after asking for input  #   |
            executedisplay.configure(state='normal')    # Enable fields after asking for input  #   |
            return errorcode["noinput"]                                                         #   |
        elif re.search("^" + literals["numbar"] + "$", liveInput):                              #   |
                sym[readdata] = [float(liveInput), "NUMBAR"]                                    #   |    
        elif re.search("^" + literals["numbr"] + "$", liveInput):                               #   |
                sym[readdata] = [int(liveInput), "NUMBR"]                                       #   |--> input asking
        else:                                                                                   #   |--> and typecasting
            outputstr = ""                                                                      #   |
            testsplit = re.split("(\")", liveInput)                                             #   |
            for item in range(0, len(testsplit)):                                               #   |
                if testsplit[item] == "\"":                                                     #   |
                    outputstr += "\\\""                                                         #   |
                else:                                                                           #   |
                    outputstr += testsplit[item]                                                #   |
            sym[readdata] = [outputstr, "YARN"]                                                 # --|
        codedisplay.configure(state='normal')       # Enable fields after asking for input
        executedisplay.configure(state='normal')    # Enable fields after asking for input
        return [[readdata, '"Variable Reference"'], sym]
    else:
        return errorcode["unknownref"] + readdata[0]

# assignment statements
def var_R(lineparse, currentsymbols):
    lex = []
    sym = {}
    readdata = re.split(regexlist["var_assign"], lineparse)
    if len(readdata[0]) == 0:           # missing left statement
        return errorcode["noRleft"]
    elif len(readdata[-1]) == 0:        # missing right statement
            return errorcode["noRRight"]
    else:
        left = re.split(" ", readdata[0].strip(" "))    # --|
        if len(left) > 1:                               #   |--> removes space trails
            return errorcode["manyRleft"]               #   |--> check if it's a single argument
        left = left[0]                                  # --|

        value = readdata[-1].strip(" ") # removes space trails
        if value[0] != "\"" and value[-1] != "\"" and not re.search(expressionregex, value):# --|
            value = re.split(" ", value.strip(" "))                                         #   |--> if it is not a string and it is not an expression 
            if len(value) > 1:                                                              #   |--> remove space trails
                return errorcode["manyRright"]                                              #   |--> and check if it's a single argument
            value = value[0]                                                                # --|

        if re.search(regexlist["varname"], left):   # check if the variable used is existing
            if left in currentsymbols:              # check if the variable is in the symbol table
                if left != "IT":                                                                    # --|
                    lex.append([left, '"Variable Reference"'])                                      #   |
                else:                                                                               #   |--> identify variable for the value
                    lex.append([left, '"Implicit Variable"'])                                       #   |
                lex.append(["R", '"Assignment Operator"'])                                          # --|

                # check for uneven quotation marks
                if value[0] == "\"" or value[-1] == "\"":
                    if value[0] != value[-1]:
                        return errorcode["missingquote"]

                # check for the type of the right hand side
                if re.search(literals["yarn"], value):                                                          # --|
                    outputstr = ""                                  # inclusive of internal double quotes       #   |
                    testsplit = re.split("(\")", value)                                                         #   |
                    if len(testsplit[0]) != 0 or len(testsplit[-1]) != 0:                                       #   |
                        return errorcode["unpairedquotes"]                                                      #   |
                    for item in range(2, len(testsplit) - 2):                                                   #   |
                        if testsplit[item] == "\"":                                                             #   |--> STRINGS
                            outputstr += "\\\""                                                                 #   |--> ( includes internal double quotes )
                        else:                                                                                   #   |
                            outputstr += testsplit[item]                                                        #   |
                    lex.append([value[0], '"String Delimiter"'])                                                #   |
                    lex.append([outputstr, 'Literal'])                                                          #   |
                    lex.append([value[-1], '"String Delimiter"'])                                               #   |
                    sym[left] = [outputstr, "YARN"]                                                             # --|
                elif re.search(expressionregex, value):                                                 # --|
                    result = expressionanalyzer(value, currentsymbols)                                  #   |
                    if isinstance(result, str):                                                         #   |
                        return result                                                                   #   |--> EXPRESSIONS
                    for item in result[1]:                                                              #   |
                        lex.append(item)                                                                #   |
                    sym[left] = result[0]                                                               # --|
                elif re.search("^" + literals["troof"] + "$", value):                           # --|
                    lex.append([value, 'Literal'])                                              #   |--> BOOLEANS
                    sym[left] = [value, "TROOF"]                                                # --|
                elif re.search(regexlist["varname"], value):                            # --|
                    if value in currentsymbols:                                         #   |
                        lex.append([value, '"Variable Reference"'])                     #   |
                        var = currentsymbols[value][0]                                  #   |
                        typestr = str(currentsymbols[value][1])     # remove            #   |--> VARIABLE
                        if re.search(literals["yarn"], str(var)):   # quotation marks   #   |--> REFERENCES
                            var = var[1:-1]                         # if variable value #   |
                        sym[left] = [var, typestr]                  # is string         #   |
                    else:                                                               #   |
                        return errorcode["unknownref"] + value + ".\n"                  # --|
                elif re.search("^" + literals["numbar"] + "$", value):          # --|
                    lex.append([value, 'Literal'])                              #   |--> FLOATS
                    sym[left] = [float(value), "NUMBAR"]                        # --|
                elif re.search("^" + literals["numbr"] + "$", value):   # --|
                    lex.append([value, 'Literal'])                      #   |--> INTEGERS
                    sym[left] = [int(value), "NUMBR"]                   # --|
                else:
                    return errorcode["invalidvalue"] + value
            else:
                return errorcode["unknownref"] + left + ".\n"  #
    return [lex, sym]

# printing
def visible(lineparse, currentsymbols):
    lex = []
    printing = ""   # final string to be printed
    readdata = (re.split(regexlist["visible"], lineparse))[-1]
    if len(readdata) == 0:                  # No arguments
        return errorcode["missingvisible"]  # after visible keyword
    else:
        # check if the yarns in the arguments are valid
        num_quotes = readdata.count("\"")
        if num_quotes % 2 != 0:
            return errorcode["missingquote"]

        # filter out string literals (to be used for comparison later)
        stringliterals = re.findall(literals["yarn"], readdata)      # list of string literals in the arguments
        for s in range(len(stringliterals)):
            # remove unnecessary quotation marks
            stringliterals[s] = stringliterals[s].replace("\"", "")
            if stringliterals[s] in readdata:   # if the string literal filter already matches the one in the original data
                continue
            if stringliterals[s][-1] == " ":    # remove extra space at the send of the string if there are any
                stringliterals[s] = stringliterals[s][:-1]

        readdata = readdata.split("\"")     # remove the quotation marks

        # remove spaces and empty strings sa na-split na list
        readdata = [i for i in readdata if i != " " and i != ""]
        for r in readdata:
            if r in stringliterals:                         # --|
                lex.append(["\"", '"String Delimiter"'])    #   |
                lex.append([r, 'Literal'])                  #   |--> STRINGS
                lex.append(["\"", '"String Delimiter"'])    #   |
                printing += r + " "                         # --|
            else:   # not string literals
                if re.search(expressionregex, r):                   # --|
                    result = expressionanalyzer(r, currentsymbols)  #   |
                    if isinstance(result, str):                     #   |
                        return result                               #   |--> EXPRESSIONS
                    for item in result[1]:                          #   |
                        lex.append(item)                            #   |
                    printing += str(result[0][0]) + " "             # --|
                else:
                    temp_str = r.strip(" ")         # remove unnecessary spaces
                    temp_str = temp_str.split(" ")  # split the variable/boolean int float literals
                    for temp in temp_str:           # iterate through each one
                        if re.search("^" + literals["troof"] + "$", temp):                                  # --|
                            lex.append([temp, 'Literal'])                                                   #   |--> BOOLEAN
                            printing += temp                                                                # --|
                        elif re.search(regexlist["varname"], temp):                                 # --|
                            if temp in currentsymbols:                                              #   |
                                lex.append([temp, '"Variable Reference"'])                          #   |
                                var = str(currentsymbols[temp][0])                                  #   |
                                if re.search(literals["yarn"], var):    # remove quotation marks    #   |--> VARIABLE REFERENCES
                                    var = var[1:-1]                     # # if variable value       #   |
                                printing += var                         # is string                 #   |
                            else:                                                                   #   |
                                return errorcode["unknownref"] + temp + ".\n"                       # --|
                        elif re.search("^" + literals["numbar"] + "$", temp):               # --|
                            lex.append([temp, 'Literal'])                                   #   |--> FLOATS
                            printing += temp                                                # --|
                        elif re.search("^" + literals["numbr"] + "$", temp):        # --|
                            lex.append([temp, 'Literal'])                           #   |--> INTEGERS
                            printing += temp                                        # --|
                        else:
                            return errorcode["invalidvalue"] + temp
                        printing += " "
    printing += "\n"
    return [lex, printing]

# variable declarations
def variabledeclaration(lineparse, currentsymbols):
    lex = []
    sym = {}
    readdata = re.split(regexlist["ihasa"], lineparse)
    if re.search(regexlist["itz"], readdata[1]):            # --|
        readdata = re.split(regexlist["itz"], readdata[1])  #   |
        if len(readdata[1]) == 0:                           #   |
            return errorcode["novalue"] + readdata[0]       #   |--> identify if value is present
    else:                                                   #   |
        readdata = [readdata[1], ""]                        #   |
    readdata[0] = readdata[0].strip(" ")                    # --|
    if re.search(regexlist["varname"], readdata[0]):
        lex.append([readdata[0], '"Variable Identifier"'])
        if len(readdata[1]) == 0:                                   # blank
            sym[readdata[0]] = ["", "NOOB"]                         # initializatons
        else:
            lex.append(["ITZ", '"Variable Assignment"'])
            if re.search(expressionregex, readdata[1]):                                     # --|
                result = expressionanalyzer(readdata[1], currentsymbols)                    #   |
                if isinstance(result, str):                                                 #   |
                    return result                                                           #   |--> expression assignment
                for item in result[1]:                                                      #   |
                    lex.append(item)                                                        #   |
                sym[readdata[0]] = result[0]                                                # --|
            elif re.search(literals["yarn"], readdata[1]):                                              # --|
                outputstr = ""                                                                          #   |
                testsplit = re.split("(\")", readdata[1])                                               #   |
                if len(testsplit[0]) != 0 or len(testsplit[-1]) != 0:                                   #   |
                    return errorcode["unpairedquotes"]                                                  #   |
                for item in range(2, len(testsplit) - 2):                                               #   |
                    if testsplit[item] == "\"":                                                         #   |--> string
                        outputstr += "\\\""                                                             #   |--> assignment
                    else:                                                                               #   |
                        outputstr += testsplit[item]                                                    #   |
                lex.append([readdata[1][0], '"String Delimiter"'])                                      #   |
                lex.append([outputstr, 'Literal'])                                                      #   |
                lex.append([readdata[1][-1], '"String Delimiter"'])                                     #   |
                sym[readdata[0]] = [outputstr, "YARN"]                                                  # --|
            elif re.search("^" + literals["troof"] + "$", readdata[1]):                         # --|
                lex.append([readdata[1], 'Literal'])                                            #   |--> boolean assignment
                sym[readdata[0]] = [(readdata[1]), "TROOF"]                                     # --|
            elif re.search(regexlist["varname"], readdata[1]):                          # --|
                if readdata[1] in currentsymbols:                                       #   |
                    lex.append([readdata[1], '"Variable Reference"'])                   #   |--> variable reference
                    sym[readdata[0]] = currentsymbols[readdata[1]]                      #   |--> assignment
                else:                                                                   #   |
                    return errorcode["unknownref"] + readdata[1] + ".\n"                # --|
            elif re.search("^" + literals["numbar"] + "$", readdata[1]):        # --|
                lex.append([readdata[1], 'Literal'])                            #   |--> float assignment
                sym[readdata[0]] = [float(readdata[1]), "NUMBAR"]               #   |
            elif re.search("^" + literals["numbr"] + "$", readdata[1]): # --|
                    lex.append([readdata[1], 'Literal'])                #   |--> integer assignment
                    sym[readdata[0]] = [int(readdata[1]), "NUMBR"]      # --|
            else:
                return errorcode["invalidvalue"] + readdata[1]
        return [lex, sym]
    else:
        return errorcode["wrongvarname"] + readdata[0] + ".\n"      # for unqualified variable names

# interpeter for ignored lines inside if-else/switch blocks
def linelexer(line, symbolgroup):
    lexemegroup = []
    if re.search(regexlist["ihasa"], line):                         # --|
        return errorcode["notvardec"]                               #   |--> variable declarations
    elif re.search(regexlist["visible"], line):                             # --|
        lexemegroup.append(["VISIBLE", '"Function Identifier"'])            #   |
        result = visible(line, symbolgroup)                                 #   |
        if isinstance(result, str):                                         #   |
            return result                                                   #   |
        for item in result[0]:                                              #   |
            lexemegroup.append(item)                                        #   |
    elif re.search(regexlist["gimmeh"], line):                                      # --|
        lexemegroup.append(["GIMMEH", '"Function Identifier"'])                     #   |
        result = gimmeh(line, symbolgroup)                                          #   |
        if isinstance(result, str):                                                 #   |
            return result                                                           #   |
        lexemegroup.append(result[0])                                               #   |
    elif re.search(expressionregex, line):                              # --|
        result = expressionanalyzer(line, symbolgroup)                  #   |
        if isinstance(result, str):                                     #   |
            return result                                               #   |--> expression
        for item in result[1]:                                          #   |
            lexemegroup.append(item)                                    #   |
    elif re.search(regexlist["var_assign"], line):                          # --|
        result = var_R(line, symbolgroup)                                   #   |
        if isinstance(result, str):                                         #   |
            return result                                                   #   |--> variable
        for item in result[0]:                                              #   |--> assignment
            lexemegroup.append(item)                                        #   |
    elif re.search(regexlist["ifblock"], line) or re.search(regexlist["switchblock"], line) or re.search(regexlist["if"], line) or re.search(regexlist["else"], line) or re.search(regexlist["case"], line) or re.search(regexlist["break"], line) or re.search(regexlist["default"], line):
        # IGNORE THE KEYWORDS OF IF-ELSE/SWITCH CLAUSES
        return lexemegroup
    else:                                                       # --|
        executedisplay.insert(tk.INSERT, line + "\n")           #   |--> unrecognized command
        return errorcode["unreqcomm"]                           # --|
    return lexemegroup

# if-else control flow
def ifelseblock(programline, index, currentsymbol):
    if currentsymbol["IT"] == ["", ""]:    # if the IT variable is empty
        return [errorcode["itemptyerror"], index]
    if not re.search(literals["troof"], str(currentsymbol["IT"][0])):    # if the preceding line does not result to the type TROOF
        return [errorcode["conditionerror"], index]

    lex = []
    condition = currentsymbol["IT"][0]  # check the condition
    lex.append(["O RLY?", '"Function Identifier"'])

    blockrange = []         # this list contains the lines that will be ignored
    blockindex = index + 1  # starting index
    with_if = False         # flag if the YA RLY is encountered
    with_else = False       # flag if the NO WAI is encountered
    skip_ignore = True      # flag whether the lines will not be added to the ignored list

    while True:
        try:
            lineread = programline[blockindex]
        except IndexError:
            return [errorcode["noOIC"], blockindex]

        # check if the starting block is not the YA RLY keyword
        if not re.search(regexlist["if"], lineread) and blockindex == index + 1:
            return [errorcode["noYARLY"], blockindex]

        # REAL IF ELSE STARTS HERE
        if condition != "WIN":  # check if the condition is false, skip the WHOLE IF BLOCK
            if re.search(regexlist["if"], lineread):  # START OF IF BLOCK ( THIS WILL NOT BE EXECUTED )
                if with_if:     # check if YA RLY already exists in the block
                    return [errorcode["multiYARLY"], blockindex]
                lex.append(["YA RLY", '"Function Identifier"'])     # this means that the NO WAI block is executed
                # trigger the flags
                with_if = True
                skip_ignore = False
            elif re.search(regexlist["else"], lineread):  # END OF IF BLOCK
                if with_else:   # check if NO WAI already exists in the block
                    return [errorcode["multiNOWAI"], blockindex]
                lex.append(["NO WAI", '"Function Identifier"'])
                blockrange.append(blockindex)   # include NO WAI to the ignored list
                # trigger flags
                with_else = True
                skip_ignore = True
            elif re.search(regexlist["blockend"], lineread):  # END OF WHOLE BLOCK
                break
            elif re.search(regexlist["ifblock"], lineread):  # another ORLY? is encountered
                return [errorcode["multiorly"], blockindex]
            else:
                if not skip_ignore:    # append the line indices between the if block
                    # GET THE LEXEMES OF THE SKIPPED LINES
                    result = linelexer(lineread, currentsymbol)
                    if isinstance(result, str):
                        return [result, blockindex]
                    for item in result:
                        lex.append(item)
                    blockrange.append(blockindex)
        else:
            if re.search(regexlist["if"], lineread):  # START OF IF BLOCK
                if with_if:  # check if YA RLY already exists in the block
                    return [errorcode["multiYARLY"], blockindex]
                lex.append(["YA RLY", '"Function Identifier"'])
                # trigger the flags
                with_if = True
            elif re.search(regexlist["else"], lineread):  # START OF ELSE BLOCK ( THIS WILL NOT BE EXECUTED )
                if with_else:
                    return [errorcode["multiNOWAI"], blockindex]
                blockrange.append(blockindex)
                with_else = True
                lex.append(["NO WAI", '"Function Identifier"'])
                skip_ignore = False
            elif re.search(regexlist["blockend"], lineread):  # END OF ELSE AND WHOLE BLOCK
                break
            elif re.search(regexlist["ifblock"], lineread):  # another ORLY? is encountered
                return [errorcode["multiorly"], blockindex]
            else:
                if not skip_ignore:       # append the line indices between the else block
                    # GET THE LEXEMES OF THE SKIPPED LINES
                    result = linelexer(lineread, currentsymbol)  # |
                    if isinstance(result, str):
                        return [result, blockindex]
                    for item in result:
                        lex.append(item)
                    blockrange.append(blockindex)
        blockindex += 1

    if not with_else:
        return [errorcode["noNOWAI"], blockindex]

    return [lex, blockrange]

# switch control flow
def switchcaseblock(programline, index, currentsymbols):
    if currentsymbols["IT"] == ["", ""]:    # if the IT variable is empty
        return [errorcode["itemptyerror"], index]

    lex = [["WTF?", '"Function Identifier"']]
    condition = currentsymbols["IT"][0]     # check the condition
    blockrange = []                         # this list contains the lines that will be ignored by the interpreter
    blockindex = index + 1                  # starting index
    omgval = None           # value of the cases
    gtfo_flag = False       # flag if the GTFO is encountered
    condition_met = False   # flag if the condition is met
    with_default = False    # flag whether the switch block contains the OMGWTF block
    skip_ignore = False     # flag whether the lines will not be added to the ignored list

    while True:
        not_yarn = False   # flag if the case is purely YARN
        try:
            lineread = programline[blockindex]
        except IndexError:
            return [errorcode["noOIC"], blockindex]

        # check if the starting block is not the OMG keyword
        if not re.search(regexlist["case"], lineread) and blockindex == index + 1:
            return [errorcode["noomg"], blockindex]

        # GET THE VALUE OF THE CASE STATEMENT
        if re.search(regexlist["case"], lineread):
            lex.append(["OMG", '"Function Identifier"'])
            value = re.split(regexlist["case"], lineread)[-1]   # filter out the case value

            if len(value) == 0:                     # check if the value is missing
                return [errorcode["missingcasevalue"], blockindex]
            value = value.strip(" ")

            troof = re.search(literals["troof"], value) # check if the value is a TROOF literal
            try_check = True if value.count("\"") == 2 and value[0] == "\"" and value[-1] == "\"" else False    # check if the value is a proper YARN
            if not try_check and not troof: # if not a YARN and a TROOF
                not_yarn = True
                value = value.split(" ")    # split the value

            # These cases check the arity of the case arguments
            if not_yarn and len(value) > 1:
                return [errorcode["multicasevalue"], blockindex]
            elif not_yarn and len(value) < 1:
                return [errorcode["missingcasevalue"], blockindex]
            else:
                if not_yarn and not troof:  # if not YARN and TROOF, the value is a list due to split
                    value = value[0]
                temp = value

                # check for uneven quotation marks
                if temp[0] == "\"" or temp[-1] == "\"":
                    if temp[0] != temp[-1]:
                        return [errorcode["missingquote"], blockindex]

                # check the data type of the case value
                if re.search(literals["yarn"], temp):       # STRING LITERAL
                    lex.append([str(temp), 'Literal'])
                    omgval = str(temp)
                elif re.search(literals["troof"], temp):    # BOOLEAN LITERAL
                    if re.search("^((NOT)?(WIN)|(FAIL))$", temp):
                        if temp == "NOT WIN":
                            temp = "FAIL"
                        elif temp == "NOT FAIL":
                            temp = "WIN"  #
                        lex.append([temp, 'Literal'])
                        omgval = temp
                    else:
                        return [errorcode["invalidcase"] + str(temp) + "\n", blockindex]
                elif re.search(regexlist["varname"], temp):     # VARIABLE NAME
                    return [errorcode["invalidliteral"] + temp, blockindex]
                elif re.search(literals["numbar"], temp):       # FLOATING POINT LITERAL
                    if re.search("^\-?[0-9]*\.[0-9]+$", temp):
                        lex.append([float(temp), 'Literal'])
                        omgval = float(temp)
                    else:
                        return [errorcode["invalidcase"] + str(temp) + "\n", blockindex]
                elif re.search(literals["numbr"], temp):        # INTEGER LITERAL
                    if re.search("^\-?[0-9]+$", temp):
                        lex.append([int(temp), 'Literal'])
                        omgval = int(temp)
                    else:
                        return [errorcode["invalidcase"] + str(temp) + "\n", blockindex]
                else:
                    return [errorcode["invalidcase"] + str(temp) + "\n", blockindex]

        # THE REAL SWITCH CASE STARTS HERE
        if condition == omgval:     # check if the case value is equal to the value of IT variable
            condition_met = True    # trigger flag
            if re.search(regexlist["case"], lineread) or re.search(regexlist["default"], lineread):  # START OF CASE BLOCK
                blockrange.append(blockindex)       # include the OMG and OMGWTF keywords in the ignored list
            elif re.search(regexlist["break"], lineread):       # IF A BREAK IS ENCOUNTERED
                lex.append(["GTFO", '"Function Identifier"'])
                gtfo_flag = True
                blockrange.append(blockindex)   # include GTFO keyword in the ignored list
            elif re.search(regexlist["blockend"], lineread):  # END OF WHOLE SWITCH BLOCK
                break
            elif re.search(regexlist["switchblock"], lineread):  # another WTF? is encountered
                return [errorcode["multiwtf"], blockindex]
        else:   # for other cases
            # checker if the case that matched the value of IT does not have GTFO (break)
            if condition_met and not gtfo_flag:
                skip_ignore = True
            if condition_met and gtfo_flag:
                skip_ignore = False

            if re.search(regexlist["case"], lineread):      # START OF CASE BLOCK
                if with_default:    # if OMGWTF is already encountered
                    return [errorcode["nowtf"], blockindex]
                blockrange.append(blockindex)
            elif re.search(regexlist["default"], lineread): # START OF DEFAULT BLOCK
                if with_default:    # if OMGWTF is already in the block
                    return [errorcode["multiOMGWTF"], blockindex]
                blockrange.append(blockindex)   # include OMGWTF in the ignored list
                lex.append(["OMGWTF", '"Function Identifier"'])
                # trigger the flags
                with_default = True
                skip_ignore = True
            elif re.search(regexlist["break"], lineread):  # IF THE BREAK IS ENCOUNTERED
                blockrange.append(blockindex)
                lex.append(["GTFO", '"Function Identifier"'])
                if condition_met:   # if the GTFO is not on the matching case
                    gtfo_flag = True
            elif re.search(regexlist["blockend"], lineread):  # END OF WHOLE BLOCK
                break
            elif re.search(regexlist["switchblock"], lineread):  # another WTF? is encountered
                return [errorcode["multiwtf"], blockindex]
            if not skip_ignore: # if the lines in between keywords are not to be executed
                # GET THE LEXEMES OF THE IGNORED LINES
                result = linelexer(lineread, currentsymbols)
                if isinstance(result, str):
                    return [result, blockindex]
                for item in result:
                    lex.append(item)
                blockrange.append(blockindex)
        blockindex += 1

    if not with_default:    # if the default block does not exist
        return [errorcode["missingdefault"], blockindex]

    return [lex, blockrange]

# main program interpreter
def lineinterpreter(perlineprogram, lexemegroup, symbolgroup):
    lineindex = 0
    jumps = []
    while True:
        if lineindex in jumps:  # do not read the line if it is in the jump list
            lineindex += 1
            continue
        try:
            line = perlineprogram[lineindex]
        except IndexError:
            lexemegroup.append(["KTHXBYE", '"Code Delimiter"'])
            return [lexemegroup, symbolgroup]
        if re.search(regexlist["ihasa"], line):                         # --|
            if len(jumps) != 0:                                         #   |
                return errorcode["notvardec"]                           #   |
            lexemegroup.append(["I HAS A", '"Variable Declaration"'])   #   | 
            result = variabledeclaration(line, symbolgroup)             #   | 
            if isinstance(result, str):                                 #   | 
                executedisplay.insert(tk.INSERT, line + "\n")           #   | 
                return result                                           #   |--> variable declarations 
            for item in result[0]:                                      #   | 
                lexemegroup.append(item)                                #   | 
            for key, value in result[1].items():                        #   | 
                symbolgroup[key] = value                                #   | 
            lineindex += 1                                              # --| 
        elif re.search(regexlist["visible"], line):                             # --|
            lexemegroup.append(["VISIBLE", '"Function Identifier"'])            #   |
            result = visible(line, symbolgroup)                                 #   |
            if isinstance(result, str):                                         #   |
                executedisplay.insert(tk.INSERT, line + "\n")                   #   |--> printing
                return result                                                   #   |--> in terminal
            for item in result[0]:                                              #   |
                lexemegroup.append(item)                                        #   |
            executedisplay.insert(tk.INSERT, result[1])                         #   |
            lineindex += 1                                                      # --|
        elif re.search(regexlist["gimmeh"], line):                                      # --|
            lexemegroup.append(["GIMMEH", '"Function Identifier"'])                     #   |
            result = gimmeh(line, symbolgroup)                                          #   |
            # print("--------", result[0], " >><<", result[1]) # DEBUG LINE             #   |
            if isinstance(result, str):                                                 #   |
                executedisplay.insert(tk.INSERT, line + "\n")                           #   |--> user input
                return result                                                           #   |
            lexemegroup.append(result[0])                                               #   |
            for key, value in result[1].items():                                        #   |
                symbolgroup[key] = value                                                #   |
            lineindex += 1                                                              # --|
        elif re.search(expressionregex, line):                              # --|
            result = expressionanalyzer(line, symbolgroup)                  #   |
            if isinstance(result, str):                                     #   |
                executedisplay.insert(tk.INSERT, line + "\n")               #   |
                return result                                               #   |--> expression
            # print("OUT RESULT", result) # DEBUG LINE                      #   |--> evaluation (stored into IT)
            for item in result[1]:                                          #   |
                lexemegroup.append(item)                                    #   |
            symbolgroup["IT"] = result[0]                                   #   |
            lineindex += 1                                                  # --|
        elif re.search(regexlist["ifblock"], line):                                             # --|
            result = ifelseblock(perlineprogram, lineindex, symbolgroup)                        #   |
            if isinstance(result[0], str):                                                      #   |
                try:                                                                            #   |
                    executedisplay.insert(tk.INSERT, perlineprogram[result[1]] + "\n")          #   |
                except IndexError:                                                              #   |
                    executedisplay.insert(tk.INSERT, perlineprogram[result[1]-1] + "\n")        #   |
                return result[0]                                                                #   |--> if-else blocks
            for item in result[0]:                                                              #   |
                lexemegroup.append(item)                                                        #   |
            jumps = result[1]                                                                   #   |
            lineindex += 2                                                                      # --|
        elif re.search(regexlist["switchblock"], line):                                                 # --|
            result = switchcaseblock(perlineprogram, lineindex, symbolgroup)                            #   |
            if isinstance(result[0], str):                                                              #   |
                try:                                                                                    #   |
                    executedisplay.insert(tk.INSERT, perlineprogram[result[1]] + "\n")                  #   |
                except IndexError:                                                                      #   |
                    executedisplay.insert(tk.INSERT, perlineprogram[result[1]-1] + "\n")                #   |
                return result[0]                                                                        #   |--> switch block
            for item in result[0]:                                                                      #   |
                lexemegroup.append(item)                                                                #   |
            jumps = result[1]                                                                           #   |
            lineindex += 1                                                                              # --|
        elif re.search(regexlist["if"], line):                                                  # --|
            executedisplay.insert(tk.INSERT, line + "\n")                                       #   |
            return errorcode["noORLY"]                                                          #   |--> invalid keywords
        elif re.search(regexlist["case"], line) or re.search(regexlist["default"], line):       #   |--> outside blocks
            executedisplay.insert(tk.INSERT, line + "\n")                                       #   |
            return errorcode["nowtf"]                                                           # --|
        elif re.search(regexlist["blockend"], line):                                    # --|
            if len(jumps) == 0:                                                         #   |
                executedisplay.insert(tk.INSERT, line + "\n")                           #   |
                return errorcode["loneOIC"]                                             #   |--> block termination
            lexemegroup.append(["OIC", '"Function Identifier"'])                        #   |
            jumps.clear()                                                               #   |
            lineindex += 1                                                              # --|
        elif re.search(regexlist["var_assign"], line):                          # --|
            result = var_R(line, symbolgroup)                                   #   |
            if isinstance(result, str):                                         #   |
                executedisplay.insert(tk.INSERT, line + "\n")                   #   |
                return result                                                   #   |--> variable
            for item in result[0]:                                              #   |--> assignment
                lexemegroup.append(item)                                        #   |
            for key, value in result[1].items():                                #   |
                symbolgroup[key] = value                                        #   |
            lineindex += 1                                                      # --|
        else:                                                       # --|
            executedisplay.insert(tk.INSERT, line + "\n")           #   |--> unrecognized command
            return errorcode["unreqcomm"]                           # --|
    return [lexemegroup, symbolgroup]

# starting function call, includes comment and excess whitespace removals, code delimiter verifications, and lexeme table & symbol table updates
def executeprogram():
    # content acquiring: https://stackoverflow.com/questions/53937400/how-to-get-the-text-out-of-a-scrolledtext-widget
    executedisplay.configure(state='normal')
    executedisplay.delete('1.0', tk.END)
    rawtextinput = codedisplay.get("1.0", tk.END)
    lexemegroup = []    # overall lexeme collector
    symbolgroup = {}    # overall symbol collector
    symbolgroup["IT"] = ["", ""]        # implicit IT declaration
    # string "***" is sourced from the file error string
    # program is split with newline char as separator
    if len(rawtextinput) - 1 != 0 and rawtextinput[0:3] != "***":
        perlineprogram = rawtextinput.split("\n")
        multiline = []
        unpaired = False
        for line in range(0, len(perlineprogram)):                                      # --|
            if re.search(regexlist["spaces"], perlineprogram[line]):                    #   |
                perlineprogram[line] = ""                                               #   |
            elif len(multiline) != 0:                                                   #   |
                if re.search(regexlist["tldr"], perlineprogram[line]):                  #   |
                    multiline.pop(-1)                                                   #   |--> comment stripper:
                perlineprogram[line] = ""                                               #   |--> transforms comments
            elif re.search(regexlist["tldr"], perlineprogram[line]):                    #   |--> ( single line, multiline, inline )
                unpaired = True                                                         #   |--> and whitespace lines
                break                                                                   #   |--> into lines
            elif re.search(regexlist["obtw"], perlineprogram[line]):                    #   |--> with no content at all (len 0)
                multiline.append(line)                                                  #   |
                perlineprogram[line] = ""                                               #   | 
            elif re.search(regexlist["btw"], perlineprogram[line]):                     #   |
                splitcomment = re.split(regexlist["btw"], perlineprogram[line])         #   |
                perlineprogram[line] = splitcomment[0]                                  # --|
        if unpaired:                                                                                        # --|
            executedisplay.insert(tk.INSERT, errorcode["nopairTLDR"])                                       #   |--> commenting
        elif len(multiline) != 0:                                                                           #   |--> errors
            executedisplay.insert(tk.INSERT, "Warning: Unpaired OBTW at line " + str(multiline[0] + 1))     # --|
        else:
            haistart = -1
            kthx_end = 0
            poplist = []
            doublehai = False
            doublektx = False
            for line in range(0, len(perlineprogram)):                                                  # --|
                if len(perlineprogram[line]) == 0:                                                      #   |
                    poplist.append(line)                                                                #   |
                elif re.search(regexlist["hai"], perlineprogram[line]):                                 #   |
                    if haistart == -1:                                                                  #   |
                        lexemegroup.append(["HAI", '"Code Delimiter"'])                                 #   |--> code
                        haistart = line                                                                 #   |--> delimiter
                    else:                                                                               #   |--> verifiers
                        doublehai = True                                                                #   |--> and
                        break                                                                           #   |--> error
                elif haistart != -1 and re.search(regexlist["kthxbye"], perlineprogram[line]):          #   |--> checking
                    if kthx_end == 0:                                                                   #   |
                        kthx_end = line                                                                 #   |
                    else:                                                                               #   |
                        doublektx = True                                                                #   |
                        break                                                                           # --|
            if doublehai:                                                   # --|
                executedisplay.insert(tk.INSERT, errorcode["dblHAI"])       #   |
            elif doublektx:                                                 #   |
                executedisplay.insert(tk.INSERT, errorcode["dblKTHXBYE"])   #   |--> program delimiter
            elif haistart == -1:                                            #   |--> errors
                executedisplay.insert(tk.INSERT, errorcode["noHAI"])        #   |
            elif kthx_end == 0:                                             #   |
                executedisplay.insert(tk.INSERT, errorcode["noKTHXBYE"])    # --|
            else:
                for line in range(len(poplist) - 1, -1, -1):        # --| 
                    perlineprogram.pop(poplist[line])               #   |--> actual line removals of comments and whitespace lines
                    value = poplist.pop(line)                       # --| 
                perlineprogram.pop(0)
                perlineprogram.pop(-1)
                result = lineinterpreter(perlineprogram, lexemegroup, symbolgroup)
                if isinstance(result, str):
                    executedisplay.insert(tk.INSERT, result)
                else:
                    [lexemegroup, symbolgroup] = result
    # a file error has occurred
    else:
        executedisplay.insert(tk.INSERT, "*** Please load a valid file before executing ***")
    # execute display is disabled to avoid editing
    executedisplay.configure(state='disabled')
    # clearing the tables: https://stackoverflow.com/questions/22812134/how-to-clear-an-entire-treeview-with-tkinter
    # Treeview/Listing updating
    for i in lexemedisplay.get_children():      # --|
        lexemedisplay.delete(i)                 #   |--> clearing previous
    for i in symboldisplay.get_children():      #   |--> lexeme and symbol entries
        symboldisplay.delete(i)                 # --|
    for item in range(0, len(lexemegroup)):                                                                             # --|
        lexemedisplay.insert(parent='', index=item, iid=item, text=lexemegroup[item][0], values=(lexemegroup[item][1])) #   |
    iterate_id = 0                                                                                                      #   |--> putting new entries
    for key, value in symbolgroup.items():                                                                              #   |--> to the table
        symboldisplay.insert(parent='', index=iterate_id, iid=iterate_id, text=key, values=(value[0]))                  #   |
        iterate_id += 1                                                                                                 # --|

# execute button
executebutton = tk.Button(projectwindow, image=exec_bt, height=20, borderwidth=0, bg="#F000FF", activebackground="#FFE700", command=executeprogram)
def exec_enter(e):
    executebutton['background'] = "#FF0101"
    executebutton['image'] = exec_bt
def exec_leave(e):
    executebutton['background'] = "#F000FF"
    executebutton['image'] = exec_bt
def exec_click(e):
    executebutton['image'] = exec_ac
def exec_done(e):
    executebutton['image'] = exec_bt
executebutton.bind("<Enter>", exec_enter)
executebutton.bind("<Leave>", exec_leave)
executebutton.bind("<ButtonPress>", exec_click)
executebutton.bind("<ButtonRelease>", exec_done)

# widget placements and spacing
header.grid(          column=0, row=0, columnspan=6)
filhead.grid(         column=0, row=1, columnspan=2,                              sticky="NSW")
lexhead.grid(         column=2, row=1, columnspan=2,                              sticky="NSW")
symhead.grid(         column=4, row=1, columnspan=2,                              sticky="NSW")
filenamerawinput.grid(column=0, row=2,                          padx=10,          sticky="NSEW")
fileuploadbutton.grid(column=1, row=2,                          padx=10,          sticky="E")
codedisplay.grid(     column=0, row=3, columnspan=2,            padx=10, pady=10, sticky="NSEW")
lexemedisplay.grid(   column=2, row=2, columnspan=2, rowspan=2, padx=5,  pady=10, sticky="NSEW")
symboldisplay.grid(   column=4, row=2, columnspan=2, rowspan=2, padx=10, pady=10, sticky="NSEW")
outhead.grid(         column=0, row=4,                                            sticky="NSW")
executebutton.grid(   column=1, row=4, columnspan=5,            padx=12, pady=5,  sticky="NSE")
executedisplay.grid(  column=0, row=5, columnspan=6,            padx=10, pady=10, sticky="NSEW")

projectwindow.grid_columnconfigure(0, weight = 1)
projectwindow.grid_columnconfigure(1, weight = 1)
projectwindow.grid_columnconfigure(2, weight = 1)
projectwindow.grid_columnconfigure(3, weight = 1)
projectwindow.grid_columnconfigure(4, weight = 1)
projectwindow.grid_columnconfigure(5, weight = 1)
projectwindow.grid_rowconfigure(3, weight = 1)
projectwindow.grid_rowconfigure(5, weight = 1)
projectwindow.mainloop()