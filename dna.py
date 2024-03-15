from flask import Flask, request, jsonify

app = Flask(__name__)


def identify_mutation(original_dna, mutated_dna):
  """
  This function identifies the type of mutation in a DNA sequence based on the original and mutated sequences.

  Args:
      original_dna: The original DNA sequence as a string.
      mutated_dna: The mutated DNA sequence as a string.

  Returns:
      A dictionary containing the mutation type and (optional) details.
  """

  if original_dna == mutated_dna:
    return {"mutation_type": "No mutation"}

  # Check for single nucleotide polymorphism (SNP)
  if len(original_dna) == len(mutated_dna) and len(original_dna) == 1:
    return {"mutation_type": "SNP"}

  # Check for insertion
  if len(mutated_dna) > len(original_dna):
    insertion_start = 0
    for i in range(len(original_dna)):
      if original_dna[i] != mutated_dna[i]:
        insertion_start = i
        break
    inserted_sequence = mutated_dna[insertion_start:len(mutated_dna)]
    return {
        "mutation_type": "Insertion",
        "inserted_sequence": inserted_sequence,
        "index": insertion_start
    }

  # Check for deletion
  if len(mutated_dna) < len(original_dna):
    deletion_start = 0
    for i in range(len(mutated_dna)):
      if original_dna[i] != mutated_dna[i]:
        deletion_start = i
        break
    deleted_sequence = original_dna[deletion_start:len(original_dna)]
    return {
        "mutation_type": "Deletion",
        "deleted_sequence": deleted_sequence,
        "index": deletion_start
    }

  # More complex mutations
  return {"mutation_type": "Complex mutation (not currently supported)"}


@app.route('/identify_mutation', methods=['POST'])
def handle_mutation_request():
  data = request.get_json()
  original_dna = data.get('original_dna')
  mutated_dna = data.get('mutated_dna')

  if not original_dna or not mutated_dna:
    return jsonify({'error': 'Missing required fields'}), 400

  mutation_result = identify_mutation(original_dna, mutated_dna)
  return jsonify(mutation_result)


if __name__ == '__main__':
  app.run(debug=True)
