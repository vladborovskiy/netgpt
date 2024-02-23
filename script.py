import pip
import subprocess
def install():
    packages = ['telebot']
    for package in packages:
        pip.main(["install", package])

if __name__ == "__main__":
    try:
    	import telebot
    	subprocess.call(['python', 'main.py'])
    except Exception as e:
    	print('!Error in main.py: '+str(e))
    	install()
    	