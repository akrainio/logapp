import getopt
import re
import sys
from math import ceil, floor
from time import strptime, mktime


class Logreader:
    def __init__(self, pattern):
        self.pattern = pattern

    def get_time(self, date):
        formatted = date[:19]
        millisec = float(date[19:])
        time = mktime(strptime(formatted, self.pattern)) + millisec
        return time

    def get_size(self, file):
        file.seek(0, 2)
        return file.tell()

    def get_line_info(self, where, file):
        offset = where
        size = self.get_size(file)
        while offset != 0:
            file.seek(offset - 1)
            if file.read(1) == '\n':
                break
            offset -= 1
        file.seek(offset)
        date = file.read(23)
        if re.match("^(19|20)\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d", date) is not None:
            time = self.get_time(date)
        else:
            print("logreader: getline: '" + date + "' does not match date pattern")
            sys.exit(2)
        tail_offset = where
        while tail_offset < size:
            file.seek(tail_offset)
            if file.read(1) == '\n':
                break
            tail_offset += 1
        return offset, tail_offset + 1, time


    def parse_file(self, params):


        def find(time, is_start):
            min_offset = 0
            max_offset = in_size
            mid_offset = int((min_offset + max_offset) / 2)
            prev_mid_offset = None
            curr_start, curr_end, curr_time = self.get_line_info(mid_offset, in_file)
            while prev_mid_offset != mid_offset:
                prev_mid_offset = mid_offset
                if curr_time > time:
                    max_offset = curr_start
                elif curr_time < time:
                    min_offset = curr_end
                elif curr_time == time:
                    return curr_start
                mid_offset = int((min_offset + max_offset) / 2)
                curr_start, curr_end, curr_time = self.get_line_info(mid_offset, in_file)
            if is_start:
                return curr_start
            else:
                if curr_time < time:
                    return curr_end
                else:
                    return curr_start

        start_stamp = None
        end_stamp = None
        in_file = None

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
            elif o in ('-s', '--start'):
                if (a != ''):
                    start_stamp = self.get_time(a)
            elif o in ('-e', '--end'):
                if (a != ''):
                    end_stamp = self.get_time(a)
            else:
                print("logreader: Unhandled option '" + a + "'")

        in_file.seek(0, 2)
        in_size = self.get_size(in_file)
        if start_stamp is None:
            start_stamp = self.get_line_info(0, in_file)[2]
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
        output_array = []
        x = 0
        writer_offset = 0
        while x < end_offset - start_offset:
            x += 1
            got = in_file.read(1)
            if got == '\n':
                in_file.seek(start_offset + writer_offset)
                line = in_file.read(x - writer_offset - 1)
                in_file.seek(start_offset + x)
                output_array.append(line)
                writer_offset = x
        in_file.close()
        return output_array

    def parse_folder(self, files, start_stamp, end_stamp):
        def find(target_time):
            min_index = 0
            max_index = len(files) - 1
            mid_index = int(max_index / 2)
            def get_file_limits(file):
                start = self.get_line_info(0, file)[2]
                end = self.get_line_info(self.get_size(file) - 10, file)[2]
                return start, end
            while True:
                prev_mid = mid_index
                cur_file = open(files[mid_index], 'r')
                cur_time = get_file_limits(cur_file)
                cur_file.close()
                if cur_time[0] <= target_time <= cur_time[1]:
                    return mid_index
                if target_time < cur_time[0]:
                    max_index = mid_index
                    mid_index = int(floor((min_index + max_index) / 2))
                if cur_time[1] < target_time:
                    min_index = mid_index
                    mid_index = int(ceil((min_index + max_index) / 2))
                if prev_mid == mid_index:
                    return mid_index
        if start_stamp == '':
            cur_file = open(files[0], 'r')
            start_time = self.get_line_info(0, cur_file)[2]
            cur_file.close()
        else:
            start_time = self.get_time(start_stamp)
        if end_stamp == '':
            cur_file = open(files[len(files) - 1], 'r')
            end_time = self.get_line_info(self.get_size(cur_file) - 1, cur_file)[2]
            cur_file.close()
        else:
            end_time = self.get_time(end_stamp)
        start_file = find(start_time)
        end_file = find(end_time)
        if start_file == end_file:
            # if start_stamp == '' and end_stamp == '':
            #     return self.parse_file([start_file])
            # if start_stamp == '':
            #     return self.parse_file(["-e", end_stamp, start_file])
            # if end_stamp == '':
            #     return self.parse_file(["-s", start_stamp, start_file])
            return self.parse_file(["-s", start_stamp, "-e", end_stamp, files[start_file]])
        else:
            return self.parse_file(["-s", start_stamp, files[start_file]]) + self.parse_file(["-e", end_stamp, files[end_file]])

