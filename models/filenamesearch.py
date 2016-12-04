import sys
from time import strptime, mktime


def find_filename(files):
    def get_time(date):
        formatted = date[:19]
        millisec = float(date[19:])
        time = mktime(strptime(formatted, pattern)) + millisec
        return time

    def get_line_info(where, file):
        offset = where
        while offset != 0:
            file.seek(offset - 1)
            if file.read(1) == '\n':
                break
            offset -= 1
        file.seek(offset)
        date = file.read(23)
        if re.match("^(19|20)\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d", date) is not None:
            time = get_time(date)
        else:
            print("logreader: getline: '" + date + "' does not match date pattern")
            sys.exit(2)
        tail_offset = where
        while tail_offset < in_size:
            in_file.seek(tail_offset)
            if in_file.read(1) == '\n':
                break
            tail_offset += 1
        return offset, tail_offset + 1, time

    def find(time, is_start):
        min_offset = 0
        max_offset = in_size
        mid_offset = int((min_offset + max_offset) / 2)
        prev_mid_offset = None
        curr_start, curr_end, curr_time = get_line_info(mid_offset)
        while prev_mid_offset != mid_offset:
            prev_mid_offset = mid_offset
            if curr_time > time:
                max_offset = curr_start
            elif curr_time < time:
                min_offset = curr_end
            elif curr_time == time:
                return curr_start
            mid_offset = int((min_offset + max_offset) / 2)
            curr_start, curr_end, curr_time = get_line_info(mid_offset)
        if is_start:
            return curr_start
        else:
            if curr_time < time:
                return curr_end
            else:
                return curr_start

    pattern = "%Y-%m-%d %H:%M:%S"



if __name__ == '__main__':
    main(sys.argv[1:])