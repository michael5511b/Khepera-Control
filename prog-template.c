#include <khepera/khepera.h>
#include <signal.h>

#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>

#include <math.h>
//#include<vector>

#define PORT 3000
#define KH4_GYRO_DEG_S   (66.0/1000.0)

static knet_dev_t * dsPic;
static int quitReq = 0; // quit variable for loop

/*--------------------------------------------------------------------*/
/* Make sure the program terminate properly on a ctrl-c */
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
/* Compute time difference

 * \param difference difference between the two times, in structure timeval type
 * \param end_time end time
 * \param start_time start time
 *
 * \return difference between the two times in [us] */
long long timeval_diff(struct timeval *difference, struct timeval *end_time, struct timeval *start_time)
{
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



/*--------velocity to pulse-------*/
int v2p(double v) {
	return (int)v / 0.678181;
}


/*---------Angular and linear velocity control of the robot----------*/
void Ang_Vel_Control(double ang, double vel) {
	int PL = (105.4 * ang + 2 * vel) / (2 * 0.678181);
	int PR = (2 * vel - 105.4 * ang) / (2 * 0.678181);
	kh4_set_speed(PL, PR, dsPic);
}




/*----------------Main Program-----------------*/
#define FOR_SPD 1000
#define SPIN_SPD 150
#define FOR_DEV_SPD 850

int main(int argc, char *argv[]) {

	/* Initial Template Setup by LinKhepera */
	int rc;

	/* Set the libkhepera debug level - Highly recommended for development. */
	kb_set_debug_level(2);

    /* Init the khepera library */
	if((rc = kb_init( argc , argv )) < 0 )
		return 1;

	/* Main Code */
  
	//printf("Wall and Object Avoidance Program\r\n");


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

  	// Set to Normal Motor Control Mode
  	kh4_SetMode(kh4RegSpeed,dsPic);
  

  	// Reset Encoders
  	 kh4_ResetEncoders(dsPic);
  
  


  	/* --------------------------------------------------- */
  	/* Socket Communication/Transmittion Code */
  	int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char sock_buffer[1024] = {0};
    // char *hello = "Hello from server";

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
    	perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 3000
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)))
    {
    	perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );

    // Forcefully attaching socket to the port 3000
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address))<0)
    {
    	perror("bind failed");
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))<0)
    {
        perror("accept");
        exit(EXIT_FAILURE);
    }


    // printf("%s\n",sock_buffer );
    // send(new_socket , hello , strlen(hello) , 0 );
    // printf("Hello message sent\n");
    /* --------------------------Socket Code End------------------------- */
  


    // Initialize a Buffer to store all the data collected from
    // the sensors by the dsPIC
    char acc_Buffer[100]; // Buffer for accelerometer
    char us_Buffer[100]; // Buffer for ultra-sonic sensors
    short usValues[5]; // Values of the 5 ultrasonic sensor readings from sensor No.1 - 5
    char ir_Buffer[256]; // Buffer for infrared sensors
    int irValues[12]; // Values of the 12 IR sensor readings from sensor No.1 - 12
    char gyro_Buffer[100]; // Buffer for Gyroscope

    double dval, dmean;
    double acc_X, acc_Y, acc_Z;
    double gyro_X, gyro_Y, gyro_Z;

    unsigned int posL, posR;
    unsigned int spdL, spdR;

    struct timeval startt,endt;
  


    // Get the starting time stamp
    gettimeofday(&startt,0x0);





    // Main Loop
    while(quitReq == 0)
    {

		  // Get current time stamp
		  gettimeofday(&endt,0x0);
		  // Print current time
		  long long t = timeval_diff(NULL, &endt, &startt);
		  long double T = t / 1000000.0;


		  //valread = read( new_socket , sock_buffer, 1024);
		  //printf("%s\n",sock_buffer );
		  //double W = strtod(sock_buffer, NULL);
		  //double W = atof(sock_buffer);
		  //memset(sock_buffer, 0, sizeof sock_buffer);

		  valread = read( new_socket , sock_buffer, 1024);
		  printf("%s\n",sock_buffer );
		  //double V = strtod(sock_buffer, NULL);
		  double V = atof(sock_buffer);
		  V = (int)V;
		  //memset(sock_buffer, 0, sizeof sock_buffer);
		  //printf("\nWW: %f\n", W);
		  printf("\nVV: %f\n", V);

		  Ang_Vel_Control(0, V);

		  printf("===============================================");
		  printf("\nTime: %Lf\n", T);

		  // Receive accelerometer readings
		  kh4_measure_acc((char *)acc_Buffer, dsPic);
		  // Receive ultrasonic sensor readings
		  //kh4_measure_us((char *)us_Buffer, dsPic);
		  // Receive infrared sensor readings
		  //kh4_proximity_ir((char *)ir_Buffer, dsPic);
		  // Receive gyroscope readings
		  kh4_measure_gyro((char *)gyro_Buffer, dsPic);
		  // Receive encoder readings
		  kh4_get_position(&posL, &posR, dsPic);
		  // Receive encoder speed readings
		  kh4_get_speed(&spdL, &spdR, dsPic);


		  // kh4_set_speed(32,-32,dsPic);


		  /* -------------- Accelerameter -------------- */
		  // Acceleration on X axis
		  printf("\nAcceleration sensor on X axis: ");

		  dmean = 0;

		  int i;

		  for (i = 0; i < 10; i++) {
			  dval = ((short)(acc_Buffer[i * 2] | acc_Buffer[ i * 2 + 1] << 8) >> 4) / 1000.0;
			  dmean += dval;
		  }

		  acc_X = dmean / 10.0;
		  printf(" %5.2f", acc_X);

		  // Acceleration on Y axis
		  printf("\nAcceleration sensor on Y axis: ");

		  dmean = 0;

		  for (i = 10; i < 20; i++) {
			  dval = ((short)(acc_Buffer[i * 2] | acc_Buffer[i * 2 + 1] << 8) >> 4) / 1000.0;
			  dmean += dval;
		  }

		  acc_Y = dmean / 10.0;
		  printf(" %5.2f", acc_Y);

		  // Acceleration on Z axis
		  printf("\nAcceleration sensor on Z axis: ");

		  dmean = 0;

		  for (i = 20; i < 30; i++) {
			  dval=((short)(acc_Buffer[i * 2] | acc_Buffer[i * 2 + 1] << 8) >> 4) / 1000.0;
			  dmean += dval;
		  }

		  acc_Z = dmean / 10.0;
		  printf(" %5.2f", acc_Z);
		  printf("\n");
		  printf("\n");
		  /*------------- Reading Accelerometer Code End --------------*/


		  /* -------------- Reading Ultrasonic Sensor -------------- */
		  /*
		  for (i = 0; i < 5; i++) {
			  usValues[i] = (short)(us_Buffer[i * 2] | us_Buffer[i * 2 + 1] << 8);
		  }
		  printf("Ultrasonic sensor 1: %5.2f \n", (double)usValues[0]);
		  printf("Ultrasonic sensor 2: %5.2f \n", (double)usValues[1]);
		  printf("Ultrasonic sensor 3: %5.2f \n", (double)usValues[2]);
		  printf("Ultrasonic sensor 4: %5.2f \n", (double)usValues[3]);
		  printf("Ultrasonic sensor 5: %5.2f \n", (double)usValues[4]);
		  printf("\n");

		   */
		  /*------------- Reading Ultrasonic Code End --------------*/

		  /* --------------- Reading Infrared sensor ---------------*/
		  /*
		  for(i = 0; i < 12; i++) {
			  irValues[i] = (ir_Buffer[i * 2] | ir_Buffer[i * 2 + 1] << 8);
			  printf("Infrared sensor %d: %d \n", i + 1, irValues[i]);
		  }
		  */
		  /* --------------- Reading Infrared sensor Code End---------------*/

		  /* -------------- Reading Gyroscope -------------- */
		  // Angular rate on X axis
		  printf("\nGyro on X axis: ");

		  dmean = 0;

		  for (i = 0; i < 10; i++) {
			  dval = ((short)(gyro_Buffer[i * 2] | gyro_Buffer[ i * 2 + 1] << 8));
			  dmean += dval;
		  }

		  gyro_X = dmean * KH4_GYRO_DEG_S / 10.0; // KH4_GYRO_DEG_S converts the reading value to deg/s
		  printf(" %5.2f deg/s", gyro_X);

		  // Angular rate on Y axis
		  printf("\nGyro on Y axis: ");

		  dmean = 0;

		  for (i = 10; i < 20; i++) {
			  dval = ((short)(gyro_Buffer[i * 2] | gyro_Buffer[ i * 2 + 1] << 8));
			  dmean += dval;
		  }

		  gyro_Y = dmean * KH4_GYRO_DEG_S / 10.0; // KH4_GYRO_DEG_S convertsthe reading value to deg/s
		  printf(" %5.2f deg/s", gyro_Y);

		  // Angular rate on Z axis
		  printf("\nGyro on Z axis: ");

		  dmean = 0;

		  for (i = 20; i < 30; i++) {
			  dval = ((short)(gyro_Buffer[i * 2] | gyro_Buffer[ i * 2 + 1] << 8));
			  dmean += dval;
		  }

		  gyro_Z = dmean * KH4_GYRO_DEG_S / 10.0; // KH4_GYRO_DEG_S convertsthe reading value to deg/s
		  printf(" %5.2f deg/s", gyro_Z);
		  printf("\n");
		  printf("\n");
		  /*------------- Reading Gyroscope Code End --------------*/

		  /*------------- Reading Encoder --------------*/
		  printf("Encoder left: %d \n", posL);
		  printf("Encoder right: %d \n", posR);
		  /*------------- Reading Encoder Code End --------------*/

		  /*------------- Reading Encoder --------------*/
		  printf("Encoder rotation speed left: %d \n", spdL);
		  printf("Encoder rotation speed right: %d \n", spdR);
		  /*------------- Reading Encoder Code End --------------*/

		  printf("===============================================");
		  printf("\n\n");


		  // This is for Socket Transmission, sending data to the client
		  // We put all the data we want to send in one big string
		  // and separate them with indicators so the client can parse the data

		  // The big string to be sent
		  char text[4096];

		  // Time stamp
		  sprintf(text, "%2.4f", T);
		  sprintf(text + strlen(text), "T");


		  // Accelerometer
		  sprintf(text + strlen(text), "%2.4f", acc_X);
		  sprintf(text + strlen(text), "AX");

		  sprintf(text + strlen(text), "%2.4f", acc_Y);
		  sprintf(text + strlen(text), "AY");

		  sprintf(text + strlen(text), "%2.4f", acc_Z);
		  sprintf(text + strlen(text), "AZ");


		  // Gyroscope
		  sprintf(text + strlen(text), "%2.4f", gyro_X);
		  sprintf(text + strlen(text), "GX");

		  sprintf(text + strlen(text), "%2.4f", gyro_Y);
		  sprintf(text + strlen(text), "GY");

		  sprintf(text + strlen(text), "%2.4f", gyro_Z);
		  sprintf(text + strlen(text), "GZ");


		  // Encoders
		  sprintf(text + strlen(text), "%d", posL);
		  sprintf(text + strlen(text), "PL");

		  sprintf(text + strlen(text), "%d", posR);
		  sprintf(text + strlen(text), "PR");

		  sprintf(text + strlen(text), "%d", spdL);
		  sprintf(text + strlen(text), "SL");

		  sprintf(text + strlen(text), "%d", spdR);
		  sprintf(text + strlen(text), "SR");

		  /*
		  // Ultrasonic sensor
		  sprintf(text + strlen(text), "%2.4f", (double)usValues[0]);
		  sprintf(text + strlen(text), "UA");

		  sprintf(text + strlen(text), "%2.4f", (double)usValues[1]);
		  sprintf(text + strlen(text), "UB");

		  sprintf(text + strlen(text), "%2.4f", (double)usValues[2]);
		  sprintf(text + strlen(text), "UC");

		  sprintf(text + strlen(text), "%2.4f", (double)usValues[3]);
		  sprintf(text + strlen(text), "UD");

		  sprintf(text + strlen(text), "%2.4f", (double)usValues[4]);
		  sprintf(text + strlen(text), "UE");


		  // Infrared sensor
		  sprintf(text + strlen(text), "%d", irValues[0]);
		  sprintf(text + strlen(text), "IA");

		  sprintf(text + strlen(text), "%d", irValues[1]);
		  sprintf(text + strlen(text), "IB");

		  sprintf(text + strlen(text), "%d", irValues[2]);
		  sprintf(text + strlen(text), "IC");

		  sprintf(text + strlen(text), "%d", irValues[3]);
		  sprintf(text + strlen(text), "ID");

		  sprintf(text + strlen(text), "%d", irValues[4]);
		  sprintf(text + strlen(text), "IE");

		  sprintf(text + strlen(text), "%d", irValues[5]);
		  sprintf(text + strlen(text), "IF");

		  sprintf(text + strlen(text), "%d", irValues[6]);
		  sprintf(text + strlen(text), "IG");

		  sprintf(text + strlen(text), "%d", irValues[7]);
		  sprintf(text + strlen(text), "IH");

		  sprintf(text + strlen(text), "%d", irValues[8]);
		  sprintf(text + strlen(text), "II");

		  sprintf(text + strlen(text), "%d", irValues[9]);
		  sprintf(text + strlen(text), "IJ");

		  sprintf(text + strlen(text), "%d", irValues[10]);
		  sprintf(text + strlen(text), "IK");

		  sprintf(text + strlen(text), "%d", irValues[11]);
		  sprintf(text + strlen(text), "IL");
		   */

		  // Have char pointer p point to the whole text, send it to the client
		  char *p = text;
		  int len = strlen(p);
		  send(new_socket , p, len , 0 );
		  usleep(105000); // wait 105 ms, time for gyro to read fresh data


	  
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
