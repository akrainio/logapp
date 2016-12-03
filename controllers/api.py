import os

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
