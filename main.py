# main.py
numbers = [42, 17, 89, 33, 10, 55, 78, 21, 94, 6,3,65,78,34,14,57,98,08,12,76]

highest = max(numbers)
lowest = min(numbers)
average = sum(numbers) / len(numbers)

print(f"List of numbers: {numbers}")
print(f"Highest number: {highest}")
print(f"Lowest number: {lowest}")
print(f"Average: {average:.2f}")
