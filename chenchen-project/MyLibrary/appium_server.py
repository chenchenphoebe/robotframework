# -*- coding:utf-8 -*-
# _author_ = 'phoebe'
import os
import sys


class appium_server(object):

    def __init__(self):

        self.__address = os.getenv('G_APPIUM_HOST_ADDRESS', '127.0.0.1')
        self.__port = os.getenv('G_APPIUM_HOST_PORT', '4723')
        self.__device_name = os.getenv('U_APPIUM_DEVICE_NAME','127.0.0.1:52001')
        self.__platform_name = os.getenv('G_APPIUM_PLATFORM_NAME', 'Android')
        self.__platform_ver = os.getenv('G_APPIUM_PLATFORM_VERSION')
        self.__auto_name = os.getenv('G_APPIUM_AUTO_NAME', 'Appium')
        reset = os.getenv('G_APPIUM_REINSTALL_RESET', 'False')
        if reset.lower() == 'false':
            self.__reset = '--no-reset'
        elif reset.lower() == 'true':
            self.__reset = '--full-reset'

    def __raiseError(self, Message=None):
        # Raise Exception with self-defined message.
        raise Exception,Message

    def start_appium_server(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        # start /b appium -a 127.0.0.1 -p 4723 -U None --platform-name Android --platform-version None --automation-name Appium --no-reset --command-timeout 600
        start_cmd = 'start /b appium -a {} -p {} -U {} --platform-name {} --platform-version {} --automation-name {} {} --command-timeout 600'\
            .format(self.__address,
                    self.__port,
                    self.__device_name,
                    self.__platform_name,
                    self.__platform_ver,
                    self.__auto_name,
                    self.__reset)
        try:
            appium_server_status = self.appium_server_status()
            if appium_server_status.lower() == 'stop' or appium_server_status.lower() == 'warn':
                print start_cmd
                status = os.system(start_cmd)
                if status == 0:
                    print 'Pass!Start Appium Server'
                else:
                    self.__raiseError('Fail,Could not start Appium server')
            else:
                print 'Appium server is already start. PID:{}'.format(appium_server_status)
        except Exception as e:
            print str(e)

    def stop_appium_server(self):
        try:
            appium_server_status = self.appium_server_status()
            if appium_server_status.lower() == 'stop':
                print 'Appium server is already stopped'
            elif appium_server_status.lower() == 'warn':
                self.__raiseError('Warning,Appium server error')
            else:
                pid = appium_server_status
                status = os.system('taskkill /f /pid {}'.format(pid))
                if status == 0:
                    print 'Pass!Stopped appium server . PID:{}'.format(pid)
                else:
                    self.__raiseError('Fail!Could not Stop Appium server')
        except Exception as e:
            print str(e)

    def appium_server_status(self):
        cmd = 'netstat -nao | findstr {}'.format(self.__port)
        try:
            text = os.popen(cmd)
            content = text.read().strip()
            print '_'*30
            print 'Appium Server Info: ', content
            print '_'*30
            if content == '':
                return 'stop'
            elif self.__port in content:
                pid = content.split()[4]
                if pid != 0:
                    return pid
                else:
                    return 'warn'
            else:
                return 'warn'
        except Exception as e:
            print str(e)


if __name__ == "__main__":
    appiumserver = appium_server()
    # appiumserver.stop_appium_server()
    appiumserver.start_appium_server()




