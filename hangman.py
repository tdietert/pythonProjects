from tkinter import *

class Hangman(Frame):

	def __init__(self, parent):

		Frame.__init__(self, parent)
		self.parent = parent

		self.alpha_buttons = []

		self.chars_in_answer = []
		self.labels_for_answer = []
		self.word_entered = StringVar()
		self.num_guesses = 0
		self.guess_max = 6

		self.initUI()

	def initUI(self):

		self.parent.title("Hangman")

		self.prompt = Label(
			self.parent, text = "Enter word:")
		self.prompt.grid(row = 0, column = 0, columnspan = 3)

		self.word_entry = Entry(self.parent, textvariable = self.word_entered)
		self.word_entry.grid(row = 0, column = 3, columnspan = 6)

		self.setWord_button = Button(self.parent, text = "Start", command = self.setWord)
		self.setWord_button.grid(row = 0, column = 9, columnspan = 2)

		self.canvas = Canvas(self.parent, height = 200, width = 300, bg = "white")
		self.canvas.grid(row = 1, column = 0, columnspan = 13, rowspan = 4)

		self.info_label = Label(self.parent, text = "Word to guess:")
		self.info_label.grid(row = 5, column = 0, columnspan = 4)

		# creates 26 alpha char buttons
		for i in range(97, 110):
			new_button = Button(self.parent, text = chr(i), width = 2)
			new_button.grid(row = 6, column = i % 13, sticky = W+E)
			self.alpha_buttons.append(new_button)
			
		column = 0
		for i in range(110, 123):
			new_button = Button(self.parent, text = chr(i), width = 2)
			new_button.grid(row = 7, column = column, sticky = W+E)
			self.alpha_buttons.append(new_button)
			column += 1

		for i in range(0, len(self.alpha_buttons)):
			self.alpha_buttons[i].configure(command = lambda i=i:self.guess(self.alpha_buttons[i]['text']))

		self.drawBase()

	def guess(self, letter):

		letter = letter.lower()

		count = 0
		# lets user guess only if word is set
		if self.num_guesses < 6 and len(self.chars_in_answer) > 0:
			for i in range(0, len(self.chars_in_answer)):
				if letter == self.chars_in_answer[i]:
					self.labels_for_answer[i].configure(text = letter)
					count += 1
				elif self.chars_in_answer[i] == ' ':
					i = i - 1

			# draws body part according to the number 
			if count == 0:
				self.num_guesses += 1
				self.drawHangman()

			# disables letter buttons that have already been guessed
			for button in self.alpha_buttons:
				if(button['text'] == letter):
					button.configure(state = DISABLED, disabledforeground = "red")

			self.checkWin()

	def setWord(self):

		# checks if word is less than 9 characters
		if(len(self.word_entered.get()) < 10):
			for letter in self.word_entered.get():
				self.chars_in_answer.append(letter)

			# disables the entry that sets the answer
			self.word_entered.set("")
			self.word_entry.config(state = "readonly")

			self.createLetterLabels()
		else:
			error_window = Toplevel()
			error_text = Label(error_window, text = "Please enter a word under 10 characters long")
			error_text.grid(row = 0, column = 0, columnspan = 3)

			error_ok = Button(error_window, text = "Ok", command = lambda:error_window.destroy())
			error_ok.grid(row = 1, column = 1)

			self.word_entered.set("")

	def createLetterLabels(self):
		# checks for spaces entered
		for i in range(0, len(self.chars_in_answer)):
			if self.chars_in_answer[i] != ' ':
				new_label = Label(self.parent, text = "__")
				new_label.grid(row = 5, column = i + 4, sticky = W+E)
				self.labels_for_answer.append(new_label)
			else:
				i = i - 1

	def drawBase(self):
		self.canvas.create_line(30, 175, 110, 175)
		self.canvas.create_line(70, 175, 70, 30)
		self.canvas.create_line(70, 30, 130, 30)
		self.canvas.create_line(130, 30, 130, 55)

	def drawHangman(self):
		# draws the hangman figure depending on how many guesses
		if self.num_guesses == 1:	
			self.canvas.create_oval(118, 55, 142, 79)
		elif self.num_guesses == 2:
			self.canvas.create_line(130, 79, 130, 125)
		elif self.num_guesses == 3:
			self.canvas.create_line(130, 90, 120, 110)
		elif self.num_guesses == 4:
			self.canvas.create_line(130, 90, 140, 110)
		elif self.num_guesses == 5:
			self.canvas.create_line(130, 125, 120, 145)
		else:
			self.canvas.create_line(130, 125, 140, 145)


	def checkWin(self):
		count = 0
		for label in self.labels_for_answer:
			if label['text'] == "__":
				count += 1
				break

		# if game is over
		if count == 0 or self.num_guesses == 6:
			gameover_window = Toplevel()
			display = Label(gameover_window, text = "")
			display.grid(row = 0, column = 0, columnspan = 4)

			if count == 0:
				display.configure(text = "Congratulations, you win! Would you like to play again?")
			else:
				display.configure(text = "Sorry, you lost! Would you like to play again?")

			yes_button = Button(gameover_window, text = "Yes", width = 4, command = lambda:self.reset(gameover_window))
			yes_button.grid(row = 1, column = 0, columnspan = 2)

			no_button = Button(gameover_window, text = "No", width = 4, command = lambda:self.quit(gameover_window))
			no_button.grid(row = 1, column = 2, columnspan = 2)

	def reset(self, window):
		for button in self.alpha_buttons:
			if button['state'] == DISABLED:
				button['state'] = NORMAL
				button['fg'] = "black"

		self.word_entry.configure(state = NORMAL)

		# clears variables used for storing current word
		for label in self.labels_for_answer:
			label['text'] = " "

		del self.labels_for_answer[:]
		del self.chars_in_answer[:]

		self.word_entered.set("")
		self.canvas.delete("all")
		self.num_guesses = 0
		self.drawBase()

		window.destroy()

	def quit(self, window):
		window.destroy()
		self.parent.destroy()


def main():
	root = Tk()
	hangman = Hangman(root)
	root.mainloop()

if __name__ == '__main__':
	main()
