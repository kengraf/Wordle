from collections import Counter
import sys

correct = [5]   # Single character values when a letter is properly placed
misplace = [5]  # Strings of letters that are in the wrong place
wrong = ""      # Letters that are not in word
answers = []    # List of possible solutions
wordlist = []   # List of words we can attempt
any = Counter()
position = [Counter(), Counter(), Counter(), Counter(), Counter()]

def reduce(matched=',,,,', misplaced=',,,,', wrong=''):
    matched = matched.split(',')
    misplaced = misplaced.split(',')
    
    # Use only words with matched letters
    for i in range( len(wordlist) -1, -1, -1):
        word = wordlist[i]
        for j in range(5):
            if matched[j] != '' and matched[j] != word[j]:
                wordlist.remove(word)
                break

    # Remove words with any wrong letter
    wrong_set = set(wrong)
    for i in range( len(wordlist) -1, -1, -1):
        if wrong_set.intersection(wordlist[i]) != set():
            wordlist.pop(i)

    # Remove words with letters in the wrong position
    for i in range( len(wordlist) -1, -1, -1):
        word = wordlist[i]
        for j in range(5):
            for k in range(len(misplaced[j])):
                if word[j] == misplaced[j][k]:
                    wordlist.pop(i)
                    break


def recommend():
    global any, position
    for word in wordlist:
        for i in range(5):
            letter = word[i]
            any[letter] += 1
            position[i][letter] += 1
    
    for i in range(5):
        print("#", i, position[i])      
    print("Total", any)
    
    max_value = 0
    for word in wordlist:
        value = 0
        for i in range(5):
            value += position[i][word[i]]
        if max_value < value:
            max_value = value
            print(word, value)

def lambda_handler(event, context):
    id = event['detail']['instance-id']
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(id)
    logger.info('instance-id='+id)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'DNS':
            route53update(ec2instance.public_ip_address,tags["Value"]) 
    logger.info('DNS='+tags["Value"])
    return ''

def main():
    # Commandline only used for debugging
    # Required command format: python suggest.py -c ",,,," -m ",,,," -w ""
#    correct = sys.argv[2]
#    misplaced = sys.argv[4]
#    wrong = sys.argv[6]
    # TODO make this a URL lookup
    global wordlist
    with open(r"solution_words", 'r') as fp:
        wordlist = fp.readlines()
        print('Total words:', len(wordlist))
    reduce(',,,,',',,,,','')
    recommend()
    reduce(',,,,',',,a,r,','bs')
    recommend()
    reduce('r,,,a,',',a,a,r,','ebsd')
    recommend()
    
if __name__ == "__main__":
    main()