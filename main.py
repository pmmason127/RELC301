from person import Person
import json
import random
import math
import datetime

'''
The inbreeding factor throughout history except in royalty seems to be super low, so I will probably just use a default value of .001
probably 8 generations of inbreeding necessary for inability to produce offspring

for each generation of inbreeding, subtract 1% off the life expectancy (1%, 1%+2%, 1+2+3%...), at 8 generations the person just dies

Women should have their children before age 35
'''

currentDate = datetime.datetime.now()
month = currentDate.strftime("%b")
day = currentDate.day
hour = currentDate.hour
minute = currentDate.strftime("%M")

dataCollectionFilename = "Outputs/" + str(month) + str(day) + "_" + str(hour) + "." + str(minute) + ".json"

data = {}

with open(dataCollectionFilename, 'w') as f:
	json.dump(data, f)

def startPopulation(currentPopulation):

	'''
	These are the dictionary keys for each parameter value:
	'year'
	'life_expectancy'
	'life_expectancy_factor'
	'birth_rate'
	'infant_mortality_rate'
	'childbirth_mortality_rate'
	'max_age'
	'average_time_between_children'
	'average_age_of_marriage'
	'chance_of_conceiving'
	    
	These are the dictionary eys for each badEvent value:
	'year'
	'title'
	'death_count'
	'''

	with open('parameters.json') as f:
		parameters = json.load(f)

	with open('badEvents.json') as f:
		badEvents = json.load(f)

	marriedCouples = []
	inbreedingMatters = True
	inbreedingFactor = .001
	chanceOfMarriage = 0.8
	inbreedingFactor = .001

	year = -4000
	while year < 0:

		thresholds = [-4000, -3500, -1500, 1, 1000, 1500, 1700, 1800, 1900, 1950, 2000, 2010, 2020]
		parameterIndex = 0
		for i, threshold in enumerate(thresholds):
			if year >= threshold:
				parameterIndex = i

		malesOfAge = []
		femalesOfAge = []

		# if year < -3500:
		inbreedingMatters = False
		# else:
		# 	inbreedingMatters = True
		print("Year: " + str(year))

		eligiblePeople = [person for person in currentPopulation if person.getAge() >= parameters[parameterIndex]['average_age_of_marriage']]
		for person in eligiblePeople:
			if person.getGender() == "male" and person.getSpouse() is None:
				malesOfAge.append(person)
			elif person.getGender() == "female" and person.getSpouse() is None:
				femalesOfAge.append(person)

		'''
		The following chunk of code looks through the femalesOfAge list, for each female it applies the chanceOfMarriage
		variable. If false, we skip this chunk, If true we check whether or not inbreeding is a factor at this point, if
		not, we choose any maleOfAge, if so, we search through all the males of age. If this woman will inbreed, she chooses
		from among her family, if she won't inbreed, or if there is no one to inbreed with, she will marry among her male
		non family members
		'''

		marriedWomenIndices = []
		for i, female in enumerate(femalesOfAge):
			if len(malesOfAge) == 0:
				break
			if random.random() < chanceOfMarriage:
				marriedWomenIndices.append(i)
				husband = None
				if inbreedingMatters:
					siblings = set(sibling.getPersonID() for sibling in female.getSiblings() if sibling.getGender() == "male")
					availableMenOfAge = [man for man in malesOfAge if man.getPersonID() not in siblings]
					if len(availableMenOfAge) > 0 and random.random() < inbreedingFactor:
						husband = random.choice(availableMenOfAge)
						husband.updateWillInbreed(True)
						female.updateWillInbreed(True)
					elif len(availableMenOfAge) > 0:
						husband = random.sample(availableMenOfAge, 1)[0]
				if husband is None:
					husband = random.sample(malesOfAge, 1)[0]
				husbandIndex = malesOfAge.index(husband)
				husband.updateSpouse(female.getPersonID())
				female.updateSpouse(husband.getPersonID())
				marriedCouples.append([husband, female])
				malesOfAge = [man for man in malesOfAge if man != husband]

		# Remove all the women who got married from the single women list
		femalesOfAge = [female for i, female in enumerate(femalesOfAge) if i not in marriedWomenIndices]

		print("Number of Couples: " + str(len(marriedCouples)))
		print("All males: " + str(len(malesOfAge)))
		print("All females: " + str(len(femalesOfAge)))
		'''
		for couple in marriedCouples:
			if one or more of the individuals in the couple died, remove the couple from the list
			if the woman in a couple is >= 35 years old, remove the couple from the list
			if the woman is under the max age for childbearing (35), apply the pregnancy function (need to write this) to determine if a woman will conceive
			if the couple is going to have a child:
				create a new person at age 0 and add it to the population
				add the parents and siblings as family members
				apply the infant mortality rate function
				apply the maternal childbirth mortality function
				accordingly adjust the "isAlive" variable
		'''
		removeCoupleIndices = []
		newPeople = 0
		for i in range(len(marriedCouples)):
			if len(marriedCouples[i][1].getChildren()) >= parameters[parameterIndex]['birth_rate']:
				marriedCouples[i][1].updateDoneHavingChildren()
			if (len(marriedCouples[i]) < 2):
				removeCoupleIndices.append(i)
				continue
			# If one or both parts of a couple are dead, remove the couple from the couples list
			if (marriedCouples[i][0].getIsAlive() == False) or (marriedCouples[i][1].getIsAlive() == False):
				removeCoupleIndices.append(i)
				continue
			# If the woman in a couple is 35 years old or more, remove couple from list (it is unlikely to get pregnant at this age)
			if (marriedCouples[i][1].getAge() >= 35 and year > -3500) or (marriedCouples[i][1].getDoneHavingChildren() == True):
				removeCoupleIndices.append(i)
				continue
			# If a woman will conceive given the chance of conceiving, create a new person and add it to the population
			if (marriedCouples[i][1].getTimeSinceLastChild() is None) or (marriedCouples[i][1].getTimeSinceLastChild() >= parameters[parameterIndex]['average_time_between_children']):
				if random.random() <= parameters[parameterIndex]['chance_of_conceiving']:
					newChild = Person()
					lastPerson = currentPopulation[-1].getGender()
					if lastPerson == "male":
						newChild.updateGender("female")
					elif lastPerson == "female":
						newChild.updateGender("male")
					# Add the child to the parent's children list
					marriedCouples[i][0].updateChildren(newChild.getPersonID())
					marriedCouples[i][1].updateChildren(newChild.getPersonID())
					# Add the parents to the child's ancestor list
					newChild.updateAncestors(marriedCouples[i][0].getPersonID())
					newChild.updateAncestors(marriedCouples[i][1].getPersonID())

					while len(newChild.getAncestors()) > 16:
						newChild.removeAncestor(0)
					# Reset the counter since last childbrith to 0
					marriedCouples[i][1].resetTimeSinceLastChild()

					# Update the siblings list for a child
					if len(marriedCouples[i][0].getChildren()) > 1:
						for child in marriedCouples[i][0].getChildren():
							if child == newChild.getPersonID():
								continue
							else:
								newChild.updateSiblings(child)
					# Add new child to the population
					newPeople += 1
					currentPopulation.append(newChild)

					# If the child dies, update their death
					if random.random() <= parameters[parameterIndex]['infant_mortality_rate']:
						newChild.updateDeath()
					# If a mother dies, update her death
					if random.random() <= parameters[parameterIndex]['childbirth_mortality_rate']:
						marriedCouples[i][1].updateDeath()

		removeCoupleIndices.sort(reverse = True)
		for index in removeCoupleIndices:
			del marriedCouples[index]
		'''
		for person in currentPopulation:
			apply the life expectancy function (need to write this) which changes the "isAlive" condition
			
		delete all the dead people from all lists
		get total population
		apply badEvents for the current year
		return final population
		'''
		peopleWhoDied = []
		for i in range(len(currentPopulation)):
			if currentPopulation[i].getIsAlive():
				# y = 5.20521813 * 10**(lfe_expectancy_factor) * math.exp(0.13803938 * age)
				deathChance = 5.20521813 * (10**(parameters[parameterIndex]['life_expectancy_factor'])) * math.exp(0.13803938 * currentPopulation[i].getAge())
				if random.random() <= deathChance:
					currentPopulation[i].updateDeath()
					peopleWhoDied.append(i)

		numDead = 0
		peopleWhoDied.sort(reverse = True)
		for index in peopleWhoDied:
			del currentPopulation[index]
			numDead += 1


		badEventDeaths = 0
		badEventsThisYear = []
		for badEvent in badEvents:
			if year == badEvent['year']:
				badEventDeaths += badEvent['death_count']
				newEventArray = [badEvent['title'], badEvent['death_count']]
				badEventsThisYear.append(newEventArray)

		for i in range(badEventDeaths):
			if len(currentPopulation) >0:
				personToDie = random.choice(currentPopulation)
				personToDieIndex = currentPopulation.index(personToDie)
				del currentPopulation[personToDieIndex]
				numDead += 1
			else:
				break

		year += 1
		for person in currentPopulation:
			person.updateAge()
			if person.getGender() == "female" and person.getSpouse() is not None :
				person.updateTimeSinceLastChild()

		with open(dataCollectionFilename, 'r') as f:
			data = json.load(f)

		if len(currentPopulation) > 0:
			data[str(year)] = {
				"events": badEventsThisYear if badEventsThisYear else [],
				"births": newPeople,
				"deaths": numDead,
				"population": len(currentPopulation)
			}
		else:
			print("Everyone Died")

		with open(dataCollectionFilename, 'w') as f:
			json.dump(data, f)

		print("Population: " + str(len(currentPopulation)))
		print("Dead this year: " + str(numDead))
		print()
		if currentPopulation == 0:
			print("Humanity went extinct!")
			break

def main():
	population = []

	# Initialize Adam and Eve
	adam = Person("male", 15)
	eve = Person("female", 15)

	population.append(adam)
	population.append(eve)

	startPopulation(population)

main()
