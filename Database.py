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
    with connector(user, password) as conn:
        try:
            cur = conn.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS M_DB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_as_cs;")
            cur.execute("USE M_DB;")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS User(User_Id varchar(35) PRIMARY KEY NOT NULL,UserName varchar(20) UNIQUE, "
                "Passwd varchar(200), Email varchar(100) UNIQUE);")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS Detail (u_id varchar(35), FirstName varchar(50), LastName varchar(50), "
                "Age int, Gender varchar(10), Mobile_No int, DOB date, FOREIGN KEY(u_id) REFERENCES User(User_Id) ON "
                "UPDATE CASCADE ON DELETE CASCADE);")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS Post(Post_Id int PRIMARY KEY NOT NULL AUTO_INCREMENT, User_Id varchar(35), "
                "content text NOT NULL, L_Count int, Comment_Count int, FOREIGN KEY(User_Id) REFERENCES User(User_Id) ON "
                "DELETE CASCADE ON UPDATE CASCADE);")
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(err)


def insert_user(**kwargs):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(
                f"INSERT INTO User (User_Id, UserName, Passwd, email) VALUES (%s,%s,%s,%s);",
                (kwargs['uid'], kwargs['uname'], kwargs['passwd'], kwargs['email'])
            )
            cur.execute(
                f"INSERT INTO Detail values (%s,null,null,null,null,null,null)", (kwargs["uid"],)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(err.msg)


def update(**kwargs):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(
                f"update Detail set FirstName=%s,LastName=%s,Age=%s,Gender=%s,Mobile_No=%s,DOB=%s WHERE u_id=%s;",
                (kwargs["fname"], kwargs["lname"], kwargs["age"], kwargs["gender"], kwargs["mob"], kwargs["dob"],
                 kwargs["uid"])
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(err.msg)


def retrieve_users():
    global User_Sql, Password_Sql
    res, di = None, {}
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(f"SELECT UserName,User_Id FROM User;")
            res = cur.fetchall()
            di = {}
            for i in res:
                di[i[0]] = i[1]
        except mysql.connector.errors as err:
            print(err.msg)
        finally:
            conn.close()
            return di


def check(username, password):
    global User_Sql, Password_Sql

    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(f"SELECT * from User where UserName=%s and Passwd=%s", (username, password))
            res = cur.fetchall()
            return True if res else None
        except Exception as e:
            print(repr(e))


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
        conn.close()
    except Exception as e:
        print(e)


def getemail(email):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(f"select Passwd from User where Email = %s", (email,))
            res = cur.fetchall()
            if res:
                return res[0][0]

        except Exception as e:
            print(e)


def resetpasswd(username, newpass):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(f"UPDATE User SET Passwd = %s WHERE UserName = %s;", (username, newpass))
            conn.commit()
            return True
        except Exception as e:
            print(e)


def insert_posts(U_id, cont):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(f"INSERT INTO Post(User_Id, content, L_Count, Comment_Count) VALUES (%s, %s, %s, %s);",
                        (U_id, cont, 0, 0))
            conn.commit()
            return True
        except Exception as e:
            print(e)


def retrieve_posts():
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute("select Post.*,User.UserName from User, Post WHERE User.User_Id = Post.User_Id ORDER BY "
                        "Post.Post_Id DESC LIMIT 30")
            res = cur.fetchall()
            res.reverse()
            ans = {}
            for i in res:
                ans[i[0]] = {"uid": i[1], "content": i[2], "lc": i[3], "cc": i[4], "uname": i[5]}
            return ans
        except Exception as e:
            print(e)


def update_post(pid, l_count=False, c_count=False):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            if l_count:
                cur.execute("SELECT L_Count FROM Post WHERE Post_Id = %s;", (pid,))
                res = cur.fetchall()[0][0]
                res += 1
                cur.execute("UPDATE Post SET L_Count = %s WHERE Post_Id = %s;", (res, pid))

            if c_count:
                cur.execute("SELECT Comment_Count FROM Post WHERE Post_Id = %s;", (pid,))
                res = cur.fetchall()[0][0]
                res += 1
                cur.execute("UPDATE Post SET Comment_Count = %s WHERE Post_Id = %s;", (res, pid))
            conn.commit()
            return True
        except Exception as e:
            print(e)


def getuserdetials(uname):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(
                "SELECT FirstName, LastName, Age, Gender, Mobile_No, DOB FROM Detail WHERE u_id = (SELECT User_Id "
                "FROM User WHERE UserName = %s);",
                (uname,))
            res = cur.fetchall()[0]
            ans = {"fname": res[0], "lname": res[1], "age": res[2], "gender": res[3], "mob": res[4], "dob": str(res[5])}

            return ans
        except Exception as e:
            print(e)


if __name__ == "__main__":
    initialize("root", "root")
    # delete()
    print(getuserdetials("cat"))
    pass
