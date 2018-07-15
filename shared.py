import re

def filter_helper(pattern: re, negative=False):
    def local(data):
        result = pattern.search(data)
        if negative:
            return not result
        else:
            return result
    return local


def filter_out(data: list, pattern: re, negative=False):
    return list(filter(filter_helper(pattern, negative), data))


def extract_re(data: list, pattern: re, group=0):
    result = []
    for item in data:
        match_obj = pattern.search(item)
        if match_obj:
            result.append(match_obj.group(group))
    return result


re_good_request = re.compile(".*\"(GET|HEAD) /(robots\.txt|.*\.(png|css|js|ico))?.*\"")

access_logs_list = []
filtered_requests = filter_out(access_logs_list, re_good_request, True)


def initialize_log_file(path):
    global access_logs_list, filtered_requests
    file = open(path, "r")
    access_logs_list = file.read().split("\n")
    file.close()

    filtered_requests = filter_out(access_logs_list, re_good_request, True)