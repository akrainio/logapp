import getopt
import re
import sys
from time import strptime, mktime


def main(params):
    def get_time(date):
        formatted = date[:19] + date[23:]
        millisec = float(date[19:23])
        time = mktime(strptime(formatted, pattern)) + millisec
        return time

    def get_line_info(where):
        offset = where
        while offset != 0:
            in_file.seek(offset - 1)
            if in_file.read(1) == '\n':
                break
            offset -= 1
        in_file.seek(offset)
        date = in_file.read(29)
        if re.match("^(19|20)\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d (-|\+)\d{4}", date) is not None:
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

    out_file = sys.__stdout__
    start_stamp = None
    end_stamp = None
    in_file = None
    pattern = "%Y-%m-%d %H:%M:%S %z"

    try:
        opts, args = getopt.getopt(params, "ho:s:e:", ["help", "output=", "start=", "end="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    in_filename = args[0]
    try:
        in_file = open(in_filename, "r")
    except IOError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            print("logreader: -o <outputfile> -s <starttimestamp> -e <endtimestamp>")
        elif o in ('-o', '--outputfile'):
            try:
                out_file = open(a, "w")
            except IOError as err:
                print("I/O error({0}): {1}".format(err.errno, err.strerror))
                sys.exit(2)
        elif o in ('-s', '--start'):
            start_stamp = get_time(a)
        elif o in ('-e', '--end'):
            end_stamp = get_time(a)
        else:
            print("logreader: Unhandled option '" + a + "'")

    in_file.seek(0, 2)
    in_size = in_file.tell()
    if start_stamp is None:
        start_stamp = get_line_info(0)[2]
    if end_stamp is not None:
        if start_stamp > end_stamp:
            temp_stamp = end_stamp
            end_stamp = start_stamp
            start_stamp = temp_stamp
        end_offset = find(end_stamp, False)
    else:
        end_offset = in_size
    start_offset = find(start_stamp, True)
    in_file.seek(start_offset)
    x = 0
    while x < end_offset - start_offset:
        x += 1
        got = in_file.read(1)
        out_file.write(got)
    in_file.seek(in_size - 1)
    if in_file.read(1) is not "\n":
        out_file.write("\n")
    in_file.close()
    out_file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
