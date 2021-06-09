from tkinter import *
import random

class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (17+20*location[1],17+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)


class GUIFreezeableDie(GUIDie):
    '''a GUIDie that can be "frozen" so that it can't be rolled'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIFreezeableDie(master,[valueList,colorList]) -> GUIFreezeableDie
        creates a GUI 6-sided freeze-able die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        GUIDie.__init__(self,master,valueList,colorList)
        self.isFrozen = False  # die starts out unfrozen

    def is_frozen(self):
        '''GUIFreezeableDie.is_frozen() -> bool
        returns True if the die is frozen, False otherwise'''
        return self.isFrozen
    
    def toggle_freeze(self):
        '''GUIFreezeableDie.toggle_freeze()
        toggles the frozen status'''
        self.isFrozen = not self.isFrozen
        if self.isFrozen:
            self['bg'] = 'gray'
        else:
            self['bg'] = 'white'

    def roll(self):
        '''GuiFreezeableDie.roll()
        overloads GUIDie.roll() to not allow a roll if frozen'''
        if not self.isFrozen:
            GUIDie.roll(self)

class DiscusFrame(Frame):

    def __init__(self,master,name):
        Frame.__init__(self,master)
        self.grid()
        self.score=0
        self.highscore=0
        self.attempt=1
        self.rollcount=0
        self.foul=0
        Label(self,text=name,font=('Arial',18)).grid(columnspan=1,sticky=W)
        self.attemptLabel=Label(self,text='Attempt #'+str(self.attempt),font=('Arial',18))
        self.attemptLabel.grid(row=0,column=2,columnspan=1)
        self.scoreLabel=Label(self,text='Score: '+str(self.score),font=('Arial',18))
        self.scoreLabel.grid(row=0,column=4,columnspan=1)
        self.highScoreLabel=Label(self,text='High Score: 0', font=('Arial',18))        
        self.highScoreLabel.grid(row=0,column=8,columnspan=1,sticky=E)
        self.dice=[]
        for n in range(5):
            self.dice.append(GUIFreezeableDie(self,[0,2,0,4,0,6],['red','black']*3))
            self.dice[n].grid(row=1,column=n,columnspan=1)
        self.rollButton = Button(self,text='Roll',state=ACTIVE,command=self.roll)
        self.rollButton.grid(row=1,column=8,columnspan=1)
        self.stopButton = Button(self,text='Stop',state=DISABLED,command=self.stop)
        self.stopButton.grid(row=2,column=8,columnspan=1)
        self.freezeButton1=Button(self,text='Freeze',state=DISABLED,command=self.toggle_freeze1)
        self.freezeButton1.grid(row=2,column=0,columnspan=1)
        self.freezeButton2=Button(self,text='Freeze',state=DISABLED,command=self.toggle_freeze2)
        self.freezeButton2.grid(row=2,column=1,columnspan=1)
        self.freezeButton3=Button(self,text='Freeze',state=DISABLED,command=self.toggle_freeze3)
        self.freezeButton3.grid(row=2,column=2,columnspan=1)
        self.freezeButton4=Button(self,text='Freeze',state=DISABLED,command=self.toggle_freeze4)
        self.freezeButton4.grid(row=2,column=3,columnspan=1)
        self.freezeButton5=Button(self,text='Freeze',state=DISABLED,command=self.toggle_freeze5)
        self.freezeButton5.grid(row=2,column=4,columnspan=1)
        
    def roll(self):
        self.freezeButton1['state']=DISABLED
        self.freezeButton2['state']=DISABLED
        self.freezeButton3['state']=DISABLED
        self.freezeButton4['state']=DISABLED
        self.freezeButton5['state']=DISABLED
        x=0
        for n in range(5):
            self.dice[n].roll()
            x+=1
            if (self.dice[n].is_frozen() == False) and self.dice[n].get_top()== 2 or (self.dice[n].is_frozen() == False) and self.dice[n].get_top()== 4 or  (self.dice[n].is_frozen() == False) and self.dice[n].get_top()==6:
                if x==1:
                    self.freezeButton1['state']=ACTIVE
                elif x==2:
                    self.freezeButton2['state']=ACTIVE
                elif x==3:
                    self.freezeButton3['state']=ACTIVE
                elif x==4:
                    self.freezeButton4['state']=ACTIVE
                elif x==5:
                    self.freezeButton5['state']=ACTIVE
                else:
                    self.freezeButton1['state']=DISABLED
                    self.freezeButton2['state']=DISABLED
                    self.freezeButton3['state']=DISABLED
                    self.freezeButton4['state']=DISABLED
                    self.freezeButton5['state']=DISABLED
                
            
    def stop(self):
        if self.score>self.highscore:
            self.score=0
            self.attempt+=1
            self.highscore=self.score
            self.highScoreLabel['text']='High Score: '+str(self.highscore)
            self.scoreLabel['text']="Score: "+str(self.score)
            self.attemptLabel['text']="Attempt# "+str(self.attempt)
        else:
            self.score=0
            self.attempt+=1
            self.scoreLabel['text']="Score: "+str(self.score)
            self.attemptLabel['text']="Attempt# "+str(self.attempt)

    
    def toggle_freeze1(self):
        self.dice[0].toggle_freeze()

    def toggle_freeze2(self):
        self.dice[1].toggle_freeze()

    def toggle_freeze3(self):
        self.dice[2].toggle_freeze()

    def toggle_freeze4(self):
        self.dice[3].toggle_freeze()

    def toggle_freeze5(self):
        self.dice[4].toggle_freeze()



        
name=input("Enter your name: ")
root = Tk()
root.title('Discus')
game = DiscusFrame(root,name)
game.mainloop()
