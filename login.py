import kivy
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.clock import Clock


# ----------GLOBAL VARIABLES------------
a=0
a1=0
score=0
the_id=None
# --------------------------------------
class SigninWindow(Screen):
    def signin(self):
        db=open('QuizLoginData.txt','r')
        usernam=self.ids.username.text
        passw=self.ids.passw0.text
        popup=Factory.MyPopup()
        spopup=Factory.MysuccessPopup()
        una=[]
        pas=[]
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

    def stateNormal(self,*args):
         for i in range(1,5):
            self.ids[f'opt{i}'].state = 'normal'

    def openquestion(self):
        global a
        try:
            self.ids.ques.text=data[the_id]['question'][a]   
            self.ids.opt1.text=data[the_id]['options'][a][0]
            self.ids.opt2.text=data[the_id]['options'][a][1]
            self.ids.opt3.text=data[the_id]['options'][a][2]
            self.ids.opt4.text=data[the_id]['options'][a][3]
            a+=1
        except:
            popup=Factory.MyPopup()
            popup.ids.message.text='All questions have been answered!!\nPlease click on submit button'
            popup.open()


    def checkscore(self,id):
        global a1
        ans=data[the_id]['answer'][a1]
        if(id==ans):
            global score
            score+=1
        a1+=1
        print("score: ",score)
        Clock.schedule_once(self.stateNormal, 0.2)


# class 

class QuizScreenManager(ScreenManager):
    pass


kv = Builder.load_file('loginLayoutCSS.kv')

class Login(App):
    def build(self):
        return kv

if __name__=='__main__':
    Login().run()