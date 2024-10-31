# Next Generation Test Runner

### Program A: Pseudo-Random Number Generator

Program A will act as a pseudo-random number generator. It reads commands from stdin, where each command is delimited by a line break, and writes responses to stdout. The program should handle the following commands:

- Hi: Responds with "Hi" on stdout.
- GetRandom: Responds with a pseudo-random integer on stdout.
- Shutdown: Gracefully terminates the program.
- Any unknown commands should be ignored.

### Program B: Controller

Program B will launch Program A as a separate process, provided as an argument. Once Program A is running, Program B should:

- Send the Hi command to Program A and verify the correct response.
- Retrieve 100 random numbers by sending the GetRandom command to Program A 100 times.
- Send the Shutdown command to Program A to terminate it gracefully.
- Sort the list of retrieved random numbers and print the sorted list to the console.
- Calculate and print the median and average of the numbers.

### How to run the program

```
python3 controller.py
```
