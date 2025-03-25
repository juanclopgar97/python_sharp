from python_sharp import *



class MovedEventArgs(EventArgs):
    
    _delta:int

    def __init__(self,delta:int)->None:
        super().__init__()
        self._delta = delta

    @property
    def delta(self)->int:
        return self._delta


class LocationChangingEventArgs(CancellableEventArgs):
    
    _location:int

    def __init__(self,location:int)->None:
        super().__init__()
        self._location = location

    @property
    def location(self)->int:
        return self._location




class Person:

    _instance_created:int = 0
    _person_created:Delegate = Delegate()

    _name:str
    _alive:bool
    _location:int
    _name_changed:Delegate
    _moved:Delegate
    _location_changing:Delegate
    _died:Delegate

    def __init__(self,name:str)->None:
        self._name = name
        self._alive = True
        self._location = 0
        self._name_changed = Delegate()
        self._moved = Delegate()
        self._location_changing = Delegate()
        self._died = Delegate()
        Person._on_person_created(EventArgs())
        
# region Properties

    @property
    def name(self)->str: 
        return self._name
               
    @name.setter 
    def name(self,value:str)->None:
        self._name = value
        self._on_name_changed(EventArgs()) 

     
    @property
    def alive(self)->bool:
        return self._alive
    

    @property
    def location(self)->int:
        return self._location
    
    @location.setter
    def location(self,value:int)->None:
        
        locationEventArgs = LocationChangingEventArgs(value)
        self._on_location_changing(locationEventArgs)
        
        if(not locationEventArgs.cancel):
            previous = self.location 
            self._location = value
            self._on_moved(MovedEventArgs(self.location - previous))


    @staticmethod
    def get_instance_created()->int:
        return Person._instance_created
    
    @staticmethod
    def _set_instance_created(value:int)->None:
        Person._instance_created = value

# endregion

# region  Methods
   
    def _on_name_changed(self,e:EventArgs)->None:
        self._name_changed(self,e)
    
    def _on_location_changing(self,e:LocationChangingEventArgs)->None:
        self._location_changing(self,e)

    def _on_moved(self,e:MovedEventArgs)->None:
        self._moved(self,e)          
        
    def _on_died(self,e:EventArgs)->None:
        self._died(self,e)   

    def move(self,distance:int)->None:
        self.location += distance

    @staticmethod
    def _on_person_created(e:EventArgs)->None:
        Person._set_instance_created(Person.get_instance_created() + 1)
        Person._person_created(None,e)

    def kill(self)->None:
        self._alive = False
        self._on_died(EventArgs())

# endregion

# region Events
    
    @event  #Simplest event, just notify something happens, no provide extra information about the event (like why,how,when), no recolection of information from suscribers
    def name_changed(self,value: Callable[[object, EventArgs], None])->None:
        self._name_changed += value 
        
    @name_changed.remover
    def name_changed(self,value: Callable[[object, EventArgs], None])->None:
       self._name_changed -= value


    @event  #event with custom EventArgs, notify something happens and provides extra information (like why,how,when),  no recolection of information from suscribers
    def moved(self,value:Callable[[object, MovedEventArgs], None])->None:
        self._moved += value
    
    @moved.remover
    def moved(self,value:Callable[[object, MovedEventArgs], None])->None:
       self._moved -= value  


    @event  #event with custom EventArgs, notify something happens provides extra information (like why,how,when), and it is capable of recolect info from its suscribers (this case implemeted as prevent)
    def location_changing(self,value:Callable[[object, LocationChangingEventArgs], None])->None:
        self._location_changing += value
    
    @location_changing.remover
    def location_changing(self,value:Callable[[object, LocationChangingEventArgs], None])->None:
       self._location_changing -= value


    @event
    def died(self,value:Callable[[object, EventArgs], None])->None:
        self._died += value
    
    @died.remover
    def died(self,value:Callable[[object, EventArgs], None])->None:
        self._died -= value


    @staticevent
    def person_created(value:Callable[[object, EventArgs], None])->None:
        Person._person_created += value

    @person_created.remover
    def person_created(value:Callable[[object, EventArgs], None])->None:
        Person._person_created -= value

# endregion

class School:
    
    _name:str
    _principal:Person|None
    
    def __init__(self,name:str)->None:
        self._name = name
        self._principal = None

    @property
    def name(self)->str: 
        return self._name
               
    @name.setter 
    def name(self,value:str)->None:
        self._name = value


    @property
    def principal(self)->Person: 
        return self._principal
               
    @principal.setter 
    def principal(self,value:Person)->None:
        if self.principal is not None:
            self.principal.died -= self._person_died

        self._principal = value

        if self.principal is not None:
            self.principal.died += self._person_died


    def person_name_changed(self,sender:object,e:EventArgs)->None:
        print("School %s just signed up %s"% (self.name,sender.name))

    def person_moved(self,sender:object,e:MovedEventArgs)->None:
        print("Person %s change its localitation by %s units" % (sender.name,e.delta))

    def person_location_changing(self,sender:object,e:LocationChangingEventArgs)->None:
        if e.location > 100:
            print("Person %s can't be changed that far, location cannot be greater than 100. value: %d'" % (sender.name,e.location))
            e.cancel = True

    def _person_died(self,sender:object,e:EventArgs): #This can be protected and shoud be due it is only interest of the school when the principal dies
        print("School %s is sad because principal %s die" % (self.name,sender.name))


    def method(self,sender:object,e:EventArgs)->None:
        print("this is a method")


def callback_function(sender:object,e:EventArgs)->None:
    print("callback sender %s, Eventargs: %s" % (sender,e))
    print("Person name %s" % sender.name)



#USAGE EXAMPLES------------------------------------------------------------------------------------------------------------------------
person = Person("Carlos")#Creates an instance of Person (This class is the one that implements the events)
school = School("University 97")#Creates an instance of School (This class contains some methods that are going to be subscribed to the person events, internally and externally)


#Use of a simple event (In this case implemented as a property change event)------------------------------------------------------------
person.name_changed += school.person_name_changed #suscribe the school instance method to Namechanged event, (this method will be executed when the person's name change)
person.name_changed += callback_function #suscribe an extra simple function (this function will be executed when the person's name change)
person.name = "Susa" #Change the person name to trigger the event
#----------------------------------------------------------------------------------------------------------------------------------------

#How to unsuscribe an event--------------------------------------------------------------------------------------------------------------
person.name_changed -= callback_function#unsuscribe only the function
person.name = "Nos"#Change the person name to trigger the event
#----------------------------------------------------------------------------------------------------------------------------------------

#Use of an event with custom EventArgs---------------------------------------------------------------------------------------------------
person.location =5#changing location to show nothing happens
person.moved += school.person_moved#add a suscriber to the event
person.location = 15#changing the location again to trigger the event
person.moved -= school.person_moved#unsuscribe to the event
person.location = 30#changing again the location to verify nothing happens
#----------------------------------------------------------------------------------------------------------------------------------------

#Use of a custom Eventargs with setter (allows to suscriber send information) in this case is implemented as a pre-event (triggers before something happens) this allows in this case cancel the Change of the person's location
person.location_changing += school.person_location_changing #add the suscriber
person.location = 13 #change the location to trigger the event
person.location = 115 #changing location again to trigger the event, suscriber has the capability to cancel the asignation of the new value
print("%s location at %s" %(person.name, person.location))#checking person's location it is (13,13) due suscriber cancel the asignation of the action thorugh the pre-event
#----------------------------------------------------------------------------------------------------------------------------------------


#suscribing a Delegate instead of passing a function/method directly (Due Delegates are callables) to an event, as well show case of using polimorfism, pasing an EventArgs parameter function to a LocationEventArgs parameter event
delegate = Delegate(callback_function) #create a delagate with one function with signature Callable[[object, EventArgs], None]
person.moved += delegate #suscribing a Callable[[object, EventArgs], None] to Callable[[object, MovedEventArgs], None] event
person.location = 1#changing location to trigger event 
#in this case the event will provide an MovedEventArgs instance to the suscriber (the 'e' parameter), and suscriber handle the object as an EventArgs instance, by polimorfism is ok
#-----------------------------------------------------------------------------------------------------------------------------------------

#suscribing the methods internally on the class-------------------------------------------------------------------------------------------
school.principal = person #Asign a principal to the school, the school will unsuscribe the old principal (if any) and suscribe to the new principal.died event due it is of its interest know when its principal dies
person.kill() #We kill the person :( (school will do its logic due its principal dies)
#------------------------------------------------------------------------------------------------------------------------------------------

#Static event example executing functions or methods
def person_created_callback(sender:object,e:EventArgs):
    print("Static callback works! person count:%d"% Person.get_instance_created())


Person.person_created += person_created_callback
Person.person_created += school.method

person2 = Person("")
