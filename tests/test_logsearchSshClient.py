from logsearch import sshclient
from unittest import TestCase

class SshClientTestCase(TestCase):
    

    psefRowOtp = "root 109947      1  0 Jul15 ?        02:03:13 java -Xmx256m -Dlog4j.formatMsgNoLookups=true -jar /myservices/myotpservice/myotpservice-SNAPSHOT.jar --spring.config.location=/my-services/my-otpservice/application.properties"
    psefRowWatchlist = "root 114871      1  0 Jul24 ?        01:01:36 java -Dlogging.config=log4j2.xml -Xmx26m -Dlog4j.formatMsgNoLookups=true -jar /myservices/mywatlist/mywatchlist.jar --spring.config.location=/my-services/my_watchlist/application.properties"


    def test_getDateSimilarity(self):
        assert sshclient.getDateSimilarity('2024-08-29 12:15:10', '2024-08-29 12:15:50') == '2024-08-29 12:15:'
        assert sshclient.getDateSimilarity('2024-08-29 12:15:10', '2024-08-29 12:18:50') == '2024-08-29 12:1'
        assert sshclient.getDateSimilarity('2024-08-29 12:15:10', '2024-08-29 12:28:50') == '2024-08-29 12:'
        assert sshclient.getDateSimilarity('2024-08-29 12:15:10', '2024-08-29 15:28:50') == '2024-08-29 1'
        assert sshclient.getDateSimilarity('2024-08-29 12:15:10', '2024-08-29 25:28:50') == '2024-08-29 '
        assert sshclient.getDateSimilarity('2024-08-28 12:15:10', '2024-08-29 25:28:50') == '2024-08-2'
        assert sshclient.getDateSimilarity('2024-08-28 12:15:10', '2024-08-30 25:28:50') == '2024-08-'
        assert sshclient.getDateSimilarity('2024-08-28 12:15:10', '2024-09-30 25:28:50') == '2024-0'
        assert sshclient.getDateSimilarity('2024-08-28 12:15:10', '2024-10-30 25:28:50') == '2024-'
    

    def test_getDateYearMonth(self):
        assert sshclient.getDateYearMonth('2024-08-30') == '2024-08'
        assert sshclient.getDateYearMonth('2024-08-3') == '2024-08'
        assert sshclient.getDateYearMonth('2024-08-') == '2024-08'
        assert sshclient.getDateYearMonth('2024-08') == '2024-08'
        assert sshclient.getDateYearMonth('2024-0') == '2024-0'
        assert sshclient.getDateYearMonth('2024-') == '2024-'
        assert sshclient.getDateYearMonth('2024') == '2024'


    def test_parsePSEFJavaRow(self):
        servicePath, serviceName, jarFile = sshclient.parsePSEFJavaRow(self.psefRowOtp)
        assert servicePath == '/myservices/'
        assert serviceName == 'myotpservice'
        assert jarFile == 'myotpservice-SNAPSHOT.jar'
        
        servicePath, serviceName, jarFile = sshclient.parsePSEFJavaRow(self.psefRowWatchlist)
        assert servicePath == '/myservices/'
        assert serviceName == 'mywatlist'
        assert jarFile == 'mywatchlist.jar'
        

    def test_parsePSEFJavaRowFromConfigPath(self):
        servicePath, serviceName, appProperties = sshclient.parsePSEFJavaRowFromConfigPath(self.psefRowOtp)
        assert servicePath == '/my-services/'
        assert serviceName == 'my-otpservice'
        assert appProperties == 'application.properties'
        
        servicePath, serviceName, jarFile = sshclient.parsePSEFJavaRowFromConfigPath(self.psefRowWatchlist)
        assert servicePath == '/my-services/'
        assert serviceName == 'my_watchlist'
        assert appProperties == 'application.properties'
        

    def test_getMinimum(self):
        assert sshclient.getMinimum(50, 40) == 40
        assert sshclient.getMinimum(50.0, 50.5) == 50.0
        assert sshclient.getMinimum(50, 50) == 50
        assert sshclient.getMinimum(40.5, 65.4) == 40.5


    def test_getFirstTimestamp(self):
        logList = list()
        logList.append('at ireutyrity.eroiertk.eorit')
        logList.append('2024-08-30 09:01:50.742  INFO [mycase-service, myserverip:myport, 55ffd9db-4fc3-4d2d-bcfd-3c921bd4effb]')
        logList.append('2024-08-30 09:01:50.744  INFO [mycase-service, myserverip:myport, 55ffd9db-4fc3-4d2d-bcfd-3c921bd4effb] 11409 --- ')
        logList.append('2024-08-30 09:01:50.744  INFO [mb')
        assert sshclient.getFirstTimestamp(logList) == '2024-08-30 09:01:50.742'
        


    def test_isLogStart(self):
        assert sshclient.isLogStart('2024-08-29 12:15:10.000')
        assert sshclient.isLogStart('2024-08-44 52:15:10.50')
        assert sshclient.isLogStart('2024-58-29 12:55:10.')
        assert not sshclient.isLogStart('2024-58-29 12:55:10')
        assert not sshclient.isLogStart('2024-58-29 12:55:10:5512')
        assert not sshclient.isLogStart('2024:58:29 12-55_10')


    def test_buildGREPCommand(self):
        keyword = 'ERROR'
        fromDate = '2024-08-29 12:12:12'
        path = '/myservices/mycase-service/'
        
        actualResult = sshclient.buildGREPCommand(keyword, fromDate, '2024-08-29 12:15:12', path, 'rawlog.out')
        expectedResult = "grep -ai  '2024-08-29 12:1' /myservices/mycase-service/rawlog.out | grep -ai 'ERROR'"
        assert actualResult == expectedResult
        
        actualResult = sshclient.buildGREPCommand(keyword, fromDate, '2024-08-29 12:15:12', path, 'archived')
        expectedResult = "zgrep -hi  '2024-08-29 12:1' /myservices/mycase-service/logs/2024-08/*.* | grep -ai 'ERROR'"
        assert actualResult == expectedResult
        
        actualResult = sshclient.buildGREPCommand(keyword, fromDate, '2024-08-29 12:15:12', path, 'appli.log')
        expectedResult = "grep -ai  '2024-08-29 12:1' /myservices/mycase-service/appli.log | grep -ai 'ERROR'"
        assert actualResult == expectedResult
        
        actualResult = sshclient.buildGREPCommand(keyword, fromDate, None, path, 'applic.log')
        expectedResult = "grep -ai 'ERROR' /myservices/mycase-service/applic.log"
        assert actualResult == expectedResult
        
        actualResult = sshclient.buildGREPCommand('ERROR', None, None, path, 'archived')
        expectedResult = "zgrep -hi 'ERROR' /myservices/mycase-service/logs/*/*.*"
        assert actualResult == expectedResult
        
        actualResult = sshclient.buildGREPCommand('ERROR', None, None, path, 'app.log')
        expectedResult = "grep -ai 'ERROR' /myservices/mycase-service/app.log"
        assert actualResult == expectedResult
 