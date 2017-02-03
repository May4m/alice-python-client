from kivy.factory import Factory
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import platform
import random

Vector = Factory.Vector
Animation = Factory.Animation

Widget = Factory.Widget
ModalView = Factory.ModalView
StackLayout = Factory.StackLayout
FloatLayout = Factory.FloatLayout
AnchorLayout = Factory.AnchorLayout
BoxLayout = Factory.BoxLayout
RelativeLayout = Factory.RelativeLayout
GridLayout = Factory.GridLayout
Label = Factory.Label
Button = Factory.Button

Ellipse = Factory.Ellipse
Color = Factory.Color
Rectangle = Factory.Rectangle
TextInput = Factory.TextInput

NumericProperty = Factory.NumericProperty
ObjectProperty = Factory.ObjectProperty
ListProperty = Factory.ListProperty
BooleanProperty = Factory.BooleanProperty
StringProperty = Factory.StringProperty


class CustomWidget(Widget):
    background_color = ListProperty([.8, .8, .8, 1.])

    # Layout background image
    source = StringProperty(None)

    def __init__(self, **kwargs):
        super(CustomWidget, self).__init__(**kwargs)

        with self.canvas.before:
            self.color = Color(*self.background_color, mode="rgba")
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_transformation,
                  size=self.update_transformation,
                  source=self.back_image,
                  background_color=self.update_color)

    def back_image(self, ins, val):
        self.rect.source = val

    def update_color(self, instance, color):
        if len(color) == 3:
            color.append(1)
        self.color.rgba = color

    def update_transformation(self, ins, val):
        self.rect.size = ins.size
        self.rect.pos = ins.pos

    def add(self, *widgets, **kw_widgets):
        """
        Custom 'add' method which can be used as an alternative for
        add_widget. It allows you to add widgets as a list.

        ie.
            ...
            parent.add( widget1, widget2, widget3 )
        """
        if widgets:
            for wid in widgets:
                self.add_widget(wid)
        if kw_widgets:
            for key, val in kw_widgets.viewitems():
                try:
                    setattr(self, key, val)
                except:
                    raise ValueError('Widgets could not be added')


class Box(CustomWidget, BoxLayout):
    pass


class Float(CustomWidget, FloatLayout):
    pass


class Anchor(CustomWidget, AnchorLayout):
    pass


class Stack(CustomWidget, StackLayout):
    pass


class Grid(GridLayout, CustomWidget):
    pass


class Relative(CustomWidget, RelativeLayout):
    pass


class CoolLoader(Widget):
    states = BooleanProperty(True)

    # Set this to True if you want the animation to start
    loading = BooleanProperty(False)

    desired_color = ListProperty([.7, .1, .9, 1])

    text = StringProperty()

    """
        The 'current' and 'max' property should be set if you want the
        widget to load as long as current < max.

        The animation will still animate as long as current < max.

        i.e current = 0%
            max     = 100%
            This will load up to 100%
    """
    current = NumericProperty(1.)

    max = NumericProperty(100.)

    def __init__(self, **kwargs):
        super(CoolLoader, self).__init__(**kwargs)

        with self.canvas.before:
            d = 120.  # Initial diameter
            pos = (self.x - d / 2.0, self.y - d / 2.0)
            self.colors = Color(1, 1, 1, 1)
            self.back_shape = Ellipse(*pos, size=(d, d))
            self.color = Color(.93, .44, .39, 1)
            self.shape = Ellipse(*pos, size=(d + 8, d + 8))
            self.color_d = Color(1, 1, 1, 1)
            self.shape_a = Ellipse(*pos, size=(d, d))

        self._in_text = Label(text=self.text)
        self._in_text.font_size = 16

        self.bind(size=self.update_geometry,
                  pos=self.update_geometry,
                  desired_color=self.update_colors,
                  loading=self._change_state,
                  text=self.update_text,
                  current=self.delta_level)

        self.add_widget(self._in_text)

    def delta_level(self, ins, val):
        """
        Shows the difference in ratio form of 'current' property and 'max'
        property.
        The value is then shown on label.
        """
        if val >= self.max:
            self.loading = False
        text = (val / self.max) * 100
        self.text = str(text) + "%"

    def update_text(self, ins, val):
        self._in_text.text = str(val)

    def update_colors(self, ins, val):
        if not len(val) == 4:
            return
        anim = Animation(rgba=val, duration=0.5)
        anim.start(self.color)

    def update_geometry(self, ins, val):
        """
        Configures the position and size of the circle in respect to
        the position and size of the Widget, considering the graphic and Widgets
        components are two entities
        """
        self.shape.size = ins.height, ins.height
        self.back_shape.size = ins.height, ins.height
        self.shape.pos = ins.pos
        self.back_shape.pos = ins.pos
        self.shape_a.size = (50, 50)
        self.shape_a.pos = [self.x + float(self.shape.size[0]) / 2.0 - self.shape_a.size[0] / 2,
                            self.y + float(self.shape.size[0] / 2.0) - self.shape_a.size[1] / 2]
        self._in_text.size_hint = None, None
        self._in_text.size = Vector(self.shape_a.size) * .35
        self._in_text.color = [.0, .0, .0, 1]
        self._in_text.pos_hint_x = None
        self._in_text.pos_hint_y = None
        self._in_text.pos = Vector(self.shape_a.pos) + Vector(self._in_text.size)

    def _change_state(self, ins, val):
        """
        Triggered when the 'loading' property is set to True.
        This initiates the animation by scheduling loops on the 'rotate_update'
        method
        """
        if val:
            self.change_color()
            Clock.schedule_interval(self.rotate_update, 1. / 60.)
        else:
            self.__time = 0
            Clock.unschedule(self.rotate_update)

    def change_color(self):
        self.desired_color = [random.random(), random.random(), random.random(), 1]

    __time = 0  # internal
    __delta = 1.5 if platform in ['ios', 'android'] else 0.1  # internal

    parentWidget = ObjectProperty(None)

    def rotate_update(self, dt):

        self.__time += self.__delta

        if self.__time >= 50:
            self.parentWidget.done_loading()

        if self.color.rgba == self.desired_color:
            self.change_color()
        if self.states:
            self.shape.angle_end -= 2
            if self.shape.angle_end == -360:
                self.shape.angle_end = 360


class FlatTextInput(TextInput):
    """
    Flat version of the standard TextInput.
    """

    show_underline = BooleanProperty(True)

    # If true a line of the same color of the cursor will be drawn under the text.
    cursor_color = ListProperty([0, 0, 0, .8])
    '''Represents the rgba color used to render the cursor.

    .. versionadded:: 1.0

    :attr:`cursor_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [ 1, 0, 0, .8 ].
    '''

    def __init__(self, **kargs):
        if 'background_color' not in kargs.keys():
            kargs['background_color'] = [0, 0, 0, 0]
        super(FlatTextInput, self).__init__(**kargs)


Builder.load_string('''
<FlatTextInput>:
#==============================================================================
    canvas.before:

        #Background
        Color:
            rgba: self.background_color
        Rectangle:
            size: self.size
            pos: self.pos

        #Cursor
        Color:
            rgba: ( self.cursor_color if self.focus and not self.cursor_blink else [ 0, 0, 0, 1 ] )
        Rectangle:
            pos: [int(x) for x in self.cursor_pos]
            size: sp(2), -self.line_height

        #Underline
        Color:
            rgba: self.cursor_color if self.focus and self.show_underline else [ 1, 1., 1, .5 ]
        Rectangle:
            size: ( self.size[0]-3, 1 )
            pos: self.pos[0], self.cursor_pos[1] - self.line_height - 3

        #Set text color
        Color:
            rgba: self.disabled_foreground_color if self.disabled else (self.hint_text_color if not self.text and not self.focus else self.foreground_color)
''')