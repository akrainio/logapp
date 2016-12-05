import os
import models.logreader


@auth.requires_signature()
def upload_file():
    # Uploads file to the logs folder
    path = os.path.join(request.folder, "logs", request.vars.file.filename)
    new_log = open(os.path.abspath(path), 'w')
    new_log.write(request.vars.file.value)
    new_log.close()
    duplicates = db(
        (db.files.folder == request.vars.selected) & (db.files.filename == request.vars.file.filename)).select()
    if len(duplicates) == 0:
        db.files.insert(
            folder=request.vars.selected,
            filename=request.vars.file.filename
        )
    return "ok"


def get_folders():
    folders = []
    rows = db(db.folders).select()
    for r in rows:
        folders.append(r.folder)
    if len(folders) == 0:
        db.folders.insert(folder="Default")
        folders.append("Default")
    return response.json(dict(folders=folders))


def add_folder():
    duplicates = db(db.folders.folder == request.vars.new_folder_name).select()
    if len(duplicates) != 0:
        return response.json(dict(succeeded=False))
    else:
        db.folders.insert(
            folder=request.vars.new_folder_name
        )
        return response.json(dict(succeeded=True))


def delete_folder():
    files = db(db.files.folder == request.vars.folder_name).select()
    for file in files:
        try:
            os.remove(os.path.join(request.folder, "logs", file.filename))
        except OSError:
            pass
    db(db.files.folder == request.vars.folder_name).delete()
    db(db.folders.folder == request.vars.folder_name).delete()


def get_stamps():
    reader = Logreader("%Y-%m-%d %H:%M:%S")
    files = db(db.files.folder == request.vars.folder).select(orderby=db.files.filename)
    file_list = []
    for file in files:
        path = os.path.join(request.folder, "logs", file.filename)
        file_list.append(path)
    parsed = (reader.parse_folder(file_list, request.vars.start_stamp, request.vars.end_stamp))
    print(parsed)
    return response.json(dict(parsed=parsed))
