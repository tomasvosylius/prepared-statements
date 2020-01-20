# ps.py

class PreparedStatement():

    def __init__(self, query):
        self.query      = query
        self.prepared   = query
        self.args       = {} # placeholders and values

    def __repr__(self):
        return self.prepared

    def SetString(self, position, string):
        self.args.update( {position : self.PrepareValue(string)} )
        return self.args

    def SetInt(self, position, value):
        if type(value) is int:
            self.args.update( {position : int(value)} )
        else:
            raise TypeError("SetInt only accepts integers")
        
    
    def SetFloat(self, position, value):
        if type(value) is float:
            self.args.update( {position : float(value)} )
        else:
            raise TypeError("SetFloat only accepts floats")

    def PrepareValue(self, value):
        value = value.replace("\'", "&quot;")
        value = value.replace("\"", "&quot;")
        return value

    def ChangePlaceholders(self):

        """
        @TODO: check whether placeholder (?) has single quotes around it (regex) and only then append if needed
        """

        new_query = self.prepared
        for key, value in self.args.items():
            new_query = new_query.replace("?", "\'" + str(value) + "\'", 1)

        return new_query

    def Execute(self):
        self.prepared = self.ChangePlaceholders()  
        print("Executing: \n" + self.prepared)
        return self.prepared

# manual test
if __name__ == "__main__":
    ps = PreparedStatement("SELECT * FROM `foo` WHERE Username = ?, Password = ?, Email = ?, Rate = ?, Level = ?")

    # set arguments
    ps.SetString(1, "'OR ANY")
    ps.SetString(2, "This is not a SQL injection\" OR \"\"=\"\" OR 1=1")
    ps.SetString(3, "This is no't a nice statement;-- DROP TABLE `foo`")
    ps.SetFloat(4, 5.0)
    ps.SetInt(5, 5)

    # execute query
    ps.Execute()
