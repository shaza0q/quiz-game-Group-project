import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.audio import SoundLoader


class MainWindow(Screen):
    
    def category(self,butt_instance):
        the_id=None
        for butt_id, button in self.ids.items():
            if button==butt_instance:
                the_id=butt_id
                break

        quizgo=self.manager.get_screen('quizgo')
        quizgo.the_butt_id=the_id
        self.manager.current='quizgo'
        self.ids.labe.text=quizgo.the_butt_id+' Quiz'

class QuizWindow(Screen):
    
    the_butt_id=''
    
    def something(self):
        scores=0
        self.ids.labelquiz.text=self.the_butt_id+' Quiz'
        f=open('questions.json')
        data=json.load(f)
        self.ids.score.text=self.the_butt_id
                   


class WindowManager(ScreenManager):
    pass

class StandAlone(App):
    def build(self):
        return Builder.load_file('StandAloneQuiz.kv')

if __name__=="__main__":
    StandAlone().run()