# Time laps app
# by H.K
# hope you enjoy it
# toDo: add save setting and load from it
# toDo: add  tab to change app theme 
import PySimpleGUI as sg # GUI
import pyautogui as sc  # screen shot
import threading    # multi threading
import time # unix time
import cv2 # image to video
#import numpy as np 
import glob # for opencv
from pathlib import Path # creat new path and folders

apptitle = "T-lapse it"
imgloc = "" # image save location
imglocsave = ""
vidloc = "" # video save location
vidlocsave = ""
interval = 22 # time between two sc
hour = 0
min = 1
sec = 0
lsec = 0 # last second
#wt = 0
totalsc = 0     # total screen shots
scnumber = 0    # screen shot number 0 to totalsc
seconds = 0     # total seconds of programm
clength = str(hour) + ":" + str(min) + ":" + str(sec)   # clip length
wlength = str(hour) + ":" + str(min) + ":" + str(sec)   # work length
fps = 0     
#cmode = ""
#name = "SayMyName" # default name for video clips
name =  str(time.ctime())   # default name for video clips
name = name.replace(":","-") # : cant be in name
vidfrmt = ""    # video format
imgfrmt = ""    #img format
utimer = ""
dtimer = ""
x , y = sg.Window.get_screen_size()
boolsec = True #second counter
up = True # is updating times?

start_time, current_time, remaining_time, paused_time, paused = 0, 0, 0, 0, True # for timers

Swstat = {  #radio-b. states
    '-R1-' : True,
    '-R2-' : False,
    '-R3-' : False,
    'videocheck' : False
}
	
sg.theme("Reddit")  # select theme

def Make_Window1():
    layout = [[sg.Text("Choose your mode:")], 
                    [sg.Radio("Infinit capture", "CaptureMode", default=True, size=(10,1), k='-R1-',enable_events=True),
                    sg.Radio('Clip limit', "CaptureMode", size=(10,1), k='-R2-',enable_events=True), 
                    sg.Radio('Work limit', "CaptureMode", size=(10,1), k='-R3-',enable_events=True)],
                    [sg.Col([
                        [sg.Text("Interval(second):"), sg.InputText("10",k="-interval-",s=10,change_submits=True), sg.Text("*",text_color="Red",visible=False,k="-et1-")],
                        [sg.Col([
                            [sg.Text("Save images in:"),sg.Button("Browse",k="-BrowseImg1-"),sg.Text("Format:"),
                             sg.Combo(values=("png","jpeg","bmp"),default_value="png",k="-imgformatcombo1-",size=12, enable_events=True)]
                            ],k="-colu5-", visible = False), sg.Canvas(size=(0,0), pad=(0,0))],
                        ],k="-colu1-",visible=True), sg.Canvas(size=(0,0), pad=(0,0))],

                    [sg.Col([
                        [sg.Text("Clip lentgh(h/m/s):"),sg.InputText(hour,k="-hour-",s=5, change_submits=True),
                        sg.InputText(min,k="-min-",s=5, change_submits=True),sg.InputText(sec,k="-sec-",s=5, change_submits=True),
                        sg.Text("*",text_color="Red",visible=False,k="-et2-")],
                    [sg.Text("Clip FPS:"),sg.Combo(values=("5","10","12","15","20","24","25","30","60"),default_value="12",size=15,k="-fpsCombo2-",enable_events=True,readonly=True)],
                    [sg.Text("Interval(second):"),sg.InputText("22", k="-interval2-", s=10, readonly=False, enable_events=True), sg.Text("*",text_color="Red",visible=False,k="-et5-")],
                    [sg.Text("Total time = "),sg.Text(text = "", k="-wt1-")],
                    [sg.Col([
                        [sg.Text("Save images in:"),sg.Button("Browse",k="-BrowseImg2-"),sg.Text("Format:"),
                         sg.Combo(values=("png","jpeg","bmp"),default_value="png",k="-imgformatcombo2-",size=12, enable_events=True)]
                        ],k="-colu6-", visible = False), sg.Canvas(size=(0,0), pad=(0,0))],
                    ],k="-colu2-",visible=False), sg.Canvas(size=(0,0), pad=(0,0))],

                    [sg.Col([
                        [sg.Text("Work lentgh(h/m/s):"),sg.InputText("1",k="-wlhour-",s=5, change_submits=True),
                        sg.InputText("0",k="-wlmin-",s=5, change_submits=True),sg.InputText("0",k="-wlsec-",s=5, change_submits=True),
                        sg.Text("*",text_color="Red",visible=False,k="-et3-")],
                        [sg.Text("Clip FPS:"),sg.Combo(values=("5","10","12","15","20","24","25","30","60"),default_value="12",size=12,k="-fpsCombo3-",enable_events=True,readonly=True)],
                        [sg.Text("Clip lentgh(h/m/s):"),sg.InputText("0",k="-chour-",s=5,readonly=True),
                        sg.InputText("0",k="-cmin-",s=5,readonly=True),sg.InputText("0",k="-csec-",s=5,readonly=True)],
                        [sg.Text("Interval(second):"),sg.InputText("22",k="-interval3-",s=10,readonly=False,enable_events=True), sg.Text("*",text_color="Red",visible=False,k="-et6-")],
                        [sg.Col([
                            [sg.Text("Save images in:"),sg.Button("Browse",k="-BrowseImg3-"),sg.Text("Format:"),sg.Combo(values=("png","jpeg","bmp"),default_value="png",k="-imgformatcombo3-",size=12, enable_events=True)]
                            ],k="-colu7-", visible = False), sg.Canvas(size=(0,0), pad=(0,0))],
                        ],k="-colu3-",visible=False), sg.Canvas(size=(0,0), pad=(0,0))],

                    [sg.Checkbox("Creat final clip",default=True,k="-videocheck-",visible=True,enable_events=True), sg.Canvas(size=(0,0), pad=(0,0))],
                    [sg.Col([
                        [sg.Text("Video format:"),sg.Combo(values=("mp4","avi"),default_value="mp4",k="-clipformat-",size=10,enable_events=True,readonly=True)],
                        [sg.Col([[sg.Text("Video FPS:"),sg.Combo(values=("5","10","12","15","20","24","25","30","60"),default_value="12",size=15,k="-fpsCombo1-",enable_events=True,readonly=True), ]], k="-colu8-",visible=True ),sg.Canvas(size=(0,0), pad=(0,0))],
                        [sg.Text("Enter name:"),sg.InputText(default_text=name,k="-clipname-",size=30),sg.Text("*",text_color="Red",visible=False,k="-et4-")],
                        [sg.Text("Save file in:"),sg.Button("Browse",k="-BrowseVideo-")],
                        [sg.Checkbox("Delete images after clip creation",default=False,k="-videocheck-",disabled=True)]
                        ],k="-colu4-",visible=True), sg.Canvas(size=(0,0), pad=(0,0))],

                    [sg.Button("Next",k="-Next-"), sg.Button("Save setting",k="-SSetting-",disabled=True), sg.Button("Load Setting",k="-LSetting-",disabled=True), sg.Button("Default",k="-default-",disabled=True), sg.Button("Cancel",k="-Exit-")]]      
    
    return sg.Window(apptitle, layout, keep_on_top=True, finalize=True)

def Make_Window2():
    layout = [[sg.Text("Review setting")],
              [],
                [sg.Col([ # if R1 selected
                    [sg.Text("capture mode: Infinit Capture")],
                    [sg.Text("Interval"), sg.Text(str(interval)), sg.Text("s")],
                    [sg.Col([   # without final clip making - only image
                        [sg.Text("Image format:"), sg.Text(imgfrmt)],
                        [sg.Multiline("Image save location: "+ imgloc + "/", s=(25,5))],
                        [sg.Checkbox("Creat final clip",default=False, disabled=True)]
                            ],k="2colu42",visible=not Swstat["videocheck"]), sg.Canvas(size=(0,0), pad=(0,0))],
                    [sg.Col([ # with final clip making
                        [sg.Checkbox("Creat final clip",default=True, disabled=True)],
                        [sg.Text("Clip format:"), sg.Text(vidfrmt)],
                        [sg.Text("Clip FPS:"), sg.Text(fps)],
                        [sg.Text("Interval:"), sg.Text(interval)],
                        [sg.Multiline("video save location: "+ vidloc + "/" + name + "." + vidfrmt, s=(25,5))]
                            ],k="2colu52",visible=Swstat["videocheck"]), sg.Canvas(size=(0,0), pad=(0,0))]
                ],k="2colu12",visible=Swstat["-R1-"]), sg.Canvas(size=(0,0), pad=(0,0))],
                [sg.Col([ # if R2 selected
                    [sg.Text("capture mode: Clip limit")],
                    [],
                    [sg.Col([ # without final clip making - only image
                        [sg.Text("Image format:"), sg.Text(imgfrmt)],
                        [sg.Text("Interval:"), sg.Text(interval)],
                        [sg.Multiline("Image save location: "+ imgloc + "/", s=(25,5))],
                        [sg.Checkbox("Creat final clip",default=False, disabled=True)]
                            ],k="2colu62",visible=not Swstat["videocheck"]), sg.Canvas(size=(0,0), pad=(0,0))],
                    [sg.Col([ # with final clip making
                        [sg.Checkbox("Creat final clip",default=True, disabled=True)],
                        [sg.Text("Clip format:"), sg.Text(vidfrmt)],
                        [sg.Text("Clip FPS:"), sg.Text(fps)],
                        [sg.Text("Interval:"), sg.Text(interval)],
                        [sg.Text("Clip length"), sg.Text(clength)],
                        [sg.Text("Work length"), sg.Text(wlength)],
                        [sg.Multiline("video save location: "+ vidloc + "/" + name + "." +vidfrmt, s=(25,5))]
                            ],k="2colu72",visible=Swstat["videocheck"]), sg.Canvas(size=(0,0), pad=(0,0))]
                ],k="2colu22", visible=Swstat["-R2-"]), sg.Canvas(size=(0,0), pad=(0,0))],
                [sg.Col([ # if R3 selected
                    [sg.Text("capture mode: Work limit")],
                    [sg.Col([ # without final clip making - only image
                        [sg.Text("Image format:"), sg.Text(imgfrmt)],
                        [sg.Text("Interval:"), sg.Text(interval)],
                        [sg.Text("Work length:"), sg.Text(wlength)],
                        [sg.Multiline("Image save location: "+ imgloc + "/", s=(25,5))],
                        [sg.Checkbox("Creat final clip",default=False, disabled=True)]
                            ],k="2colu82",visible=not Swstat["videocheck"]), sg.Canvas(size=(0,0), pad=(0,0))],
                    [sg.Col([ # with final clip making
                        [sg.Checkbox("Creat final clip",default=True, disabled=True)],
                        [sg.Text("Clip format:"), sg.Text(vidfrmt)],
                        [sg.Text("Clip FPS:"), sg.Text(fps)],
                        [sg.Text("Interval:"), sg.Text(interval)],
                        [sg.Text("Clip length:"), sg.Text(clength)],
                        [sg.Text("Work length:"), sg.Text(wlength)],
                        [sg.Multiline("video save location: "+ vidloc +"/" + name + "." + vidfrmt, s=(25,5))]
                            ],k="2colu92",visible=Swstat["videocheck"]), sg.Canvas(size=(0,0), pad=(0,0))]
                ],k="2colu32",visible=Swstat["-R3-"]), sg.Canvas(size=(0,0), pad=(0,0))],
                [sg.Button("Back",k="2Back2"), sg.Button("Start now",k="2SNow2"),sg.Button("Start in 5s",k="2S5sec2",disabled=True)]
                ]
    
    return sg.Window(apptitle + "Review", layout, keep_on_top=True, finalize=True)

def makeWindow3():
    layout = [
    [sg.Text("Capturing screen shots")],
    [sg.Text("Elapsed time/scs:"), sg.Text(utimer, k="3uTimer3")],
    [sg.Col([
        [sg.Text("Remaining time/scs:"), sg.Text(dtimer, k="3dTimer3")]
        ],visible = not Swstat["-R1-"]), sg.Canvas(size=(0,0), pad=(0,0))],
    [sg.Button(button_text =  "Pause", k = "3pa-co3", disabled=False), 
     sg.Button("Capture now", k = "3CPnow3", disabled = False), 
     sg.Button("End capture",k="3eCapture3")]
    ]
    return sg.Window(apptitle + "Capturing", 
                        layout, 
                        finalize=True,
                        keep_on_top=True, 
                        margins=(0,0),
                        location=(x,y),
                        no_titlebar=True, 
                        grab_anywhere=True,)

def Make_Window3(): #creat window 3
    global x
    global y
    window3 = makeWindow3()
    x = x - window3.size[0] - 50
    y = y - window3.size[1] - 50
    window3.close()
    return makeWindow3()
    
def Make_Window4():
    global scnumber
    layout = [[sg.Col([
                [sg.Text("Finished :)")],
                [sg.Multiline("Image save location: "+ imgloc + "/", s=(25,5))],
                [sg.Button("Finish", k = "4Exit14")]
                       ], k = "4colu14", visible= not Swstat["videocheck"]), sg.Canvas(size=(0,0), pad=(0,0))],
              [sg.Col([
                [sg.Text("Converting...")],
                [sg.ProgressBar(scnumber, orientation='h', size=(20, 20), key='4PROGRESS BAR4')]
                       ], k = "4colu24", visible=Swstat["videocheck"]), sg.Canvas(size=(0,0), pad=(0,0))],
              [sg.Col([
                [sg.Text("Finished :)")],
                [sg.Multiline("Clip save location: "+ vidloc + "/" + name + "." + vidfrmt, s=(25,5))],
                [sg.Button("Finish", k = "4Exit24")]
                       ], k = "4colu34", visible= False), sg.Canvas(size=(0,0), pad=(0,0))]
              ]

    return sg.Window(apptitle + " last station", layout, keep_on_top=True, finalize=True)

def wtmaker():  # Work time calculator - R2
    global totalsc
    global seconds
    seconds = ((int(values["-fpsCombo2-"])) * ((hour * 60 * 60) + (min * 60) + (sec)) * interval) + (2 * interval) #total seconds
    totalsc = ((int(values["-fpsCombo2-"])) * ((hour * 60 * 60) + (min * 60) + (sec)))  + 1  #total screenshot
    m = seconds // 60
    s = seconds % 60
    h = m // 60
    m = m % 60
    return str(h) + ":" + str(m) + ":" + str(s)

def cpmaker(tsec):  # Clip time calculator - R3
    global totalsc, seconds
    seconds = tsec
    tsec //= interval
    totalsc = tsec  
    tsec //= (int(values["-fpsCombo3-"])) 
    tsec += 1
    s = tsec % 60
    m = tsec //60
    m = m % 60
    h = m // 60
    return s,m,h
    
    
    
def time_as_int():  # return unix time as seconds
    return int(round(time.time() * 100)) # with ms
    

def Count_Down(): # count down timer for remaining time
    global count_down
    remaining_time = count_down - time_as_int()
    cdhour = ((remaining_time // 100) // 60) // 60
    cdmin = ((remaining_time // 100) // 60) % 60
    cdsec = (remaining_time // 100) % 60
    #cdmsec = remaining_time % 100
    return "{:02d}:{:02d}:{:02d}".format(cdhour, cdmin, cdsec)

def Count_Up(): # count up timer for elapsed time
    global start_time 
    current_time = time_as_int() - start_time
    cuhour = ((current_time // 100) // 60) // 60
    cumin = ((current_time // 100) // 60) % 60
    cusec = (current_time // 100) % 60
    return "{:02d}:{:02d}:{:02d}".format(cuhour, cumin, cusec)
 
def captureSCs(): #capture screen shots
    global imgfrmt
    global scnumber
    global imglocsave
    thename = imglocsave + str(scnumber) + "." + imgfrmt
    sc.screenshot().save(thename)
    scnumber += 1

def videomaker():   # creating final video
    global fps
    global imgfrmt
    global vidfrmt
    global window4
    global scnumber
    x , y = sg.Window.get_screen_size()
    if vidfrmt == "mp4": #select mp4 codec
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    elif vidfrmt == "avi": #select avi codec
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        
    frameSize = (int(x), int(y))
    fps = int(fps)
    out = cv2.VideoWriter( vidloc + name + "." + vidfrmt ,fourcc, fps, frameSize)
    for j in range(0,scnumber):
        filename = glob.glob(imglocsave  + str(j) + "." + imgfrmt)
        if filename:
            img = cv2.imread(filename[0])
            out.write(img)
            window4['4PROGRESS BAR4'].update(current_count = j + 1)
        else:
            break
        
    out.release()
    #window4['4PROGRESS BAR4'].update(bar_color="green")
    time.sleep(3)
    #print("finished")
    window4["4colu24"].update(visible = False)
    window4["4colu34"].update(visible = True)
    
    
    return
      
def w3update(): #threading for timers
    global up
    global scnumber
    global interval
    global totalsc
    global window4
    i = interval
    while True:
        if up == True:
            window3["3uTimer3"].update(value = Count_Up()+ "/" + str(scnumber))
            window3["3dTimer3"].update(value = Count_Down() + "/" + str(totalsc - scnumber))
            if i == interval:
                captureSCs()
                i=0
            i += 1
        if(scnumber >= totalsc):
            #window3.close()
            #window4 = Make_Window4()
            #if Swstat["videocheck"]:
            #    videomaker()
            window3["3eCapture3"].update(text = "Next")
            window3["3pa-co3"].update(disabled = True)
            window3["3dTimer3"].update(visible = False)
            break
        time.sleep(1) # 1 second

tr_A = threading.Thread(target=w3update, daemon=True) # target tread a to func.

window1, window2, window3, window4 = Make_Window1(), None, None, None

#print(window1)
#print(window2)

while True:                             # The Event Loop
    window, event, values = sg.read_all_windows()
    #print(event)
    
    #if window == window1 and event in (sg.WIN_CLOSED, 'Exit'):
    #    break
       
    if event == sg.WIN_CLOSED or event == "-Exit-":
        window1.close()
        break
    
    if window == window1:
        if event == "-Exit-":
            window1.close()
            break
            
        elif event == "-Next-":
            if vidloc == "" and imgloc == "":
                sg.popup_error("Select save location",keep_on_top=True)
                continue
            else:
                Swstat["-R1-"] = values["-R1-"] 
                Swstat["-R2-"] = values["-R2-"] 
                Swstat["-R3-"] = values["-R3-"]   
                Swstat["videocheck"] = values["-videocheck-"]
                vidfrmt = values["-clipformat-"]
                
                
                if values["-R1-"]:
                    interval = int(values["-interval-"])
                    fps = values["-fpsCombo1-"]
                    imgfrmt = values["-imgformatcombo1-"]
                elif values["-R2-"]:
                    interval = int(values["-interval2-"])
                    clength = str(hour) + ":" + str(min) + ":" + str(sec)
                    wlength = wtmaker()
                    fps = values["-fpsCombo2-"]
                    imgfrmt = values["-imgformatcombo2-"]
                elif values["-R3-"]:
                    interval = int(values["-interval3-"])
                    clength = str(h) + ":" + str(m) + ":" + str(s)
                    wlength = str(hour) + ":" + str(min) + ":" + str(sec)
                    fps = values["-fpsCombo3-"]
                    imgfrmt = values["-imgformatcombo3-"]
                window1.hide()
                window2 = Make_Window2()
    
        elif event == "-BrowseVideo-":
            vidloc = sg.popup_get_folder('Choose your folder', keep_on_top=True, default_path=vidloc)
        elif (event == "-BrowseImg1-" or event == "-BrowseImg2-" or event == "-BrowseImg3-"):
            imgloc = sg.popup_get_folder('Choose your folder', keep_on_top=True, default_path=imgloc)
        elif event == "-SSetting-":
            #ToDo:
            break 
        elif event == "-LSetting-":
            #ToDo:
            break 
        elif event == "-default-":
            #todo:
            break 
        elif event == "-R1-":
            window1["-colu1-"].update(visible = True)
            window1["-colu2-"].update(visible = False)
            window1["-colu3-"].update(visible = False)
            window1["-colu4-"].update(visible = True)
            window1["-videocheck-"].update(visible = True)
            window1["-colu8-"].update(visible = True)
            
            if values['-videocheck-']== True:
                window1["-colu4-"].update(visible = True)
                window1["-colu5-"].update(visible = False)
                window1["-colu6-"].update(visible = False)
                window1["-colu7-"].update(visible = False)
                
            else:
                window1["-colu4-"].update(visible = False) 
                window1["-colu5-"].update(visible = True)
                window1["-colu6-"].update(visible = True)
                window1["-colu7-"].update(visible = True)
            
        elif event == "-R2-":
            window1["-colu1-"].update(visible = False)
            window1["-colu2-"].update(visible = True)
            window1["-colu3-"].update(visible = False)
            window1["-videocheck-"].update(visible = True)
            window1["-colu8-"].update(visible = False)
            
            if values['-videocheck-']== True:
                window1["-colu4-"].update(visible = True)
                window1["-colu5-"].update(visible = False)
                window1["-colu6-"].update(visible = False)
                window1["-colu7-"].update(visible = False)
                
            else:
                window1["-colu4-"].update(visible = False) 
                window1["-colu5-"].update(visible = True)
                window1["-colu6-"].update(visible = True)
                window1["-colu7-"].update(visible = True)
            
        elif event == "-R3-":
            window1["-colu1-"].update(visible = False)
            window1["-colu2-"].update(visible = False)
            window1["-colu3-"].update(visible = True)
            window1["-videocheck-"].update(visible = True)
            window1["-colu8-"].update(visible = False)
            
            if values['-videocheck-']== True:
                window1["-colu4-"].update(visible = True)
                window1["-colu5-"].update(visible = False)
                window1["-colu6-"].update(visible = False)
                window1["-colu7-"].update(visible = False)

            else:
                window1["-colu4-"].update(visible = False)
                window1["-colu5-"].update(visible = True)
                window1["-colu6-"].update(visible = True)
                window1["-colu7-"].update(visible = True) 
                
        elif event == "-videocheck-":
            if values['-videocheck-']== True:
                window1["-colu4-"].update(visible = True)
                window1["-colu5-"].update(visible = False)
                window1["-colu6-"].update(visible = False)
                window1["-colu7-"].update(visible = False)
            else:
                window1["-colu4-"].update(visible = False)
                window1["-colu5-"].update(visible = True)
                window1["-colu6-"].update(visible = True) 
                window1["-colu7-"].update(visible = True)
            
        elif event == "-interval-":
            try:
                interval = int(values["-interval-"])     
            except:
                window1["-et1-"].update(visible = True)
            else:
                if interval > 0 :
                    window1["-et1-"].update(visible = False)
                else:
                    window1["-et1-"].update(visible = True)
        elif event == "-interval2-":
            try:
                interval = int(values["-interval2-"])     
            except:
                window1["-et5-"].update(visible = True)
            else:
                if interval > 0 :
                    window1["-et5-"].update(visible = False)
                    try:
                        hour = int(values["-hour-"])
                        min = int(values["-min-"])   
                        sec = int(values["-sec-"])    
                    except:
                        window1["-et2-"].update(visible = True)
                    else:
                        if hour < 0 or min < 0 or sec < 0:
                            window1["-et2-"].update(visible = True)
                        else:
                            window1["-et2-"].update(visible = False)
                            window1["-wt1-"].update(value = wtmaker())
                else:
                    window1["-et5-"].update(visible = True)
        elif event == "-interval3-":
            try:
                interval = int(values["-interval3-"])     
            except:
                window1["-et6-"].update(visible = True)
            else:
                if interval > 0 :
                    window1["-et6-"].update(visible = False)
                    try:
                        hour = int(values["-wlhour-"])
                        min = int(values["-wlmin-"])   
                        sec = int(values["-wlsec-"])    
                    except:
                        window1["-et3-"].update(visible = True)
                    else:
                        window1["-et6-"].update(visible = False)
                        s,m,h = cpmaker(((hour * 60 * 60) + (min * 60) + (sec)))
                        window1["-chour-"].update(value = h)
                        window1["-cmin-"].update(value = m)
                        window1["-csec-"].update(value = s)
        
        elif event == "-hour-" or event == "-min-" or event == "-sec-":
            try:
                hour = int(values["-hour-"])
                min = int(values["-min-"])   
                sec = int(values["-sec-"])    
            except:
                window1["-et2-"].update(visible = True)
            else:
                if hour < 0 or min < 0 or sec < 0:
                    window1["-et2-"].update(visible = True)
                else:
                    window1["-et2-"].update(visible = False)
                    window1["-wt1-"].update(value = wtmaker())
            
        elif event == "-fpsCombo2-":
            try:
                hour = int(values["-hour-"])
                min = int(values["-min-"])   
                sec = int(values["-sec-"])    
            except:
                window1["-et2-"].update(visible = True)
            else:
                if hour < 0 or min < 0 or sec < 0:
                    window1["-et2-"].update(visible = True)
                else:
                    window1["-et2-"].update(visible = False)
                    window1["-wt1-"].update(value = wtmaker())
                    
        elif event == "-wlhour-" or event == "-wlmin-" or event == "-wlsec-":
            try:
                hour = int(values["-wlhour-"])
                min = int(values["-wlmin-"])   
                sec = int(values["-wlsec-"])    
            except:
                window1["-et3-"].update(visible = True)
            else:
                if hour < 0 or min < 0 or sec < 0:
                    window1["-et3-"].update(visible = True)
                else:
                    window1["-et3-"].update(visible = False)
                    #window1["-wt3-"].update(value = wtmaker())
                    s,m,h = cpmaker((hour * 60 * 60) + (min * 60) + (sec))
                    window1["-chour-"].update(value = h)
                    window1["-cmin-"].update(value = m)
                    window1["-csec-"].update(value = s)
            
        elif event == "-fpsCombo3-":
            try:
                hour = int(values["-wlhour-"])
                min = int(values["-wlmin-"])   
                sec = int(values["-wlsec-"])    
            except:
                window1["-et3-"].update(visible = True)
            else:
                if hour < 0 or min < 0 or sec < 0:
                    window1["-et3-"].update(visible = True)
                else:
                    window1["-et3-"].update(visible = False)
                    s,m,h = cpmaker((hour * 60 * 60) + (min * 60) + (sec))
                    window1["-chour-"].update(value = h)
                    window1["-cmin-"].update(value = m)
                    window1["-csec-"].update(value = s)
                        
    elif window == window2:
        if event == "2Back2":
            window2.close()
            window1.un_hide()
        elif event == "2SNow2":
            window1.close() 
            window2.close()
            window3 = Make_Window3()
            if Swstat["videocheck"] == True:
                vidloc = vidloc + "/" + name + "/"
                vidlocsave = vidloc.replace(r"/", r"//")
                imgloc = vidloc + "/Temp/"
                imglocsave = imgloc.replace(r"/", r"//")
                Path(vidloc).mkdir(parents=True, exist_ok=True)
                Path(vidloc + "/Temp/").mkdir(parents=True, exist_ok=True)
            else:
                imgloc = imgloc + "/"
                imglocsave = imgloc.replace(r"/", r"//")
                Path(imgloc).mkdir(parents=True, exist_ok=True)   
            start_time = time_as_int()
            count_down = start_time + (seconds * 100)
            tr_A.start()
            continue
        elif event == "2S5sec2":
            continue
        
    elif window == window3: 
        if event == "3pa-co3":
            if paused == True:
                paused = False
                up = False
                paused_time = time_as_int()
                window3["3pa-co3"].update(text = "Continiue")
            else:
                paused = True
                up = True
                start_time = start_time + time_as_int() - paused_time
                count_down = (+seconds * 100) + start_time
                window3["3pa-co3"].update(text = "Pause")
            
        elif event == "3CPnow3":
            totalsc +=1
            captureSCs()
            continue

        elif event == "3eCapture3":
            up = False
            window3.close()
            window4 = Make_Window4()
            if Swstat["videocheck"]:
                videomaker()
            continue
    elif window == window4:
        if event == sg.WIN_CLOSED or event == "4Exit14" or event == "4Exit24":
            window4.close()
            break
        