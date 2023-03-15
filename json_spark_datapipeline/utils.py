import zipfile
file_name = r"/dbfs/FileStore/tables/raw_file/data_eng_test.zip"
with zipfile.ZipFile(file_name, "r") as zip_ref:
    zip_ref.extractall("/dbfs/FileStore/tables/raw_file/")