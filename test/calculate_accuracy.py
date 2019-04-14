import os

executable_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "src", "char2", "pinyin.py")
input_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "input1.txt")
output_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "output1.txt")
std_output_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "output_std1.txt")
return_value = os.system("python3 " + executable_file_path + " " +
                         input_file_path + " " + output_file_path)
if return_value == 0:
    total_sentence_number = 0
    accurate_sentence_number = 0
    total_character_number = 0
    accurate_character_number = 0
    with open(output_file_path, 'r') as output_file, open(std_output_file_path, 'r') as std_output_file:
        for sentence, std_sentence in zip(output_file, std_output_file):
            # Sentence
            if sentence == std_sentence:
                accurate_sentence_number += 1
            else:
                print(sentence, "should be", std_sentence)
            total_sentence_number += 1
            # Character
            for character, std_character in zip(sentence, std_sentence):
                if character == std_character:
                    accurate_character_number += 1
                total_character_number += 1
    print("Sentence accuracy:", accurate_sentence_number, "/", total_sentence_number,
          "=", accurate_sentence_number / total_sentence_number * 100, "%")
    print("Character accuracy:", accurate_character_number, "/", total_character_number,
          "=", accurate_character_number / total_character_number * 100, "%")
else:
    print("Pinyin program is not executed properly.")
