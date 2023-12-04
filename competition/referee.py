# from competition.player1_competition import Player1
# from competition.player2_competition import Player2
# from competition.shuttlecock_competition import Shuttlecock


# class Referee:
#
#     def __init__(self):
#         self.x = 400
#         self.y = 50
#
#     def check_when_shuttlecock_drop(self):
#         from competition.player1_competition import Player1
#         from competition.player2_competition import Player2
#         from competition.shuttlecock_competition import Shuttlecock
#
#         if Shuttlecock.who_hit_shuttlecock == 'player1':
#             if Shuttlecock.x > 700 or Shuttlecock.x < 400:
#                 print('플레이어1 우승')
#                 Player1.score += 1
#         if Shuttlecock.who_hit_shuttlecock == 'player2':
#             if Shuttlecock.x < 100 or Shuttlecock.x > 400:
#                 Player2.score += 1
#                 print('플레이어2 우승')
#     def update(self):
#         pass
#
#     def get_bb(self):
#         pass