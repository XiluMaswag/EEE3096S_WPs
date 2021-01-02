#Practical one is to be done:

You are on a team responsible for developing a super simple SPI interface for working with a low baud-rate multiplexer. To save costs, you suggest that, given the scope of the
problem is so well defined and the requirements so loose, you can get away with using the GPIO pins of a cheap microcontroller instead of having to buy a microcontroller 
with dedicated SPI pins.

Your team leader takes this idea and presents it to management as their own.
Your corporate overlords then decide that contracting out development of their new simple SPI shifter device would work out even cheaper. You build up some courage and 
send an email: You're quite certain third-party developers (especially ones considered \cheap") might not have the technical insight and experience with the product 
you're developing, and perhaps might not be as experienced in the field as a whole. This unfortunately results in nothing but a meeting with HR about corporate 
structure and respecting seniors in the company.

Much to their surprise (but defnitely not yours), the code is returned badly written, dysfunctional, and completely unusable. It's clear that the 
developer they found doesn't understand SPI, or even C programming. They've now tasked you with finding the errors and fixing the code. 
Your team leader, now claiming that the idea was yours, gets upset and makes you work over the weekend to fix the problem.

Consider the code below. It is intended to implement the ability to shift out data over SPI using GPIO pins. The code below contains multiple errors -
both in terms of logic and what is expected of the SPI protocol. Using gdb, determine the failure points of the program.

You can make the following assumptions:

• The hardware is all connected and configured correctly
• Setting the variables dataPin and clockPin writes those vales to the given pins
• The clock pin normally sits sits low (CPOL = 0)
• The expected value should be written out on the rising edge of clockPin (CPHA = 1)
• The value intended to be shifted out is 0b11010101
