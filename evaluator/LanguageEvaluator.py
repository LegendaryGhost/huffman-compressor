import json

class LanguageEvaluator:
    @staticmethod
    def evaluate_language(language_file: str) -> bool:
        # 1. Read the original language
        languages = []
        with open(language_file, "r") as lf:
            languages.append(set(json.load(lf)))

        languages.append(LanguageEvaluator.get_quotient(languages[0], languages[0]))
        languages[1].remove("")

        i = 1
        while i <= 1000:
            print(i)
            new_language = LanguageEvaluator.get_quotient(languages[0], languages[i])
            current_quotient = LanguageEvaluator.get_quotient(languages[i], languages[0])
            new_language.update(current_quotient)
            
            if "" in new_language:
                return False
            
            for previous in languages:
                if previous == new_language:
                    return True
            
            languages.append(new_language)
            i += 1

        return True

    @staticmethod
    def get_residual(letter: str, language: set[str]) -> set[str]:
        residual = set()
        for element in language:
            if element.startswith(letter):
                residual.add(element.removeprefix(letter))
        return residual
    
    @staticmethod
    def get_quotient(left_language: set[str], right_language: set[str]) -> set[str]:
        quotient = set()
        for left_letter in left_language:
            quotient.update(LanguageEvaluator.get_residual(left_letter, right_language))
        return quotient