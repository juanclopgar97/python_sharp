from python_sharp import *



class MovedEventArgs(EventArgs):
    
    _delta:int

    def __init__(self,delta:int)->None:
        super().__init__()
        self._delta = delta

    @property
    def Delta(self)->int:
        return self._delta


class LocationChangingEventArgs(CancellableEventArgs):
    
    _location:int

    def __init__(self,location:int)->None:
        super().__init__()
        self._location = location

    @property
    def Location(self)->int:
        return self._location




class Person:

    _instance_created:int = 0
    _personCreatedcallbacks:Delegate = Delegate()

    _name:str
    _alive:bool
    _location:int
    _nameChangedcalbacks:Delegate
    _movedcallbacks:Delegate
    _locationChangingcallbacks:Delegate
    _diedcallbacks:Delegate

    def __init__(self,name:str)->None:
        self._name = name
        self._alive = True
        self._location = 0
        self._nameChangedcalbacks = Delegate()
        self._movedcallbacks = Delegate()
        self._locationChangingcallbacks = Delegate()
        self._diedcallbacks = Delegate()
        Person._OnPersonCreated(EventArgs())
        
# region Properties

    @property
    def Name(self)->str: 
        return self._name
               
    @Name.setter 
    def Name(self,value:str)->None:
        self._name = value
        self._OnNameChanged(EventArgs()) 

     
    @property
    def Alive(self)->bool:
        return self._alive
    

    @property
    def Location(self)->int:
        return self._location
    
    @Location.setter
    def Location(self,value:int)->None:
        
        locationEventArgs = LocationChangingEventArgs(value)
        self._OnLocationChanging(locationEventArgs)
        
        if(not locationEventArgs.Cancel):
            previous = self.Location 
            self._location = value
            self._OnMoved(MovedEventArgs(self.Location - previous))


    @staticmethod
    def get_InstanceCreated()->int:
        return Person._instance_created
    
    @staticmethod
    def _set_InstanceCreated(value:int)->None:
        Person._instance_created = value

# endregion

# region  Methods
   
    def _OnNameChanged(self,e:EventArgs)->None:
        self._nameChangedcalbacks(self,e)
    
    def _OnLocationChanging(self,e:LocationChangingEventArgs)->None:
        self._locationChangingcallbacks(self,e)

    def _OnMoved(self,e:MovedEventArgs)->None:
        self._movedcallbacks(self,e)          
        
    def _OnDied(self,e:EventArgs)->None:
        self._diedcallbacks(self,e)   

    def Move(self,distance:int)->None:
        self.Location += distance

    @staticmethod
    def _OnPersonCreated(e:EventArgs)->None:
        Person._set_InstanceCreated(Person.get_InstanceCreated())
        Person._personCreatedcallbacks(None,e)

    def Kill(self)->None:
        self._alive = False
        self._OnDied(EventArgs())

# endregion

# region Events
    
    @event  #Simplest event, just notify something happens, no provide extra information about the event (like why,how,when), no recolection of information from suscribers
    def NameChanged(self,value: Callable[[object, EventArgs], None])->None:
        self._nameChangedcalbacks += value 
        
    @NameChanged.remove
    def NameChanged(self,value: Callable[[object, EventArgs], None])->None:
       self._nameChangedcalbacks -= value


    @event  #event with custom EventArgs, notify something happens and provides extra information (like why,how,when),  no recolection of information from suscribers
    def Moved(self,value:Callable[[object, MovedEventArgs], None])->None:
        self._movedcallbacks += value
    
    @Moved.remove
    def Moved(self,value:Callable[[object, MovedEventArgs], None])->None:
       self._movedcallbacks -= value  


    @event  #event with custom EventArgs, notify something happens provides extra information (like why,how,when), and it is capable of recolect info from its suscribers (this case implemeted as prevent)
    def LocationChanging(self,value:Callable[[object, LocationChangingEventArgs], None])->None:
        self._locationChangingcallbacks += value
    
    @LocationChanging.remove
    def LocationChanging(self,value:Callable[[object, LocationChangingEventArgs], None])->None:
       self._locationChangingcallbacks -= value


    @event
    def Died(self,value:Callable[[object, EventArgs], None])->None:
        self._diedcallbacks += value
    
    @Died.remove
    def Died(self,value:Callable[[object, EventArgs], None])->None:
        self._diedcallbacks -= value


    @staticevent
    def PersonCreated(value:Callable[[object, EventArgs], None])->None:
        Person._personCreatedcallbacks += value

    @PersonCreated.remove
    def PersonCreated(value:Callable[[object, EventArgs], None])->None:
        Person._personCreatedcallbacks -= value

# endregion

class School:
    
    _name:str
    _principal:Person|None
    
    def __init__(self,name:str)->None:
        self._name = name
        self._principal = None

    @property
    def Name(self)->str: 
        return self._name
               
    @Name.setter 
    def Name(self,value:str)->None:
        self._name = value


    @property
    def Principal(self)->Person: 
        return self._principal
               
    @Principal.setter 
    def Principal(self,value:Person)->None:
        if self.Principal is not None:
            self.Principal.Died -= self._person_died

        self._principal = value

        if self.Principal is not None:
            self.Principal.Died += self._person_died


    def person_nameChanged(self,sender:object,e:EventArgs)->None:
        print("School %s just signed up %s"% (self.Name,sender.Name))

    def person_moved(self,sender:object,e:MovedEventArgs)->None:
        print("Person %s change its localitation by %s units" % (sender.Name,e.Delta))

    def person_locationchanging(self,sender:object,e:LocationChangingEventArgs)->None:
        if e.Location > 100:
            print("Person %s can't be changed that far, Location cannot be greater than 100. value: %d'" % (sender.Name,e.Location))
            e.Cancel = True

    def _person_died(self,sender:object,e:EventArgs):
        print("School %s is sad because principal %s die" % (self.Name,sender.Name))


    def method(self,sender:object,e:EventArgs)->None:
        print("this is a method")


def callback_function(sender:object,e:EventArgs)->None:
    print("callback sender %s, Eventargs: %s" % (sender,e))
    print("Person name %s" % sender.Name)



#USAGE EXAMPLES------------------------------------------------------------------------------------------------------------------------
person = Person("Carlos")#Creates an instance of Person (This class is the one that implements the events)
school = School("University 97")#Creates an instance of School (This class contains some methods that are going to be subscribed to the person events, internally and externally)


#Use of a simple event (In this case implemented as a property change event)------------------------------------------------------------
person.NameChanged += school.person_nameChanged #suscribe the school instance method to Namechanged event, (this method will be executed when the person's name change)
person.NameChanged += callback_function #suscribe an extra simple function (this function will be executed when the person's name change)
person.Name = "Susa" #Change the person name to trigger the event
#----------------------------------------------------------------------------------------------------------------------------------------

#How to unsuscribe an event--------------------------------------------------------------------------------------------------------------
person.NameChanged -= callback_function#unsuscribe only the function
person.Name = "Nos"#Change the person name to trigger the event
#----------------------------------------------------------------------------------------------------------------------------------------

#Use of an event with custom EventArgs---------------------------------------------------------------------------------------------------
person.Location =5#changing location to show nothing happens
person.Moved += school.person_moved#add a suscriber to the event
person.Location = 15#changing the location again to trigger the event
person.Moved -= school.person_moved#unsuscribe to the event
person.Location = 30#changing again the location to verify nothing happens
#----------------------------------------------------------------------------------------------------------------------------------------

#Use of a custom Eventargs with setter (allows to suscriber send information) in this case is implemented as a pre-event (triggers before something happens) this allows in this case cancel the Change of the person's location
person.LocationChanging += school.person_locationchanging #add the suscriber
person.Location = 13 #change the location to trigger the event
person.Location = 115 #changing location again to trigger the event, suscriber has the capability to cancel the asignation of the new value
print("%s location at %s" %(person.Name, person.Location))#checking person's location it is (13,13) due suscriber cancel the asignation of the action thorugh the pre-event
#----------------------------------------------------------------------------------------------------------------------------------------


#suscribing a Delegate instead of passing a function/method directly (Due Delegates are callables) to an event, as well show case of using polimorfism, pasing an EventArgs parameter function to a LocationEventArgs parameter event
delegate = Delegate(callback_function) #create a delagate with one function with signature Callable[[object, EventArgs], None]
person.Moved += delegate #suscribing a Callable[[object, EventArgs], None] to Callable[[object, MovedEventArgs], None] event
person.Location = 1#changing location to trigger event 
#in this case the event will provide an MovedEventArgs instance to the suscriber (the 'e' parameter), and suscriber handle the object as an EventArgs instance, by polimorfism is ok
#-----------------------------------------------------------------------------------------------------------------------------------------

#suscribing the methods internally on the class-------------------------------------------------------------------------------------------
school.Principal = person #Asign a principal to the school, the school will unsuscribe the old principal (if any) and suscribe to the new principal.Died event due it is of its interest know when its principal dies
person.Kill() #We kill the person :( (school will do its logic due its principal dies)
#------------------------------------------------------------------------------------------------------------------------------------------

#Static event example executing functions or methods
def person_created_callback(sender:object,e:EventArgs):
    print("Static callback works! person count:%d"% Person.get_InstanceCreated())


Person.PersonCreated += person_created_callback
Person.PersonCreated += school.method

person2 = Person("")
