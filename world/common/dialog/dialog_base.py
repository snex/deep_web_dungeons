import os

class DialogBase:
    def _load_file(self, filename, gender="none", pronoun_type="none"):
        filename = f"{os.path.dirname(os.path.realpath(__file__))}/data/{filename}.txt"
        with open(filename, "r") as f:
            data = [line.strip().replace("$pronoun$", f"#.pronoun({gender},{pronoun_type})#") for line in f.readlines()]

        return data

    def _pos(self, text, *params):
        if text[-1] == "s":
            return f"{text}'"
        else:
            return f"{text}'s"

    def _possessive_modifiers(self):
        return {
            "pos": self._pos
        }

    def _get_pronoun(self, *params):
        _, gender, pronoun_type = params
        match gender:
            case "male":
                match pronoun_type:
                    case "sub":
                        return "he"
                    case "obj":
                        return "him"
                    case "pos":
                        return "his"
                    case _:
                        return ""
            case "female":
                match pronoun_type:
                    case "sub":
                        return "she"
                    case "obj":
                        return "her"
                    case "pos":
                        return "her"
                    case _:
                        return ""
            case _:
                match pronoun_type:
                    case "sub":
                        return "they"
                    case "obj":
                        return "them"
                    case "obj":
                        return "their"
                    case _:
                        return ""
    def _pronoun_modifiers(self):
        return {
            "pronoun": self._get_pronoun
        }

