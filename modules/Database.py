import argon2.exceptions
import mysql.connector
from argon2 import PasswordHasher

User_Sql = None
Password_Sql = None
ph = PasswordHasher()


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
                "CREATE TABLE IF NOT EXISTS User(User_Id varchar(35) PRIMARY KEY NOT NULL,UserName varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci UNIQUE, "
                "Passwd varchar(200), Email varchar(100) UNIQUE);")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS Detail (u_id varchar(35), FirstName varchar(50), LastName varchar(50), "
                "Age int, Gender varchar(10), Mobile_No varchar(10), DOB date, FOREIGN KEY(u_id) REFERENCES User("
                "User_Id) ON UPDATE CASCADE ON DELETE CASCADE);")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS Post(Post_Id int PRIMARY KEY NOT NULL AUTO_INCREMENT, User_Id varchar(35), "
                "content text NOT NULL, L_Count int, FOREIGN KEY(User_Id) REFERENCES User(User_Id) ON "
                "DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS Likes(User_Id varchar(35) NOT NULL, Post_Id int NOT NULL);"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS requests(username varchar(35) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci NOT NULL UNIQUE,guid TEXT NOT NULL, "
                "tstamp timestamp); "
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(err)


def insert_user(**kwargs):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:

            passwd = kwargs['passwd']

            hashpass = ph.hash(passwd)

            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(
                f"INSERT INTO User (User_Id, UserName, Passwd, email) VALUES (%s,%s,%s,%s);",
                (kwargs['uid'], kwargs['uname'], hashpass, kwargs['email'])
            )
            cur.execute(
                f"INSERT INTO Detail values (%s,'','',0,'','','0000-00-00')", (kwargs["uid"],)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(err.msg)


def update(**kwargs):
    global User_Sql, Password_Sql

    if len(str(kwargs["mob"])) != 10 and kwargs["mob"] != 0:
        return "mob"

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
            cur.execute(f"SELECT Passwd from User where UserName=%s", (username,))
            res = cur.fetchall()
            if res:
                try:
                    pwhash = res[0][0]
                    ph.verify(pwhash, password)
                    return True
                except argon2.exceptions.VerifyMismatchError as e:
                    print(e)
            else:
                return False
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
        cur.execute("DROP TABLE IF EXISTS Likes;")
        cur.execute("DROP TABLE IF EXISTS requests;")

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
            cur.execute(f"select UserName from User where Email = %s", (email,))
            res = cur.fetchall()
            if res:
                return res[0][0]
        except Exception as e:
            print(e)


def resetpasswd(username, newpass):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            pwhash = ph.hash(newpass)
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(f"UPDATE User SET Passwd = %s WHERE UserName = %s;", (pwhash, username))
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
            cur.execute("INSERT INTO Post(User_Id, content, L_Count) VALUES (%s, %s, %s);",
                        (U_id, cont, 0))
            conn.commit()
            return True
        except Exception as e:
            print(e)


def retrieve_posts(uid):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute("select Post.*,User.UserName from User, Post WHERE User.User_Id = Post.User_Id ORDER BY "
                        "Post.Post_Id DESC LIMIT 30")
            res = cur.fetchall()
            res.reverse()
            cur.execute("SELECT * FROM Likes where User_Id = %s;", (uid,))
            res1 = cur.fetchall()
            ans = {}
            for i in res:
                ans[i[0]] = {"uid": i[1], "content": i[2], "lc": i[3], "uname": i[4],
                             "islike": 1 if (uid, i[0]) in res1 else 0}
            return ans
        except Exception as e:
            print(e)


def update_post(uid, pid):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")

            cur.execute("SELECT count(User_Id) FROM Likes WHERE User_Id = %s AND Post_Id = %s", (uid, pid))
            res = cur.fetchall()
            if not res[0][0]:  # User has liked the post
                cur.execute("INSERT INTO Likes(User_Id, Post_Id) VALUES (%s,%s)", (uid, pid))
                # Update like count
                cur.execute("UPDATE Post SET L_Count = L_Count + 1 WHERE Post_Id = %s;", (pid,))
            else:  # User has unliked the post
                cur.execute("DELETE FROM Likes WHERE User_Id = %s AND Post_Id = %s", (uid, pid))
                # Update the like count
                cur.execute("UPDATE Post SET L_Count = L_Count - 1 WHERE Post_Id = %s;", (pid,))
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
                "FROM User WHERE UserName = %s);", (uname,))
            res = cur.fetchall()[0]
            ans = {"fname": res[0], "lname": res[1], "age": res[2], "gender": res[3], "mob": res[4],
                   "dob": "0000-00-00" if not res[5] else str(res[5])}

            return ans
        except Exception as e:
            print(e)


def insert_reset_request(uname, guid):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            guidhash = ph.hash(guid)
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute(f"DROP EVENT IF EXISTS {uname}_reset")
            cur.execute("INSERT INTO requests values (%s,%s,timestamp(sysdate()))", (uname, guidhash))
            cur.execute(f"CREATE EVENT {uname}_reset ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 1 DAY DO DELETE FROM "
                        f"requests where username = %s", (uname,))
            conn.commit()

        except Exception as e:
            print(e)


def check_reset(guid, uname):
    global User_Sql, Password_Sql
    with connector(User_Sql, Password_Sql) as conn:
        try:
            cur = conn.cursor()
            cur.execute("USE M_DB;")
            cur.execute("SELECT guid FROM requests WHERE username = %s", (uname,))
            res = cur.fetchall()
            if res:
                hashed_id = res[0][0]
                try:
                    if ph.verify(hashed_id, guid):
                        cur.execute("DELETE FROM requests WHERE username = %s", (uname,))
                        cur.execute(f"DROP EVENT IF EXISTS {uname}_reset")
                        conn.commit()
                        return True
                except argon2.exceptions.VerifyMismatchError as e:
                    print(e)
            else:
                return False
        except:
            return False


if __name__ == "__main__":
    initialize("root", "ABCD1234!@")
    delete()
