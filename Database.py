import mysql.connector
import mysql.connector.errors

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
        cur.execute("CREATE DATABASE IF NOT EXISTS M_DB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_as_cs;")
        cur.execute("USE M_DB;")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS User(User_Id varchar(35) PRIMARY KEY NOT NULL,UserName varchar(20) UNIQUE, "
            "Passwd varchar(200), Email varchar(100) UNIQUE);")
        cur.execute("CREATE TABLE IF NOT EXISTS Detail (u_id varchar(35), FirstName varchar(50), LastName varchar(50), Age int, Gender varchar(10), "
            "Mobile_No int, DOB date, FOREIGN KEY(u_id) REFERENCES User(User_Id) ON UPDATE CASCADE ON DELETE CASCADE);")
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
            f"INSERT INTO User (User_Id, UserName, Passwd, email) VALUES (%s,%s,%s,%s);",
            (kwargs['uid'], kwargs['uname'], kwargs['passwd'], kwargs['email'])
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
            f"update Detail set FirstName=%s,LastName=%s,Age=%s,Gender=%s,Mobile_No=%s,DOB=%s WHERE u_id=%s;",
            (kwargs["fname"], kwargs["lname"], kwargs["age"], kwargs["gender"], kwargs["mob"], kwargs["dob"],
             kwargs["uname"])
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        conn.close()


def retrieve_users():

    global User_Sql, Password_Sql
    res, di = None,{}
    conn = connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute(f"SELECT UserName,User_Id FROM User;")
        res = cur.fetchall()
        di = {}
        for i in res:
            di[i[0]]=i[1]         
    except mysql.connector.errors as err:
        print(err.msg)
    finally:
        conn.close()
        return di


def check(username, password):
    global User_Sql, Password_Sql

    conn = connector(User_Sql, Password_Sql)
    try:
        cur = conn.cursor()
        cur.execute("USE M_DB;")
        cur.execute(f"SELECT * from User where UserName=%s and Passwd=%s", (username, password))
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
        cur.execute("DROP TABLE IF EXISTS Detail;")
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
        cur.execute(f"UPDATE User SET Passwd = %s WHERE UserName = %s;", (username, newpass))
        conn.commit()
        return True
    except Exception as e:
        print(e)
    finally:
        conn.close()



if __name__ == "__main__":
    initialize("root", "ABCD1234!@")
    # delete()
    insert_user(uid = "w",uname="U", passwd = "2", email="wq")
    insert_user(uid = "Q",uname="u", passwd = "2", email="dw1")
    print("Check 1 : ", check("U","2"))
    print("Check 2 : ", check("u","2"))
    res = retrieve_users()
    print(res)

    # delete()
    pass
