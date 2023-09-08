
#from RPi.GPIO import GPIO
#import RPi.GPIO as GPIO
from gpiozero import Button, LED


class gpio_pins():
    INTER_1_PIN = 18
    INTER_2_PIN = 12
    INTER_3_PIN = 6
    INTER_4_PIN = 5
    LED1_PIN = 23
    LED2_PIN = 4
    LED3_PIN = 21
    LED4_PIN = 16

    ALED2_PIN = 17
    ALED3_PIN = 25
    ALED1_PIN = 24

    TIRETTE_PIN = 26
    URGENCE_PIN = 20
    DEV_MODE_PIN = 22

class Device:
    list_pin = [False] * 59


class Switch(Device):
    def launch_function(self):
            self.function()

    def __init__(self, input_pin, function=None, active_high=True):
        if not Device.list_pin[input_pin]:
            self.function = function
            self.state = False
            Device.list_pin[input_pin] = True
            self.input_pin = input_pin
            self.button = Button(input_pin, pull_up=None, active_state=active_high)
            self.button.when_pressed = self.function

        else:
            raise RuntimeError('pin already in use')

    def set_function(self, function):
        self.function = function
        self.button.when_pressed = self.function

    def close(self):
        Device.list_pin[self.input_pin] = False
        self.button.close()


class LightButton(Device):
    def __init__(self, input_pin, light_pin, function=None):
        if not Device.list_pin[input_pin] and not Device.list_pin[light_pin]:
            self.function = function
            self.state = False
            Device.list_pin[input_pin] = True
            Device.list_pin[light_pin] = True
            self.auto_switch = False
            self.input_pin = input_pin
            self.light_pin = light_pin
            
            self.button = Button(self.input_pin, pull_up=None, active_state=False, bounce_time=0.01)
            self.led = LED(self.light_pin)
            
            self.button.when_pressed = self.function
            
        else:
            raise RuntimeError('pin already in use')

    def launch_function(self):
        self.function()

        if self.auto_switch:
            self.switch()

    def set_auto_switch(self, value):
        self.auto_switch = value

    def on(self):
        self.state = True
        self.led.on()

    def off(self):
        self.state = False
        self.led.off()

    def switch(self):
        if not self.state:
            self.on()
        else:
            self.off()

    def set_function(self, function):
        self.function = function
        self.button.when_pressed = self.function

    def close(self):
        Device.list_pin[self.input_pin] = False
        self.led.close()

        Device.list_pin[self.light_pin] = False
        self.button.close()

if __name__ == "__main__":
    def test():
        print("test")

    from time import sleep
    btn1 = LightButton(gpio_pins.INTER_1_PIN, gpio_pins.LED1_PIN, None)
    btn1.set_function(btn1.switch)
    btn1.on()

    btn2 = LightButton(gpio_pins.INTER_2_PIN, gpio_pins.LED2_PIN, None)
    btn2.set_function(btn2.switch)
    btn2.on()

    btn3 = LightButton(gpio_pins.INTER_1_PIN, gpio_pins.LED3_PIN, None)
    btn3.set_function(btn3.switch)
    btn3.on()

    btn4 = LightButton(gpio_pins.INTER_4_PIN, gpio_pins.LED4_PIN, None)
    btn4.set_function(btn4.switch)
    btn4.on()

    tirette = Switch(gpio_pins.TIRETTE_PIN, test, True)
    
    while 1:
        print(btn1.button.is_pressed)
        sleep(0.1)
