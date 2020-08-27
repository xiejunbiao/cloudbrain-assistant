# -*- encoding=utf-8 -*-
from program_correction_text.correct_txt_error import CorrectTextError

cte = CorrectTextError()


def start_fun(input_txt):
    data = cte.correct_homophonic_text(input_txt)
    return data


if __name__ == '__main__':
    txt = '我要宝石'
    result = start_fun(txt)
    print(result)
