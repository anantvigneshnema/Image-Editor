import os
import ctypes


class userDataInputClass:
    def __init__(self):
        pass

    # sanitizes input
    def getAllMovieFilesInFolder(self, text):
            # with disable_file_system_redirection():
            #      print(os.listdir(text))
            return [
                    name
                    for name in os.listdir(text)
                    if (
                        name.lower().endswith(".mov")
                        or name.lower().endswith(".avi")
                        or name.lower().endswith(".mp4")
                    )
                   ]


# class disable_file_system_redirection:
#     _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
#     _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    
#     def __enter__(self):
#         self.old_value = ctypes.c_long()
#         self.success = self._disable(ctypes.byref(self.old_value))
    
#     def __exit__(self, type, value, traceback):
#         if self.success:
#             self._revert(self.old_value)

