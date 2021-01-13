class Player():
	cards = dict()
	name = ""

	def __init__(self, name):
		self.name = name
		self.cards = dict()

	def do_local(self):
		print("Spam")


players = dict()

def main():
	with open("DominionLog.txt", 'r') as log_file:
		# start configuration
		for line in log_file:
			if "beginnt" in line:
				players_name = line[0:line.find(" beginnt")]
				card_str = line[line.find("folgenden Karten: ")+len("folgenden Karten: "):len(line)-2]
				card_num_temp, card_name = card_str.split(" ")
				card_num = int(card_num_temp)

				print("Neue Karte gefunden")
				print("Spielername: "+players_name)
				print(str(card_num)+" mal "+card_name)

				if players_name in players.keys():
					print("Spieler bereits gefunden")
					if card_name in players[players_name].cards:
						print("Kartentyp bereits gefunden")
						players[players_name].cards[card_name] = players[players_name].cards[card_name] + card_num
					else:
						print("Kartentyp noch nicht vorhanden")
						players[players_name].cards[card_name] = card_num
					print("Karten des Spielers: "+str(players[players_name].cards))
				else:
					print("Spieler neu anlegen")
					new_player = Player(players_name)
					new_player.cards[card_name] = card_num
					players[players_name] = new_player
					print("Karten des neuen Spielers: "+str(new_player.cards))
				
				print("===========")
			
			if "mischt" in line:
				break
		
		for player in players.values():
			print(player.name)
			print(player.cards)



if __name__ == '__main__':
	main()




