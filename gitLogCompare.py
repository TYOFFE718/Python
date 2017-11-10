import subprocess

def main():
    '''
    Here's where the whole thing starts.
    '''
    #Edit this constant to change the file name in the git log command.
    FILE_NAME = 'market_rules_cs_pub.reader.xml'

    #Do the git describe command to get the tag names.
    gitDescribe = 'git describe --tags `git rev-list --tags --max-count=2`'
    print ('Invoking: {0}'.format(gitDescribe))
    p1 = subprocess.Popen(gitDescribe, shell=True, stdout=subprocess.PIPE)
    output = p1.stdout.read()

    #Get the first 2 tags from the output.
    parsedOutput = output.split('\n')
    tag1 = parsedOutput[0]
    tag2 = parsedOutput[1]
    
    print('First revision: {0}'.format(tag1))
    print('Second revision: {0}'.format(tag2)) 
    #Do the git log command for the revision comparison.
    gitLog = 'git log {1}..{0} --pretty=format:"%an %h %ad %d %s" --date=short --topo-order --no-merges {2}'.format(tag1, tag2, FILE_NAME)
    print('Invoking: {0}'.format(gitLog))
    p2 = subprocess.Popen(gitLog, shell=True, stdout=subprocess.PIPE)
    output = p2.stdout.read()
    print(output)

if __name__ == "__main__":
    main()
