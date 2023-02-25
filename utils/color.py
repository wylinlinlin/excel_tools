class FontColor:
    """ set font color """
    # 颜色码
    black = "\033[30;"  # default
    red = "\033[31;"
    green = "\033[32;"
    yellow = "\033[33;"
    blue = "\033[34;"
    violet = "\033[35;"  # 紫色
    sky_blue = "\033[36;"
    sky_blue = "\033[36;"
    white = "\033[38;"

    # 下划线标志
    default = "0m"  # default
    underline = "4m"

    # 结束标志位
    end = "\033[0m"

    # 设置字体色
    @classmethod
    def set_font(self, text, color="white", underline=False):
        if hasattr(self, color):
            if underline:
                return getattr(self, color) + self.underline + text + self.end
            else:
                return getattr(self, color) + self.default + text + self.end
        else:
            return text
