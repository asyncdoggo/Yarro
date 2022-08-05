import mysql.connector
import mysql.connector.errors

import uuid

User_Sql = None
Password_Sql = None

def Connector(USER, PASSWORD):
    global User_Sql, Password_Sql
    User_Sql = USER
    Password_Sql = PASSWORD    
    try:
        SQL_cnx = mysql.connector.connect(host='localhost',user=USER,password=PASSWORD)
        return SQL_cnx
    except mysql.connector.Error as err:
        print(err.msg)
        return None
    
    
def Initialize(USER, PASSWORD):
    
    conn = Connector(USER,PASSWORD)        
    try:
        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS M_DB;")
        cur.execute("USE M_DB;")
        cur.execute("CREATE TABLE IF NOT EXISTS User(User_Id varchar(200) PRIMARY KEY NOT NULL,UserName varchar(20) UNIQUE, Passwd varchar(200) NOT NULL, FirstName varchar(50), LastName varchar(50), Age int, Gender varchar(10), Mobile_No int, Email varchar(100), DOB date);")
        cur.execute("CREATE OR REPLACE VIEW U_login as SELECT UserName, Passwd FROM User;")
        cur.execute("CREATE TABLE IF NOT EXISTS Post(Post_Id int PRIMARY KEY NOT NULL, U_ID varchar(50) NOT NULL, content text NOT NULL, L_count int, comment_Count int, FOREIGN KEY(U_ID) REFERENCES User(User_Id) ON DELETE CASCADE ON UPDATE CASCADE);")        
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
        return None
    finally:
        conn.close()


def Insert_User(**kwargs):
    global User_Sql, Password_Sql
    conn = Connector(User_Sql, Password_Sql) 
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute(f"INSERT INTO User (User_Id, UserName, Passwd, FirstName, LastName, Age, Gender, Mobile_No, Email, DOB) VALUES ({kwargs['uid']},{kwargs['uname']},{kwargs['passwd']},{kwargs['fname']},{kwargs['lname']},{kwargs['age']},{kwargs['gender']},{kwargs['mob']},{kwargs['email']},{kwargs['dob']});")
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        conn.close()
        
    
def Retrive_Users():
    global User_Sql, Password_Sql
    res = None
    conn = Connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute("SELECT * FROM U_login;")
        res = cur.fetchall();        
    except mysql.connector.errors as err:
        print(err.msg)
        return None
    finally:
        conn.close()
        return res

def Del_DB():
    global User_Sql, Password_Sql
    res = None
    conn = Connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute("DROP VIEW IF EXISTS U_login;")        
        cur.execute("DROP TABLE IF EXISTS Post;")
        cur.execute("DROP TABLE IF EXISTS User;")
        cur.execute("DROP DATABASE IF EXISTS M_DB;")
        conn.commit()      
    except Exception as e:
        print(e)
    finally:
        conn.close()


    

if __name__ == "__main__":
    Initialize('root','ABCD1234!@')
    # Insert_User(uid=uuid.uuid4().int,uname="\"ADMINS\"",passwd="\"ROOTS\"",fname="\" \"",lname="\" \"",age=0,gender="\" \"",mob=0,email="\" \"",dob = "\"20-1-12\"")
    print(Retrive_Users())
    # Del_DB()
    