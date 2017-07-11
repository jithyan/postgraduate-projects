-----------
To compile
-----------
gcc -o asg1 asg1.c -l pthread

Compiles with no warnings or errors.


--------
To use
--------
./asg1 num_thread increment

e.g. compute sum of squares from 0 to 100 using two threads:
./asg1 2 50


-------
Output
-------
Your arguments entered.
The time for each thread to complete.
The time for the entire program to complete.
The time if a single function were to compute the sum of squares without spawning threads.
The answer.


------------
Constraints
------------
Will not accept values where the product of the arguments exceed 2200.
The code uses uint32_t to guarantee that the system will use a 32 bit unsigned integer.
Using trial and error, I found approximately past the 2200 mark the sum of squares will generate a value
greater than what can be stored by a 32 bit unsigned int.

The program will produce errors if you enter any invalid arguments. Valid arguments are:
 - Positive number
 - only two arguments
 - Greater than 0
 - The product of the arguments is less than 2200