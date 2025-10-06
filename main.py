import os
from dotenv import load_dotenv
import sys


def check_missing_and_adjacent_input_violations():
    # Load environment variables from .env file
    load_dotenv()

    try:
        num_words_to_take = int(os.getenv('WORD_COUNT', 0))
    except ValueError:
        print("Error: WORD_COUNT environment variable must be a valid integer")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python script.py word1 word2 word3 ...")
        sys.exit(1)

    input_words = sys.argv[1:]
    input_words_lower = [word.lower() for word in input_words]
    print(f"Input words: {input_words}")

    try:
        with open('test.txt', 'r') as file:
            content = file.read().strip()

        words = [word.strip() for word in content.split(',')]
        words = [word for word in words if word]

        print(f"Total words in file: {len(words)}")

        if num_words_to_take > 0:
            selected_words = words[:num_words_to_take]
            print(f"Using first {num_words_to_take} words from file: {selected_words}")
        else:
            selected_words = words
            print(f"Using all words from file: {selected_words}")

        # --- Part 1: Words from file missing in input ---
        input_words_set = set(word.lower() for word in input_words)
        missing_from_input = [word for word in selected_words if word.lower() not in input_words_set]
        missing_count = len(missing_from_input)
        print(f"\nWords from file missing in input: {missing_from_input}")
        print(f"Missing count: {missing_count}")

        # --- Part 2: Check adjacent pairs from file that are BOTH in input AND adjacent in input ---
        violations = []
        if len(selected_words) < 2:
            print("\nNot enough words in file to form adjacent pairs.")
            adjacent_violation_count = 0
        else:
            # Get all adjacent pairs from file
            for i in range(len(selected_words) - 1):
                word1 = selected_words[i]
                word2 = selected_words[i + 1]

                # Check if both words are in input
                if word1.lower() in input_words_set and word2.lower() in input_words_set:
                    # Find their positions in input
                    try:
                        pos1 = input_words_lower.index(word1.lower())
                        pos2 = input_words_lower.index(word2.lower())

                        # Check if they are adjacent in input (difference of 1)
                        if abs(pos1 - pos2) == 1:
                            violations.append((word1, word2))
                    except ValueError:
                        continue  # Shouldn't happen since we checked they're in input set

            adjacent_violation_count = len(violations)
            print(f"\n⚠️ Adjacent word pairs from file that are BOTH in input AND adjacent in input (violations):")
            for pair in violations:
                print(f"  - {pair[0]} & {pair[1]}")
            print(f"Total adjacent violations: {adjacent_violation_count}")

        return missing_count, adjacent_violation_count

    except FileNotFoundError:
        print("Error: test.txt file not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    check_missing_and_adjacent_input_violations()