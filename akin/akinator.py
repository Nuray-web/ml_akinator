import pygame
from pygame.locals import *
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from PIL import Image

class Akinator:
    def __init__(self, dataset):
        self.dataset = dataset
        self.label_encoder = LabelEncoder()
        self.clf = DecisionTreeClassifier()
        self.build_decision_tree()

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Akinator Game")
        self.font = pygame.font.Font(None, 36)
        self.background = pygame.image.load("akin/background.jpg").convert()

    def build_decision_tree(self):
        X = self.dataset.drop(columns=['champion'])
        y = self.label_encoder.fit_transform(self.dataset['champion'])
        self.clf.fit(X, y)

    def calculate_bayesian_probability(self, node_index, prior_probability, likelihood):
        epsilon = 1e-9
        prior_probability = max(prior_probability, epsilon)

        posterior_probability = (prior_probability * likelihood) / (
            (prior_probability * likelihood) + ((1 - prior_probability) * (1 - likelihood)))

        return posterior_probability

    def ask_question(self, question):
        self.screen.blit(self.background, (0, 0))
        input_text = self.font.render(question, True, (255, 255, 255))
        text_rect = input_text.get_rect(center=(400, 50))
        self.screen.blit(input_text, text_rect)

        instructions_text = ["Press 'Y' for Yes, 'N' for No,", "'I' for I don't know", "'S' for quitting game"]
        for i, line in enumerate(instructions_text):
            line_surface = self.font.render(line, True, (255, 255, 255))
            line_rect = line_surface.get_rect(center=(400, 300 + i * 30))  # Adjust vertical position
            self.screen.blit(line_surface, line_rect)

        pygame.display.flip()

        answer = None
        while answer not in ['yes', 'no', "idk"]:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        answer = 'yes'
                    elif event.key == K_n:
                        answer = 'no'
                    elif event.key == K_i:
                        answer = 'idk'
                    elif event.key == K_s:
                        pygame.quit()
        return answer

    def display_result(self, most_likely_champion, posterior_probability):
        result_text = f"I think the champion is {most_likely_champion} with a probability of {posterior_probability:.2%}."
        result_surface = self.font.render(result_text, True, (255, 255, 255))
        self.screen.blit(result_surface, (30, 100))
        pygame.display.flip()

    def display_correct_guess(self):
        correct_text = "I guessed the correct champion! Well done!"
        correct_surface = self.font.render(correct_text, True, (255, 255, 255))
        text_rec = correct_surface.get_rect(center=(400, 300))
        self.screen.blit(correct_surface, text_rec)
        pygame.display.flip()

    def display_confirmation(self):
        self.screen.blit(self.background, (0, 0))
        guess_text = "Did I guess correctly? (yes/no)"
        guess_surface = self.font.render(guess_text, True, (255, 255, 255))
        text_rec = guess_surface.get_rect(center=(400, 300))
        self.screen.blit(guess_surface, text_rec)
        pygame.display.flip()


    def play(self, node_index=0, prior_probability=None):
        if prior_probability is None:
            prior_probability = 0.5

        node = self.clf.tree_
        feature_names = self.dataset.drop(columns=['champion']).columns

        while node.feature[node_index] != -2:
            feature_index = node.feature[node_index]
            feature = feature_names[feature_index]

            question = f"The champion {feature}?"
            answer = self.ask_question(question)

            if answer == "idk":
                # print("Okay. Let's move on to the next question.")
                node_index += 1
            elif answer == 'yes':
                prior_probability = 1.0
                node_index = node.children_right[node_index]
            elif answer == 'no':
                prior_probability = 0.0
                node_index = node.children_left[node_index]

        predicted_class = int(node.value[node_index].argmax())
        likelihood = node.value[node_index][0, predicted_class] / node.value[node_index].sum()
        posterior_probability = self.calculate_bayesian_probability(node_index, prior_probability, likelihood)

        most_likely_champion = self.label_encoder.classes_[predicted_class]

        self.display_result(most_likely_champion, posterior_probability)

        path = "champions\\" + most_likely_champion.lower().replace(" ", "").replace(".", "") + '.jpg'
        img = Image.open(path)

        max_width, max_height = 700, 300
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)

        img = img.convert('RGB')
        img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
        img_rect = img.get_rect(center=(400, 350))
        self.screen.blit(img, img_rect)
        pygame.display.flip()

        pygame.time.delay(2000)

        self.display_confirmation()

        correct_answer = None
        while correct_answer not in ['yes', 'no']:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        correct_answer = 'yes'
                    elif event.key == K_n:
                        correct_answer = 'no'
                    elif event.key == K_s:
                        pygame.quit()

        if correct_answer == 'yes':
            self.display_correct_guess()

            self.screen.blit(self.background, (0, 0))
            play_again_text = "Do you want to play again? (yes/no)"
            play_again_surface = self.font.render(play_again_text, True, (255, 255, 255))
            text_rec = play_again_surface.get_rect(center=(400, 300))
            self.screen.blit(play_again_surface, text_rec)
            pygame.display.flip()

            play_again = None
            while play_again not in ['yes', 'no']:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_y:
                            play_again = 'yes'
                        elif event.key == K_n:
                            play_again = 'no'
                        elif event.key == K_s:
                            pygame.quit()

            if play_again == 'yes':
                self.play()
            else:
                self.screen.blit(self.background, (0, 0))
                text = "Thank you for playing! <3"
                surface = self.font.render(text, True, (255, 255, 255))
                text_rec = surface.get_rect(center=(400, 300))
                self.screen.blit(surface, text_rec)
                pygame.display.flip()
                pygame.time.delay(2000)
                pygame.quit()

        else:
            text = "Let me continue guessing."
            surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (50, 50))
            pygame.display.flip()
            pygame.time.delay(2000)
            node_index += 1
            self.play(node_index)
        

dataset = pd.read_csv('akin\League of Legends.csv')

akinator = Akinator(dataset)
akinator.play()
