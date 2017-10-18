import enum


class Attr(enum.Enum):
    none = 0
    x_dependant = 1
    m_dependant = 2
    indexed_x = 3
    indexed_y = 4
    enter_sub = 5
    return_sub = 6
    reset_p = 7
    set_p = 8
    branch = 9
    jump = 10
    unconditional = 11
