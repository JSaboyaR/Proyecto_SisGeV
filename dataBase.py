import sqlite3
database = 'dataBase_SisGeV.db'

def elegirlist(db) -> list:
    try:
        with sqlite3.connect(database) as con:
            buscar = con.cursor()
            lista = buscar.execute(db).fetchall()
    except Exception:
        lista = None
    return lista

def validardata(db,data) -> int:
    try:
        with sqlite3.connect(database) as con:
            buscar = con.cursor()
            lista = buscar.execute(db,data).rowcount
            if lista!=0:
                con.commit()
    except Exception:
        lista = 0
    return lista

def listadata(db, id) -> list:
    try:
        with sqlite3.connect(database) as con:
            buscar = con.cursor()
            lista = buscar.execute(db, (id,)).fetchall()
    except Exception:
        lista = None
    return lista

def eliminardata(db, id) -> int:
    try:
        with sqlite3.connect(database) as con:
            buscar = con.cursor()
            lista = buscar.execute(db, (id,))
            con.commit()
    except Exception:
        return 0
    return 1
