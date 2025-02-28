from typing import Callable,Any,List,Generic,TypeVar,Union

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

        return results
    

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

class event:
    """
    Event attribute, used to define a managed callback

    Attributes:
        _fadd (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for adding a callable value.
        _fremove (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for removing a callable value.
        _proxy:"Event" | None: Object to be use as proxy for the descriptor
    """
    _fadd: Callable[[Callable[[object,EventArgs], None]], None] | None
    _fremove:Callable[[Callable[[object,EventArgs], None]], None] | None
    _proxy: Union["Event" , None]

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

    
    def add(self,fadd:Callable[[Callable[[object,EventArgs], None]], None])->"event":
        """
        Allows provide the function will be use to add a callable.

        Parameters:
            fadd (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for adding a callable value.
        Return:
            event: Current instance with the new fadd function
        """
        if fadd is not None and self._fremove is not None and self._fremove.__name__ != fadd.__name__:
            raise AttributeError("add function name provided '%s' does not match with remove function name %s" % (fadd.__name__,self._fremove.__name__))

        self._fadd = fadd
        return self

    def remove(self,fremove:Callable[[Callable[[object,EventArgs], None]], None])->"event":
        """
        Allows provide the function will be use to remove a callable.

        Parameters:
            fremove (Callable[[Callable[[object,EventArgs], None]], None] | None): function to be used for removing a callable value.
        Return:
            event: Current instance with the new fremove function
        """
        if fremove is not None and self._fadd is not None and self._fadd.__name__ != fremove.__name__:
            raise AttributeError("remove function '%s'and add function '%s' name missmatch, both members must have same name" % (fremove.__name__,self._fadd.__name__))

        self._fremove = fremove
        return self
    
    def __get__(self, instance:object, owner:type)->"Event":
        """
        Method to get descriptor value.

        Parameters:
            instance (object): The instance of the owning class. This parameter
                is `None` when accessed from the class instead of from the instance.
            owner (type): The type of the owning class.

        Return:
            Event: Event value stored in the descriptor.
        """

        if self._fadd is None or self._fremove is None:
            error_message = ""

            if self._fadd is None and self._fremove is None:
                error_message = "event in %s is not defining any function (add/remove)" % owner
            else:
                function_info= (self._fremove,"add") if self._fadd is None else (self._fadd,"remove") 
                error_message = "event %s does not have '%s' function assigned in %s" % (function_info[0].__name__,function_info[1],owner)
            
            raise NotImplementedError(error_message) 

        if self._proxy is None or self._proxy._instance != instance:
            self._proxy = self.Event(instance, self)

        return self._proxy
    

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
    
 
#staticproperty

