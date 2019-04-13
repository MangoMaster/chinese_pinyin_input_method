import os

executable_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "src", "word2", "pinyin.py")
input_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "input1.txt")
output_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "output1.txt")
std_output_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "std_output1.txt")
return_value = os.system("python3 " + executable_file_path + " " +
                         input_file_path + " " + output_file_path)
if return_value == 0:
    total_number = 0
    accurate_number = 0
    with open(output_file_path, 'r') as output_file, open(std_output_file_path, 'r') as std_output_file:
        for output, std_output in zip(output_file, std_output_file):
            if output == std_output:
                accurate_number += 1
            else:
                print(output, "should be", std_output)
            total_number += 1
    print("Accuracy:", accurate_number, "/", total_number,
          "=", accurate_number / total_number * 100, "%")
else:
    print("Pinyin program is not executed properly.")
