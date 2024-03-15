from aalpy.oracles import StatePrefixEqOracle, RandomWalkEqOracle, CacheBasedEqOracle
from aalpy.learning_algs import run_KV
from aalpy.utils import save_automaton_to_file, visualize_automaton
import os
import sys
# Import custom classes for verification and membership queries.
from verifier import Verifier
from CertificateTemplate import CertificateTemplate
from MembershipOracle import MembershipOracle


class ActiveLearningFramework:
    def __init__(self, name, id_type):
        # Initialize the alphabet, name, and ID type for the learning process.
        self.alphabet = ['a', 'x', 'n', '-', '1', '.', ' ', '@', 'A', '=', '*']
        self.name = name
        self.id_type = id_type
        self.sul = None # System Under Learning (SUL)
        self.cache_based_eq_oracle = None  # CacheBasedEqOracle placeholder
        self.setup()

    def setup(self):
        # Set up the membership oracle and equivalence oracle with the necessary configurations.
        id_verifier = Verifier(self.id_type)
        self.sul = MembershipOracle(id_verifier, self.name, self.id_type)

        # Initialize CacheBasedEqOracle with specific parameters for the active learning framework.
        self.cache_based_eq_oracle = CacheBasedEqOracle(
            alphabet=self.alphabet,
            sul=self.sul,
            num_walks=400,
            depth_increase=6,
            reset_after_cex=True
        )

    def run_learning_algorithm(self, eq_oracle):
        # Execute the KV learning algorithm with the provided equivalence oracle and other settings.
        learner_result = run_KV(
            alphabet=self.alphabet,
            sul=self.sul,
            eq_oracle=eq_oracle,
            automaton_type='dfa',   # Specifies the type of automaton (DFA) to learn.
            cache_and_non_det_check=True
        )
        return learner_result

    def refine_hypothesis_with_cache(self):
        # Iteratively refine the learned hypothesis using the cache-based equivalence oracle.
        learner_result = None
        counterexample_found = True

        while counterexample_found:
            learner_result = self.run_learning_algorithm(self.cache_based_eq_oracle)

            # Check for counterexamples in the current hypothesis.
            counterexample = self.cache_based_eq_oracle.find_cex(learner_result)

            if counterexample:
                print(f"Counterexample found: {counterexample}")
                counterexample_found = True
            else:
                print("No new counterexample found. Hypothesis is considered refined.")
                counterexample_found = False

        return learner_result

    def main_active_learning_loop(self):
        # File paths
        dot_file = 'learned_model.dot'
        pdf_file = 'learned_model.pdf'

        # Delete old files if they exist
        if os.path.exists(dot_file):
            os.remove(dot_file)
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

        # Main method to run the active learning loop, refine the hypothesis, and save/visualize the model.
        learner_result = self.refine_hypothesis_with_cache()

        # Save and visualize the learned model
        model_file = 'learned_model.dot'
        print('accepted: ', self.sul.accepted_queries)
        save_automaton_to_file(learner_result, model_file)
        visualize_automaton(learner_result, path=model_file.replace('.dot', '.pdf'))


# Define the mapping of id_type strings to numeric values
id_type_mapping = {
        "NONE": 0,  # Common name
        "DNS": 1,  # DNS
        "IPADDR": 2,  # IP ADDRESS
        "EMAIL": 3  # EMAIL
    }
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ActiveLearning.py <hostname>")
        print("id_type options: NONE, DNS, IPADDR, EMAIL")
        sys.exit(1)

    hostname = sys.argv[1]
    id_type_str = sys.argv[2].upper()

    # Validate and convert id_type from string to its numeric representation
    if id_type_str in id_type_mapping:
        id_type = id_type_mapping[id_type_str]
    else:
        print(f"Invalid id_type: {id_type_str}")
        print("Valid options are: NONE, DNS, IPADDR, EMAIL")
        sys.exit(1)

    learning_framework = ActiveLearningFramework(name=hostname, id_type=id_type)
    learning_framework.main_active_learning_loop()

