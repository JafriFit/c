#include <stdio.h>
// #include <math.h>  // Not necessary for this code
#include <string.h>
#include <stdlib.h>
#include <time.h>
void hello(char name[20], int age){
    printf("Hello %s, and the age is %d\n", name, age );
}


#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // Seed the random number generator with the current time
    srand(time(NULL)); ~

    // Generate a random number
    int random_number = rand() ; 

    // Print the random number
    printf("Random number: %d\n", random_number); 

    return 0;
}   
