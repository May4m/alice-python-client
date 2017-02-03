

from uix import Float
from graph import Graph, MeshLinePlot

from kivy.logger import Logger
from kivy.factory import Factory
from kivy.clock import Clock

import math
import time
import json
import random

import endpoint
import widgets

_range = range(-101, 101)
_range.remove(0)


class RootLayout(Factory.FloatLayout, Factory.Image):
    graph_area = Factory.ObjectProperty(None)
    text_input = Factory.ObjectProperty(None)
    send_button = Factory.ObjectProperty(None)
    __graf_initialized = False  # flag to check whether the graph has already been rendered

    def send_command(self):
        manager = Factory.get('ViewManager')
        manager.current = 'botresponse'

    def animate_sound_wave(self):
        self.j = 0
        def _animate(dt):
            amplitude = random.choice([0.5, 1, 1.5])
            freq = random.choice([0.3, 0.2])
            p1 = [(x, amplitude * math.sin(x * freq) / (0.05 * x)) for x in _range]
            p2 = [(x, -1 * amplitude * math.sin(x * freq) / (0.05 * x)) for x in _range]
            anim = Factory.Animation(points=(p1, p2)[self.j], duration=0.2, t='in_cubic')
            anim.start(self.plot)
            if self.j == 0:
                self.j  = 1
            elif self.j == 1:
                self.j = 0

        self.graph_animation = _animate
        Clock.schedule_interval(_animate, 1/5.)

    def reset_graph(self):
        Clock.unschedule(self.graph_animation)
        r = [(x, 0) for x in _range]
        anim = Factory.Animation(points=r, duration=0.2)
        anim.start(self.plot)    

    def render_graph(self):
        if self.__graf_initialized == False:
            self.plot = MeshLinePlot(color=[0.2, 0.2, 0.2, 1])
            self.plot.points = [(x, math.sin(x / 2.) / (0.05 * x)) for x in _range]
            self.graph_area.add_plot(self.plot)
            self.__graf_initialized = True
        self.animate_sound_wave()

    def reset_layout_configuration(self):
        self.reset_graph()
        move_voice_search = Factory.Animation(pos_hint={'center_x': 0.5, 'center_y': 0.1}, duration=0.1, t='in_quad')
        move_voice_search.start(self.voice_search_button)
        self.graph_area.remove_plot(self.plot)
        self.__graf_initialized = False

    def start_recognition(self):
        self.render_graph()

    def stop_recognition(self):
        self.reset_layout_configuration()


class HomeLayout(RootLayout):
    graph_area = Factory.ObjectProperty(None)
    voice_search_button = Factory.ObjectProperty(None)
    response_layout = Factory.ObjectProperty(None)

    def start_recognition(self):
        super(HomeLayout, self).start_recognition()

        move_voice_search = Factory.Animation(pos_hint={'center_x': 0.5, 'center_y': 0.23}, duration=0.1, t='in_quad')
        move_voice_search.start(self.voice_search_button)

    def to_home_screen(self):
        manager = Factory.get('ViewManager')
        manager.current = 'homescreen'
    
    def add_response(self, text, who='alice'):
        who = 'left' if who == 'alice' else 'right'
        widget = widgets.ChatWidget(text=text, align=who)
        widget.align = who
        widget.text = text
        self.response_layout.add_widget(widget)

    def send_command(self):
        _t0 = 0
        def _success(url, results):
            response = json.loads(results)
            Logger.info("Response time from the engine: " + str(time.time() - _t0))
            self.add_response(response['results'])
        _t0 = time.time()
        self.add_response(self.text_input.text, 'user')
        endpoint.alice_request(self.text_input.text, _success)