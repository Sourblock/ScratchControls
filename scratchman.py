from enum import unique
import scratchconnect

class ScratchMan :
    def __init__(self):
        self.user = None
    
    def login(self, username, password) :
        try :
            self.user = scratchconnect.ScratchConnect(username, password)
            return True
        except :
            return False

    def logout(self) :
        self.user =None

    def createNewVar(self, project_id, name, value) :
        project = self.user.connect_project(project_id=project_id)
        variables = project.connect_cloud_variables()
        set = variables.set_cloud_variable(variable_name=name, value=value)
        return set

    def getMessageCount(self) :
        return self.user.messages_count()

    def getFollowersCount(self) :
        return self.user.followers_count()

    def getFollowingCount(self):
        return self.user.following_count()

    def getLoveCount(self):
        return self.user.total_loves_count()

    def getViewsCount(self):
        return self.user.total_views()

    def getFavoritesCount(self):
        return self.user.total_favourites_count()

    def setCloudVar(self, project_id, name, value):
        project = self.user.connect_project(project_id=project_id)
        variables = project.connect_cloud_variables()
        set = variables.set_cloud_variable(variable_name=name, value=value)
        return set

    def getAllVars(self, project_id) :
        unique_var_names = set()
        project = self.user.connect_project(project_id=project_id)
        variables = project.connect_cloud_variables()
        vars = variables.get_variable_data()
        for var in vars :
            unique_var_names.add(var["Name"])
        return list(unique_var_names)

    def getVarValue(self, project_id, var_name) :
        project = self.user.connect_project(project_id=project_id)
        variables = project.connect_cloud_variables()
        var = variables.get_cloud_variable_value(var_name)
        return var
        

    def getAllProjects(self):
        projects = {}
        projects_data = self.user.projects(all=True)[0]

        for project in projects_data :
            projects[project['title']] = project['id']

        return projects

    def getBio(self) :
        return self.user.bio()

    def getStatus(self) :
        return self.user.status()

    def getCountry(self):
        return self.user.country()

    def getJoinDate(self):
        return self.getJoinDate()
