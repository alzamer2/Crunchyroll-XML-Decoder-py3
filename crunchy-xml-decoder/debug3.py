import linecache
import sys
from unidecode import unidecode
import types

class debug:

    def __init__(self):
        self.debugfile = None

    def traceit(self, frame, event, arg):
        if event == "line":
            lineno = frame.f_lineno
            if "__file__" in frame.f_globals:
                filename = frame.f_globals["__file__"]
                if filename.endswith(".pyc") or filename.endswith(".pyo"):
                    filename = filename[:-1]
                line = linecache.getline(filename, lineno)
            else:
                line = ''
            name = frame.f_globals["__name__"]
            debugvalue = unidecode(
                str("%s:%s: %s\n%s" % (name, lineno, line.rstrip(), self.debug_nice(frame.f_globals))) + '\n')
            self.debugfile.write(debugvalue)
            if "xmlconfig" in frame.f_globals:
                decodec_xml = open('.\\decodec_xml.txt', 'w')
                decodec_xml.write(str(frame.f_globals["xmlconfig"]))
                decodec_xml.close()
        return self.traceit

    @staticmethod
    def debug_nice(locals_dict, keys=None):
        if keys is None:
            keys = []
        exclude_keys = ['copyright', 'credits', 'False',
                        'SW_HIDE', 'STDOUT', 'STARTUPINFO',
                        'MAXFD', 'pywintypes', 'STARTF_USESTDHANDLES',
                        'PIPE', 'STD_ERROR_HANDLE', 'CREATE_NEW_CONSOLE',
                        'STARTF_USESHOWWINDOW', 'mswindows', 'STD_INPUT_HANDLE',
                        'CREATE_NEW_PROCESS_GROUP', 'STD_OUTPUT_HANDLE', 'Hashable',
                        'Sized', 'Set', 'Container', 'Iterator', 'ValuesView',
                        'MutableMapping', 'Sequence', 'Mapping', 'MutableSequence',
                        'Callable', 'Iterable', 'ItemsView', 'KeysView', 'MutableSet',
                        'MappingView', 'SafeConfigParser', 'RawConfigParser',
                        'MAX_INTERPOLATION_DEPTH', 'DEFAULTSECT', 'ConfigParser',
                        'True', 'None', 'Ellipsis', 'quit']
        exclude_valuetypes = [types.BuiltinFunctionType,
                              types.BuiltinMethodType,
                              types.ModuleType,
                              type,
                              types.FunctionType
                              ]
        return {k: v for k, v in locals_dict.items() if not
        (k in keys or k in exclude_keys or type(v) in exclude_valuetypes)
                and k[0] != '_'
                }

    def debug_start(self):
        self.debugfile = open('.\\debug.p.log', 'w')
        sys.settrace(self.traceit)

    def debug_end(self):
        if not self.debugfile is None:
            sys.settrace(None)
            self.debugfile.close()

