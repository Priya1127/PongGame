import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty)
from kivy.uix.screenmanager import ScreenManager
from kivy.vector import Vector
from kivy.clock import Clock

kivy.require('1.11.1')

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.3
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(PongGame,self).__init__(*args,**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self,dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        Clock.schedule_interval(self.resume_file, 1)

    #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

    #went of to a side to score point
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        if (self.player1.score==5):
            mainapp.sm.current='winner'
            self.ball.center = self.center
            self.ball.velocity = self.vel=(0, 0)

        elif (self.player2.score==5):
            mainapp.sm.current='winner'
            self.ball.center = self.center
            self.ball.velocity = self.vel=(0, 0)

    def PlayAgain(self):
            self.player1.center_y=self.center_y
            self.player2.center_y=self.center_y
            self.player1.score=0
            self.player2.score=0
            self.serve_ball(vel=(4,0))
        
    def homebutton(self):
        self.player1.center_y=self.center_y
        self.player2.center_y=self.center_y
        self.player1.score=0
        self.player2.score=0
        mainapp.sm.current='home'
            
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def Exit_Screen(self):
        mainapp.stop()
    
    def resume_file(self,dt):
        with open("resume.txt", "w") as f:
            f.write(f"{self.ball.velocity},{self.player1.score},{self.player2.score}")

    def resume(self):
        with open('resume.txt', 'r') as f:
            x=f.read()
            d=eval(x)
            self.ball.velocity=d[0]
            self.player1.score=d[1]
            self.player2.score=d[2]
            if d[0]==[0,0]:
                mainapp.sm.current='home'
            else:
                self.serve_ball(vel=d[0])

class MainApp(App):
    
    def build(self):
        self.load_kv('pong_trial.kv')
        self.sm=ScreenManager()
        return self.sm

if __name__ == '__main__':
    mainapp = MainApp()
    mainapp.run()