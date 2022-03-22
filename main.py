import requests
import random
from typing import List
import html
import json


class Question:
    def __init__(self, question: str, answers: dict, correct_answer: str):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer

    def __repr__(self):
        return f"Question ({self.question})\n"


class QuestionBuilder:
    """Take raw data from API and build a list with question, all answers, and the correct answer"""
    def __init__(self, api_data):
        self.api_data = api_data

    @staticmethod
    def answers_shuffle(incorrect_answers: List, correct_answer: str):
        all_answers = incorrect_answers[:]
        all_answers.append(correct_answer)
        random.shuffle(all_answers)
        return all_answers

    def build_questions(self):
        """Build and shuffle the question and answers. Distinguishing between T/F and multiple"""
        final_compilation = []
        for item in self.api_data["results"]:

            all_answers = self.answers_shuffle(item["incorrect_answers"], item["correct_answer"])
            question = item["question"]
            correct_answer = item["correct_answer"]
            if item["type"] == "multiple":
                answers = {
                    "A": all_answers[0],
                    "B": all_answers[1],
                    "C": all_answers[2],
                    "D": all_answers[3]
                }
            elif item["type"] == "boolean":
                answers = {
                    "A": all_answers[0],
                    "B": all_answers[1]
                }
            else:
                raise Exception("Invalid question type")
            answer_key = get_correct_answer(answers, correct_answer)
            final_compilation.append(Question(question, answers, answer_key))
        return final_compilation


def get_correct_answer(ans_dictionary: dict, right_answer):
    """GETTING THE ANSWER KEY TO MATCH WITH USER ANSWER"""
    for k, v in ans_dictionary.items():
        if v == right_answer:
            return k


def main():
    """User choice for number of questions. Request from API"""
    play_game = True
    while play_game:
        number_of_questions = input("\nHow many questions would you like for your quiz?: ")
        response = requests.get(url=f"https://opentdb.com/api.php?amount={number_of_questions}")
        response.raise_for_status()
        data = json.loads(response.content)
        score = 0
        question_answer_bank = QuestionBuilder(data).build_questions()

        for question in question_answer_bank:
            next_question = question
            formatted_answers = list(map(lambda x: ": ".join(x), next_question.answers.items()))
            all_answers = "\n".join(formatted_answers) + "\n"
            print(f"\n{html.unescape(next_question.question)}")
            print(f"\n{html.unescape(all_answers)}")
            user_answer = input("Please choose an answer: ").upper()

            if next_question.correct_answer == user_answer:
                print("\nYou got it right! ")
                score += 1
            else:
                print("\nSorry, that's wrong")
                print(f"\nThe correct answer was {next_question.correct_answer}\n")

        print("Game is finished. Great work!")
        print(f"Your final score was {score}/{len(question_answer_bank)}\n")
        play_again = input("Would you like to play again (Y or N)? ")
        if play_again == "N".lower():
            play_game = False


if __name__ == "__main__":
    main()
