from python_sharp import *

class Point:
    def __init__(self,x,y):
        self.x =x
        self.y =y 

    @property
    def X(self):
        return self.x
    
    @property
    def Y(self):
        return self.y

    def __sub__(self,value):
        if isinstance(value, Point):
            return Vector(self.x - value.x, self.y - value.y)
        return NotImplemented

    def __str__(self):
        return "(%d, %d)" % (self.X,self.Y)
    
class Vector:
    def __init__(self,i,j):
        self.i =i
        self.j =j 

    @property
    def I(self):
        return self.i
    
    @property
    def J(self):
        return self.j 

    def __str__(self):
        return "%d i, %d j" % (self.I,self.J)



class LocationChangedEventArgs(EventArgs):
    
    def __init__(self,delta:Vector):
        super().__init__()
        self.delta = delta

    @property
    def Delta(self)->Vector:
        return self.delta

class LocationChangingEventArgs(CancellableEventArg):
    def __init__(self,location:Point):
        super().__init__()
        self.location = location

    @property
    def Location(self)->Vector:
        return self.location




class Person:
    def __init__(self,name):
        self.name = name
        self.location = Point(0,0)
        self.nameChangedcalbacks = Delegate()
        self.locationChangedcallbacks = Delegate()
        self.locationChangingcallbacks = Delegate()
        

# region Properties


    @property
    def Name(self): 
        return self.name
               
    @Name.setter 
    def Name(self,value:str):
        self.name = value
        self._OnNameChanged(EventArgs()) 

     
    @property
    def Location(self):
        return self.location
    
    @Location.setter
    def Location(self,value:Point)->None:
        
        locationEventArgs = LocationChangingEventArgs(value)
        self._OnLocationChanging(locationEventArgs)
        
        if(not locationEventArgs.Cancel):
            previous = self.location 
            self.location = value
            self._OnLocationChanged(LocationChangedEventArgs(self.location - previous))

# endregion

# region  Methods
   
    def _OnNameChanged(self,e:EventArgs)->None:
        self.nameChangedcalbacks(self,e)
    
    def _OnLocationChanging(self,e:LocationChangingEventArgs)->None:
        self.locationChangingcallbacks(self,e)

    def _OnLocationChanged(self,e:LocationChangedEventArgs)->None:
        self.locationChangedcallbacks(self,e)          
        
# endregion

# region Events
    
    @event
    def NameChanged(self,value: Callable[[object, EventArgs], None] ):
        self.nameChangedcalbacks += value 
        
    @NameChanged.remove
    def NameChanged(self,value: Callable[[object, EventArgs], None]):
       self.nameChangedcalbacks -= value


    @event
    def LocationChanging(self,value:Callable[[object, LocationChangedEventArgs], None]):
        self.locationChangingcallbacks += value
    
    @LocationChanging.remove
    def LocationChanging(self,value:Callable[[object, LocationChangedEventArgs], None]):
       self.locationChangingcallbacks -= value
                     
    
    @event      
    def LocationChanged(self,value:Callable[[object, LocationChangingEventArgs], None]):
        self.locationChangedcallbacks += value
    
    @LocationChanged.remove
    def LocationChanged(self,value:Callable[[object, LocationChangingEventArgs], None]):
       self.locationChangedcallbacks -= value  

    
# endregion


    

#use of it

p = Person("Carlos")

def callback_function(sender:object,e:EventArgs):
    print("callback sender %s, Eventargs: %s" % (sender,e))
    print("Person name %s" % sender.Name)


class School:
    def __init__(self):
        pass

    def persona_nameChanged(self,sender:object,e:EventArgs)->None:
        print("School just signed up to %s"% sender.Name)

    def persona_locationchanged(self,sender:object,e:LocationChangedEventArgs)->None:
        print("Person %s change its localitation by %s units" % (sender.Name,e.Delta))

    def persona_locationchanging(self,sender:object,e:LocationChangingEventArgs)->None:
        if e.Location.X > 100:
            print("Person %s can't be changed that far, 'X can't be greater than 100. value: %d'" % (sender.Name,e.Location.X))
            e.Cancel = True

e = School()
p.NameChanged += e.persona_nameChanged 
p.NameChanged += callback_function
p.Name = "Susa"
p.NameChanged -= callback_function
p.Name = "Nos"
p.Location = Point(5,5)
p.LocationChanged += e.persona_locationchanged
p.Location = Point(15,15)
p.LocationChanged -= e.persona_locationchanged 
p.Location = Point(30,30)
p.LocationChanging += e.persona_locationchanging

p.Location = Point(13,13)
p.Location = Point(115,2)

print("%s location at %s" %(p.Name, p.Location))

########################################################

#Asigning a Delegate instead of passing a function/method directly (Due Delegates are callables) to an event, using polimorfism and pasing a function with parameter EventArg to a LocationEventArg event
d = Delegate(callback_function) 
p.LocationChanged += d
p.Name = "Chisus"
######################################################################################################################################
