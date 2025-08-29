import mysql.connector
from mysql.connector import Error

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

# استخدام الدالة للاتصال
# تأكد من استبدال القيم أدناه بمعلومات قاعدة بياناتك
connection = create_db_connection("localhost", "root", "your_password", "social_media")

# يمكنك الآن استخدام الكائن connection لإرسال استعلامات SQL
# مثال:
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM users")
# users = cursor.fetchall()
# for user in users:
#     print(user)