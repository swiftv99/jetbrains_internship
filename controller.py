import subprocess
import statistics

def main():
    # Start Program A as a subprocess
    process = subprocess.Popen(
        ["python3", "pseudo_random_generator.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        text=True
    )

    def send_command(command):
        """Send a command to Program A and read the response."""
        process.stdin.write(command + "\n")
        process.stdin.flush()
        for _ in range(5):
            process.stdout.readline()
        return process.stdout.readline().strip()

    # Step 1: Send "Hi" command and verify the response
    if send_command("Hi") != "Hi":
        print("Failed to receive expected 'Hi' response")
        process.terminate()
        return

    # Step 2: Collect 100 random numbers
    random_numbers = []
    for _ in range(100):
        response = send_command("GetRandom")
        try:
            number = int(response)
            random_numbers.append(number)
        except ValueError:
            print(f"Unexpected response: {response}")

    # Step 3: Send "Shutdown" to terminate Program A
    send_command("Shutdown")
    process.wait()  # Ensure the process has terminated

    # Step 4: Sort the list and calculate median and average
    random_numbers.sort()
    median = statistics.median(random_numbers)
    average = statistics.mean(random_numbers)

    # Output the results
    print("Sorted random numbers:", random_numbers)
    print("Median:", median)
    print("Average:", average)

if __name__ == "__main__":
    main()
