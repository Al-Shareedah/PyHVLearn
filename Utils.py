class Utils:
    @staticmethod
    def read_alphabets(file_path):
        """
        Reads characters from a file, one character per line.

        :param file_path: Path to the file containing the alphabets.
        :return: A list of characters read from the file.
        """
        alphabets = []
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Make sure the line is not empty
                    alphabets.append(line[0])  # Add the first character of the line
        return alphabets

    @staticmethod
    def read_name(file_path):
        """
                Reads the first line of a file and returns it as a string.

                :param file_path: Path to the file.
                :return: The first line of the file as a string.
        """
        with open(file_path, 'r') as file:
            return file.readline().strip()
