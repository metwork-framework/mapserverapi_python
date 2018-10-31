import six
from ctypes import c_char_p, cdll, POINTER, c_ulong, c_int, byref, \
    c_char, c_void_p, cast

from mapserverapi.glib2_wrapper import Glib2Wrapper


class MapserverApiContext(object):

    def __init__(self, lib):
        self.__lib = lib

    def __enter__(self):
        self.__lib.mapserverapi_init()

    def __exit__(self, *args, **kwargs):
        self.__lib.mapserverapi_destroy()


class MapserverApi(object):

    __lib = None

    @staticmethod
    def __make_instance():
        if MapserverApi.__lib is None:
            MapserverApi.__lib = cdll.LoadLibrary("libmapserverapi.so")
            MapserverApi.__lib.mapserverapi_init.restype = None
            MapserverApi.__lib.mapserverapi_init.argtypes = []
            MapserverApi.__lib.mapserverapi_destroy.restype = None
            MapserverApi.__lib.mapserverapi_destroy.argtypes = []
            MapserverApi.__lib.mapserverapi_invoke.restype = c_int
            MapserverApi.__lib.mapserverapi_invoke.argtypes = \
                [c_char_p, c_char_p, POINTER(c_void_p),
                 POINTER(c_char_p), POINTER(c_ulong)]
            MapserverApi.__lib.mapserverapi_invoke_to_file.restype = c_char_p
            MapserverApi.__lib.mapserverapi_invoke_to_file.argtypes = \
                [c_char_p, c_char_p, c_char_p]

    @staticmethod
    def invoke(mapfile_content, query_string):
        MapserverApi.__make_instance()
        lib = MapserverApi.__lib
        with MapserverApiContext(lib):
            tmp_body = c_void_p()
            tmp_content_type = c_char_p()
            tmp_body_length = c_ulong()
            res = lib.mapserverapi_invoke(six.b(mapfile_content),
                                          six.b(query_string),
                                          byref(tmp_body),
                                          byref(tmp_content_type),
                                          byref(tmp_body_length))
            if not(res):
                return (None, None)
            body = cast(tmp_body, POINTER(c_char))
            body_length = tmp_body_length.value
            content_type = tmp_content_type.value
            Glib2Wrapper.g_free(tmp_content_type)
            buf = ""
            if body_length > 0:
                # FIXME: is it a way to avoid this copy ?
                output = six.BytesIO()
                output.write(body[0:body_length])
                buf = output.getvalue()
                output.close()
            return (buf, content_type)

    @staticmethod
    def invoke_to_file(mapfile_content, query_string, target_file):
        MapserverApi.__make_instance()
        lib = MapserverApi.__lib
        with MapserverApiContext(lib):
            content_type = \
                lib.mapserverapi_invoke_to_file(six.b(mapfile_content),
                                                six.b(query_string),
                                                six.b(target_file))
            if not(content_type):
                return None
        return content_type


def invoke(*args, **kwargs):
    return MapserverApi.invoke(*args, **kwargs)


def invoke_to_file(*args, **kwargs):
    return MapserverApi.invoke_to_file(*args, **kwargs)
