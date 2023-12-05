from typing import List

FILENAME = "./aoc1.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


class CalibrationValue:
    def __init__(self, raw_value: str):
        self.raw_value = raw_value

    def get_calibration_value(self) -> int:
        first_digit = 0
        second_digit = 0
        for c in self.raw_value:
            if c.isnumeric():
                first_digit = int(c)
                break
        for c in self.raw_value[::-1]:
            if c.isnumeric():
                second_digit = int(c)
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


device = CalibrationDevice(raw_data)
print(device.get_calibration_sum())
