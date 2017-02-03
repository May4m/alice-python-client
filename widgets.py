
from uix.buttons import RoundButtonTemplate, ImageButton, FullRoundButton
from kivy.factory import Factory
from kivy.clock import Clock


class ResultsLayout(Factory.Grid):
    """
    This layout is used with the scroll view to pack all chats and make
    them scrollable

    """
    
    def __init__(self, *args, **kwargs):
        super(ResultsLayout, self).__init__(*args, **kwargs)
        self.bind(minimum_height=self.setter('height'))
    


class ChatWidget(Factory.Float):
    """
    A widget that is used to represent the response chat of the bot and sent chat

    """

    background_color = Factory.ListProperty([1, 1, 1, 0])
    text = Factory.StringProperty(None)
    align = Factory.StringProperty('left')
    orientation = Factory.StringProperty('vertical')

    def __init__(self, *args, **kwargs):
        text = kwargs.get('text')
        if text:
            self.label = Factory.Label(text=text)
        else:
            self.label = Factory.Label()
        align = kwargs.get('align', 'left')

        super(ChatWidget, self).__init__(*args, **kwargs)

        # set label styling
        self.label.font_name = "resources/fonts/OpenSans-CondLight.ttf"
        self.label.pos_hint = {'x': 0, 'y': 0}
        self.size_hint_y = None
        self.height = 40
        self.label.font_size = '18sp'
        self.label.color = [0, 1, 1, 1] if align == 'left' else [1, 1, 1, 1]
        self.label.text_size = (self.width, self.height)
        self.label.halign = align
        self.add_widget(self.label)

        # create a bar seperator which is basically a squeezed Rectangle
        with self.canvas:
            self.separator_color = Factory.Color(1, 1, 1, 0.5)
            self.separator = Factory.Rectangle(pos=self.pos, size=(self.width, 1))
        
        self.bind(size=self._on_size_change, pos=self._on_size_change)

    def on_align(self, instance, value):
        instance.label.halign = value
        self.label.color = [1, 1, 0, 1] if value == 'left' else [1, 1, 1, 1]

    def on_text(self, instance, value):
        self.label.text = value

    def _on_size_change(self, instance, value):
        """
        The change in the parent widget's dimensions should trigger a change
        on the child widgets
        """
        self.label.size = self.size
        self.label.text_size = self.size
        self.separator.pos = self.pos
        self.separator.size =  (self.width, 1)
        

class VoiceButton(ImageButton, RoundButtonTemplate):
    bubble_max = Factory.ListProperty([100, 100])  # maximum size of the wave
    bubble_min = Factory.ListProperty([80, 80])  # minimum size of the wave

    _wave_started = False
    def _wave_animation(self, dt):
        width_x, height_x = self.bubble_max
        width_n, height_n = self.bubble_min

        if self.width >= width_x and self.height >= height_x:
            self.direction = 'down'
        elif self.width <= width_n and self.height <= height_n:
            self.direction = 'up'
        if self.direction == 'up':
            self.width, self.height = self.width + .3, self.height + .3
        else:
            self.width, self.height = self.width - .3, self.height - .3
    
    def wave_animation(self, start):
        if start and (not self._wave_started):
            self._wave_started = True
            Clock.schedule_interval(self._wave_animation, 1/60.0)
        if (not start) and self._wave_started:
            self._wave_started = False
            Clock.unschedule(self._wave_animation)

    def on_bubble_max(self, instance, value):
        pass

    def on_press(self):
        self.wave_animation(True)

    def on_release(self):
        self.wave_animation(False)
        animation = Factory.Animation(size=self.bubble_min, duration=.2)
        animation.start(self)