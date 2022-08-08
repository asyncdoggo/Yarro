import mysql.connector
import mysql.connector.errors

import uuid

User_Sql = None
Password_Sql = None


def connector(user: str, password: str):
    global User_Sql, Password_Sql
    User_Sql = user
    Password_Sql = password
    try:
        conn = mysql.connector.connect(host='localhost', user=user, password=password)
        return conn
    except mysql.connector.Error as err:
        print(err.msg)


def initialize(user: str, password: str):
    conn = connector(user, password)
    try:
        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS M_DB;")
        cur.execute("USE M_DB;")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS User(User_Id varchar(35) PRIMARY KEY NOT NULL,UserName varchar(20) UNIQUE, "
            "Passwd varchar(200), FirstName varchar(50), LastName varchar(50), Age int, Gender varchar(10), "
            "Mobile_No int, Email varchar(100) UNIQUE, DOB date);")
        cur.execute("CREATE OR REPLACE VIEW U_login as SELECT UserName, Passwd FROM User;")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Post(Post_Id int PRIMARY KEY NOT NULL, U_ID varchar(50) NOT NULL, "
            "content text NOT NULL, L_count int, comment_Count int, FOREIGN KEY(U_ID) REFERENCES User(User_Id) ON "
            "DELETE CASCADE ON UPDATE CASCADE);")
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
    finally:
        conn.close()


def insert_user(**kwargs):
    global User_Sql, Password_Sql
    conn = connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute(
            f"""INSERT INTO User (User_Id, UserName, Passwd,email) VALUES ("{kwargs['uid']}", "{kwargs['uname']}", "{kwargs['passwd']}", "{kwargs['email']}"); """
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        conn.close()


def update(**kwargs):
    global User_Sql, Password_Sql
    conn = connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute(
            f"""update User set FirstName="{kwargs["fname"]}", LastName="{kwargs["lname"]}", Age="{kwargs["age"]}",
            Gender="{kwargs["gender"]}", Mobile_No={kwargs["mob"]},DOB={kwargs["dob"]}
            WHERE UserName="{kwargs["uname"]}";
            """
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        conn.close()


def retrieve_users():
    global User_Sql, Password_Sql
    res = None
    conn = connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute(f"SELECT UserName FROM U_login;")
        res = cur.fetchall()
    except mysql.connector.errors as err:
        print(err.msg)
    finally:
        conn.close()
        return res


def check(username, password):
    global User_Sql, Password_Sql
    conn = connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute(f"SELECT * from U_Login where UserName=\"{username}\" and Passwd=\"{password}\"")
        res = cur.fetchall()
        return True if res else False
    except Exception as e:
        print(repr(e))
    finally:
        conn.close()


def delete():
    global User_Sql, Password_Sql
    conn = connector(User_Sql, Password_Sql)
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


def resetpasswd(username, newpass):
    global User_Sql, Password_Sql
    conn = connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute(f"UPDATE User SET Passwd = {newpass} WHERE UserName = {username};")
        conn.commit()
        return True
    except Exception as e:
        print(e)
    finally:
        conn.close()
    


if __name__ == "__main__":
    initialize("root","ABCD1234!@")
    resetpasswd("eqweq","wqqw")
    pass
    
