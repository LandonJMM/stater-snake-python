import subprocess


#go install github.com/BattlesnakeOfficial/rules/cli/battlesnake@latest

def installBattleSnake():
    try:
        ans = subprocess.check_output(["go", "install", "github.com/BattlesnakeOfficial/rules/cli/battlesnake@latest"], text=True)
        print(ans)

    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")


#TODO: install pip and psutil (and other python packages if needed)

main()