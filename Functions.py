'''
@Creator Andrew Sauerwin
In this script is a list of functions that can be used to leverage automation tasks within ArcGIS Portal and even ArcGIS Online.
The idea is that this set of functions can be leveraged as imports for other scripts. Simply Place the library in the Python home folder.
Then import from the library as needed.

Expect updates over time.
'''
#
# Import the modules needed for the associated functions below. 
#
import os, time
from arcgis.gis import GIS
from os import path
from pandas import DataFrame


def portalUserReport(url, portalUser,portalPass, csvLog):
    '''
    Generates a log of detailed information about a Portal User's details. 
    The primary use was to obtain the user's last login details to see when/or if a user has accessed a portal environment. 
    
    The script will log the following:
    1. Full Name
    2. Username
    3. Email
    4. User Access
    5. Role
    6. Level (whether they are a level 1 or 2 user)
    7. Users Associated Groups #Is modified to not list right now but can if the client want's this information
    8. Last Modified Date
    9. User Created Date
    10. User Last Active Date

    Additional information about the arcgis.gis module can be found at:
    https://developers.arcgis.com/python/api-reference/arcgis.gis.toc.html

    More information about Pandas Data Frames can be found at:
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
    '''
    #
    # Set Variables and notice the csvLong variable is specific to CSV files.
    #
    csvLog = r""
    url = ""
    portalUser =  ""
    portalPass = ""
    gis = GIS(url, portalUser, portalPass)

    '''
    # Setting the environment to search for the groups inside the portal environment
    groups = gis.groups.search()

    # Can be used to find users per a portal group
    for group in groups:
        print(group)'''

    # Setting the environment to search for user acocunts in the portal environment    
    print("Object set for searching on User Accounts.")        
    accounts = gis.users.search()

    # Looping through each user account to gather User detail information
    print("Gathering user report informaiton...")
    
    # If CSV log file exists, delete it
    if path.exists(csvLog) == True:
        print("{} file has been deleted.".format(csvLog))
        os.remove(csvLog)
    else:
        pass
    
    # Lists
    FullName = []
    UserName = []
    Email = []
    Access = []
    Role = []
    Level = []
    Groups = []
    ModifiedDate = []
    CreatedDate = []
    LastActiveDate = []
    NotActive = []

    # Looping through each user account to gather User detail information
    for account in accounts:
        # Setting this object allows us to call specific information about the user listed below
        user = gis.users.get("{}".format(account.username))

        if account.username.startswith("esri"): # Disregard any generic named accounts such as those that do not seem user specific like esri_boundaries, etc... 
            pass
        elif account.username.startswith("system_"): # Disregard any system related IDs such as "system_publisher" otherwise the parameter is not valid to pass for the last login.
            pass
        else:
            print("\tFull Name: {}".format(user.fullName))
            FullName.append(user.fullName)

            print("\tUsername: {}".format(user.username))
            UserName.append("Username: {0}".format(user.username))

            print("\tEmail: {}".format(user.email))
            Email.append("Email: {0}".format(user.email))

            print("\tUsers Access: {}".format(user.access))
            Access.append("Access: {0}".format(user.access))

            print("\tRole: {}".format(user.role))
            Role.append("Role: {0}".format(user.role))

            print("\tLevel: {}".format(user.level))
            Level.append("Level: {0}".format(user.level))

            print("\tAssociated Portal Groups: {}".format(user.groups))
            Groups.append("Assigned: {0}".format(user.groups))

            modDate = time.localtime(user.modified/1000)
            print("\tLast modified: {}/{}/{}".format(modDate[0], modDate[1], modDate[2]))
            ModifiedDate.append("{}/{}/{}".format(modDate[0], modDate[1], modDate[2]))

            created = time.localtime(user.created/1000)
            print("\tUser created: {}/{}/{}".format(created[0], created[1], created[2]))
            CreatedDate.append("{}/{}/{}".format(created[0], created[1], created[2]))

            if user.lastLogin > 0:
                last_accessed = time.localtime(user.lastLogin/1000)
                print("\tLast active: {}/{}/{}\n".format(last_accessed[0], last_accessed[1], last_accessed[2]))
                LastActiveDate.append("{}/{}/{}".format(last_accessed[0], last_accessed[1], last_accessed[2]))

                ## Adding code to work around the logging issue for Array lengths when appending to CSV.
                NotActive.append("Not applicable")
            else:
                print("\t***{} Has not yet logged in\n".format(account.username))
                NotActive.append("{} Has not yet logged in".format(account.username))
                LastActiveDate.append("Not applicable - Check other columns for details")

    
    '''This section of code can be used to check the length of each list.
    This will let the developer know which arrary may not match the when generating the CSV log.'''
    '''print("FullName length is: {0}".format(len(FullName)))
    print("UserName length is: {0}".format(len(UserName)))
    print("Email length is: {0}".format(len(Email)))
    print("Access length is: {0}".format(len(Access)))
    print("Role length is: {0}".format(len(Role)))
    print("Level length is: {0}".format(len(Level)))
    print("ModifiedDate length is: {0}".format(len(ModifiedDate)))
    print("CreatedDate length is: {0}".format(len(CreatedDate)))
    print("LastActiveDate length is: {0}".format(len(LastActiveDate)))
    print("NotActive length is: {0}".format(len(NotActive)))
    print("Groups length is: {0}".format(len(Groups)))'''

    print("...Setting up the User Info CSV log structure.")
    Header = {'Full Name': FullName, 
                'Username': UserName, 
                'Email': Email, 
                'Access': Access, 
                'Role': Role, 
                'Level': Level,
                'Portal Groups': Groups, 
                'Modified Date': ModifiedDate, 
                'Created Date': CreatedDate, 
                'Last Active Date': LastActiveDate, 
                'Inactive': NotActive
                }

    try:
        print("...Setting up Pandas Data Frame to log the Portal User details to the CSV File.")
        df = DataFrame(Header, columns= ['Full Name', 
                                            'Username', 
                                            'Email', 
                                            'Access', 
                                            'Role', 
                                            'Level',
                                            'Portal Groups', 
                                            'Modified Date', 
                                            'Created Date', 
                                            'Last Active Date', 
                                            'Inactive'])
        df.from_dict(Header, orient='index')
        df.transpose()

        print("...Creating the Users Detail CSV log.")
        df.to_csv (csvLog, index=None, header=True)
    except Exception as error_e:
        print("Exception raised at CSV generation: {0}...".format(error_e))
    
    print("...Process Complete")

    return 0

