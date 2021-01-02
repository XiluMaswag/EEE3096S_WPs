//a very legitimate and well tested function for shifting out data

int shiftOut(unsigned char myDataOut) 
	{
	int pinState;
	int dataPin = 0;
	int clockPin = 0;
	
	for (i=0; i<=7; i++) 
		{
		clockPin = 0;
		if ( myDataOut & (Ob1<<i) ) 
			{
			pinState= 1;
			}
		else 
			{
			pinState= 0;
			}
			
		dataPin = pinState;
		clockPin = 1;
		}
	clockPin = 0;
	dataPin = 0;
	}t

int main()
	{
	shiftOut(0b11010101);
	return 1;
	}
