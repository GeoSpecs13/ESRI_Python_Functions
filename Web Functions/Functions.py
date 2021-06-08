'''
@Creator Andrew Sauerwin
In this file is a list of functions that can be used to leverage automation tasks within ArcGIS Portal and even ArcGIS Online.
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

#Global Variables for functions
portalUrl = ""
portalUser = ""
portalPass = ""
gis = GIS(portalUrl, portalUser, portalPass)

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

# Variable examples for add_Users
userDoc = r''
group_query = "<insert portal gorup name>"

def add_Users(userDoc, group_query):
    '''This function was designed to add users from a CSV via usernames to ArcGIS Portal.
    Usernames may differ via Active Directory accounts which need an @DOMAIN (whatever your domain is)
    Anyone seeking to use this function should first import the appropriate python modules. 
    
    Those are:
    1. csv (will need to use: import csv)
    2. arcgis (will need to use: from arcgis.gis import GIS)
    3. os (will use import os)
    
    **Parameters required for this function are:
    1. userDoc which is a variable pointing at a CSV document with a list of usernames in it.
    2. group_query = a variable passes to represent the Portal Groups to be used to add users.
    
    **IMPORTANT: Before using this function, the portal environment being used needs to be invoked.
    '''
    #Setting Count to iterate the number of users added
    count = 0
    #List used to stage users from CSV.
    username = []
    
    #Reads the CSV file containing the User names, it is assumed that the csv is only using one row with values in it.
    with open(userDoc, newline='') as csvfile:
         users_csv = csv.reader(csvfile)
         #loop through and append users from CSV to list
         for row in users_csv:
             username.append(row)

    # count is set to iterate in the loop
    count = count + 1
    
    print("Getting Portal Group, by setting the query.")
    portal_groups = gis.groups.search(group_query)

    print("Searching groups based on the query.")
    for group in portal_groups:
        print('Group name: ' + str(group.title))
        print('List of group members: ' + str(group.get_members()) + "\n")
        
        for user in username:
            print('\tAdding {0} to group, number of users added so far {1}.'.format(group.add_users(user), count))

    print("Process complete...")
    
    return 0


#Variable examples for portal_Flex
role = 'role:"<Insert user>"' #is the typs of user you want to query by. EX: 'role:"org_user"'
max_user_count = #assign number value
doc = r""
level_change = '' #Assign role level numberic value

def portal_Flex(role, max_user_count, doc, level_change):
    '''This function has been developed to be flexible. A developer should be able to point to any
    administrative operation in the User class of the arcgis.gis module. 
    See the API reference documentation for more information.
    
    Python Modules:
    1. csv (will need to use: import csv)
    2. arcgis (will need to use: from arcgis.gis import GIS)
    3. os (will use import os)
    
    ***Parameters:
    1. role is the assignment you want to search on for the groups of users you are interested in. 
        See variable example for reference.
    2. max_user_count is set to the number of users you want to identify as the maximum. This could be 
    everyone in the organizations portal environment.
    3. doc is set to the csv or excel spreadsheet containing the information of interest. User IDs in this case.
    these contents will also be appended to a list in the script to be worked on later in the code.
    4. level_change is set to identify the users license level in Portal. As of right now, this can either be
        a '1' or '2'.
    
    **IMPORTANT: Before using this function, the portal environment being used needs to be invoked.    
    '''
    
    # Setting the environment to search for user acocunts in the portal environment    
    print("Object set for searching on User Accounts.")        
    accounts = gis.users.search(query=role, max_users=max_user_count)

    #Count variable
    count = 0

    # Lists
    update_List = []

    #Reads the CSV file containing the User names, it is assumed that the csv is only using one row with values in it.
    with open(doc, newline='') as csvfile:
         users_csv = csv.reader(csvfile)
         #loop through and append users from CSV to list
         for row in users_csv:
             update_List.append(row)

    # Looping through each user account
    for account in accounts:
        # Query Portal for specific user accounts
        user = gis.users.get("{}".format(account.username))

        # Disregard any generic named accounts
        if account.username.startswith("esri"): 
            print("Passing this user: {0}".format(user.username))
        elif account.username.startswith("system_"):
            print("Passing this user: {0}".format(user.username))
        elif account.username.endswith("_boundaries"):
            print("Passing this user: {0}".format(user.username))
        elif account.username.endswith("_livingatlas"):
            print("Passing this user: {0}".format(user.username))
        elif account.username.endswith("_nav"):
            print("Passing this user: {0}".format(user.username))
        else:
            print(user.fullName)
            print(user.username)

            for item in update_List:
                if item == user.username:
                    count = count + 1
                    user.update_level(level_change)
                    print("UserLever changed for {0} as it matched {1} values updated so far = {2}".format(user.username, item, count))

    print("Process complete...")
    
    return 0
