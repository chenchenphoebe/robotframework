# -*- coding:utf-8 -*-
# _author_ = 'phoebe'
import os
import time


class AdbShell:
    def __init__(self):
        self._device_name = os.getenv('U_APPIUM_DEVICE_NAME')
        self._start_server = 'adb start-server'
        self._kill_server = 'adb kill-server'
        # Default Log Path:
        self._current_dir = os.getenv('G_CURRENTLOG', 'f:\\robotframework\\logs\\current')
        # os.putenv('G_CURRENTLOG', 'f:\\robotframework\\logs\\current')
        self._bugreport_dir = 'f:\\robotframework\\logs\\current'
        self.__chkbugreport_dir = os.getenv('G_APPIUM_APP_BUGREPORT_DIR', 'f:\\robotframework\\tools\\bugreport')

    def __raiseError(self, Message=None):
        # Raise Exception with self-defined message.
        raise Exception, Message

    def kill_process(self):
        try:
            re = self.check_adb_status()
            if re == True:
                # os.system用来执行cmd指令，在cmd输出的内容会直接在控制台输出
                # os.system是简单粗暴的执行cmd指令，如果想获取在cmd输出的内容，是没办法获到的
                status = os.system('taskkill /f /im adb.exe')
                if status == 0:
                    print 'Pass,killed the process'
                else:
                    print 'faild'
            else:
                print 'adb is already stopped'
        except Exception as e:
            print str(e)

    def check_adb_status(self):
        try:
            # 如果想获取控制台输出的内容，那就用os.popen的方法了
            # popen返回的是一个file对象，跟open打开文件一样操作了，r是以读的方式打开
            content = os.popen('tasklist | findstr adb.exe')
            if 'adb.exe' in content:
                return True
            else:
                return False
        except Exception as e:
            print str(e)

    def start_adb_services(self):
        try:
            text = os.popen(self._start_server)
            time.sleep(3)
            content = text.read()
            print content
            if '5037' not in content:
                print 'start server faild'
            else:
                print 'Pass,adb start sucess'

        except Exception as e:
            print str(e)

    def get_device_name(self):
        device_name = ''
        adb_devices = 'adb devices'
        status = os.system('adb connect 127.0.0.1:52001')
        if status == 0:
            print 'connect successed'
        else:
            os.system('adb connect 127.0.0.1:52001')
        try:
            text = os.popen(adb_devices)
            time.sleep(2)
            content = text.read()
            res = content.splitlines()
            if '127.0.0.1:52001\tdevice' not in content:
                self.__raiseError('Error: Could Not get device -> {}'.format(res[-1].split()[1]))
            device_name = res[1].split()[0]
        except Exception as e:
            if str(e) == 'list index out of range':
                self.__raiseError('Error: Could NOT find device! Please check the phone has been attached to TestBed.')
            else:
                print str(e)
        return device_name

    def set_device_name(self, name=None):
        if name == None:
            devicename = self.get_device_name()
        else:
            devicename = name
        if self._device_name != '' and self._device_name == devicename:
            print '_'*30
            print 'Pass! Set device name!'
            print 'Device Name:' + self.__device_name
            print '-' * 30
        elif devicename == '':
            self.__raiseError('FAIL: Could NOT get device name!')
        else:
            self._device_name = devicename
            # 添加环境变量参数，然后os.getenv()获取值
            os.environ['U_APPIUM_DEVICE_NAME'] = str(devicename)
            print '-' * 30
            print 'Pass! Set device name!'
            print 'Device Name: ' + os.getenv('U_APPIUM_DEVICE_NAME')
            print '-' * 30
			
if __name__ == "__main__":
	pass





