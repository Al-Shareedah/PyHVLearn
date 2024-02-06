import os
from Utils import Utils


class DFAInfer:
    # Static variables from DFAInfer, values assumed for demonstration
    WP_METHOD_DEPTH = 1
    NUM_INSTANCES = 1
    MIN_BATCH_SIZE = 1
    LOG_PATH = "./log"

    def __init__(self):
        self.idType = None
        self.alphabetFile = None
        self.nameFile = None
        self.alphabets = None
        self.name = None
        self.idVerifier = None
        self.wpMethodDepth = DFAInfer.WP_METHOD_DEPTH
        self.numInstances = DFAInfer.NUM_INSTANCES
        self.minBatchSize = DFAInfer.MIN_BATCH_SIZE
        self.logPath = DFAInfer.LOG_PATH

    def setAlphabetFile(self, alphabetFile):
        self.alphabetFile = alphabetFile

    def setNameFile(self, nameFile):
        self.nameFile = nameFile

    def setIdentityVerifier(self, idVerifier):
        self.idVerifier = idVerifier
        
    def setIdType(self, idType):
        self.idType = idType

    def makeLogPath(self):
        """
        Creates the log directory if it does not exist.

        Returns:
            success (bool): True if the directory was created successfully or already exists, False otherwise.
        """
        try:
            # Check if the directory already exists
            if not os.path.exists(self.logPath):
                # Attempt to create the directory
                os.makedirs(self.logPath)
                print(f"Directory created: {self.logPath}")
                return True
            else:
                # Directory already exists, considered a successful case
                print(f"Directory already exists: {self.logPath}")
                return True
        except Exception as e:
            print(f"Cannot create directory: {self.logPath}. Error: {e}")
            exit(-1)

    def do_setup(self):
        # Read alphabet file
        if self.alphabets is None and self.alphabetFile:
            try:
                self.alphabets = Utils.read_alphabets(self.alphabetFile)
            except Exception as e:
                print(f"[FAILED] Read alphabet file {self.alphabetFile}: {e}")
                exit(-1)

        # Read name
        if self.name is None and self.nameFile:
            try:
                self.name = Utils.read_name(self.nameFile)
            except Exception as e:
                print(f"[FAILED] Read name file {self.nameFile}: {e}")
                exit(-1)

        # Check IdentityVerifier
        if self.idVerifier is None:
            print("[FAILED] Identity Verifier not set")
            exit(-1)

        # Set log path based on the IdentityVerifier's name
        # This assumes the idVerifier has a getName() method to retrieve the verifier's name
        self.logPath = os.path.join(self.logPath, self.idVerifier.getName())
        self.makeLogPath()
