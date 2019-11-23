import os
import subprocess
import inspect
import sys
if sys.version_info > (3, 0, 0):
    import winreg
else:
    import _winreg as winreg
def run_code_with_console():
    # print(inspect.currentframe().f_back.f_code.co_filename)
    # print(os.path.abspath(os.path.split(inspect.currentframe().f_back.f_code.co_filename)[0]))
    pyfile ='''\
import sys
sys.path.append(r'%s')
locals().update({'%s':__import__('%s')})
'''% (os.path.abspath(os.path.split(inspect.currentframe().f_back.f_code.co_filename)[0]),
      os.path.splitext(os.path.split(inspect.currentframe().f_back.f_code.co_filename)[1])[0],
      os.path.splitext(os.path.split(inspect.currentframe().f_back.f_code.co_filename)[1])[0],
      )
    isfunction_ = True
    frame_argvalues = inspect.getargvalues(inspect.currentframe().f_back)
    for i in frame_argvalues[3]:
        isfunction_ = isfunction_ and not '__module__' in dir(frame_argvalues[3][i])
        if '__module__' in dir(frame_argvalues[3][i]):
            pyfile +='''temp_class=%s.%s()\n''' % (os.path.splitext(os.path.split(inspect.currentframe().f_back.f_code.co_filename)[1])[0],
                                                frame_argvalues[3][i].__class__.__name__)
            pyfile +='''temp_class.%s(''' % inspect.currentframe().f_back.f_code.co_name

    if isfunction_:
        pyfile +='''%s.%s('''% (os.path.splitext(os.path.split(inspect.currentframe().f_back.f_code.co_filename)[1])[0],
                                inspect.currentframe().f_back.f_code.co_name
                                )
    for arg_ in frame_argvalues[0]:
        if not '__module__' in dir(frame_argvalues[3][arg_]):
            if isinstance(frame_argvalues[3][arg_],str):
                pyfile += '\'\'\''+frame_argvalues[3][arg_].replace('\\','\\\\')+'\'\'\'' + ', '
            else:
                pyfile += str(frame_argvalues[3][arg_]) + ', '
    if not frame_argvalues[1] is None:
        for arg_ in frame_argvalues[3][frame_argvalues[1]]:
            if not '__module__' in dir(arg_):
                if isinstance(arg_,str):
                    pyfile += '\'\'\''+arg_.replace('\\','\\\\')+'\'\'\'' + ', '
                else:
                    pyfile += str(arg_) + ', '
    if not frame_argvalues[2] is None:
        for arg_key in frame_argvalues[3][frame_argvalues[2]]:
            if not '__module__' in dir(frame_argvalues[3][frame_argvalues[2]][arg_key]):
                if isinstance(frame_argvalues[3][frame_argvalues[2]][arg_key],str):
                    pyfile += arg_key+'='+'\'\'\''+frame_argvalues[3][frame_argvalues[2]][arg_key].replace('\\','\\\\')+'\'\'\''+', '
                else:
                    pyfile += arg_key+'='+str(frame_argvalues[3][frame_argvalues[2]][arg_key])+', '
    if pyfile[-2:]==', ':
        pyfile = pyfile[:-2]

    pyfile +=''')\n'''
    #print(pyfile) ####for debug
    # to find python3 path and run with its console (using pip3 as ref)
    command = 'where' # Windows
    if os.name != "nt":# non-Windows
        command = 'which'
    python_path_ = os.path.normpath(os.path.join(os.path.split(subprocess.getoutput([command, 'pip3']))[0],'..','python.exe'))
    try:
        return subprocess.call([python_path_,'-c', pyfile])
    except FileNotFoundError: # fix for old version windows that dont have 'where' command
        reg_ = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Python\PythonCore')
        python_request_v = open(inspect.currentframe().f_back.f_code.co_filename).readline().split('python')
        python_request_v_t = list()
        for i in python_request_v[1].strip():
            if i.isdigit():
                python_request_v_t += [int(i)]
        python_request_v = python_request_v_t
        if len(python_request_v) > 0:
            if len(python_request_v) < 2:
                python_request_v += [0]
            python_request_v = python_request_v[0]+python_request_v[1]/10
        else:
            python_request_v = 0.0
        for reg_i in range(0,winreg.QueryInfoKey(reg_)[0]):
            reg_2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Python\PythonCore')
            if float(winreg.EnumKey(reg_2,reg_i)) >= python_request_v and\
               True if python_request_v == 0.0 else float(winreg.EnumKey(reg_2,reg_i)) < float(round(python_request_v)+1):
                reg_2 = winreg.OpenKey(reg_2,winreg.EnumKey(reg_2,reg_i))
                reg_2 = winreg.OpenKey(reg_2,r'PythonPath')
                python_path_ = os.path.normpath(os.path.join(winreg.EnumValue(reg_2,0)[1].split(';')[0],'..','python.exe'))
        return subprocess.call([python_path_,'-c', pyfile])
    
if __name__ == '__main__':
    pass
