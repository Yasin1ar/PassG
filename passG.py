""" A program that generates Solid 8-digits passwords, and keep them safe in .txt file in the chosen folder,
 and sends update via telegram """
 
from random import choices, choice
import os
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename = os.getcwd(),
					format=LOG_FORMAT,
					level=logging.DEBUG)

logger = logging.getLogger("Main")

class PassGenerator:

	chars = ["1234567890", "qwertyuiopasdfghjklzxcvbnm", "!@#$%&"]

	def create_pass() -> str:

		password = ""
		for i in choices(PassGenerator.chars[1],k=3) : password += i ; password = password.title()
		for i in choices(PassGenerator.chars[0],k=3) : password += i 
		for i in choices(PassGenerator.chars[2],k=2) : password += i 

		password = set(password)
		temporary_variable = ""
		for i in password: temporary_variable += i
		password = temporary_variable 

		if ( 8 - len(set(password)) ) != 0 :
			list = PassGenerator.chars[0] + PassGenerator.chars[1]
			while len(set(password)) != 8:
				l = choice(list)
				if l not in password.lower() : 
					password += l

		return password

class PassManager:

	file = os.getcwd()

	def add():
		with open(PassManager.file, "a") as f:
			password = PassGenerator.create_pass()
			f.write(f"{profile.strip()} : {password}\n")
			s = len(profile) - 7
			space_a = 0 ; space_b = 0
			if s > 0 : space_a = s 
			elif s < 0 : space_b = abs(s)  
			print(f" Succussfully added    profile{space_a *  ' '} : password\n")
			print(f"                       {profile}{space_b * ' '} : {password}\n")
			logger.info("Password added")

	def delete():
		with open(PassManager.file, "r") as f:
			lines = f.readlines()
			lines.remove(line_to_remove)
			with open(PassManager.file, "w") as f:
				for line in lines:
					f.write(line)
		
		logger.info(f"{line_to_remove} was deleted")
		print(f" {profile}'ve been successfully deleted ")

	def replace():
		with open(PassManager.file, "r") as f:
			lines = f.readlines()
			with open(PassManager.file, "w") as f:
				for line in lines:
					line_split = line.split(":")
					if profile in line_split[0]:
						new_password = PassGenerator.create_pass()
						line = f"{profile} : {new_password}\n"
					f.write(line)
		
		logger.info(f"{line_} replaced with new password {new_password_}")
		print(" successfully replaced the previous password with new one({})".format(new_password))

	def reorder():
		with open(PassManager.file, "r") as f:
			lines = f.readlines()
			longest_len = 4
			for line in lines:
				profile_len = len(line.split(":")[0].strip())
				if profile_len > longest_len : longest_len = profile_len
			with open(PassManager.file , "w") as f:
				space = " "
				for line in lines : 
					l = line.split(":")
					f.write(f"{l[0].strip()}{space * (longest_len - len(l[0].strip()))} :  {l[1].strip()}\n")
					
					
class Main:
	
	def main():

		global profile
		profile = ""

		commands = ["show", "delete all", "exit", "help", "Help", "HELP", "passG", "PassG", "passg"]
		while profile in commands or len(profile) < 3:

			with open(PassManager.file, "r") as f:
				lines = f.readlines()

				profile = input(" >> ")

				if profile == "show":
					if len(lines) >= 1:
						list = []
						for i in lines:
							l = i.split(":")
							line=f"{l[0].strip()} : {l[1][0:-1]}"
							list.append(line)
					else:
						print(" The file is empty")
						continue	

					print(" ",list)
					
				elif profile == "delete all":
					if len(lines) == 0:
						print(" The file is already empty")
					else:
						response = input(" Are you sure you want to delete all your passwords? (y/n) : ")
						if response in ["Yes", "yes", "Y", "y"]:
							with open(PassManager.file, "w") as f:
								f.write("")
								print(" The file is clear now and all the passwords are gone")
								logger.warn("delete all command have deleted all passwords")

							
				elif profile in commands[3:]:
					print(" Commands are 'show' and 'delete all' ")
					print(" hint : strongly recommend to use a good and memorable or informational profile \
					that will help you to know which password is for which , \
					e.x of profile [ Yasin10ar@gmail.com , facebook.com , Crypto Wallet & ...] ")

				elif len(profile) < 3 :
					print(" If you want to generate a password, you must enter a word with or more than 3 character")
					print(" type 'help' for more\n")

				elif profile == "exit": 
					PassManager.reorder()
					exit()

		with open(PassManager.file, "r") as f:
			lines = f.readlines()
			profiles = [line.split(':')[0].strip() for line in lines]

			if len(lines) == 0 : PassManager.add()
			
			add_flag = True
			for p in profiles:
				if profile.strip() == p:
					option = input(f" {profile} already exist, what do you want to do? (delete/replace) : ")
					
					if option == "delete":
						global line_to_remove
						line_to_remove = i
						PassManager.delete()
						add_flag = False
						break
					elif option == "replace":
						PassManager.replace()
						add_flag = False
						break
					else:
						print( "wrong input, options are 'delete' and 'replace'\n exiting ...")

		
			if add_flag : PassManager.add()

if __name__ == "__main__":
	key = " on "
	while len(key) > 0:
		Main.main()
		PassManager.reorder()
		key = input("\n Type anything to add another one or press Enter to exit : ")
