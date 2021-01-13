import csv

class Player():
	cards = dict()
	name = ""
	cards_log_diff = dict() # [turn, card_name] = num
	cards_log_cum = dict()

	def __init__(self, name):
		self.name = name
		self.cards = dict()
		self.cards_log_diff = dict()
		self.cards_log_cum = dict()

	def do_local(self):
		print("Spam")


players = dict()

def main():
	with open("DominionLog.txt", 'r') as log_file:
		# start configuration
		turn = 0
		for line in log_file:
			if "beginnt" in line:
				players_name = line[0:line.find(" beginnt")]
				card_str = line[line.find("folgenden Karten: ")+len("folgenden Karten: "):len(line)-2].replace(".", "")
				card_num_temp, card_name = card_str.split(" ")
				card_num = int(card_num_temp)

				# print("Neue Karte gefunden")
				# print("Spielername: "+players_name)
				# print(str(card_num)+" mal "+card_name)

				if players_name in players.keys():
					# print("Spieler bereits gefunden")
					if card_name in players[players_name].cards:
						# print("Kartentyp bereits gefunden")
						players[players_name].cards[card_name] = players[players_name].cards[card_name] + card_num
						players[players_name].cards_log_diff[(turn, card_name)] = card_num
						players[players_name].cards_log_cum[(turn, card_name)] = players[players_name].cards[card_name]
					else:
						# print("Kartentyp noch nicht vorhanden")
						players[players_name].cards[card_name] = card_num
						players[players_name].cards_log_diff[(turn, card_name)] = card_num
						players[players_name].cards_log_cum[(turn, card_name)] = card_num
					# print("Karten des Spielers: "+str(players[players_name].cards))
				else:
					# print("Spieler neu anlegen")
					new_player = Player(players_name)
					new_player.cards[card_name] = card_num
					new_player.cards_log_diff[(turn, card_name)] = card_num
					new_player.cards_log_cum[(turn, card_name)] = card_num
					players[players_name] = new_player
					# print("Karten des neuen Spielers: "+str(new_player.cards))
				
				# print("===========")
			
			if "mischt" in line:
				break
		
		# Game itself
		for line in log_file:
			if line.startswith("Zug"):
				line_split = line.split(" ")
				turn = int(line_split[1])
			
			if "nimmt" in line:
				if line.endswith("."):
					line_str = line[:-1]
				else:
					line_str = line
				line_split = line_str.split(" ")
				pos_nimmt = line_split.index("nimmt")
				amount_str = line_split[pos_nimmt+1]
				players_name = line_split[0]

				# names with two parts
				if pos_nimmt+2 < len(line_split)-1:
					card_name = line_split[pos_nimmt+2] + " " + line_split[pos_nimmt+3].strip().replace(".", "")
				else:
					card_name = line_split[pos_nimmt+2].strip().replace(".", "")
				amount = int(amount_str.replace("einen", "1").replace("eine", "1").replace("ein", "1"))
				# print("%s zieht %d %s" % (players_name, amount, card_name))

				if card_name in players[players_name].cards:
						# print("Kartentyp bereits gefunden")
						players[players_name].cards[card_name] = players[players_name].cards[card_name] + amount
						players[players_name].cards_log_diff[(turn, card_name)] = amount
						players[players_name].cards_log_cum[(turn, card_name)] = players[players_name].cards[card_name]
				else:
					# print("Kartentyp noch nicht vorhanden")
					players[players_name].cards[card_name] = amount
					players[players_name].cards_log_diff[(turn, card_name)] = amount
					players[players_name].cards_log_cum[(turn, card_name)] = amount

			# trash cards
			if "entsorgt" in line:
				if line.endswith("."):
					line_str = line[:-1]
				else:
					line_str = line
				line_split = line_str.split(" ")
				pos_nimmt = line_split.index("entsorgt")
				amount_str = line_split[pos_nimmt+1]
				players_name = line_split[0]

				# names with two parts
				if pos_nimmt+2 < len(line_split)-1:
					card_name = line_split[pos_nimmt+2] + " " + line_split[pos_nimmt+3].strip()
				else:
					card_name = line_split[pos_nimmt+2].strip()
				amount = int(amount_str.replace("einen", "1").replace("eine", "1").replace("ein", "1"))
				# print("%s zieht %d %s" % (players_name, amount, card_name))

				if card_name in players[players_name].cards:
						# print("Kartentyp bereits gefunden")
						players[players_name].cards[card_name] = players[players_name].cards[card_name] - amount
						players[players_name].cards_log_diff[(turn, card_name)] = -amount
						players[players_name].cards_log_cum[(turn, card_name)] = players[players_name].cards[card_name]

		for player in players.values():
			print(player.name)
			print(player.cards)
			
	with open("results_diff.csv", mode='w') as evalTable:
		evalTable.write("Name,Zug,Karte,Anzahl\n")
		evalWriter = csv.writer(evalTable, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		for player in players.values():
			for el, amount in player.cards_log_diff.items():
				evalWriter.writerow([player.name, el[0], el[1], amount])
	
	with open("results_cum.csv", mode='w') as evalTable:
		evalTable.write("Name,Zug,Karte,Anzahl\n")
		evalWriter = csv.writer(evalTable, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		for player in players.values():
			for el, amount in player.cards_log_cum.items():
				evalWriter.writerow([player.name, el[0], el[1], amount])



if __name__ == '__main__':
	main()




