#include <khepera/khepera.h>


int main(int argc, char *argv[]) {
  int rc;

  /* Set the libkhepera debug level - Highly recommended for development. */
  kb_set_debug_level(2);

  printf("LibKhepera Template Program\r\n");
  
    /* Init the khepera library */
  if((rc = kb_init( argc , argv )) < 0 )
    return 1;

	/* ADD YOUR CODE HERE */

 return 0;  
}

