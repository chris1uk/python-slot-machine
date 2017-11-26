# python-slot-machine
This is just a small fruit machine I put together to fill up some spare time.

It is based on a catagory D AWP fruit machine with a five pound jackpot 

The code does look for a coin mechanism but will work without just press 1 for credit and space to spin

this is not intended to be a fully funtional game but maybe of use to somebody 


If you wish to connect a coin mechanism the code is designed to work with an sr5/sr5i mech in cctalk mode an interface can be made using an ftdi uart and 2 small components a 10k resistor and a fast switching diode 1N4148 the diode is used to join rx and tx and the resistor pulls the signal high providing the one wire bus required for cctalk.

Other cctalk coin mechs could/should work 
