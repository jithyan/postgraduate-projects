/*=============================================================================
|Description:
| This program calculates the sum of squares in the interval [0, b].
| It uses threads to solve the problem, the number of threads are specified as the
| first argument to the program.
| The end of the interval 'b' is calculated from the second argument of the program, the
| increment: b = number of threads * increment
|
| For example, if the arguments are: 10 2
| The interval to calculate the sum of squares is [0,20]. The program would generate
| 10 threads that would each handle two integers from the interval. The result
| of each thread would be summed to get the final answer.
|
| Note: A constraint to this program is that the interval cannot exceed 2200,
| as that is the approximate point where the sum of squares past it cannnot be
| held in a 32bit uint32_t which is used in the implementation of this program.
+============================================================================*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <stdint.h>

/*---------------------------------------------------------------------------------------
| Data Structure: thread_args_t
|
| Description:
|  Holds all the parameters to be sent to a new thread computing sum of squares.
|
| Fields:
|  a: The starting interval.
|  b: The ending interval.
|  ans: A pointer to the final answer, shared by all threads that compute a portion
|       of the sum of squares.
*---------------------------------------------------------------------------------------*/
typedef struct {
   uint32_t a;
   uint32_t b;
   uint32_t* ans;
} thread_args_t;


/*---------------------------------------------------------------------------------------
| Function: sum_squares_threaded
|
| Description:
|  The function executed by a new thread to calculate the sum of squares of a particular
|  interval of values.
|
| Parameters:
|  param - Expects a thread_args_t struct with initialized values.
|
| Returns: Nothing.
*---------------------------------------------------------------------------------------*/
void* sum_squares_threaded(void* data);

/*---------------------------------------------------------------------------------------
| Function: safe_malloc
|
| Description:
|  Makes a call to malloc and checks if NULL is returned (which indicates there is
|  no more memory in the heap). If NULL is returned, the program terminates with
|  an error message.
|
| Parameters:
|  size - The total amount of memory that needs to be allocated.
|
| Returns: A pointer to the newly allocated memory, provided it is available.
*---------------------------------------------------------------------------------------*/
void* safe_malloc(uint32_t size);

/*---------------------------------------------------------------------------------------
| Function: sum_squares_nothread
|
| Description:
|  Computes the sum of squares in the interval [0, interval_end]
|  without thread creation. This is used to check if the threaded version of this function
|  gives correct results.
|
| Parameters:
|  interval_end: The number of integers you want to square and sum.
|
| Returns: The sum of squares
*---------------------------------------------------------------------------------------*/
uint32_t sum_squares_nothread(uint32_t interval_end);

// Global variable, initializing the mutex used for the sum_squares_threaded function
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

int main(int argc, char** argv) {
   uint32_t num_threads = 0;
   uint32_t increment = 0;

   // Validate arguments to the program
   if (argc != 3) {
      printf("Invalid number of arguments: Please enter two arguments\n");
      return 1;

   } else if (strlen(argv[1]) > 4) {
      printf("You're making too many threads!\n");
      return 1;

   } else if (strlen(argv[2]) > 4) {
      printf("Your increment is too large!\n");
      return 1;

   } else {
      num_threads = atoi(argv[1]);
      increment = atoi(argv[2]);

      if (((int32_t)increment <= 0) || ((int32_t)num_threads <= 0)) {
         printf("Invalid increment or thread number: Please enter an integer greater than 0\n");
         return 1;
      } else if ((increment * num_threads) > 2200) {
         printf("The product of increment and number of threads cannot exceed 2200.\n");
         return 1;
      }

      //Successfully validated arguments
      printf("Your arguments are:\n threads: %u, increment: %u\n\n", num_threads, increment);

      double cpu_time_used = 0;
      clock_t start, end;
      start = clock();

      uint32_t ans = 0;
      thread_args_t* args = (thread_args_t*)
         safe_malloc(sizeof(thread_args_t) * num_threads);
      pthread_t* pthread_info = (pthread_t*)
         safe_malloc(sizeof(pthread_t) * num_threads);

      //Create new threads to calculate the sum of squares
      for (uint32_t i = 0, a = 0; i < num_threads; i++) {
         args[i].a = a;
         args[i].b = increment;
         args[i].ans = &ans;
         pthread_create(&(pthread_info[i]), NULL, sum_squares_threaded, (void*) &(args[i]));
         a = a + increment;
      }

      // Wait for all threads to finish
      for (uint32_t i = 0; i < num_threads; i++) {
         pthread_join(pthread_info[i], NULL);
      }

      pthread_mutex_destroy(&mutex);
      free(pthread_info);
      free(args);

      end = clock();
      cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
      printf("Program took %f in total time to execute.\n", cpu_time_used);
      sum_squares_nothread(num_threads * increment);
      printf("\nThe answer is %u\n", ans);

      return 0;
   }
}


uint32_t sum_squares_nothread(uint32_t interval_end) {
   double cpu_time_used = 0;
   clock_t start, end;
   start = clock();
   uint32_t ans = 0;
   uint32_t a = 0;
   uint32_t b = interval_end;

   for (; a < b; a++) {
      ans = ans + (a * a);
   }

   end = clock();
   cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
   printf("Time taken to execute entire problem without multiple threads: %f\n", cpu_time_used);

   return ans;
}


void* safe_malloc (uint32_t size) {
   void* new_ptr = (void*) malloc(size);

   if (new_ptr == NULL) {
      printf("Error: Out of memory.\n");
      exit(1);
   } else {
      return new_ptr;
   }
}


void* sum_squares_threaded(void* data) {
   double cpu_time_used = 0;
   clock_t start, end;
   start = clock();

   thread_args_t* args = (thread_args_t*) data;
   uint32_t a = args->a;
   uint32_t b = args->b;
   uint32_t* ans = args->ans;
   uint32_t temp = 0;

   for (uint32_t i = 0; i < b; i++) {
      temp = temp + (a*a);
      a++;
   }

   pthread_mutex_lock(&mutex);
   *ans = *ans + temp;
   pthread_mutex_unlock(&mutex);
   end = clock();
   cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
   printf("Thread took %f time to execute.\n", cpu_time_used);
   pthread_exit((void*) 0);
}
