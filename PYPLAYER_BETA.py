#PYPLAYER_BETA_1.08



from tkinter import *
from tkinter import filedialog
import os
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading

mixer.init()

window=Tk()

#music player icon
window.geometry('600x350')
window.iconbitmap(r'E:\py player\PYPLAYER.ico')
window.title('Py Player')
window.resizable(0,0)




bg=PhotoImage(file=r'E:\py player\2846435-resized-1.png')
bg_label=Label(window, image= bg,height=350,width=600 )
bg_label.place(x=0,y=0,relheight=1,relwidth=1)





#FRAMES
btnframe=Frame(window, height=64 ,width=244 ,bd=2 ,relief=GROOVE,bg='#000000')
btnframe.place(x=325,y=125)

                              
#BUTTONS

songdata=list()



def selection(event):
    try:
        global point,song,tol
        pointed=musicdis.curselection()
        for e in range(len(songdata)):  
            musicdis.itemconfig(e,background='#FFFFFF',foreground='#000000')
        point=0
        for i in pointed: 
            point+=i  
        song=songdata[point][0]
        if mixer.music.get_busy()==0  :
            statusbar['text']=str(songdata[point][1])
        del pointed 
    except:
        pass

def previoussong():
    try:
        global song,playbtnpushed,songrunscale,status_song
        
        if musicdis.size()!=0:

            for q,(w,e) in list(enumerate(songdata)) :
                
                if currsong==w:
                    
                    if q>0:
                        song=(songdata[q-1][0])
                        if len(songdata)!=0  :
                            for e in range(len(songdata)):
                                musicdis.itemconfig(e,background='#FFFFFF',foreground='#000000')           
                        musicdis.see(q-1)
                        for i in musicdis.curselection():
                            musicdis.select_clear(i)                                               
                        musicdis.itemconfig(q-1,background='#FF7142',foreground='#FFFFFF')        
                        musicdis.select_set(q-1)
                        musicdis.activate(q-1)                        
                        
                    elif q==0:
                        q=(musicdis.size()-1)
                        song=(songdata[q][0])
                        if len(songdata)!=0  :
                            for e in range(len(songdata)):
                                musicdis.itemconfig(e,background='#FFFFFF',foreground='#000000')           
                        musicdis.see(q)
                        for i in musicdis.curselection():
                            musicdis.select_clear(i)                                               
                        musicdis.itemconfig(q,background='#FF7142',foreground='#FFFFFF')        
                        musicdis.select_set(q)
                        musicdis.activate(q)  
  
            stop()
             
            i=0
            while True :
                if cnt.is_alive()==False :
                    pl=threading.Thread(target=play)
                    pl.start()
                    break
                else:
                    _j_=8*i
                    for _ in range(_j_):
                        stoped=True
                        stop()
                    i+=1
        else:
            pass
    except:
        pass
    
#previous button
previousphoto = PhotoImage(file=r'E:\py player\PREVIOUS.png')
previousbutton=Button(btnframe, image=previousphoto,height=55,width=55,bd=1,command=previoussong,bg='#FFFFFF' )
previousbutton.pack(side=LEFT,padx=1)

def total_len(song):
        global tlen
        tlen=0
        if '.wav' in song:
            aud=mixer.Sound(song)
            tlen+=aud.get_length()       
        elif 'mp3' in song :
            aud= MP3(song)
            tlen+=aud.info.length
        return tlen
    
flags=threading.Event()    
    
def slider_move(event):
    global tol,songrunscale,song,currsong,musicdis,songdata,song,currtime,playbtnpushed,cnt,flags,ius,ttime
    if playbtnpushed :
        ius=songrunscale.get()
        if ius<tol :
            flags.set()
            mixer.music.rewind()
            mixer.music.play(start=songrunscale.get())    
        elif ius>=tol :
            stop()                
    else:
        pass
      

def slider_move_pause(event):
    global ius,flags,playbtnpushed
    if playbtnpushed :
        mixer.music.pause()
        flags.clear()
        ius-=ius

            
    else:
        pass

def counts():
    global tol,songrunscale,song,currsong,musicdis,songdata,song,currtime,playbtnpushed,ius,stoped
    try:
        try:
            ius-=ius
            songrunscale.forget()
            currtime['text']=('--:--')
        except:
            pass
        tol=int(total_len(song))
        songrunscale=Scale(runsongframe,length=209,width=5,orient=HORIZONTAL,from_=0,to = tol,bg='#FFFFFF',relief=GROOVE,troughcolor='#d3eef4',showvalue=0)
        songrunscale.place(x=26,y=10)
        songrunscale.bind('<Button-1>',slider_move_pause)
        songrunscale.bind('<ButtonRelease-1>',slider_move)
        ius=songrunscale.get()
        if playbtnpushed==True   :
            mq,sq=divmod(tol,60)  
            mq,sq=int(mq),int(sq)
            totaltime['text']=('{0}:{1:02d}'.format(mq,sq))

            while True :
                if ius <= int(tol)    :
                    if stoped==False:
                        try:
                            flags.wait()
                            songrunscale.set(ius)
                            mk,sk=divmod(int(songrunscale.get()),60)
                            currtime['text']=('{0}:{1:02d}'.format(int(mk),int(sk)))
                            ius+=1
                            time.sleep(1)
                        except RuntimeError :
                            pass
                    elif stoped==True :
                        assert (stoped),"the song is stoped"
                        break
                    
                elif ius > tol  :
                    nexs=threading.Thread(target=nextsong)
                    nexs.start()
                    break
    except AssertionError :
        pass
    

def addsong():
    global songfile,pointed_index,songfilename,song
    songfile=filedialog.askopenfilenames(filetypes=(('MP3','.mp3'),('WAV','.wav')))
    for i in songfile:
        songfilename=os.path.basename(i)
        pointed_index=len(songdata)
        insertingvalue=songfile
        if insertingvalue != '':    
            musicdis.insert(pointed_index,songfilename)
            tuple_of_data=tuple([i,songfilename]) 
            songdata.append(tuple_of_data)    
        else:
            pass
        try:
            del point
        except:
            pass
    
def delsong(): 
    global song,songdata,currsong,musicdis
    try:
        if currsong==songdata[point][0] :
            stop()
        musicdis.delete(point)
        del songdata[point]
        del song
    except:
        pass
    
def clearsong():
    global song,songdata,currsong,musicdis
    try:
        stop()
        musicdis.delete(0,len(songdata)+1)
        songdata.clear()
        del song
    except:
        pass
    
#play buTton
    
cnt=threading.Thread(target=counts)

playbtnpushed=False
pausephoto = PhotoImage(file=r'E:\py player\PAUSE.png')
resumephoto=PhotoImage(file=r'E:\py player\RESUME.png')
playphoto = PhotoImage(file=r'E:\py player\PLAY.png')

status_song=None
def play():
    if musicdis.size()==len(songdata) and musicdis.size()!=0 :
        try:
            global currenttime,playbtnpushed,currsong,tol,status_song,cnt,stoped
            tol=total_len(song)
            currsong=song
            currenttime=int(mixer.music.get_pos()*(0.001))  
            if playbtnpushed==False :    
                playbutton['image']=pausephoto
                if (currenttime==0) and currenttime<int(tol) :
     
                    mixer.music.load(song)
                    if cnt.is_alive()==False  :
                        cnt=threading.Thread(target=counts)
                        cnt.start()
                    else:
                        pass
                    mixer.music.play()
                    del playbtnpushed
                    playbtnpushed=True
                    del stoped
                    stoped=False
                    
                    flags.set()
                    
                    
                    for q,(w,e) in list(enumerate(songdata)) :
                        if currsong==w  and int(mixer.music.get_busy())==1 :
                            statusbar['text']=(str(songdata[q][1])+'   is playing')
                            status_song=str(songdata[q][1])
                            
                elif (currenttime>0 ) and currenttime<int(tol):

                    mixer.music.unpause()
                    
                    flags.set()
                    
                    del playbtnpushed
                    playbtnpushed=True
                    if status_song!=None :
                        statusbar['text']=(status_song+'   is playing')
                    del stoped
                    stoped=False

            elif playbtnpushed==True :
                playbutton['image']=resumephoto
                mixer.music.pause()
                flags.clear()
                
                del playbtnpushed
                playbtnpushed=False
                del stoped
                stoped=False
                if status_song!=None:
                    statusbar['text']=(status_song+'  is paused')

        
        except (NameError,KeyError):
            pass
    else:
        pass

def nextsong():
    try:

        global song,playbtnpushed,songrunscale,status_song,stoped,playbtnpushed
 
        if musicdis.size()!=0 :

            for q,(w,e) in list(enumerate(songdata)) :
                
                if currsong==w:
                    
                    if q<(musicdis.size()-1):
                        song=(songdata[q+1][0])
                        if len(songdata)!=0  :
                            for e in range(len(songdata)):
                                musicdis.itemconfig(e,background='#FFFFFF',foreground='#000000')           
                        musicdis.see(q+1)
                        for i in musicdis.curselection():
                            musicdis.select_clear(i)                                               
                        musicdis.itemconfig(q+1,background='#FF7142',foreground='#FFFFFF')        
                        musicdis.select_set(q+1)
                        musicdis.activate(q+1)
                        
                    elif q==(musicdis.size()-1):
                        q=0
                        song=(songdata[q][0])
                        if len(songdata)!=0  :
                            for e in range(len(songdata)):
                                musicdis.itemconfig(e,background='#FFFFFF',foreground='#000000')  
                        musicdis.see(q)
                        for i in musicdis.curselection():
                            musicdis.select_clear(i)                                               
                        musicdis.itemconfig(q,background='#FF7142',foreground='#FFFFFF')        
                        musicdis.select_set(q)
                        musicdis.activate(q)                                            

            stop()
             
            i=0
            while True :
                if cnt.is_alive()==False :
                    pl=threading.Thread(target=play)
                    pl.start()
                    
                    break
                else:
                    _j_=(8*i)
                    for _ in range(_j_):
                        stoped=True
                    i+=1
                    
        else:
            print('else')
            pass

    except:
        pass

stoped=False
def stop():
    global playbtnpushed,songfile,song,tol,status_song,ius,songrunscale, stoped

    flags.clear()
    del stoped 
    stoped=True
    playbutton['image']=playphoto
    mixer.music.stop()
    del playbtnpushed
    playbtnpushed=False
    statusbar['text']='::::::::::::::::Pyplayer:::::::::::::::::::::::'  
    totaltime['text']=('--:--')
    currtime['text']=('--:--')
    del status_song
    status_song=None     
    songrunscale.set(0)
    try:
        del songfile
        ius-=ius
    except:
        pass

    
def volume(event):
    global muted
    v=int(volscale.get())/100
    mixer.music.set_volume(v)
    if mixer.music.get_volume()!=0 and muted:
        mutebtn['image']=unmutephoto 
        muted=False
    elif mixer.music.get_volume()==0:
        mutebtn['image']=mutephoto
        mixer.music.set_volume(0)
        volscale.set(0)
        muted=True
               
playbutton=Button(btnframe, image=playphoto,height=55,width=55,bd=1,command=play,bg='#FFFFFF')
playbutton.pack(side=LEFT,padx=1)

#pause button
stopphoto=PhotoImage(file=r'E:\py player\STOP.png')
stopbutton=Button(btnframe,image=stopphoto,height=55,bd=1,width=55,command=stop,bg='#FFFFFF')
stopbutton.pack(side=LEFT,padx=1)
    
#next button

nextphoto = PhotoImage(file=r'E:\py player\NEXT.png')
nextbutton=Button(btnframe, image=nextphoto,height=55,width=55,bd=1,padx=25,command=nextsong,bg='#FFFFFF')
nextbutton.pack(side=LEFT,padx=1)

display=Frame(window,bd=1,height=247,width=325,relief=GROOVE)
display.place(x=10,y=35)



scrollbar=Scrollbar(display,orient=VERTICAL)

musicdis=Listbox(display,height=15,width=45,yscrollcommand=scrollbar.set,selectbackground='#FF7142',selectmode=SINGLE )

scrollbar.config(command=musicdis.yview)
scrollbar.pack(side=RIGHT,fill=Y)

musicdis.bind('<ButtonRelease-1>',selection)

def select_play(event):
    global song,songdata,stoped
    try:
        if int(mixer.music.get_busy())== 1:
            flags.clear()
            stop()
            ius-=ius
            songrunscale.set(0)
            for u in musicdis.curselection() :
                song=songdata[u][0]
            flags.set()
            pyl=threading.Thread(target=play)
            pyl.start()
        else:
            for u in musicdis.curselection() :
                song=songdata[u][0]
            pyl=threading.Thread(target=play)
            pyl.start()
    except:
        pass

musicdis.bind('<Double-Button-1>',select_play)

musicdis.pack(side=LEFT)


addbtn=Button(window,height=1,width=5,text='ADD',command=addsong,bg='#FFFFFF')
addbtn.place(x=10,y=290)
rembtn=Button(window,height=1,width=5,text='DEL',command=delsong,bg='#FFFFFF')
rembtn.place(x=59,y=290)
clearbtn=Button(window,height=1,width=5,text='CLEAR',command=clearsong,bg='#FFFFFF')
clearbtn.place(x=106,y=290)

searchframe=Frame(window,height=28,width=300,bd=1,relief=GROOVE,bg='#FFFFFF')
searchframe.place(y=0,x=285)


def searching(): 
    global pointed,song,start
    entered=searchbar.get()
    
    if len(songdata)!=0 and entered != '' :

        for e in range(len(songdata)):
            musicdis.itemconfig(e,background='#FFFFFF',foreground='#000000')

        data=songdata
        for i,j in data:
            if entered.lower()  in j.lower():
                start=0
                while start<(musicdis.size()) :
                    music=str(musicdis.get(start))
                    if j[-5::-1]== music[-5::-1] :   
                        musicdis.see(start)
                        for i in musicdis.curselection():
                            musicdis.select_clear(i)  
                            
                        musicdis.itemconfig(start,background='#FF7142',foreground='#FFFFFF')
                        searchbar.delete(0,len(entered))
                        musicdis.select_set(start)
                        musicdis.activate(start)
                        if mixer.music.get_busy()==0  :
                            for op in musicdis.curselection():
                                statusbar['text']=str(songdata[op][1]) 
                            
                        break
                    start+=1
    else:
        pass
    
def status_searching(event): 
    global pointed,song,start,status_song,statusbar
    try:
        if len(songdata)!=0 and status_song!=None :
            
            for e in range(len(songdata)):
                musicdis.itemconfig(e,background='#FFFFFF',foreground='#000000')
                                    
            for q,(w,e) in list(enumerate(songdata)) :
                if status_song==e :
                    
                    musicdis.see(q)
                    for i in musicdis.curselection():
                        musicdis.select_clear(i)                                               
                    musicdis.itemconfig(q,background='#FF7142',foreground='#FFFFFF')        
                    musicdis.select_set(q)
                    musicdis.activate(q)
                    
        elif statusbar['text']==('::::::::::::::::Pyplayer:::::::::::::::::::::::')    :
            for e in range(len(songdata)):
                musicdis.itemconfig(e,background='#FFFFFF',foreground='#000000')      
            for i in musicdis.curselection():
                musicdis.select_clear(i)          
                
        else:
            pass
    except:
        pass

    
searchphoto=PhotoImage(file=r'E:\py player\loupe.png')
searchbtn=Button(searchframe,image=searchphoto ,command=searching,bg='#FFFFFF'  )
searchbtn.pack(side=RIGHT)

searchbar=Entry(searchframe,width=42,bg='#FFFFFF')
searchbar.pack(side=LEFT)

statusbar=Label(window,text='::::::::::::::::Pyplayer:::::::::::::::::::::::',height=2,width=22 ,relief=GROOVE,bg='#d3eef4',font=32,anchor='w')
statusbar.place(x=325,y=60)
statusbar.bind('<Button-1>',status_searching)


volframe=Frame(window,height=30,width=205,bd=1,relief=GROOVE,bg='#FFFFFF')
volframe.pack(side=BOTTOM,anchor='e',padx=10,pady=8)



volscale=Scale(volframe,orient=HORIZONTAL,length=160,width=13,bd=1,bg='#FFFFFF',troughcolor='#d3eef4')
volscale.pack(side=RIGHT,anchor='s')
volscale.bind('<ButtonRelease-1>',volume)
volscale.set(30)


mutephoto=PhotoImage(file=r'E:\py player\mute-speaker.png')
muted=False

def muteing():
    global muted
    if muted==False:
        mutebtn['image']=mutephoto
        mixer.music.set_volume(0)
        volscale.set(0)
        muted=True
    
unmutephoto = PhotoImage(file=r'E:\py player\iconfinder_volume-24_103167 (2).png')
mutebtn=Button(volframe,image=unmutephoto,command=muteing,bg='#FFFFFF',relief=GROOVE)
mutebtn.pack(side=LEFT,ipadx=6,ipady=6)

runsongframe=Frame(window,height=32,width=279,bd=2,relief=GROOVE,bg='#FFFFFF')
runsongframe.place(x=315,y=200)  
    
mixer.music.set_volume(0.30)


currtime=Label(runsongframe,text='--:--',bg='#FFFFFF')
currtime.place(x=0,y=5)



totaltime=Label(runsongframe,text='--:--',bg='#FFFFFF')
totaltime.place(x=243,y=5)



def destroy_slpwindw() :
    try:
        stop()
    except:
        pass
    window.destroy()



songrunscale=Scale(runsongframe,length=209,width=5,orient=HORIZONTAL,from_=0,to = 100,bg='#FFFFFF',relief=GROOVE,troughcolor='#d3eef4',showvalue=0)
songrunscale.place(x=26,y=10)


window.protocol("WM_DELETE_WINDOW",destroy_slpwindw)

window.mainloop()
