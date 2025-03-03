
from paramiko import SSHClient, AutoAddPolicy
import datetime, json

readBufferSize = 15000

jsonTimestamp = 'timestamp'
jsonLogtype = 'logType'
jsonThread = 'thread'
jsonMessage = 'message'

nohupout = 'nohup.out'
applicationlog = 'application.log'

#===================================================================== LOGS METHODS ================================================================

def searchServiceLogs(keyword, fromDateStr, toDateStr, serviceLogPath, targetLogfile, ipAddress, username, password):
   print('searchServiceLogs()  ')
   commandStr = buildGREPCommand(keyword, fromDateStr, toDateStr, serviceLogPath, targetLogfile)
   print(commandStr)
   return executeSSHCommand(ipAddress, username, password, commandStr)
   

def buildGREPCommand(keyword, fromDateStr, toDateStr, serviceLogPath, targetLogfile):
    print('buildGREPCommand()  ')
    commandString = "grep -ai "
    serviceLogFile = serviceLogPath
    if targetLogfile.lower() == 'archived':
        commandString = "zgrep -hi "
        if fromDateStr:
            serviceLogFile += 'logs/' + getDateYearMonth(fromDateStr) + '/*.*'
        else:
            serviceLogFile += 'logs/*/*.*'
    else:
        serviceLogFile += targetLogfile
        
    dateSimilarity = None
    if fromDateStr and toDateStr:
        dateSimilarity = getDateSimilarity(fromDateStr, toDateStr)
        if dateSimilarity:
            commandString += " '" + dateSimilarity + "' " + serviceLogFile

    if keyword:
        if dateSimilarity:
            commandString +=  " | grep -ai '" + keyword + "'"
        else:
            commandString +=  "'" + keyword + "' " + serviceLogFile
        
    return commandString


def isLogStart(logstr):
    if len(logstr) >= 20:
      separators = logstr[4:5] + logstr[7:8] + logstr[10:11] + logstr[13:14] + logstr[16:17] + logstr[19:20]
      if separators == '-- ::.':
        return True
    return False


def getDateSimilarity(fromDateStr, toDateStr):
   endCompareIndex = getMinimum(len(fromDateStr), len(toDateStr))
   
   while fromDateStr[0:endCompareIndex] != toDateStr[0:endCompareIndex]:
      endCompareIndex -= 1
      if endCompareIndex < 1:
         return ''
     
   return fromDateStr[0:endCompareIndex]

#===================================================================== SERVICES/PROPERTIES METHODS ===================================================================

def parsePSEFJavaRow(psefRow):
    print('parsePSEFJavaRow()  ')
    dashJarIndex = psefRow.find('-jar')
    dotJarIndex = psefRow.find('.jar', dashJarIndex)
    jarFile = ''
    serviceName = ''
    servicePath = ''
    if dotJarIndex > 0:
       sub = psefRow[dashJarIndex:dotJarIndex + 4]
       startIndex = sub.rfind(' ')
       lastSlashIndex = sub.rfind('/')
       fullPath = sub[startIndex + 1:len(sub)]
       if lastSlashIndex > -1:
          lastSlashIndex = fullPath.rfind('/', 0, len(fullPath))
          secondSlashIndex = fullPath.rfind('/', 0, lastSlashIndex - 1)
          jarFile = fullPath[lastSlashIndex + 1:len(sub)]
          serviceName = fullPath[secondSlashIndex + 1:lastSlashIndex]
          servicePath = fullPath[0:secondSlashIndex + 1]
       
    return servicePath, serviceName, jarFile
    

def parsePSEFJavaRowFromConfigPath(psefRow):
    print('parsePSEFJavaRowFromConfigPath()  ')
    dashConfigIndex = psefRow.find('--spring.config.location=')
    dotPropIndex = psefRow.find('.properties', dashConfigIndex)
    appProperties = ''
    serviceName = ''
    servicePath = ''
    if dotPropIndex > 0:
       sub = psefRow[dashConfigIndex:dotPropIndex + 11]
       startIndex = sub.find('/')
       lastSlashIndex = sub.rfind('/')
       fullPath = sub[startIndex:len(sub)]
       if lastSlashIndex > -1:
          lastSlashIndex = fullPath.rfind('/', 0, len(fullPath))
          secondSlashIndex = fullPath.rfind('/', 0, lastSlashIndex - 1)
          appProperties = fullPath[lastSlashIndex + 1:len(sub)]
          serviceName = fullPath[secondSlashIndex + 1:lastSlashIndex]
          servicePath = fullPath[0:secondSlashIndex + 1]
          
    return servicePath, serviceName, appProperties


def getHostAllJavaProcesses(ip, username, password):
    print('getHostAllJavaProcesses()  ')
    
    client = SSHClient()
    try:
      client.set_missing_host_key_policy(AutoAddPolicy())
      client.connect(ip, username=username, password=password)
  
      ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('ps -ef | grep "java -Xm"')
      
      output = str(ssh_stdout.read(readBufferSize), 'utf-8')
      #output.replace('\r', '')
      return output
          
    except Exception as e:
      print('Connection failed! ' + str(e))
      return e
    finally:
      client.close()
      

def getApplicationProperties(ip, username, password, fullpath):
    print('getApplicationProperties()  ' + fullpath)
    client = SSHClient()
    
    try:
      client.set_missing_host_key_policy(AutoAddPolicy())
      client.connect(ip, username=username, password=password)
  
      ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('cat ' + fullpath)
      
      output = str(ssh_stdout.read(readBufferSize), 'utf-8')
      return output
            
    except Exception as e:
      print('Connection failed! ' + str(e))
      return e
    finally:
      client.close()



   
#========================================================== UTILITY METHODS ================================================================

def executeSSHCommand(ip, username, password, command):
    client = SSHClient()
    try:
      client.set_missing_host_key_policy(AutoAddPolicy())
      client.connect(ip, username=username, password=password)
      ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
      output = str(ssh_stdout.read(readBufferSize), 'utf-8')
      
      return output
          
    except Exception as e:
      print('Connection failed! ' + str(e))
      print(e)
    finally:
      client.close()
    return '' 

def isValidCredentials(ip, user, password):
    client = SSHClient()
    try:
      client.set_missing_host_key_policy(AutoAddPolicy())
      client.connect(ip, user, password)
      return True
    except Exception as e:
        print('Connection failed! ' + str(e))
        print(e)
    finally:
        client.close()
    return False

def getHostLoginCredentials(hostname):
    usern = 't-melcagape'
    passw = '52@O690Dd6F70Ga6_'
    
    return usern, passw  
   

def getDateYearMonth(dateStr):
   if dateStr and len(dateStr) > 6:
      return dateStr[0:7]
   return dateStr


def getMinimum(numberA, numberB):
   if numberA >= numberB:
      return numberB
   return numberA 

    
def getFirstTimestamp(loglist):
    if len(loglist) > 0:
      for x in loglist:
        if isLogStart(x):
          return x[0:23]
  
    return ''


def parseLogToJson(log, logfile):
   timestamp = ''
   logtype = ''
   thread = ''
   msg = ''
   if logfile == nohupout:
     timestamp = log[0:23]
     logtypeendindex = log.find(' ', 25, 30)
     logtype = log[24:logtypeendindex]
     loglength = len(log)
     colonindex = log.find(':', logtypeendindex, loglength)
     thread = log[logtypeendindex + 1:colonindex]
     msg = log[colonindex:loglength]
   else:
     timestamp = log[0:23]
     logtypeendindex = log.find(' ', 25, 30)
     logtype = log[24:logtypeendindex]
     loglength = len(log)
     colonindex = log.find(':', logtypeendindex, loglength)
     thread = log[logtypeendindex + 1:colonindex]
     msg = log[colonindex:loglength]
   returnObj = {
        "timestamp": timestamp,
        "logType": logtype,
        "thread": thread,
        "message": msg
        }
   return returnObj  


def convertDateStrToTimestamp(dateStr):
   return datetime.datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S.%f')
