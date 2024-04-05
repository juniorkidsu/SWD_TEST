def factorial(number : int):
    sum_all = 1
    for i in range(1, number+1):
        sum_all = sum_all * i
    return f"Total_zero_stick is : {find_zero_stick(str(sum_all))}"

def find_zero_stick(num_stack : str):
    checker_zero_stick = 0
    for position in reversed(num_stack):
        if position != "0":
            return checker_zero_stick
        else:
            checker_zero_stick+=1

        


if __name__ == '__main__':
    print(factorial(7))