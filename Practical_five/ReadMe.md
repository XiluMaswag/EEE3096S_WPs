# Practical five was built on the following requirement and specifications:

In this prac you're going to sample temperature and light data from the ADC every 10 seconds. We're going to be using the Adafruit MCP3008 Library for Python.

Circuit 
You need to connect the following:
• MCP3008 CLK to Pi SCLK
• MCP3008 DOUT to Pi MISO
• MCP3008 DIN to Pi MOSI
• MCP3008 CS/SHDN to Pi CE0
• MCP3008 VDD to Pi 3.3V
• MCP3008 VREF to Pi 3.3V
• MCP3008 AGND to Pi GND
• MCP3008 DGND to Pi GND
• Build a voltage divider circuit with the LDR to measure the light and connect it to channel 0 (pin 1) of the ADC
• Read the data sheet for the MCP9700 and connect it correctly to channel 1 (pin 2) of the ADC.
