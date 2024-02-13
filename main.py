from collections import Counter


class Player(object):
    def __init__(self, name):
        self.name = name
        self.last_move = True
        self.round = 0
        self.other_cheated = False


class Cheater(Player):
    def play(self, other):
        return False


class Cooperator(Player):
    def play(self, other):
        return True


class Copycat(Player):
    def play(self, other):
        if other.last_move:
            return True
        return False


class Grudger(Player):
    def play(self, other):
        if self.other_cheated:
            return False
        if other.last_move:
            result = True
        else:
            result = False
            self.other_cheated = True
        return result


class Detective(Player):
    def __init__(self, name):
        super().__init__(name)
        self.strategy = [True, False, True, True]

    def play(self, other):
        if self.round < 4:
            result = self.strategy[self.round]
            self.round += 1
            if other.last_move == False:
                self.other_cheated = True
        elif self.other_cheated:
            # становится copycat
            result = other.last_move
        else:
            # становится cheater
            result = False
        return result


class Game(object):
    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def reset_data(self, player):
        player.last_move = True
        player.round = 0
        player.other_cheated = False

    def play(self, player1, player2):
        for _ in range(self.matches):
            player1_move = player1.play(player2)
            player2_move = player2.play(player1)
            player1.last_move = player1_move
            player2.last_move = player2_move

            if player1_move and player2_move:
                self.registry[player1.name] += 2
                self.registry[player2.name] += 2
            elif player1_move and not player2_move:
                self.registry[player1.name] -= 1
                self.registry[player2.name] += 3
            elif player2_move and not player1_move:
                self.registry[player1.name] += 3
                self.registry[player2.name] -= 1
        self.reset_data(player1)
        self.reset_data(player2)

    def top3(self):
        playeres_scores = list(sorted(self.registry.values(), reverse=True))
        top_three_points = [playeres_scores[0]]
        for score in playeres_scores:
            if top_three_points[-1] != score:
                top_three_points.append(score)
            if len(top_three_points) == 3:
                break

        for score in top_three_points:
            for player, player_score in self.registry.items():
                if player_score == score:
                    print(player, player_score)


if __name__ == '__main__':
    cooperator = Cooperator('cooperator')
    cheater = Cheater('cheater')
    copycat = Copycat('copycat')
    grudger = Grudger('grudger')
    detective = Detective('detective')
    game = Game()
    players = [cooperator, cheater, copycat, grudger, detective]
    for player1 in players:
        for player2 in players:
            if player1 == player2:
                break
            game.play(player1, player2)
    game.top3()
