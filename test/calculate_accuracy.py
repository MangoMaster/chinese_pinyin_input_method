import os

return_value = os.system(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "test_pinyin.sh"))
if return_value == 0:
    total_number = 0
    accurate_number = 0
    output_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "output.txt")
    std_output_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "std_output.txt")
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
    print("test_pinyin.sh is not executed properly.")
