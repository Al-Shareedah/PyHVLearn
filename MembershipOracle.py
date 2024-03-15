from CertificateTemplate import CertificateTemplate
from verifier import Verifier
import random
import numpy as np
# Set seeds to ensure reproducibility
random.seed(1)
np.random.seed(1)
from aalpy.base import SUL


class MembershipOracle(SUL):
    ACCEPT = 1  # 1 represents acceptance
    REJECT = 0  # 0 represents rejection

    def __init__(self, id_verifier, name, id_type):
        super().__init__()  # Initialize the base class
        self.id_verifier = id_verifier
        self.name = name
        self.id_type = id_type
        self.cert_file_name = None
        self.key_file_name = None
        self.alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.current_input = ''  # Track the current input sequence
        self.accepted_queries = 0
        self.do_setup()

    def do_setup(self):
        try:
            cert_template = CertificateTemplate(self.name, self.id_type)
            self.cert_file_name = cert_template.get_cert_file_name()
            self.key_file_name = cert_template.get_key_file_name()
        except Exception as e:
            print("[FAILED]", e)
            exit(-1)

        try:
            self.id_verifier.read_cert(self.cert_file_name, self.key_file_name)
        except Exception as e:
            print("[FAILED]", e)
            exit(-1)

    def get_possible_accepted_strings(self, name):
        possible_accepted_strings = set()

        def adjust_name_based_on_id_type(name):
            for prefix in ("DNS:", "IP:", "email:"):
                if name.startswith(prefix):
                    return name[len(prefix):]
            return name

        no_id_name = adjust_name_based_on_id_type(name)

        # Generate strings by replacing '*' with random characters from the alphabet
        if '*' in no_id_name:
            for _ in range(10):  # Generate a fixed number of possible strings
                replaced_string = ''.join(random.choice(self.alphabet) if c == '*' else c for c in no_id_name)
                possible_accepted_strings.add(replaced_string)
        else:
            possible_accepted_strings.add(no_id_name)

        return list(possible_accepted_strings)

    def find_counterexample(self):
        possible_accepted_strings = self.get_possible_accepted_strings(self.name)

        for string in possible_accepted_strings:
            if self.id_verifier.verify(string, self.id_type) == self.ACCEPT:
                return self.string_to_query(string)

        return None  # No counterexample found

    def string_to_query(self, string):
        """Convert string to query by converting each character into a list element."""
        query = [c for c in string]  # List comprehension to create a list of characters from the string
        return query

    def pre(self):
        # Reset or initialize SUL state before processing a new input sequence
        super().pre()  # Call the base class's pre method if it exists
        self.current_input = ''  # Reset the current input to start fresh for each query

    def post(self):
        pass

    def query(self, word):
        if not word:  # Check if the word is empty
            return (False,)  # Return a tuple with a single False, or True if your initial state is accepting

        self.pre()
        results = []  # Always start with an empty list

        for symbol in word:
            results.append(self.step(symbol))

        print("Output tuple:", tuple(results))
        return tuple(results)

    def step(self, symbol):
        # Construct a query string and get the result for a single symbol
        self.current_input += symbol
        # print(f"[step] Processing symbol: {symbol}, current input: {self.current_input}")
        accepted = self.id_verifier.verify(self.current_input, self.id_type)


        print(f"query: {self.current_input} >> ", end="")
        if accepted == self.ACCEPT:
            print("[accepted]")
            self.accepted_queries = self.accepted_queries + 1
            return True
        elif accepted == self.REJECT:
            print("[rejected]")
            return False

