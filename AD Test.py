import _pyio
import active_directory
import csv

class WriteUser:
    def __init__(self):
        self.cn = 0
        self.username = 0
        self.ad = 0
        self.email = 0
        self.VPN = 0
        self.token = 0
        self.webex = 0
        self.laptop = 0

    def reset(self):
        dict = vars(self)
        for i in dict.keys():
            dict[i]=0

with open ('Workspace.csv') as original:
    with open('Workspace_Results.csv', 'w', newline='') as output:
      fieldnames = ['Name', 'AD Account', 'Email', 'Laptop', 'Active Token', 'WebEx']
      writer = csv.DictWriter(output, fieldnames=fieldnames)
      writer.writeheader()
      queryname = csv.DictReader(original)
      print("Now running AD scan")
      for row in queryname:
          print('.', end="")
          inst = WriteUser()
          inst.webex = "No"
          inst.VPN = "No"
          inst.ad = "No"
          inst.token= 0
          user = active_directory.find_user (row["username"])
          inst.cn = row['username']
          if (user is not None):
            inst.ad = "Yes"
            user2 = active_directory.find_user (user.sAMAccountName)
            inst.email = user2.mail
            inst.username = user.sAMAccountName
            for group in user2.memberOf:
              if (group.cn =="WebEx Users"):
                 inst.webex = "Yes"          
              if (group.cn == "VPN-Technical" or group.cn == "VPN-Default" or group.cn =="VPN-Development"):
                 with open('tokens.csv') as token:
                     search = csv.reader(token)
                     for row in search:
                         if row[0].lower() == inst.username.lower():
                             inst.token = "Yes"
                             break
            with open("workstations.csv") as workstations:
                laptopSearch = csv.reader(workstations)
                for row in laptopSearch:
                    if row[1].lower() == inst.username.lower() and row[0].startswith("L"):
                        inst.laptop = row[0]
                        break
            writer.writerow({'Name': inst.cn, 'AD Account': inst.ad, 'Email': inst.email, 'Laptop': inst.laptop, 'Active Token': inst.token, 'WebEx': inst.webex})
          else:
            writer.writerow({'Name': row["username"], 'AD Account': inst.ad})    
          inst.reset()
print('\nQuery Complete')
original.close()
output.close()
token.close()
workstations.close()

