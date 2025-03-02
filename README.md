<img src="https://github.com/juanclopgar97/python_sharp/blob/master/documentation_images/python_sharp.png" width="300">

# Python# (Python sharp)


## Introduction

python# (python sharp) module was created with the intention of adding EOP (event oriented programing) and some other features like static properties into python in the most native feeling, easy sintax way possible.

This module was thought to accomplish EOP with 2 objetives in mind:

1. Features should looks and feel like a native python feature.
2. Implementation should be based in another famous EOP language to decrease learning curve and improve user experience.

Events are just another possible way to declare a class member like: fields/attributes, properties and methods, python already have a way to define a property with **@property**, this helps to define objective number 1, events should be implemented with **@event** sintax to be consistent with python.:

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

2. delegates are not publicly expose commonly due security reasons, as the fields/attributes have to be encapsulated, delegates as well, and the way to encapsulate them is with events. fileds/attributes are to properties as delegates are to events.

3. Properties encapsulate fields/attributes with 2 functions/methods called "get" and "set" functions/methods which define the logic and specify how data should be GET and SET out of the object, in C# events encapsulate delegates with 2 functions as well called "add" and "remove" functions which define the logic and specify how functions/subscribers should be added or removed out of the delegate.

With these 2 objetives explained and the basic module introduction finished, lets jump into the use cases!

## Use cases and examples:

In this repository there are 2 main files "python_sharp.py" (which is the module file) and "test.py", this last file contains all the features applied in one single script, this could be really usefull if you want to do a quick check about how something is implemented. However, due it is a "testing" script and not a "walk through" it could be confusing if you do not know what is going on, so it is **Highly recommended** read the below part of the document which explains step by step how to implement every single feature in the module.

### Delegates

Python sharp Delegates are a list of callables with the same signature, when a delegate is being executed (delegates are callable objects), it executes every single callable in its list.
It is really important that the callables added into the delagete collection keep consistent signatures due parameters passed to the delegate when is being executed are the same ones passed to every single callable in the collection, so if one callable signature is expecting only 2 parametters and the next callable 3 parametters this is going to cause a TypeError that might look like: 

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
Here *function1* was executed correctly due the signature of the function match with how the delegate was executed (passing only one integer "5"), and *function2* was expecting a second string parameter resulting in a TypeError. So, is really important keep signatures in a homogeneous manner.



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


As summary, Delegates are really usefull to execute a bulk of callables, and its return values (if any) are returned by the delegate in a tuple.

### Events

Events can be implemented as members of an instance or a class (static events) on different flavors, we can group this flavors into 3 main implementations:

1. **Simple events** (Normally implemented as *property changed* events):
  This events only "notify" that something relevant happens, they do not provide extra information about the event like: How, When, Why etc

2. **Events with arguments**:
  This events are like the previous one but they are capable of provide extra information about the event like: How, When, Why etc, to the subscribers through a parameter (Normally a custom 'EventArgs' type called 'e')

3. **Events with modifiable arguments** (Normally implemented as *pre-events*)
  This events are like the one in the point number 2, but now the arguments are not only *read_only* arguments, on point 2, event arguments are *read_only* arguments because the arguments are information passed from         the publisher (object that implement the event) to subscribers (object that is interested to be notified) so there is no reason to let the subscriber change that information. However the events described on this
  point (point 3) can contain editable arguments, this arguments are not designed to provide information about the event, but rather they act like a channel to let the subcriber set and pass information to the publisher.

  An example to clarify this could be an event called "WindowClosing", this event will notify that a window is about to close, the subscribers will have the power to pass information through the event arguments to cancel   the action, this is really useful if the changes in the app are not saved.

  This might sound a little bit confusing at the begining but in fact, is not once you see an example and apply one. 

<br/>

#### EventArgs, CustomEventArgs and CancellableEventArgs class

<br/>

*EventArgs* class is an empty class designed to be a base class for the event arguments (extra information of the event) that are going to be passed from the publisher to the subscriber.

-  **Simple events** use *EventArgs* objects to pass the event arguments to the subscriber, due *EventArgs* is an empty class, no arguments are passed to the subscriber, this is the reason why these events are the simplest to implement and the ones used for *property changed* events, they only notify an specific property change and that is it. Worth mentioning *property changed* events are not the only use for these event types, it is just a use case example

-  **Events with arguments** use a custom class that inherit from *EventArgs* class to describe what arguments are going to be passed to the subscriber, the arguments passed to the subscriber are passed as read_only properties (properties with only getter). In this way if the event is a little bit more complex and a **simple event** is not enough, you can use a custom EventArgs that contain your information. As a use case example imagine an event called *Moved*, this event notifies when the object moves, but maybe only notify the movement is not enough and we want to inform how much the object moves, this is a perfect use for our custom *EventArgs* class:

```python
class Vector:
    '''
    designed to describe a distance in 2 dimensions
    '''
    _i:int
    _j:int

    def __init__(self,i:int,j:int)->None:
        self._i =i
        self._j =j 

    @property
    def I(self)->int:
        return self._i
    
    @property
    def J(self)->int:
        return self._j 

    def __str__(self)->str:
        return "%d i, %d j" % (self.I,self.J)



class MovedEventArgs(EventArgs): # example of Custom EventArgs to pass event information (distance moved in this case)
    
    _delta:Vector

    def __init__(self,delta:Vector)->None: # Request the distance of the movement
        super().__init__()
        self._delta = delta # Save the distance

    @property
    def Delta(self)->Vector: #encapsulate the value and placing its getter
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


- **Simple events**

```python
from python_sharp import *

class Person: #class that is going to implement an event

  def __init__(self, name): # we request a name for the person
    self._name = name # store the name
    self._namechanged_callbacks = Delegate() # we create a delegate to store callables

  @property # define a getter for name
  def Name(self):
    return self._name

  @Name.setter # define a setter for name
  def Name(self,value):
    self._name = value
    self._OnNameChanged(EventArgs()) # We execute out internal logic (if any) when the name is changed

  def _OnNameChanged(e:EventArgs): # define a method that execute necesarry code when the name change (if any)
    # execute internal logic when the name change (if any)
    self.self._namechanged_callbacks(self,e) #execute external logic # execute the callbacks stored in self._namechanged_callbacks

  @event #define an adder for NameChanged (describes how a callable should be added into our delegate)
  def NameChanged(self,value):
    self._namechanged_callbacks += value # in this case there is no more logic than add the callable to the delegate

  @NameChanged.remove #define an remover for NameChanged (describes how a callable should be removed from our delegate)
  def NameChanged(self,value):
    self._namechanged_callbacks += value

def person_NameChanged(sender:object,e:EventArgs):
  print("person change its name to %s" % sender.Name)

person = Person("Juan") #creates a new person
person += person_NameChanged # subscribe person_NameChanged into the NameChanged event. (person_NameChanged is our callable that is going to be added to a delegate, in order to know how to add it += operator will call the function under @event decorator and pass the callable as the parameter 'value') 
person.Name = "Carlos" #Change the person Name, this will cause execute Name setter->_OnNamechanged->execute the delegate which contains "person_NameChanged" function printing the message
person -= person_NameChanged #unsucribe the function, the operator -= wil cause execute the method under @NameChanged.remove decorator in order to know how a callable should be removed, person_NameChanged will be passed as 'value' parammeter
person.Name = "Something" # As person_NameChanged is not subcribed to the event is not going to be executed.
```

(suggested signature and value parametter documentation)
  

  ### Static properties

  
