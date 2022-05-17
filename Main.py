import kivy
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.clock import Clock


# ----------GLOBAL VARIABLES------------

a=0
a1=0
score=0
the_id=None
sec=0
min=10

# -----------FONT STYLES----------------

LabelBase.register(name="Freshman",fn_regular='Freshman.ttf')
LabelBase.register(name="old_school",fn_regular='old_school.ttf')
LabelBase.register(name='sports_day',fn_regular='Sport Day Bold.ttf')
LabelBase.register(name='hungry',fn_regular='HungryCharlie-Serif.ttf')

# --------------------------------------

class WelcomeWindow(Screen):
    def pressed(self):
        self.ids.image.source='pressed'

class SigninWindow(Screen):
    def signin(self):
        db=open('QuizLoginData.txt','r')
        usernam=self.ids.username.text
        passw=self.ids.passw0.text
        popup=Factory.MyPopup()
        spopup=Factory.MysuccessPopup()
        una=[]
        pas=[]  #data=lock-usernam,key-password
        for i in db:                   
            a,b=i.split(', ')
            b=b.strip()
            una.append(a)
            pas.append(b)
        data=dict(zip(una,pas))
        if usernam in data:
            if passw==data[usernam]:
                spopup.ids.message0.text = '''Login successful'''
                spopup.open()
                self.manager.current='category'
            else:
                popup.ids.message.text = '''Password Doesn't match'''
                popup.open()
                self.ids.passw0.text = ''
        else:
            popup.ids.message.text = '''Shi username dalo'''
            popup.open()
            self.ids.username.text = ''

class SignupWindow(Screen):
    def signup(self):
        db=open('QuizLoginData.txt','r')
        username=self.ids.uname.text
        passw1=self.ids.passw1.text
        passw2=self.ids.passw2.text
        popup=Factory.MyPopup()
        spopup=Factory.MysuccessPopup()
        una=[]
        pas=[]
        for i in db:
            a,b=i.split(', ')
            b=b.strip()
            una.append(a)
            pas.append(b)


        if(passw1!=passw2):
            popup.ids.message.text='Shi Password dalo!!'
            popup.open()
            self.ids.passw1.text=''
            self.ids.passw2.text=''
        
        else:
            if (len(passw1)<=5)or(len(username)<=3):
                popup.ids.message.text='lamba password rakho'
                popup.open()
                self.ids.passw1.text=''
                self.ids.passw2.text=''
            elif username in una:
                popup.ids.message.text='Username exist karta hai\nnya username dalo'
                popup.open()
                self.ids.uname.text=''  
            
            else:
                db=open('QuizLoginData.txt','a')
                db.write(username+', '+passw1+'\n')
                spopup.ids.message0.text='Success!!'
                spopup.open()
                self.ids.passw1.text=''
                self.ids.passw2.text=''
                self.ids.uname.text=''

    def test(self):
        pass

class CategoryWindow(Screen):
     def category(self,butt_instance):
        global the_id
        for butt_id, button in self.ids.items():
            if button==butt_instance:
                the_id=butt_id
                break
        self.manager.current='indexrules'

class IndexRulesWindow(Screen):

    def labelnam(self):
        self.ids.rullab.text=the_id


class QuizMainWindow(Screen):

    f=open('question.json')
    global data
    data=json.load(f)

    def timer_start(self, **kwargs):   
        Clock.schedule_interval(self.increment_time, .1) 
        self.increment_time(0)

    def increment_time(self, interval): 
        global sec
        if(sec<60):
            sec+=1
        else:
            sec=0
#-------------------------------------------------------
    def build(self):
        self.ids.timer.text='10 minutes left'
        Clock.schedule_interval(self.Callback_Clock, 1)
        return self.timer

    def Callback_Clock(self, dt):
        sec=sec-1
        self.ids.timer.text = " % d minutes left" % sec
#-------------------------------------------------------------
    def timer(self):
        Clock.schedule_interval(self.increment_time, .1)
        self.ids.timer.text=str(sec)

    def stateNormal(self,*args):
         for i in range(1,5):
            self.ids[f'opt{i}'].state = 'normal'

    def openquestion(self):
        global a
        if(a<=9):
            self.ids.ques.text=data[the_id]['question'][a]   
            self.ids.opt1.text=data[the_id]['options'][a][0]
            self.ids.opt2.text=data[the_id]['options'][a][1]
            self.ids.opt3.text=data[the_id]['options'][a][2]
            self.ids.opt4.text=data[the_id]['options'][a][3]  
            a+=1  
        else:
            popup=Factory.MyPopup()
            popup.ids.message.text='All questions have been answered!!\nPlease click on submit button'
            popup.open()


    def checkscore(self,id):
        global a1
        if(a1<=9):
            ans=data[the_id]['answer'][a1]
            if(id==ans):
                global score
                score+=1
            a1+=1
            print("score: ",score)
            Clock.schedule_once(self.stateNormal, 0.2)
        else:
            popup=Factory.MyPopup()
            popup.ids.message.text='All questions have been answered!!\nPlease click on submit button'
            popup.open()


class ResultWindow(Screen):
    def show_score(self):
        self.ids.score_text.text+=str(score)


class QuizScreenManager(ScreenManager):
    pass


kv = Builder.load_file('loginLayoutCSS.kv')

class QUIZ(App):
    def build(self):
        return kv

if __name__=='__main__':
    QUIZ().run()