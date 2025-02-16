#!/usr/bin/python3
import os
import sys
import subprocess
import argparse
import shutil

def run_command(cmd):
    print("{}".format(cmd))
    print((subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)).decode("utf-8"))

def run_install(packages, method):
    if method == "sudo apt-get":
        method = "sudo apt-get -y"
    install_string = "{} install {}".format(method, packages)
    run_command(install_string)

def replace_kivy_config(username):
    kivy_config_path = "/home/{}/.kivy/config.ini".format(username)
    mimic_config_path = "/home/{}/Mimic/Pi/config.ini".format(username)
    print("\nUpdating the Kivy config.ini file.")
    shutil.copyfile(mimic_config_path, kivy_config_path)

def main():
    parser = argparse.ArgumentParser(description='ISS Mimic initial Pi setup tool.')
    parser.add_argument(
            '--skip_kivy', action='store_true',
            help='Skip installing the Kivy package and replacing the Kivy config file.',
            default=False)
    
    username = os.getlogin()
    args = parser.parse_args()

    #Mimic Install Steps

    run_command("sudo apt-get update")
    run_command("sudo apt-get -y upgrade")
    run_command("sudo apt-get -y autoremove")
    run_install("rdate","sudo apt-get")
    run_install("vim", "sudo apt-get") #test editor
    run_install("sqlite3", "sudo apt-get") #telemetry database
    run_install("python3-sdl2", "sudo apt-get") #required for kivy window
    run_install("python3-mpltoolkits.basemap", "sudo apt-get") #required for nightshade
    run_command("pip install -U numpy") #update numpy
    run_install("libatlas-base-dev", "sudo apt-get") #fix numpy issue
    run_install("ephem pytz matplotlib pyudev lightstreamer-client-lib", "python -m pip") #python libs used by Mimic

    if not args.skip_kivy:
        print("\nInstalling Kivy requirements and package.")
        run_install("kivy", "python -m pip")
        #run_install("'kivy[base,media]'", "python -m pip") # might need this kivy install if we do audio/video stuff but it might be outdated?
        run_command("python -c 'import kivy'") # run kivy init to create the config.ini file
        print("Replacing Kivy config file")
        replace_kivy_config(username)
    else:
        print("\nSkipping Kivy setup.")

if __name__ == '__main__':
    main()
