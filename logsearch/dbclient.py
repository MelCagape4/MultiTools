import sqlite3
from sqlite3 import Error
from django.contrib.auth.hashers import make_password, check_password

dbName = 'db.sqlite3'

def create_sqlite_database():
    #---------- create a database connection to an SQLite database --------------------------------
    conn = None
    try:
        conn = sqlite3.connect(dbName)
        return sqlite3.sqlite_version
    except Error as e:
        print(e)
        return str(e)
    finally:
        if conn:
            conn.close()

def createDBConnection():
    try:
        return sqlite3.connect(dbName)
    except sqlite3.Error as e:
        print(e)
        return str(e)

#=================================================== HOSTS ==================================================

def getHostsJSON(includeServices=False, includeLogfiles=False):
    hosts = getHosts()
    servers = []
    
    for x, y, z in hosts:
        if includeServices:
            logfiles = getServicesJSON(x, includeLogfiles)
            servers.append({"serverID":x, "serverName":z, "serverIP":y, "services":logfiles})
        else:
            servers.append({"serverID":x, "serverName":z, "serverIP":y})
        
    return servers

def getHosts():
    dbconnect = None
    rows = None
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('''SELECT serverID, serverIP, serverName FROM servers ORDER BY serverName''')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
            
    return rows

#=================================================== SERVICES ==================================================

def getServiceById(serviceId):
    service = None
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('SELECT serviceID, serviceName, servicePath, description FROM services WHERE serviceID = ?', (serviceId,))
        service = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
            
    return service

def getServicesJSON(serverID=-1, includeLogfiles=False):
    services = []
    rows = None
    if serverID > -1:
        rows = getServicesByServer(serverID)
    else:
        rows = getAllServices()
        
    if rows:
        for i, j , k, l in rows:
            if includeLogfiles:
                services.append({"serviceID":i, "serviceName":j, "servicePath":k, "description":l, "logFiles":[]})
            else:
                services.append({"serviceID":i, "serviceName":j, "servicePath":k, "description":l})
                
    return services
            

def getServicesByServer(serverID):
    dbconnect = None
    rows = None
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('''SELECT serviceID, S.serviceName, S.servicePath, S.description FROM server_services LEFT JOIN services S  WHERE serverID=? ORDER BY serviceName''', (serverID,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
            
    return rows
    
def getAllServices():
    dbconnect = None
    rows = None
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('''SELECT serviceID, serviceName, servicePath, description FROM services ORDER BY serviceName''')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
            
    return rows

#==================================================== logFiles ==================================================
def getAllLogfiles():
    dbconnect = None
    rows = None
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('''SELECT logfileID, logFilename, defaultPath, description FROM logfiles ORDER BY logFilename''')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
            
    return rows

def getLogFilenameAndPathById(logfileId):
    print("getLogFilenameAndPathById() " + str(logfileId))
    dbconnect = None
    rows = None
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('''SELECT logFilename, defaultPath FROM logfiles WHERE logfileID=?''', logfileId)
        rows = cur.fetchall()
        for i, j in rows:
            return str(i), str(j)
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
            
    return '', ''

def getLogfilesJSON():
    rows = getAllLogfiles()
    logfiles = []
    if rows:
        for i, j, k, l in rows:
            logfiles.append({"logfileID":i, "logFilename":j, "defaultPath":k, "description":l})
            
    return logfiles

#==================================================== USERS =====================================================

def getServerCredentials(ip, username):
    print('getServerCredentials() ' + ip + '  ' + username)
    dbconnect = None
    rows = None
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('''SELECT loginUser, loginPassword, server_users.lockoutCredentials FROM server_users INNER JOIN servers s ON server_users.server_id=s.serverID INNER JOIN auth_user u ON server_users.user_id=u.id WHERE s.serverIP=? AND u.username=?''', (ip, username,))
        rows = cur.fetchall()
        for i, j, k in rows:
            if i and j:
                user = str(i)
                password = str(j)
                if k:
                    print('Credential is locked! (' + username + ')')
                elif user and password:
                    return user, password
                
        cur.execute('''SELECT defaultUser, defaultPassword, lockoutCredentials FROM servers WHERE serverIP=?''', (ip,))
        rows = cur.fetchall()
        for i, j, k in rows:
            if i and j:
                user = str(i)
                password = str(i)
                if k:
                    print('Default credential is locked! (' + ip + ')')
                    return '', ''
                elif user and password:
                    return user, password
                
        print('No Credentials available!')
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
    return '', ''

def lockUserCredentials(ip, username):
    print('lockUserCredentials(): ' + username + ',  ' + ip)
    
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('''UPDATE server_users SET lockoutCredentials=? WHERE server_id=(SELECT serverID FROM servers WHERE serverIP=?) AND user_id=(SELECT id FROM auth_user WHERE username=?)''', (True, ip, username,))
        dbconnect.commit()
        
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
    return '', ''
    

def getUsers():
    dbconnect = None
    rows = None
    try:
        dbconnect = sqlite3.connect(dbName)
        cur = dbconnect.cursor()
        cur.execute('''SELECT * FROM auth_user''')
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if dbconnect:
            dbconnect.close()
            
    return rows

def hasUser(dbconnect, username):
    sql = ''' SELECT username FROM users WHERE username = ? '''
    payload = (username,)
    cur = dbconnect.cursor()
    cur.execute(sql, payload)
    rows = cur.fetchall()
    for i in rows:
        return True
    return False
