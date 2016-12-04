import os
import models.logreader


# @auth.requires_signature()
def upload_file():
    # Uploads file to the logs folder
    print(request.folder)
    path = os.path.join(request.folder, "logs", request.vars.file.filename)
    print(path)
    new_log = open(os.path.abspath(path), 'w')
    new_log.write(request.vars.file.value)
    new_log.close()
    return "ok"


def get_stamps():
    # params = ["-s", request.vars.start_stamp, "-e", request.vars.end_stamp, os.path.join(request.folder, "logs", "smallLog.log")]
    params = [[os.path.join(request.folder, "logs", "smallLog.log")], request.vars.start_stamp, request.vars.end_stamp]
    reader = Logreader("%Y-%m-%d %H:%M:%S")
    parsed = (reader.parse_folder([os.path.join(request.folder, "logs", "smallLog.log"), os.path.join(request.folder, "logs", "smallLog2.log")], request.vars.start_stamp, request.vars.end_stamp))
    print(parsed)
    return response.json(dict(parsed=parsed))
