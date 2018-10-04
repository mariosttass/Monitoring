#!/usr/bin/python3
import sys
import subprocess
from termcolor import colored

#Configuration file
CONFIG_FILE ='service.conf'

#logfile = open("logfile.txt", "w")

class ServiceMonitor(object):

    def __init__(self, service):
        self.service = service
        #self.logfile = logfile

    def is_active(self):
        """Return True if service is running"""
        #systemctl status $1 --state=active
        cmd = 'systemctl status ' + self.service
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        stdout_list = proc.communicate()[0].decode('utf-8').split('\n')
        #print(stdout_list)
        for line in stdout_list:
            if 'Active:' in line:
                if '(running)' in line:
                    print(colored(self.service, "green"))
                    return True
                else:
                    print(colored(self.service, "red"))
                    return False
    
    def start(self):
        cmd = 'systemctl start '+ self.service #+ '> /dev/null'
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        proc.communicate()
    
    def stop(self):
        cmd = 'systemctl stop ' + self.service 
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        proc.communicate()
        #print(proc,self.service)

    def get_status(self):
        cmd = 'systemctl status ' + self.service
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0].decode('utf-8').split('\n')
        print(output)

    def get_version(self):
        cmd = 'dpkg -s ' + self.service 
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0].decode('utf-8').split('\n')
        for line in output:
            if 'Version' in line:
                print(colored(line, 'green'))
                return True
        
        return False



def menu():
    print(30 * "-" , "MENU" , 30 * "-")
    print("1. Check Which Processes are running")
    print("2. Start Process ")
    print("3. Stop Process")
    print("4. Start All Processes ")
    print("5. Stop All Processes")
    print("6. See full log")
    print("7. Check Version of the Package")
    print("8. Check Version of All Packages")
    print("9. Exit")
    print(67 * "-")


if __name__ == '__main__':
    # TODO: Show usage                                                 
    loop = True
    choice = 0
    while loop:
        menu()

        choice = input("Enter Your Choise [1-9]: ")
        choice = int(choice)
        if choice in range(1, 10):
            if choice == 1:
                for line in open(CONFIG_FILE,'r'):
                    monitor = ServiceMonitor(line)
                    monitor.is_active()
        
            elif choice == 2:
                process = input("Enter The Name of The Process: ")
                process = str(process)
                monitor = ServiceMonitor(process)
                monitor.start()
                monitor.is_active()
        
            elif choice == 3:
                process = input("Enter The Name of The Process: ")
                process = str(process)
                monitor = ServiceMonitor(process)
                monitor.stop()
                monitor.is_active()
        
            elif choice == 4:
                for pid in open(CONFIG_FILE, 'r'):
                    monitor = ServiceMonitor(pid)
                    monitor.start()
        
            elif choice == 5:
                for pid in open(CONFIG_FILE, 'r'):
                    monitor = ServiceMonitor(pid)
                    monitor.stop()
        
            elif choice == 6:
                print("You want to see Full Logs from All processes [Y/N]: ")
                answer = input()
                answer = str(answer)

                if answer in ['y', 'Y', 'yes', 'Yes', 'YES']: 
                    for pid in open(CONFIG_FILE, 'r'):
                        monitor = ServiceMonitor(pid)
                        monitor.get_status()
                elif answer in ['n', 'N', 'no', 'No', 'NO']:
                    pid = input("Please type the name of the process: ")
                    pid = str(pid)
                    monitor = ServiceMonitor(pid)
                    monitor.get_status()
        
            elif choice == 7:
                pkg = input("Please type the package: ")
                pkg = str(pkg)
                monitor = ServiceMonitor(pkg)
                monitor.get_version()
        
            elif choice == 8:
                for pkg in open(CONFIG_FILE, 'r'):
                    monitor = ServiceMonitor(pkg)
                    monitor.get_version()
        
            elif choice == 9:
                loop = False
        else:
            print("Exit")
            loop = False    
        
    