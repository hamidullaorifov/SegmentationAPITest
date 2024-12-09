from db.setup import db, fs
import os




# files_collection = db['files']

async def save_file_to_db(file_path: str, file_name):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            file_id = await fs.upload_from_stream(file_name, file)
        return {'status':'success','file_id':file_id}
    {'status':'fail','message':"File not found"}