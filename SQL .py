import sqlite3

conn = sqlite3.connect('FTresult.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS FTpayment(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                transictionid TEXT,
                time TEXT,
                Month TEXT,
                Before INTEGER,
                After INTEGER,
                unit INTEGER,
                result REAL   
            )""")

def insert_FT(transictionid,time,Month,Before,After,unit,result):
    ID = None
    with conn:
        c.execute("""INSERT INTO FTpayment VALUES (?,?,?,?,?,?,?,?)""",
        (ID,transictionid,time,Month,Before,After,unit,"{:.2f}".format(result)))
    conn.commit()

def Show_FT():
    with conn:
        c.execute("SELECT * FROM FTpayment")
        Ft = c.fetchall()
        print('รายละเอียด',Ft)
    return Ft

def Update_FT(transictionid,Month,Before,After,unit,result):
    with conn:
        c.execute("UPDATE FTpayment SET Month=?, Before=?, After=?, unit=?, result=? WHERE transictionid=(?)",([Month,Before,After,unit,result,transictionid]))
    conn.commit()

    print('สำเร็จ')

def Delete_FT(transictionid):
    with conn:
        c.execute("DELETE FROM FTpayment WHERE transictionid=?",([transictionid]))
    conn.commit()   













