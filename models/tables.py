# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('folders',
                Field('dir', 'text'),
                Field('filename', 'text'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow()),
                )

# I don't want to display the user email by default in all forms.
db.folders.dir.requires = IS_NOT_EMPTY()
db.folders.filename.requires = IS_NOT_EMPTY()
db.folders.created_on.readable = db.folders.created_on.writable = False
db.folders.updated_on.readable = db.folders.updated_on.writable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
