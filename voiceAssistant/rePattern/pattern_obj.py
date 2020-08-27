import re


class GetPatternByRe(object):
    """

    """
    def __init__(self, pstr):
        self._pattern_str = pstr
        # print(self._pattern_str)
        self.compile_ptn = re.compile(self._pattern_str)

    def get_compile_ptn(self):
        """
        :return:
        """
        return self.compile_ptn

    def get_compile_repair(self, ):
        pass

    def get_compile_complaint(self):
        pass

    def get_compile_quary(self):
        pass

    def get_compile_buy(self):
        pass
