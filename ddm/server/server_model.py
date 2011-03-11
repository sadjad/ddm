import peewee

database = peewee.Database(peewee.SqliteAdapter(), "ddm.db")

class User(peewee.Model):
    username = peewee.CharField()
    password = peewee.CharField()
    auth_key = peewee.CharField()
    
    class Meta:
        database = database
        
class DownloadRequest(peewee.Model):
    user = peewee.ForeignKeyField(User)
    url = peewee.CharField()
    chunks_count = peewee.IntegerField()
    size = peewee.IntegerField()
    state = peewee.IntegerField()
    
class FileChunk(peewee.Model):
    file = peewee.ForeignKeyField(DownloadRequest)
    index = peewee.IntegerField()
    chunk_state = peewee.IntegerField()
    
    
    