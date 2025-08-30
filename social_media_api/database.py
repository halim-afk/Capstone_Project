import mysql.connector
from mysql.connector import Error
from decouple import config

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
db_host = config('DB_HOST')
db_user = config('DB_USER')
db_password = config('DB_PASSWORD')
db_name = config('DB_NAME')
# استخدام الدالة للاتصال
# تأكد من استبدال القيم أدناه بمعلومات قاعدة بياناتك
connection = create_db_connection(db_host, db_user, db_password, db_name)

# يمكنك الآن استخدام الكائن connection لإرسال استعلامات SQL
# مثال:
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM users")
# users = cursor.fetchall()
# for user in users:
#     print(user)