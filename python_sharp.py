from typing import Callable,Any,List,Generic,TypeVar,Union
from abc import ABC, abstractmethod

T=TypeVar("T")

class Delegate(Generic[T]):
    """
    Delegate is a simple class that represents a collection of Callables. When is being called execute all the callables in its collection.

    Attributes:
        _callables (list): Stores a collection of Callables.
    """
    _callables:list

    def __init__(self,callable:Callable[..., T] | None = None)->None:
        """
        Delegate constructor.

        Parameters:
            callable (Callable[..., T] | None): first callable to be added to the collection of callables.

        Return:
            None
        """
        self._callables = [] 

        if callable is not None:
            self += callable


    def __iadd__(self, value:Callable[..., T])->"Delegate":
        """
        Implements the addition of a callable into the callable collection.

        Parameters:
            value (Callable[..., T]): callable to be added to the collection of callables.

        Return:
            Delegate: Current instance with the extra callable.
        """
        self._callables.append(value)
        return self

    def __isub__(self, value:Callable[..., T])->"Delegate":
        """
        Implements the subtraction of a callable into the callable collection.

        Parameters:
            value (Callable[..., T]): callable to be subtracted to the collection of callables.

        Return:
            Delegate: Current instance with without the passed callable.
        """
        self._callables.remove(value)
        return self
    

    def __call__(self, *args:Any, **kwds:Any)->List[T]:
        """
        Allows the Delegate instance to be called as a function.

        Parameters:
            *args: A variable number of positional arguments that are going to be pass to every callable in the callable collection.
            **kwds: A variable number of named arguments that are going to be pass to every callable in the callable collection (keyword arguments).

        Return:
            List[T]: A list of the results of every callable in the callable collection.
        """
        results = []

        for callable in self._callables:
            results.append(callable( *args, **kwds))

        return tuple(results)
    

class EventArgs:
    """
    EventArgs is a class that represents a object that contains the event arguments (reasons or extra information about why the event was triggered)
    """
    pass


class CancellableEventArg(EventArgs):
    """
    CancellableEventArg is a class that represents an EventArg that implements the posibility of cancelling the upcomming event setting the property Cancel to 'True'.

    Attributes:
        _cancel (bool): Contains the value if the action advertise by the pre-event should continue or not.
    """
    _cancel:bool

    def __init__(self)->None:
        """
        CancellableEventArg constructor.

        Return:
            None
        """
        super().__init__()
        self._cancel = False 

    
    @property
    def Cancel(self)->bool:
        """
        Gets property value.

        Return:
            bool: current value.
        """
        return self._cancel
    
    @Cancel.setter
    def Cancel(self,value:bool)->None:
        """
        Sets a new value.

        Parameters:
            value (bool): New value to set.
        """
        self._cancel = value

class BaseEvent(ABC):
    """
    BaseEvent an abstaract class to define a base event

    Attributes:
        _fadd (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for adding a callable value.
        _fremove (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for removing a callable value.
        _proxy: object | None: Object to be use as proxy for the descriptor
    """
    _fadd: Callable[[Callable[[object,EventArgs], None]], None] | None
    _fremove:Callable[[Callable[[object,EventArgs], None]], None] | None
    _proxy: object | None

    def __init__(
        self,
        fadd:Callable[[Callable[[object,EventArgs], None]], None] | None = None,
        fremove:Callable[[Callable[[object,EventArgs], None]], None] | None = None
    )->None:
        """
        event constructor.

        Parameters:
            fadd (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for adding a callable value.
            fremove (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for removing a callable value.
        Return:
            None
        """
        self._fadd = None
        self._fremove = None

        self.add(fadd)
        self.remove(fremove)

        self._proxy = None

    
    def add(self,fadd:Callable[[Callable[[object,EventArgs], None]], None] | None)->"BaseEvent":
        """
        Allows provide the function will be use to add a callable.

        Parameters:
            fadd (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for adding a callable value.
        Return:
            BaseEvent: Current instance with the new fadd function
        """
        if fadd is not None and self._fremove is not None and self._fremove.__name__ != fadd.__name__:
            raise AttributeError("add function '%s'and remove function '%s' name missmatch, both members must have same name" % (fadd.__name__,self._fremove.__name__))

        self._fadd = fadd
        return self

    def remove(self,fremove:Callable[[Callable[[object,EventArgs], None]], None] | None)->"BaseEvent":
        """
        Allows provide the function will be use to remove a callable.

        Parameters:
            fremove (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for removing a callable value.
        Return:
            BaseEvent: Current instance with the new fremove function
        """
        if fremove is not None and self._fadd is not None and self._fadd.__name__ != fremove.__name__:
            raise AttributeError("remove function '%s'and add function '%s' name missmatch, both members must have same name" % (fremove.__name__,self._fadd.__name__))

        self._fremove = fremove
        return self
    
    @abstractmethod
    def _get_proxy(self, instance: Any, owner: type) -> Any:
        """
        Allows provide the specific proxy use for every child of this class

        Parameters:
            instance (Any): The instance of the owning class. This parameter
                is `None` when accessed from the class instead of from the instance.
            owner (type): The type of the owning class.

        Return:
            Any: Descriptor proxy.
        """
        pass

    def __get__(self, instance:Any, owner:type)->Any:
        """
        Method to get descriptor value.

        Parameters:
            instance (Any): The instance of the owning class. This parameter
                is `None` when accessed from the class instead of from the instance.
            owner (type): The type of the owning class.

        Return:
            Any: Descriptor proxy.
        """

        if self._fadd is None or self._fremove is None:
            error_message = ""

            if self._fadd is None and self._fremove is None:
                error_message = "event in %s is not defining any function (add/remove)" % owner
            else:
                function_info= (self._fremove,"add") if self._fadd is None else (self._fadd,"remove") 
                error_message = "event %s does not have '%s' function assigned in %s" % (function_info[0].__name__,function_info[1],owner)
            
            raise NotImplementedError(error_message) 

        return self._get_proxy(instance,owner) 


class event(BaseEvent):
    """
    event attribute, used to define a managed callback in an instance

    Attributes:
    _proxy: Event: Object to be use as proxy for the descriptor
    """

    _proxy:"Event"

    class Event:
        """
        Event is class used as proxy for the 'event' descriptor. its responsability is execute _fadd and _fremove when operators += and -- are used over the member marked as @event.

        Attributes:
            _instance (Any): Stores the object using @event as memeber (the object implementing the event).
            _event_descriptor (event): Stores the descriptor that is using the instance as proxy.
        """
        _instance:Any
        _event_descriptor:"event"

        def __init__(self, instance:Any, event_descriptor:"event")->None:
            """
            Event constructor.

            Parameters:
                instance (Any): object using @event as memeber (the object implementing the event).
                event_descriptor (event): descriptor that is going to use this instance as proxy.
            Return:
                None
            """
            self._instance = instance
            self._event_descriptor = event_descriptor

        def __iadd__(self, value:Callable[[object,EventArgs], None])->"event.Event":
            """
            Executes the _fadd (responsible of describe how the callable sholud be added) passing the callable as parameter.

            Parameters:
                value (Callable[[object,EventArgs], None]): callable to be passed as parammeter to _fadd.

            Return:
                event.Event: Current instance.
            """
            self._event_descriptor._fadd(self._instance, value)
            return self

        def __isub__(self, value:Callable[[object,EventArgs], None])->"event.Event":
            """
            Executes the _fremove (responsible of describe how the callable sholud be removed) passing the callable as parameter.

            Parameters:
                value (Callable[[object,EventArgs], None]): callable to be passed as parammeter to _fremove.

            Return:
                event.Event: Current instance.
            """
            self._event_descriptor._fremove(self._instance, value)
            return self

    def _get_proxy(self, instance: Any, owner: type) -> "event.Event":
        """
        Allows provide the specific proxy use for every child of this class

        Parameters:
            instance (Any): The instance of the owning class. This parameter
                is `None` when accessed from the class instead of from the instance.
            owner (type): The type of the owning class.

        Return:
            event.Event: Descriptor proxy.
        """
        if self._proxy is None or self._proxy._instance != instance:
            self._proxy = event.Event(instance, self)
        return self._proxy
 

class staticevent(BaseEvent):
    """
    static event attribute, used to define a managed callback in a class

    Attributes:
    _proxy: StaticEvent: Object to be use as proxy for the descriptor
    """

    _proxy:"StaticEvent"

    class StaticEvent:
        """
        StaticEvent is class used as proxy for the 'staticevent' descriptor. its responsability is execute _fadd and _fremove when operators += and -- are used over the member marked as @staticevent.

        Attributes:
            _event_descriptor (staticevent): Stores the descriptor that is using the instance as proxy.
        """
        _event_descriptor: "staticevent"


        def __init__(self, event_descriptor: "staticevent") -> None:
            """
            StaticEvent constructor.

            Parameters:
                event_descriptor (staticevent): descriptor that is going to use this instance as proxy.
            Return:
                None
            """
            self._event_descriptor = event_descriptor


        def __iadd__(self, value: Callable[[object, EventArgs], None]) -> "staticevent.StaticEvent":
            """
            Executes the _fadd (responsible of describe how the callable sholud be added) passing the callable as parameter.

            Parameters:
                value (Callable[[object,EventArgs], None]): callable to be passed as parammeter to _fadd.

            Return:
                staticevent.StaticEvent: Current instance.
            """
            self._event_descriptor._fadd(value)
            return self

        def __isub__(self, value: Callable[[object, EventArgs], None]) -> "staticevent.StaticEvent":
            """
            Executes the _fremove (responsible of describe how the callable sholud be removed) passing the callable as parameter.

            Parameters:
                value (Callable[[object,EventArgs], None]): callable to be passed as parammeter to _fremove.

            Return:
                staticevent.StaticEvent: Current instance.
            """
            self._event_descriptor._fremove(value)
            return self


    def _get_proxy(self, instance: Any, owner: type) -> "staticevent.StaticEvent":
        """
        Allows provide the specific proxy use for every child of this class

        Parameters:
            instance (Any): The instance of the owning class. This parameter
                is `None` when accessed from the class instead of from the instance.
            owner (type): The type of the owning class.

        Return:
            staticevent.StaticEvent: Descriptor proxy.
        """
        if self._proxy is None:
            self._proxy = staticevent.StaticEvent(self)
        return self._proxy


class staticproperty:
    """
    staticproperty attribute, used to define a static property

    Attributes:
    _fget:Callable[[], Any] | None: function to be used for getting the value.
    _fset:Callable[[Any], Any] | None: function to be used for setting the value.
    """
    _fget:Callable[[], Any] | None
    _fset:Callable[[Any], Any] | None

    def __init__(self, fget:Callable[[], Any] | None = None,fset:Callable[[Any], Any] | None = None)->None:
        """
        staticproperty constructor.

        Parameters:
            fget (Callable[[], Any] | None): function to be used for getting the value.
            fset (Callable[[Any], Any] | None): function to be used for setting the value.
        Return:
            None
        """
        self._fget = None
        self._fset = None

        self.getter(fget)
        self.setter(fset)

    def __get__(self, instance:Any, owner:type)->Any:
        """
        Method to get descriptor value.

        Parameters:
            instance (Any): The instance of the owning class. This parameter
                is `None` when accessed from the class instead of from the instance.
            owner (type): The type of the owning class.

        Return:
            Any: result of execution the fget function passed
        """
        if self._fget is None:
            raise AttributeError("No getter defined for this static property")

        return self._fget()

    def __set__(self, instance:Any, value:Any)->None:
        """
        Method to set descriptor value.

        Parameters:
            instance (Any): The instance of the owning class. This parameter
                is `None` when accessed from the class instead of from the instance.
            value (Any): value to be set.

        Return:
           None
        """
        if self._fset is None:
            raise AttributeError("No setter defined for this static property")
        
        self._fset(value)


    def getter(self, fget:Callable[[], Any] | None)->"staticproperty":
        """
        Allows provide the function will be use to get the descriptor value.

        Parameters:
            fget (Callable[[], Any] | None): function to be used for getting descriptor value.
        Return:
            staticproperty: Current instance 
        """
        self._fget = fget
        return self

    def setter(self, fset:Callable[[Any], Any] | None)->"staticproperty":
        """
        Allows provide the function will be use to set the descriptor value.

        Parameters:
            fset (Callable[[Any], Any] | None): function to be used for setting descriptor value.
        Return:
            staticproperty: Current instance 
        """
        self._fset = fset
        return self

