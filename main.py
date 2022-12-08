import orjson, csv, os, re, unicodedata, string

HEADER = ['word', 'first-letter', 'length', 'grammatical-class', 'gender']

# _______________________________________________________________________

def getDatafromJSON(file):
  f = open(file, 'r')
  return orjson.loads(f.read())

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

rootPath = './vocabulaire-francais'
output = []
letters = {}

for letter in string.ascii_lowercase:
  letters[letter] = 0

for filename in os.listdir(rootPath):
  file = os.path.join(rootPath, filename)

  if not os.path.isfile(file): continue

  [grammaticalClass, gender] = re.split(',',re.sub(".json", "", filename))

  if re.search(' ', gender):
    [gender, null] = re.split(' ', gender)

  data = getDatafromJSON(file)
  for word in data:
    wordFirstLetter = remove_accents(word[0])
    wordlength = len(word)
    output.append([word, wordFirstLetter, wordlength, grammaticalClass, gender])

    for letter in word:
      if letter in string.ascii_lowercase:
        unaccentedLetter = remove_accents(letter)
        letters[unaccentedLetter] += 1
      

with open('distribution.csv', 'w') as distribution:
  writer = csv.writer(distribution)
  writer.writerow(['letter', 'occurences'])
  for letter in letters:
    writer.writerow([letter, letters[letter]])

# print(letters)
# with open('output.csv', 'w') as csvFile:
#   writer = csv.writer(csvFile)
#   writer.writerow(HEADER)
#   writer.writerows(output)