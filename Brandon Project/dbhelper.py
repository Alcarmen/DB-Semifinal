"""
	Python Database helper
"""
from mysql.connector import connect

def db_connect()->object:
    return connect(
        host="localhost",
        user="root",
        password="",
        database="customer"
    )
    
def doProcess(sql:str)->bool:
    db:object = db_connect()
    cursor:object = db.cursor()
    cursor.execute(sql)
    db.commit()
    return True if cursor.rowcount>0 else False
    
def getProcess(sql:str)->list:
    db:object = db_connect()
    cursor:object = db.cursor(dictionary=True)
    cursor.execute(sql)
    return cursor.fetchall()

def getall(table:str)->list:
    sql:str = f"SELECT * FROM `{table}` WHERE active = 1"
    return getProcess(sql)

def getrecord(table:str,**kwargs)->list:
    params:list = list(kwargs.items())
    flds:list = list(params[0])
    sql:str = f"SELECT * FROM `{table}` WHERE `{flds[0]}`='{flds[1]}'"
    return getProcess(sql)
    
def addrecord(table:str,**kwargs)->bool:
    flds:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    fld:str = "`,`".join(flds)
    val:str = "','".join(vals)
    sql:str = f"INSERT INTO `{table}`(`{fld}`) values('{val}')"
    print(sql)
    return doProcess(sql)
    
def updaterecord(table:str,**kwargs)->bool:
    flds:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    fld:list = []
    for i in range(1,len(flds)):
        fld.append(f"`{flds[i]}`='{vals[i]}'")
    params:str = ",".join(fld)
    sql:str = f"UPDATE `{table}` SET {params} WHERE `{flds[0]}`='{vals[0]}'"
    print(sql)
    return doProcess(sql)
    
def deleterecord(table:str,**kwargs)->bool:
    params:list = list(kwargs.items())
    flds:list = list(params[0])
    sql:str = f"UPDATE `{table}` SET active = 0 WHERE `{flds[0]}`='{flds[1]}'"
    return doProcess(sql)
    
def searchrecord(table:str,search_term)->list:
    sql:str = f"SELECT * FROM `{table}` WHERE active = 1 AND (c_name LIKE '%{search_term}%' OR c_email LIKE '%{search_term}%' OR c_address LIKE '%{search_term}%')"
    return getProcess(sql)
def itemrecord(table:str,search_item)->list:
    sql:str = f"SELECT * FROM `{table}` WHERE active = 1 AND (ISBN LIKE '%{search_item}%' OR title LIKE '%{search_item}%' OR author LIKE '%{search_item}%' OR genre LIKE '%{search_item}%' OR price LIKE '%{search_item}%' OR i_type LIKE '%{search_item}%')"
    return getProcess(sql)
    

