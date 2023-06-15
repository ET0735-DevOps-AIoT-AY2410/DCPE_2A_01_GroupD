import time


from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc



def main():
    #initialization of HAL modules
    led.init()
    adc.init()
    lcd = LCD.lcd()

    lcd.lcd_clear()

    lcd.lcd_display_string("Mini-Project", 1)
    lcd.lcd_display_string("Template", 2)

    while(True):
        led.set_output(1, 1)
        time.sleep(1)

        led.set_output(1, 0)
        time.sleep(1)

        pot_val = adc.get_adc_value(1)
        print("potentiometer " +str(pot_val))
        lcd.lcd_display_string("potval " +str(pot_val), 2)
        time.sleep(1)

if __name__ == '__main__':
    main()