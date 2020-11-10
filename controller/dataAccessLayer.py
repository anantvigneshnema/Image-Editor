import sys
from model.dataModels.userInput import userDataInputClass


class dataInputOutputClass:
    def __init__(self):
        self.dataAccessModelObject = userDataInputClass()

    def testAction(self, text):
        return print(text)

    def moviesInInputFolderByUser(self, inputFolderString):
        return self.dataAccessModelObject.getAllMovieFilesInFolder(
            inputFolderString
        )
      

