import datetime
import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    # math.ceil rounds up; math.floor rounds down
    read_time_min = math.ceil(count/200.0)  # assuming 200 words per minute
    return int(read_time)  
