from typing import List

FILENAME = "./aoc2.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


WORD_TO_NUM = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

VALID_WORDS = WORD_TO_NUM.keys()


class CalibrationValue:
    def __init__(self, raw_value: str):
        self.raw_value = raw_value

    def get_calibration_value(self) -> int:
        first_digit = 0
        second_digit = 0
        for i in range(len(self.raw_value)):
            c = self.raw_value[i]
            if c.isnumeric():
                first_digit = int(c)
                break

            snip = self.raw_value[i:]
            for word in VALID_WORDS:
                if snip.startswith(word):
                    first_digit = WORD_TO_NUM[word]
                    break
            else:
                continue
            break

        for i in range(len(self.raw_value)-1, -1, -1):
            c = self.raw_value[i]
            if c.isnumeric():
                second_digit = int(c)
                break

            snip = self.raw_value[i:]
            for word in VALID_WORDS:
                if snip.startswith(word):
                    second_digit = WORD_TO_NUM[word]
                    break
            else:
                continue
            break

        num = int(f'{first_digit}{second_digit}')
        return num


class CalibrationDevice:
    calibration_values: List[CalibrationValue]

    def __init__(self, raw_data: List[str]):
        self.calibration_values = []
        for raw_value in raw_data:
            self.calibration_values.append(CalibrationValue(raw_value))

    def get_calibration_sum(self) -> int:
        return sum([value.get_calibration_value() for value in self.calibration_values])

    def get_all_calibrated_values(self):
        for value in self.calibration_values:
            print(value.raw_value)
            print(value.get_calibration_value())
            print()

device = CalibrationDevice(raw_data)
print(device.get_all_calibrated_values())
print(device.get_calibration_sum())
