#include <khepera/khepera.h>
#include <signal.h>

static knet_dev_t * dsPic;
static int quitReq = 0; // quit variable for loop

/*--------------------------------------------------------------------*/
/*!
 * Make sure the program terminate properly on a ctrl-c
 */
static void ctrlc_handler( int sig ) 
{
	quitReq = 1;
  
	kh4_set_speed(0 ,0 ,dsPic); // stop robot
	kh4_SetMode( kh4RegIdle,dsPic );
  
	kh4_SetRGBLeds(0,0,0,0,0,0,0,0,0,dsPic); // clear rgb leds because consumes energy
  
	kb_change_term_mode(0); // revert to original terminal if called
  
	exit(0);
}


/*------------------- Time Value Difference -----------*/
/*!
 * Compute time difference
 *

 * \param difference difference between the two times, in structure timeval type
 * \param end_time end time
 * \param start_time start time  
 *
 * \return difference between the two times in [us]
 *
 */
long long timeval_diff(struct timeval *difference,
             	 	   struct timeval *end_time,
                       struct timeval *start_time) {
	struct timeval temp_diff;

	if(difference == NULL) {
		difference =& temp_diff;
	}

	difference -> tv_sec  = end_time -> tv_sec  - start_time -> tv_sec ;
	difference -> tv_usec = end_time -> tv_usec - start_time -> tv_usec;

	/* Using while instead of if below makes the code slightly more robust. */

	while(difference -> tv_usec < 0) {
		difference -> tv_usec += 1000000;
		difference -> tv_sec  -= 1;
	}

	return 1000000LL * difference -> tv_sec + difference -> tv_usec;

} /* timeval_diff() */


/*--------real-world velocity to pulse-------*/
int v2p(double v) {
	return (int)v / 0.678181;
}

/*--------Main Program----------*/

int main(int argc, char *argv[]) {
	
	/*-----This is the pre-coded initiation stuff that came with the lib khepera template--------*/
	int rc;

	/* Set the libkhepera debug level - Highly recommended for development. */
	kb_set_debug_level(2);

	printf("LibKhepera Template Program\r\n");
	printf("Bears, Beets, Battlestar Galactica\r\n");
  
    /* Init the khepera library */
	if((rc = kb_init( argc , argv )) < 0 )
		return 1;
	/*------------------Initiation End-------------------------*/

	/*------------------Real Code Starts Here------------------*/
  
	
  
	
	
	// dsPIC is the microcontroller of khepera
	// It handles all the inputs and outputs
	dsPic  = knet_open( "Khepera4:dsPic" , KNET_BUS_I2C , 0 , NULL );
  
  
	// This is for the move forward at X m/s code
	/* 
  	  kh4_SetMode(kh4RegSpeed,dsPic);
  	  printf("Enter Speed: \r\n");
  	  double speed;
  	  scanf("%lf", &speed);
  	  int v = v2p(speed);
	*/
 
	// This is for the ctrl-C handler
	signal( SIGINT , ctrlc_handler );
  
	// Setting the term mode to 1 will return the pressed key immediately!
	kb_change_term_mode(1);
  
	/*Starting here is the code for the accelerometer reading*/
  
	// Initialize a Buffer to store all the data collected from 
	// the sensors by the dsPIC 
	char Buffer[100];
  
	// Initialize some variables
	double dval, dmean;
  
	// These variables are for the time stamps 
	struct timeval startt, endt;
  
	// Main Loop
	while(quitReq == 0)
	{
		// Get the starting time stamp 
		gettimeofday(&startt,0x0);
	  
		while(!kb_kbhit()) {
		  
			// Get current time stamp
			gettimeofday(&endt,0x0);
			// Print current time
			long long t = timeval_diff(NULL, &endt, &startt);
			long double T = t / 1000000.0;
			printf("time: %Lf\n", T);
		  
			// Receive accelerometer readings 
			kh4_measure_acc((char *)Buffer, dsPic);

			// Acceleration on X axis
			printf("\nAcceleration sensor X: ");
		  
			dmean = 0;
		  
			int i;
		  
			for (i = 0; i < 10; i++) {
				dval = ((short)(Buffer[i * 2] | Buffer[i * 2 + 1] << 8) >> 4) / 1000.0;
				dmean += dval;                                                                                       
			}
		  						
			dval = dmean / 10.0;
			printf(" %5.2f", dval); 

		  
			// Acceleration on Y axis
			printf("\nAcceleration sensor Y: ");
		  
			dmean = 0;
		  		  
			for (i = 10; i < 20; i++) {
				dval = ((short)(Buffer[i * 2] | Buffer[i * 2 + 1] << 8) >> 4) / 1000.0;
				dmean += dval;                                                                                       
			}
		  		  						
			dval = dmean / 10.0;
			printf(" %5.2f", dval); 
		  
			// Acceleration on Z axis
			printf("\nAcceleration sensor Z: ");
		  		  
			dmean = 0;
		  		  		  
			for (i = 20;i < 30; i++) {
				dval = ((short)(Buffer[i * 2] | Buffer[i * 2 + 1] << 8) >> 4) / 1000.0;
				dmean += dval;                                                                                       
			}
		  		  		  						
			dval = dmean / 10.0;
			printf(" %5.2f", dval); 
			printf("\n");
  
			usleep(5000); // us sensor needs 200ms to refresh
		  
		  
		}

		char c;
		c = getchar();
		if(c == 'q') {
			quitReq = 1;
			kb_change_term_mode(0); 
			usleep(10000); // wait some ms, without this the program would not stop! 
		}

	}

  
  
	// switch to normal key input mode
	// This is important, if we don't switch the term mode back to zero
	// It will still return the pressed key immediately
	// even at the root@r1:~/tests#
	// resulting in no characters showing up even if you press any keys on keyboard
	kb_change_term_mode(0); 	
  
	// stop robot
	kh4_set_speed(0, 0, dsPic);	
  
	// set to regular idle mode!
	kh4_SetMode(kh4RegIdle, dsPic);
  

	return 0;  
}

