"""
These are a set of Widgets extended from the original kivy widgets to give
a different feel and look of the interface.
They can use used and manipulated normally as default kivy widgets.
Buttons:
    RoundButton - Round button. make sure you make the width and height equal so it can been
                a perfect circle.
    RectButton - Rectangular buttons with different colors and states

from UiUx import *
from kivy.app import App

class Myapp(App):
    def build(self):
        root = Box()
        button = RectButton(text="Kivy")
        button.nature = "danger"
        button.size_hint = (None, None)
        root.add(button) #add can accept multiple widgets. i.e root.add(Lable, Button)
        return root
"""

from kivy.clock import Clock
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import DictProperty
from kivy.lang import Builder

Ellipse = Factory.Ellipse
Line = Factory.Line
Color = Factory.Color
Rectangle = Factory.Rectangle

NumericProperty = Factory.NumericProperty
ObjectProperty = Factory.ObjectProperty
ListProperty = Factory.ListProperty
BooleanProperty = Factory.BooleanProperty
StringProperty = Factory.StringProperty

Image = Factory.Image
Button = Factory.Button
ButtonBehavior = Factory.ButtonBehavior
Label = Factory.Label


class Base(object):
    draggable = BooleanProperty(False)
    button_type = DictProperty({'danger': [.93, .44, .39, 1.],
                                'success': [.33, .84, .55, 1.],
                                'warning': [.96, .83, .30, 1.],
                                'default': [.80, .80, .80, .5],
                                'blue': [.36, .68, .89, 1.]})

    nature = StringProperty('default')
    blink_color = ListProperty([.8, .8, .8, .5])
    blink = BooleanProperty(False)
    r_state = True

    def __init__(self, **kwargs):
        super(Base, self).__init__(**kwargs)

    def allow_blink(self, ins, val):
        if val:
            Clock.schedule_interval(self.blink_update, 1 / 3.)
        if not val:
            Clock.unschedule(self.blink_update)

    def blink_update(self, dt):
        self.run_blinks = True
        if self.r_state:
            self.background_color = self.blink_color
            self.r_state = False
            return
        if not self.r_state:
            self.background_color = self.back_color
            self.r_state = True
            return

    def _update_blink_color(self, ins, val):
        self.blink_color = val

    def do_press(self):
        if self.blink:
            self.blink = False
        # self.canvas.before.children[0].rgba = color

    def do_release(self):
        if 'run_blinks' in dir(self):
            self.blink = True

class FullRoundButton(ButtonBehavior, Base):
    background_color = ListProperty([])
    nature = StringProperty('default')
    back_color = ListProperty(Base.button_type.defaultvalue[nature.defaultvalue])
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(FullRoundButton, self).__init__(**kwargs)
        self.kwargs = kwargs
        if self.kwargs.get('nature'):
            self.button_nature = self.kwargs.get('nature')
        self.back_color = self.button_type[self.nature]
        with self.canvas.before:
            d = 60.
            self.background_color = self.back_color
            Color(*self.back_color, mode="rgba")
            self.shape_ = Factory.Ellipse(pos=self.pos, size=self.size)
            #self.circle = Factory.Line(ellipse=[self.x + 10, self.y + 10,
            #                                     self.width - 20, self.height - 20],
            #                                     width=1.2)

        self.bind(size=self._update_rect,
                  pos=self._update_rect,
                  nature=self.update_nature,
                  background_color=self._delta_bg_color,
                  color=self._text_color,
                  blink_color=self._update_blink_color,
                  blink=self.allow_blink)

    def _text_color(self, ins, val):
        self.color = val

    # self.disabled_color = val

    def _delta_bg_color(self, ins, val):
        self.canvas.before.children[0].rgba = val

    def update_nature(self, ins, val):
        self.nature = val
        self.back_color = self.button_type[self.nature]
        self.canvas.before.children[0].rgba = self.back_color

    def _update_rect(self, ins, val):
        self.shape_.pos = ins.pos
        self.shape_.size = ins.size
        #self.circle.ellipse = [self.x + 10, self.y + 10, self.width - 20, self.height - 20]
    def _do_press(self):
        super(FullRoundButton, self).do_press()

    def _do_release(self):
        super(FullRoundButton, self).do_release()

class ShadedRoundButton(FullRoundButton, Label):
    
    pass


Factory.register('ShadedRoundButton', cls=ShadedRoundButton)


class RoundButtonNature(ButtonBehavior, Base):
    background_color = ListProperty([])
    nature = StringProperty('default')
    back_color = ListProperty(Base.button_type.defaultvalue[nature.defaultvalue])
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(RoundButtonNature, self).__init__(**kwargs)
        self.kwargs = kwargs
        if self.kwargs.get('nature'):
            self.button_nature = self.kwargs.get('nature')
        self.back_color = self.button_type[self.nature]
        with self.canvas.before:
            d = 60.
            self.background_color = self.back_color
            self.shape_color = Color(*self.back_color, mode="rgba")
            self.shape_ = Factory.Ellipse(size=self.size, pos=self.pos)
            #self.circle = Factory.Line(ellipse=[self.x + 10, self.y + 10,
            #                                     self.width - 20, self.height - 20],
            #                                     width=1.2)

        self.bind(size=self._update_rect,
                  pos=self._update_rect,
                  nature=self.update_nature,
                  background_color=self._delta_bg_color,
                  color=self._text_color,
                  blink_color=self._update_blink_color,
                  blink=self.allow_blink)

    def _text_color(self, ins, val):
        self.color = val
    


    # self.disabled_color = val

    def _delta_bg_color(self, ins, val):
        self.canvas.before.children[0].rgba = val

    def update_nature(self, ins, val):
        self.nature = val
        self.back_color = self.button_type[self.nature]
        self.canvas.before.children[0].rgba = self.back_color
        self.shape_color = self.back_color

    def _update_rect(self, ins, val):
        self.shape_.pos = ins.pos
        self.shape_.size = ins.size
        #self.circle.ellipse = [self.x + 10, self.y + 10, self.width - 20, self.height - 20]

    def _do_press(self):
        super(RoundButtonNature, self).do_press()

    def _do_release(self):
        super(RoundButtonNature, self).do_release()


class RoundButtonTemplate(RoundButtonNature, Label):
    pass


kv_image = Builder.load_string('''
<AbstractImage>:
    canvas:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            texture: self.texture
            size: self.size
            pos: self.pos
''')


class ImageButton(ButtonBehavior, Image):
    pass


class RoundButton(RoundButtonTemplate):
    button_nature = 'default'


class ButtonMeta(Button, Base):
    background_normal = StringProperty('/res/background_pic.png')
    background_down = StringProperty('/res/modal_view.png')
    allow_animation = BooleanProperty(True)
    border = ListProperty([16, 16, 16, 16])
    background_color = ListProperty([.79, .81, .82, 1])
    back_color = ListProperty(Base.button_type.defaultvalue[Base.nature.defaultvalue])
    font_size = NumericProperty('15sp')
    color_down = ListProperty([1, 1, 1, .5])
    state_image = StringProperty("resources/b1.png")

    def __init__(self, **kwargs):
        super(ButtonMeta, self).__init__(**kwargs)
        self.kwargs = kwargs
        if kwargs.get('nature'):
            self.background_color = list(self.button_type[kwargs.get('nature').lower()])
            self.back_color = self.background_color
        self.bind(nature=self._delta_nature)
        self.bind(blink_color=self._update_blink_color, blink=self.allow_blink)

    def _delta_nature(self, ins, val):
        color = self.button_type[val.lower()]
        self.back_color = color
        self.background_color = color

    def refresh(self):
        self.__init__(**self.kwargs)

    def _do_press(self, *arg):
        self.temp_color = self.background_color
        self.background_color = self.color_down

    def _do_release(self, *arg):
        self.background_color = self.temp_color

class _MaterialButton( ButtonBehavior, Label ) : #labels.BindedLabel ) :
    '''
    Replacement for Button class, just more flexible...
    '''

    background_color = ListProperty( [ 1, 1, 1, 1 ] )
    '''Represents the rgba color used to render the frame in the normal state.

    .. versionadded:: 1.0

    The :attr:`background_color` is a
    :class:`~kivy.properties.ListProperty` and defaults to [ 0, 0, 0, 0 ].
    '''

    background_color_down = ListProperty( [ 0, 0, 0, .2 ] )
    '''Represents the rgba color used to render the frame in the down state.

    .. versionadded:: 1.0

    :attr:`background_color_down` is a :class:`~kivy.properties.ListProperty`.
    '''

    color_down = ListProperty( [ 0, 0, 0, .8 ] )
    '''Represents the rgba color used to render the button text in the down state.

    .. versionadded:: 1.0

    :attr:`color_down` is a :class:`~kivy.properties.ListProperty`.
    '''

    background_color_disabled = ListProperty( [ 0, 0, 0, .1 ] )
    '''Represents the rgba color used to render the button when disabled.

    .. versionadded:: 1.0

    :attr:`background_color_down` is a :class:`~kivy.properties.ListProperty`
    '''

    icon = StringProperty( '' )
    '''Icon image file.

    .. versionadded:: 1.0

    :attr:`icon` is a :class:`~kivy.properties.StringProperty`, default to ''.
    '''

    shadow_alpha = NumericProperty( 0.05 )
    '''Alpha channel used to render the rgba shadow.

    .. versionadded:: 1.0

    :attr:`shadow_alpha` is a :class:`~kivy.properties.NumericProperty`, default to 0.4.
    '''

    corner_radius = NumericProperty( dp(2) )
    '''Button corner radius.

    .. versionadded:: 1.0

    :attr:`corner_radius` is a :class:`~kivy.properties.NumericProperty`.
    '''
    
    def __init__( self, **kargs ) :
        if not 'valign' in kargs.keys() : kargs['valign'] = 'middle'
        if not 'halign' in kargs.keys() : kargs['halign'] = 'center'
        super( _MaterialButton, self ).__init__( **kargs )
    
        for key in kargs.keys() :
            self.__setattr__( key, kargs[key] )


class SquareButton(ButtonMeta):
    pass
	
class RaisedButton( _MaterialButton ) :
    '''
    Material UI raised button.
    '''
   
    pass

Builder.load_string('''
#==============================================================================
<RaisedButton>:
#==============================================================================

	canvas.before:

        PushMatrix:
        Translate:
            x: root.pos[0]
            y: root.pos[1]

        PushMatrix:
        Translate:
            y: -1

		#Shadow
		Color:
            rgba: [ 0.4, 0.4, 0.4, root.shadow_alpha if root.state != 'down' else 0 ]

        #Fill
		Rectangle:
			size: root.size[0]/2, root.size[1]-2*root.corner_radius
			pos: 0, root.corner_radius
		Rectangle:
			size: root.size[0]/2, root.size[1]-2*root.corner_radius
			pos: root.size[0]/2, root.corner_radius
		Rectangle:
			size: root.size[0]-2.4*root.corner_radius, root.corner_radius
			pos: 1.2*root.corner_radius, root.size[1]-root.corner_radius
		Rectangle:
			size: root.size[0]-2.4*root.corner_radius, root.corner_radius
			pos: 1.2*root.corner_radius, 0

        #Corners
        Ellipse:
            size: root.corner_radius*2, root.corner_radius*2
            pos: 0, 0
        Ellipse:
            size: root.corner_radius*2, root.corner_radius*2
            pos: root.size[0]-2*root.corner_radius, 0
        Ellipse:
            size: root.corner_radius*2, root.corner_radius*2
            pos: 0, root.size[1]-2*root.corner_radius
        Ellipse:
            size: root.corner_radius*2, root.corner_radius*2
            pos: root.size[0]-2*root.corner_radius, root.size[1]-2*root.corner_radius

        PopMatrix:

#Content color
		Color:
            rgba: ( root.background_color if root.state == 'normal' else root.background_color_down ) if not root.disabled else root.background_color_disabled

    #Fill
		Rectangle:
			size: root.size[0]/2, root.size[1]-2*root.corner_radius
			pos: 0, root.corner_radius
		Rectangle:
			size: root.size[0]/2, root.size[1]-2*root.corner_radius
			pos: root.size[0]/2, root.corner_radius
		Rectangle:
			size: root.size[0]-2*root.corner_radius, root.corner_radius
			pos: root.corner_radius, root.size[1]-root.corner_radius
		Rectangle:
			size: root.size[0]-2*root.corner_radius, root.corner_radius
			pos: root.corner_radius, 0

    #Corners
        Ellipse:
            size: root.corner_radius*2, root.corner_radius*2
            pos: 0, 0
        Ellipse:
            size: root.corner_radius*2, root.corner_radius*2
            pos: root.size[0]-2*root.corner_radius, 0
        Ellipse:
            size: root.corner_radius*2, root.corner_radius*2
            pos: 0, root.size[1]-2*root.corner_radius
        Ellipse:
            size: root.corner_radius*2, root.corner_radius*2
            pos: root.size[0]-2*root.corner_radius, root.size[1]-2*root.corner_radius

        PopMatrix:

    canvas.after:

        Color:
            rgba: [1,1,1,1] if self.icon and self.icon != '' else [0,0,0,0]
        Rectangle:
            source: self.icon
            pos: root.center[0]-min(root.size)/2.4, root.center[1]-min(root.size)/2.4
            size: min(root.size)/1.2, min(root.size)/1.2

''')