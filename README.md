<!--img src="https://github.com/juanclopgar97/python_sharp/blob/master/documentation_images/python_sharp.png" width="300"-->
<img src="./documentation_images/python_sharp.png" width="300">

# Python# (Python sharp)

## Table of Contents
1. [Introduction](#Introduction)
2. [Installation](#Installation)
3. [Use cases and examples](#Use-cases-and-examples)
    1. [Delegates](#Delegates)
        1. [How to add callables into a Delegate](#How-to-add-callables-into-a-Delegate)
        2. [How to get returned values of callables out of a Delegate](#How-to-get-returned-values-of-callables-out-of-a-Delegate)
        3. [Delegates Summary](#Delegates-Summary)
    2. [Events](#Events)
        1. [EventArgs, CustomEventArgs and CancellableEventArgs class](#eventargs-customeventargs-and-cancellableeventargs-class)
        2. [Implementation](#Implementation)
            1. [Simple events](#Simple-events)
            2. [Events with arguments](#Events-with-argumentss)
            3. [Events with modifiable arguments](#Events-with-modifiable-arguments)

## Introduction

python# (python sharp) module was created with the intention of adding EOP (event oriented programing) into python in the most native feeling, easy sintax way possible.

This module was thought to accomplish EOP with 2 objetives in mind:

1. Features should look and feel like a native python feature.
2. Implementation should be based in another famous EOP language to decrease learning curve and improve user experience.

Events are just another possible way to declare a class member like: fields/attributes, properties and methods, python already have a way to define a property with **@property**, this helps to define objective number 1, for this reason events are implemented with **@event** sintax to be consistent with python:

```python #5
class Person:
  def __init__(self,name:str)->None:
    self._name = name

  @property
  def Name(self)->str: 
        return self._name

  @Name.setter 
  def Name(self,value:str)->None:
        self._name = value

  @event
  def NameChanged(self,value):
    #some implementation
    pass
```

For objective 2, the module was architected thinking in how another EOP language (in this case C#) implements its events. This implementation will be explain below, keep in mind this is a really simplified explanation of how C# events actually work, if you are interested in learn how they work exactly please go to C# documentation. With this clarified, let's move on to the explanation: 

1. C# implements events as a collection of callbacks that will be executed in some point of time, this collection of functions are called **Delegates**, invoking(executing) the delegate will cause the execution of all functions(callables) in its collection.

2. delegates are not publicly expose, commonly due security reasons, as the fields/attributes have to be encapsulated, delegates as well, and the way to encapsulate them is with events. Fields/attributes are to properties as delegates are to events.

3. Properties encapsulate fields/attributes with 2 functions/methods called "get" and "set", which define the logic of how data should be GET and SET out of the object, in C# events encapsulate delegates with 2 functions as well called "add" and "remove", which define the logic of how functions/subscribers should be added or removed out of the delegate.


## Installation

(To be documented, from downloading this repo to downloading from Pypi)

## Use cases and examples:

In this repository there are 2 main files "python_sharp.py" (which is the module file) and "test.py". This last file contains all the features applied into one single script, this could be really usefull if you want to do a quick check about how something is implemented, however, due it is a "testing" script and not a "walk through" it could be confusing if you do not know what is going on, so it is **Highly recommended** read the below documentation which explains step by step how to implement every single feature in the module.

### Delegates

Python sharp Delegates are a list of callables with the same signature, when a delegate is being executed (delegates are callable objects), it executes every single callable in its list.

#### How to add callables into a Delegate
It is really important to keep the callables added into the delegate with consistent signatures due parameters passed to the delegate when is being executed are the same ones passed to every single callable in the collection, so if one callable signature is expecting only 2 parametters and the next callable 3 parametters this is going to cause a TypeError that might look like this: 

```python
from python_sharp import *

def function1(parameter1:int): #defining a function with 1 parameter (int type)
  print("function1")

def function2(parameter1:int,parameter2:str): #defining a function with 2 parametrs (int,str types)
  print("function2")

delegate = Delegate() #creating a Delegate
delegate += function1 #adding function1
delegate += function2 #adding function2

delegate(5) # executing the delegate with only 1 parameter

```

OUTPUT:
```
function1
Traceback (most recent call last):
  File "c:\PATH\test.py", line 341, in <module>
    delegate(5) # executing the delegate with only 1 parameter
    ^^^^^^^^^^^
  File "c:\PATH\python_sharp.py", line 72, in __call__
    results.append(callable( *args, **kwds))
                   ^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: function2() missing 1 required positional argument: 'parameter2'
```

Here *function1* was executed correctly due the signature of the function match with how the delegate was executed (passing only one integer "5"), and *function2* was expecting a second string parameter resulting in a TypeError. So, it is really important keep signatures in a homogeneous manner.

#### How to get returned values of callables out of a Delegate

Once the delegate is executed you can get the returned values (if Any) as a tuple returned by the delegate, this tuple represents the values returned by every callable in the delegate's callable collection:

```python
from python_sharp import *

def function(text:str):
  print("%s, Function is being executed!" % text)
  return "function result"

class Test:
  def method(self,text:str):
    print("%s, Method is being executed!" % text)
    return "method result"

test_instance = Test()

first_delegate = Delegate(function) #adding a function. You can pass the first callble optionally through the constructor

delegate = Delegate() # creates an empty delegate
delegate += first_delegate #adding a delegate. You can add a delegate to another delegate due a Delegate is callable
delegate += test_instance.method #adding a method

results = delegate("Hello!")

print(f"returned values: {results}")
```

OUTPUT:
```
Hello!, Function is being executed!
Hello!, Method is being executed!
returned values: (('function result'), 'method result')
```
In this example we can see that *delegate* executes its first item added which is *first_delegate*, as result 'function' is executed and *first_delegate* return a tuple with the return value of 'function', this tuple is added into *delegate* results, then *delegate* executes its next item *test_instance.method* as result it returns a string that is going to be added into the *delegate* results.

At the end we finish with all callables executed and the results: 
  - ('function result'): result of *first_delegate* execution
  - 'method result': result of *test_instance.method* execution.

#### Delegates Summary

As summary, Delegates are really usefull to execute a bulk of callables, and its return values (if any) are returned by the delegate in a tuple.

### Events

In programming, an event refers to an action or occurrence that a program can detect and respond to. Events can be triggered by user interactions (like clicking a button, typing text, or moving a mouse), system-generated activities (like a file being updated or a timer expiring), or even messages from other parts of the program. Typically, an event is associated with subscribers (event listeners) which are functions or blocks of code designed to execute when the specific event occurs.

Events are commonly part of an event-driven programming paradigm, where the flow of the program is determined by these events.

Events can be implemented as members of an instance or a class (static events) on different ways, in this module we can group this "ways" into 3 main implementations:

1. **Simple events** (Normally implemented as *property changed* events):
  This events only "notify" that something relevant happens, they do not provide extra information about the event like: How, When, Why etc

2. **Events with arguments**:
  This events are like the previous one but they are capable of provide extra information about the event like: How, When, Why etc, to the subscribers through a parameter (Normally a custom 'EventArgs' type called 'e')

3. **Events with modifiable arguments** (Normally implemented as *pre-events*)
  This events are like the one in the point number 2, but now the arguments are not only *read_only* arguments, on point 2, event arguments are *read_only* arguments because the arguments are information passed from         the publisher (object that implement the event) to subscribers (object that is interested to be notified) so there is no reason to let the subscriber change that information. However the events described on this
  point (point 3) can contain editable arguments, this arguments are not designed to provide information about the event, but rather they act like a channel to let the subcriber set and pass information to the publisher.

  An example to clarify this could be an event called "WindowClosing", this event will notify that a window is about to close, the subscribers will have the power to pass information through the event arguments to cancel   the action, this is really useful if the changes in the app are not saved.

#### EventArgs, CustomEventArgs and CancellableEventArgs class

*EventArgs* class is an empty class designed to be a base class to pass the event arguments, these arguments are going to be passed from the publisher to the subscriber in order to provide more information about what happens.

-  **Simple events** use *EventArgs* objects to pass the event arguments to the subscriber, due *EventArgs* is an empty class, no arguments are passed to the subscriber, this is the reason why these events are the simplest to implement and the ones used for *property changed* events, they only notify something happens and that's it, no more information. Worth mentioning *property changed* events are not the only use for these event types, it is just a use case example

-  **Events with arguments** use a custom class that inherit from *EventArgs* class to describe what arguments are going to be passed to the subscriber. The arguments passed to the subscriber are passed as read_only properties (properties with only getter). If a **simple event** is not enough, you might need an **Event with arguments**, in this case, you can use a custom EventArgs that contains your arguments.

    As a use case example imagine an event called *Moved*, this event notifies when the object moves, but maybe only notify the movement is not enough and we want to inform how much the object moves, this is a perfect use for our custom *EventArgs* class:


    ```python
    class MovedEventArgs(EventArgs): # example of Custom EventArgs to pass event information (distance moved in this case)

        _delta:int

        def __init__(self,delta:int)->None: # Request the distance of the movement
            super().__init__()
            self._delta = delta # Save the distance

        @property
        def Delta(self)->int: #encapsulate the value and placing its getter
            return self._delta
    ```

- **Events with modifiable arguments** use a custom class that inherit from *EventArgs* class to describe what arguments are going to be passed from the subscriber to the publisher, this module already include one example of this aproach *CancellableEventargs*:

    ```python
    
    class CancellableEventArgs(EventArgs):
    
        _cancel:bool
    
        def __init__(self)->None:
            super().__init__()
            self._cancel = False 
    
        
        @property
        def Cancel(self)->bool: #to show the value of _cancel attribute
            return self._cancel
        
        @Cancel.setter
        def Cancel(self,value:bool)->None: #to let the subscriber set a value into _cancel
            self._cancel = value
    ```

    as you can see, this implementation is really similar to **Events with arguments**, the only difference is we are placing a setter method to let modify the cancel value, this value can be used for the publisher at the end of the exectution of all the callbacks stored.

#### Implementation

Below this text, the use cases and explanation about the events are shown, please read the examples and after READ THE EXPLANATION OF THE EXAMPLE CODE, this is really important because it specifies step by step the "WHY"s of the implementation.

##### Simple events

  ```python
    from python_sharp import *

    class Person: 
    
      def __init__(self, name:str)->None: 
        self._name = name 
        self._namechanged_callbacks = Delegate() 

      @property 
      def Name(self)->str:
        return self._name

      @Name.setter 
      def Name(self,value:str)->None:
        self._name = value
        self._OnNameChanged(EventArgs()) 

      def _OnNameChanged(self,e:EventArgs)->None:
        self._namechanged_callbacks(self,e) 

      @event 
      def NameChanged(self,value)->None:
        self._namechanged_callbacks += value

      @NameChanged.remove
      def NameChanged(self,value)->None:
        self._namechanged_callbacks -= value 


    def person_NameChanged(sender:object,e:EventArgs)->None:
      print("person change its name to %s" % sender.Name)

    person = Person("Juan")
    person.NameChanged += person_NameChanged 
    person.Name = "Carlos" 
    person.NameChanged -= person_NameChanged 
    person.Name = "Something" 
  ```

  OUTPUT
  ```
  person change its name to Carlos
  ```

To implement a simple event the first thing you have to do is create a variable to store the subscribers, look at this variable as a "To do list" due it contains the callables that are going to be executed at some specific time.

```python
self._namechanged_callbacks = Delegate() # it can be viewed as a "To do list"
```

As you might notice the variable that is going to store the subscribers is a Delegate and the name starts with '_' to "protect" the attribute. Expose the attribute "publicly" is not a good practice, due other part of the code can manipulate the attribute wrongly or get/set information in a way that was not mean to. To fix this, we can define 2 methods to encapsulate the delegate (add/remove methods), Through these 2 methods the other objects in the code can subscribe/unsubscribe (add/remove) callables to our delegate.

```python
      @event 
      def NameChanged(self,value)->None:
        self._namechanged_callbacks += value # add the new callable to the attribute with a delegate

      @NameChanged.remove
      def NameChanged(self,value)->None:
        self._namechanged_callbacks -= value # remove the callable to the attribute with a delegate
```

Code above implements add/remove logic to the delegate. Function below *@event* decorator defines the logic for the *add* or how a callable should be added to our "To do list". Function below *@NameChanged.remove* defines the logic for the *remove* or how a callable should be removed from the delegate

Notice the functions HAVE to be named exactly with the same name, and if an *@event* is defined you **must** implement *@IDENTIFIER.remove* or the code will throw a traceback, this is to protect the integrity of the code and provide instructions about how to add AND remove a callable.

The callable to be added/removed will be passed through the "value" parameter. Notice in this example "value" parameter doesn't have any type annotation, this is only to keep this first example "simple/readable" at first sight, however is HIGHLY RECOMMENDED annotate the type as the following examples (Events with arguments or Events with modifiable arguments), due this is the way to indicate clearly what is the signature expected from the event to their subcribers (callables).

Once this is in place, we have:

- A place to store the callables 
- Logic to let to other parts of the code add/remove callables

Now we need to execute the callables in the right momment, in this case the event is called "NameChanged" so the callables should be executed when the name changes, this means our extra logic needs to be added in the Name setter due that is the part of the code that has this responsability (change the person's name).

```python
      @Name.setter 
      def Name(self,value:str)->None:
        self._name = value
        # execute our "To do list" or delegate
```

In the snippet code above the comment defines where the "To do list" needs to be executed, however, sometimes the own object needs to implement its own logic when (in this case) the property Name change, for this purpose is HIGHLY RECOMMENDED as a good practice define another function/method called "_On[EVENT NAME]"

```python
      @Name.setter 
      def Name(self,value:str)->None:
        self._name = value
        self._OnNameChanged()

      def _OnNameChanged(self)->None:
        #logic when the name change (if any)
        self._namechanged_callbacks() #external logic
```
Inside of this method the own internal and external logic when the name change must be implemented, in other words, *What as a Person I need to do when my name changes?* (own/internal logic), and after, attend external logic (To do list) in other words instructionss provided by other objects or parts of the code. *What others needs to do when my name changes?*

In this case the class Person doesn't need to do "something" when the name changes (internal logic), so we only need to execute the external logic (execute the delegate)


Now we have a way to add/remove subscribers and trigger the event, however, you might notice the code above is not exactly the same as the example code, this is because despite the event is now implemented and working is not following a good practice CONVENTION. So even with a working code, is HIGHLY RECOMMENDED follow next convention:

```python
      @Name.setter 
      def Name(self,value:str)->None:
        self._name = value
        self._OnNameChanged(EventArgs())

      def _OnNameChanged(self,e:EventArgs)->None:
        #internal logic if any
        self._namechanged_callbacks(self,e)
```

You can notice 2 things

1. *_OnNameChanged* now requires a parametter called 'e' which is an EventArgs, this is a safety implementation, every "_On[EVENT NAME]" must require an EventArgs (or any other class that inherits from it), this is a way to say "Are you sure the event happens? show me the evidence!", in this case there is no arguments so the evidence is an empty EventArgs object. EventArgs object is used first for the internal logic and then passed to the external logic as a parameter.

2. 'self' is passed to the external logic as first parameter, this is to allow the subcribers know 'Who is executing my piece of code"



**As summary:** 

- There are 2 main sections to implement when you want to define an event: 

    1. Part that store and define how to add/remove callables
    2. Part that executes/trigger those callables stored

- There are conventions about how the logic must be implemented to facilitate reading and maintenance of the code.

- Callables to be subscribed to a simple event should follow the next signature:

    *Callable[[object, EventArgs], None]* (a callable with 2 parameters, first one contains the publisher and second the event arguments, the function must return None)

The next snipped code shows and example of how the *simple events* should be implemented with the recomended annotation: 

```python
      @event 
      def NameChanged(self,value:Callable[[object, EventArgs], None])->None:
        self._namechanged_callbacks += value

      @NameChanged.remove
      def NameChanged(self,value:Callable[[object, EventArgs], None])->None:
        self._namechanged_callbacks -= value 
```

This is done with the intention of clarify what is the event expecting from its subscribers signature.


To use the event:

```python
    def person_NameChanged(sender:object,e:EventArgs)->None: #function to be executed when the name changes (subscriber)
      print("person change its name to %s" % sender.Name)

    person = Person("Juan")  #creates a person
    person.NameChanged += person_NameChanged # we add 'person_NameChanged' (subcriber) to event NameChanged of 'person', this line will execute function under @event decorator (add function)
    person.Name = "Carlos" # change the name to trigger the event (this will execute 'person_NameChanged') 
    person.NameChanged -= person_NameChanged #unsubcribe the function, this line will execute function under @NameChanged.remove decorator (remove function)
    person.Name = "Something" # change the name again to prove 'person_NameChanged' is not executed anymore
```


##### Events with arguments

  ```python
    from python_sharp import *
    from typing import Callable

    class MovedEventArgs(EventArgs):

        _delta:int

        def __init__(self,delta:int)->None:
            super().__init__()
            self._delta = delta

        @property
        def Delta(self)->int:
            return self._delta

    class Person:
    
        def __init__(self)->None:
            self._location = 0
            self._movedcallbacks = Delegate()

        @property
        def Location(self)->int:
            return self._location

        @Location.setter
        def Location(self,value:int)->None:      
            previous = self.Location 
            self._location = value
            self._OnMoved(MovedEventArgs(self.Location - previous))

        def Move(self,distance:int)->None:
            self.Location += distance

        def _OnMoved(self,e:MovedEventArgs)->None:
            self._movedcallbacks(self,e)

        @event 
        def Moved(self,value:Callable[[object, MovedEventArgs], None])->None:
            self._movedcallbacks += value

        @Moved.remove
        def Moved(self,value:Callable[[object, MovedEventArgs], None])->None:
           self._movedcallbacks -= value  


    def person_Moved(sender:object,e:MovedEventArgs)->None:
      print("Person moves %d units" % e.Delta)

    person = Person()
    person.Move(15)
    person.Moved += person_moved
    person.Location = 25
    person.Moved -= person_moved
    person.Location = 0
  ```

  OUTPUT
  ```
  Person moves 10 units
  ```

*Events with arguments* are almost the same as *simple events* so, the next explanation will only address the differences between the 2 cases.

```python
    class MovedEventArgs(EventArgs):

        _delta:int

        def __init__(self,delta:int)->None:
            super().__init__()
            self._delta = delta

        @property
        def Delta(self)->int:
            return self._delta
```

In this case a custom EventArgs is created in order to be capable of store the event arguments, on this example the event is named "Moved", and is going to be triggered when the person changes its location, in addition, it will provide HOW MUCH the person moves, this is the job of the *MovedEventArgs* and the main difference with a *simple event*.

In the next code block we can see how the event is being defined:

```python
        @event 
        def Moved(self,value:Callable[[object, MovedEventArgs], None])->None:
            self._movedcallbacks += value

        @Moved.remove
        def Moved(self,value:Callable[[object, MovedEventArgs], None])->None:
           self._movedcallbacks -= value  
```

in this case the only difference is the 'value' parameter annotation,  this indicates that the event requieres a *Callable[[object, MovedEventArgs], None]* subscriber signature, in other words a *MovedEventArgs* will be provided to the subscriber.

It is HIGHLY IMPORTANT to realize *Moved* event signature is *Callable[[object, MovedEventArgs], None]* therefore it can accept subscribers with the next signatures:

- *Callable[[object, MovedEventArgs], None]*
- *Callable[[object, EventArgs], None]*

This 2 signatures are ok due polimorfism, it can be confusing due at first sight seems like we are asigning an *EventArgs* to a *MovedEventArgs* (*MovedEventArgs* <- *EventArgs*), this case is not valid, due it might throw a Traceback if a *MovedEventArgs* member is trying to be acceses into a *EventArgs* object. However in this example case is not the same,
the subscriber with *Callable[[object, EventArgs], None]* signature defines how the paramater object is going to be treated by the callable, in this case, the parameter will be used/treated as an *EventArgs*, and the event will provide a *MovedEventArgs* object to the callable so in reallity we are asigning a *MovedEventArgs* object to an *EventArgs* variable (*EventArgs* <- *MovedEventArgs*) wich by polimorfism will not cause any issue trying to access any of the *EventArgs* members.

Next diagram explains a general case for what was explained above (event subscriber signatures accepted by an event):

<img src="./documentation_images/event_assignament_example.png" width="100%">


And the last difference but not less important is how the event is going to be trigerred:

```python
        @Location.setter
        def Location(self,value:int)->None:      
            previous = self.Location 
            self._location = value
            self._OnMoved(MovedEventArgs(self.Location - previous))

        def _OnMoved(self,e:MovedEventArgs)->None:
            self._movedcallbacks(self,e)
```

We can see in the code block above now *_OnMoved* method now requires a *MovedEventArgs*, as *simple events* did, this is for security reasons, if we are going to execute *_OnMoved* method because the event happens, that is a way to say "prove it or show the evidence!".

Second difference is when *Location* settter is calling *_OnMoved* method, now it needs to create an instance of *MovedEventArgs* and to do so, it requieres a quantity to be passed to the constructor, this quantity of "how much the person moves" can be calculated with a substraction of previous and current location.


**As summary:** 

*Events with arguments* and *simple arguments* are really similar and there are only some differences:

1. Needs a custom *EventArgs* class defined.
2. Events with custom *EventArgs* can accept different subscriber signatures
3. _On[Event name] method uses the custom *EventArgs* class and this causes an extra security layer
4. Trigger code now needs to create an instance of the new custom *EventArgs* and to do so, it needs to provide/calculate the arguments needed by the custom *EventArgs* constructor


##### Events with modifiable arguments

  ```python
    from python_sharp import *
    from typing import Callable

    class LocationChangingEventArgs(CancellableEventArgs):

        _value:int

        def __init__(self,value:int)->None:
            super().__init__()
            self._value = value

        @property
        def Value(self)->int:
            return self._value

    class Person:
    
      def __init__(self)->None:
        self._location = 0
        self._locationChangingcallbacks = Delegate()

        @property
        def Location(self)->int:
            return self._location

        @Location.setter
        def Location(self,value:int)->None:

            locationEventArgs = LocationChangingEventArgs(value)
            self._OnLocationChanging(locationEventArgs)

            if(not locationEventArgs.Cancel):
                self._location = value


        def _OnLocationChanging(self,e:LocationChangingEventArgs)->None:
            self._locationChangingcallbacks(self,e)


        @event
        def LocationChanging(self,value:Callable[[object, LocationChangingEventArgs], None])->None:
            self._locationChangingcallbacks += value

        @LocationChanging.remove
        def LocationChanging(self,value:Callable[[object, LocationChangingEventArgs], None])->None:
           self._locationChangingcallbacks -= value


    def person_LocationChanging(sender:object,e:LocationChangingEventArgs):
      if e.Value > 100:
        e.Cancel = True

    person = Person()
    person.Location = 50
    person.LocationChanging += person_LocationChanging
    person.Location = 150
    print(person.Location)

  ```




