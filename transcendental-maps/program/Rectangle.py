class Rectangle:
    def __init__ (self, top, bottom, left, right):
        self . top = top
        self . bottom = bottom
        self . left = left
        self . right = right
        self . horizontal_coefficient = 1. / (right - left)
        self . vertical_coefficient = 1. / (top - bottom)
