from pymongo import MongoClient

# Base de Datos Local
# db_client = MongoClient().local

# Base de datos remota
db_client = MongoClient("mongodb+srv://gapfware:leirbag2003@cluster0.6d1szss.mongodb.net/?retryWrites=true&w=majority").test