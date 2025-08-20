import subprocess
import signal
import sys
import psutil
import argparse
import xml.etree.ElementTree as ET 
import time
#TODO: make sure all imports are being used and are nessisary

#TODO: make sure all these work on different OS
#TODO: move the team name to a different location

def cleanup(signum, frame):
        print("Terminating child process...")
        parent = psutil.Process()

        for child in parent.children(recursive=True):
            print(f"Killed process with PID: {child.pid}") #TODO: is this really needed
            child.terminate()
        
        sys.exit(0) # Exit this proccess as everything is closed properly


def loadBattleFromXML(xmlPath, battleID):  #TODO: might need to make this a bit easier to read
    tree = ET.parse(xmlPath)
    root = tree.getroot()

    # Search for the battle with the matching ID
    found = False
    parsedInfo = {}
    for battle in tree.findall('battle'): #TODO: board args
        battle_id = battle.get('id')

        if (battle.get('id') != battleID): 
            continue

        # At this point we have found the battle with the correct ID
        found = True

        # Parse all the snakes in this battle
        snakes = []
        count = 0
        for snake in battle.findall('./snake'):
            name = snake.findtext('name')
            try:
                url = snake.findtext('url')
                snakes.append({'name': name, 'url': url})
            except: #TODO: no support for this yet
                port = 8000 + count
                count += 1
                file = snake.findtext('file')
                snakes.append({'name': name, 'port': port, 'file': file})

        parsedInfo['snakes'] = snakes

        # Parse all the board setting in this battle
        #TODO: finish this

        break

    if (found):
        return parsedInfo
    else:
        print(f"Could not find battle with ID: {battleID}")
        sys.exit(-1)


def generateBattleArguments(parsedInfo):
    args = ['battlesnake', 'play', '-W', '11', '-H', '11','-g', 'solo', '--browser'] #TODO: update to not use solo

    # Generate the commands for the snakes
    snakes = parsedInfo['snakes']
    for snake in snakes:
        args.append('--name')
        args.append(snake['name'])

        args.append('--url')
        args.append(snake['url'])
    
    return args


def startSnakeServer(): #TODO: extend to work with already running servers
    proc = subprocess.Popen(["py", "main.py"]) #TODO: people are going to change the name of this file
    print(f"Started process with PID: {proc.pid}")
    time.sleep(2) # needed to allow for the snake server to fully starup before the battle starts


def runBattle(args):
    proc = subprocess.Popen(args) #TODO: needs to be adjustable so people can run more than one snake
    print(f"Started process with PID: {proc.pid}")

    proc.wait()


def main():
    xmlFile = "battle.xml"

    # Parse the inputed battle ID
    try:
        parser = argparse.ArgumentParser(
            description="Run a Battlesnake battle by ID from the XML file.",
            exit_on_error=False
            )
        parser.add_argument("battleID", type=str, help="ID of the battle to run")
        args = parser.parse_args()
    except:
        print("Error: Missing command line argument <battleID>. Example \"$py .\\startBattle ExampleID\"\n")
        sys.exit(-1)

    # Parse the command arguments from the battle in the xml file
    parsedInfo = loadBattleFromXML(xmlFile, args.battleID)
    commandArgs = generateBattleArguments(parsedInfo)

    # run the cleanup function when the termination signal is recived
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    startSnakeServer()
    runBattle(commandArgs)

if __name__ == "__main__":
    main()