import random
import string


def generate_id(length):
	return ''.join(
		random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation, k=length))


class Person:
	random.seed()
	def __init__(self, gender=random.choice(["male", "female"]), age=0):
		self.personID = generate_id(12)
		self.gender = gender
		self.age = age
		self.spouse = None
		self.ancestors = []
		self.children = []
		self.siblings = []
		self.isAlive = True
		self.wasInbred = False
		self.inbreedHistory = []
		self.willInbreed = False
		self.numChildren = 0

		# This only applies if the person is a woman
		self.timeSinceLastChild = None
		self.doneHavingChildren = False

	def updateGender(self, gender):
		self.gender = gender

	def updateAge(self):
		self.age += 1

	def updateSpouse(self, spouseID):
		self.spouse = spouseID

	def updateAncestors(self, newAncestor):
		self.ancestors.append(newAncestor)

	def removeAncestor(self, index):
		self.ancestors.pop(index)

	def updateChildren(self, newChild):
		self.children.append(newChild)

	def updateSiblings(self, newSibling):
		self.siblings.append(newSibling)

	def updateDeath(self):
		self.isAlive = False

	def updateIsInbred(self):
		self.wasInbred = True

	def updateNumChildren(self):
		self.numChildren += 1

	def updateWillInbreed(self, yesOrNo):
		self.willInbreed = yesOrNo

	def updateInbreedHistory(self, newHistory):
		self.inbreedHistory.append(newHistory)

	def updateTimeSinceLastChild(self):
		if self.timeSinceLastChild is not None:
			self.timeSinceLastChild += 1

	def resetTimeSinceLastChild(self):
		self.timeSinceLastChild = 0

	def updateDoneHavingChildren(self):
		self.doneHavingChildren = True

	def getPersonID(self):
		return self.personID

	def getGender(self):
		return self.gender

	def getAge(self):
		return self.age

	def getSpouse(self):
		return self.spouse

	def getAncestors(self):
		return self.ancestors

	def getChildren(self):
		return self.children

	def getSiblings(self):
		return self.siblings

	def getIsAlive(self):
		return self.isAlive

	def getWasInbred(self):
		return self.wasInbred

	def getWillInbreed(self):
		return self.willInbreed

	def getTimeSinceLastChild(self):
		return self.timeSinceLastChild

	def getDoneHavingChildren(self):
		return self.doneHavingChildren

	def getInbreedHistory(self):
		return self.inbreedHistory

	def printAll(self):
		print("PersonID: " + str(self.personID))
		print("Gender: " + str(self.gender))
		print("Age: " + str(self.age))
		print("Spouse: " + str(self.spouse))
		print("Ancestors: " + str(self.ancestors))
		print("Children: " + str(self.children))
		print("IsAlive?: " + str(self.isAlive))
