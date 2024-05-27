from tqdm import tqdm

def sub_function_a(value):
    return value * value

def sub_function_b(value):
    return value * 2

def main_function(num_list):
    result_a = []
    result_b = []
    for num in tqdm(num_list, desc='Main Function'):
        # Create a separate tqdm instance for sub_function_a
        with tqdm(total=1, desc='Sub-function A') as progress_a:
            square = sub_function_a(num)
            result_a.append(square)
            progress_a.update(1)  # Update the tqdm instance for sub_function_a

        # Create a separate tqdm instance for sub_function_b
        with tqdm(total=1, desc='Sub-function B') as progress_b:
            double = sub_function_b(num)
            result_b.append(double)
            progress_b.update(1)  # Update the tqdm instance for sub_function_b

    return result_a, result_b

if __name__ == '__main__':
    num_list = [1, 2, 3, 4, 5]
    result_a, result_b = main_function(num_list)
    print(result_a)
    print(result_b)

