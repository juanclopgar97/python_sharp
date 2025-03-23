![Python Sharp Logo](https://raw.githubusercontent.com/juanclopgar97/python_sharp/refs/heads/master/documentation_images/python_sharp.png)

```python
    def project_finished(sender:object,e:EventArgs)->None:
      print("Develop is fun!!!")

    project = Project() 
    project.finished += project_finished
    project.finish()

```
```
"Develop is fun!!!"
```

# Python# (Python sharp)

## Table of Contents
1. [Introduction](#Introduction)
2. [Installation](#Installation)
3. [Tools and support](#tools-and-support)
4. [Important disclaimer](#important-disclaimer)
5. [Use cases and examples](#Use-cases-and-examples)
    1. [Delegates](#Delegates)
        1. [How to add callables into a Delegate](#How-to-add-callables-into-a-Delegate)
        2. [How to get returned values of callables out of a Delegate](#How-to-get-returned-values-of-callables-out-of-a-Delegate)
        3. [Delegates Summary](#Delegates-Summary)
    2. [Events](#Events)
        1. [EventArgs, CustomEventArgs and CancellableEventArgs class](#eventargs-customeventargs-and-cancellableeventargs-class)
        2. [Implementation](#Implementation)
            1. [Simple events](#Simple-events)
            2. [Events with arguments](#Events-with-arguments)
            3. [Events with modifiable arguments](#Events-with-modifiable-arguments)
            4. [Implementation summary](#implementation-summary)
    3. [Static events](#Static-events)

## Introduction

python# (python sharp) module was created with the intention of adding EOP (event oriented programming) into python in the most native feeling, easy syntax way possible.

EOP is a programming paradigm that allows execute actions (code) based on "doings" or events, this is really useful when you have to execute specific actions when something happens but you do not have the certainty when or how many times is going to happen.

This module was thought to accomplish EOP with 2 objectives in mind:

1. Features should look and feel like a native python feature.
2. Implementation should be based in another famous EOP language to decrease learning curve and improve user experience.

Events are just another possible way to declare a class member like: fields/attributes, properties and methods, python already have a way to define a property with **@property**, this helps to define objective number 1, for this reason events are implemented with **@event** syntax to be consistent with python:

```python #5
class Person:
  def __init__(self,name:str)->None:
    self._name = name

  @property
  def name(self)->str: 
        return self._name

  @name.setter 
  def name(self,value:str)->None:
        self._name = value

  @event
  def name_changed(self,value)->None:
    #some implementation
    pass
```

For objective 2, the module was architected thinking in how another EOP language (in this case C#) implements its events. This implementation will be explained below, keep in mind this is a really simplified explanation of how C# events actually work, if you are interested in learn how they work exactly please go to C# documentation. With this clarified, let's move on to the explanation: 

1. C# implements events as a collection of callbacks that will be executed in some point of time, this collection of functions are called **Delegates**, invoking(executing) the delegate will cause the execution of all functions(callables) in its collection.

2. delegates are not commonly exposed publicly, due security reasons. As the fields/attributes in a class have to be encapsulated, delegates as well, and the way to encapsulate them is with events. Fields/attributes are to properties as delegates are to events.

3. Properties encapsulate fields/attributes with 2 functions/methods called "get" and "set", which define the logic of how data should be GET and SET out of the object, in C# events encapsulate delegates with 2 functions as well called "add" and "remove", which define the logic of how functions/subscribers should be added or removed out of the delegate.


## Installation

### Requirements

- **Python**: Version 3.6 or higher
- **pip**: Python package manager

To install `python_sharp` you can follow either of the options listed:

### Disclaimer

version 1.0.0 is only available through GitHub PyPI does not contain that version.

### 1. Clone the Repository 
If you want to explore the source code, you can clone the repository:
```bash
git clone https://github.com/juanclopgar97/python_sharp.git
cd python_sharp
```

### 2. Install the package directly from GitHub using pip:

```bash
pip install git+https://github.com/juanclopgar97/python_sharp.git
```

from a specific branch/commit/version:

```bash
pip install git+https://github.com/juanclopgar97/python_sharp.git@<branch_or_commit_or_version>
```

Example:

```bash
pip install git+https://github.com/juanclopgar97/python_sharp.git@v1.0.0
```

### 3. Install from PyPI

```bash
pip install python_sharp
```
or select your version

```bash
pip install python_sharp==<version>
```

Example:

```bash
pip install python_sharp==1.0.1
```
Upgrade it:

```bash
pip install python-sharp --upgrade
```


### Usage

```python
from python_sharp import *

#your code
```

## Tools and support

Currently there is an upcoming effort to create a VS code extension to deliver a better experience while using python sharp, an example of this is a custom OUTLINE to visualize *@property* and *@event* with its corresponding icons as the next image shows:

![outline support](https://raw.githubusercontent.com/juanclopgar97/python_sharp/refs/heads/master/documentation_images/outline_support.png)

and so much more!, if you want to see it come true you can show interest using and spreading the use of python sharp, this will help to add more support to the project.

To create an enhancement request, report a bug, raise a question etc. you can use the [issues](https://github.com/juanclopgar97/python_sharp/issues) section of this repository with the corresponding labels **enhancement**, **bug**, **question** etc. in this way collaborators can check for the request and attend it.

## Important disclaimer

In some parts of this documentation you will find the words "**HIGHLY RECOMMENDED**", this words are used to highlight some important use aspects of python sharp.

The omission of "**HIGHLY RECOMMENDED**" conventions (like naming conventions, or implementation conventions) might not break your code and it might be work without them, even you might found a way to create your own way to implement them, HOWEVER, this could lead to readability, clarity, maintenance and scalability issues of the code. 

For this reason always **FOLLOW THE CONVENTIONS** due this is necessary to keep the readability, clarity, maintenance and scalability of your code, in this way other collaborators can go over your code easily and improve the work flow.


## Use cases and examples:

In this repository there are 2 main files "python_sharp.py" (which is the module file) and "test.py". This last file contains all the features applied into one single script, this could be really useful if you want to do a quick check about how something is implemented, however, due it is a "testing" script and not a "walk through" it could be confusing if you do not know what is going on, so it is **Highly recommended** read the below documentation which explains step by step how to implement every single feature in the module.

### Delegates

Python sharp Delegates are a list of callables with the same signature, when a delegate is being executed (delegates are callable objects), it executes every single callable in its list.

#### How to add callables into a Delegate
It is really important to keep the callables added into the delegate with consistent signatures due parameters passed to the delegate when is being executed are the same ones passed to every single callable in the collection, so if one callable signature is expecting only 2 parameters and the next callable 3 parameters this is going to cause a TypeError that might look like this: 

```python
from python_sharp import *

def function_1(parameter_1:int): # defining a function with 1 parameter (int type)
  print("function 1")

def function_2(parameter_1:int,parameter_2:str): # defining a function with 2 parameters (int,str types)
  print("function 2")

delegate = Delegate() #creating a Delegate
delegate += function_1 #adding function_1
delegate += function_2 #adding function_2

delegate(5) # executing the delegate with only 1 parameter

```

OUTPUT:
```
function 1
Traceback (most recent call last):
  File "c:\PATH\test.py", line 341, in <module>
    delegate(5) # executing the delegate with only 1 parameter
    ^^^^^^^^^^^
  File "c:\PATH\python_sharp.py", line 72, in __call__
    results.append(callable( *args, **kwds))
                   ^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: function_2() missing 1 required positional argument: 'parameter_2'
```

Here *function_1* was executed correctly due the signature of the function match with how the delegate was executed (passing only one integer "5"), and *function_2* was expecting a second string parameter resulting in a TypeError. So, it is really important keep signatures in a homogeneous manner.

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

As summary, Delegates are really useful to execute a bulk of callables, and its return values (if any) are returned by the delegate in a tuple.

### Events

In programming, an event refers to an action or occurrence that a program can detect and respond to. Events can be triggered by user interactions (like clicking a button, typing text, or moving a mouse), system-generated activities (like a file being updated or a timer expiring), or even messages from other parts of the program. Typically, an event is associated with subscribers (event listeners) which are functions or blocks of code designed to execute when the specific event occurs.

Events are commonly part of an event-driven programming paradigm, where the flow of the program is determined by these events.

Events can be implemented as members of an instance or a class (static events) on different ways, in this module we can group this "ways" into 3 main implementations:

1. **Simple events** (Normally implemented as *property changed* events):
  These events only "notify" that something relevant happens, they do not provide extra information about the event like: How, When, Why etc.
  
  Name convention for this events is: [optional subject or adjective] +  VERB + 'ed' (past simple).

  Examples:

  - name_changed (this is an example of property change implementation in this case for *name* property)
  - location_changed (this is an example of property change implementation in this case for *location* property)
  - moved
  - executed

2. **Events with arguments**:
  This events are like *simple events* but they are capable of provide extra information about the event like: How, When, Why etc, to the subscribers through a parameter. They follow the same name convention as *simple events*.

3. **Events with modifiable arguments** (Normally implemented as *pre-events*)

  *Events with modifiable arguments* are most likely implemented as **pre-events** this means the event advertise something that is about to happen, and it will let the subscribers provide information to determine the future, like cancelling what was about to happen or modify how it was going to be done.

  Name convention for this events is: [optional subject or adjective] + VERB + 'ing' (present continuous).

  Examples:

  - name_changing 
  - house_changing 
  - moving
  - executing

  - Another example to clarify this could be an event called "window_closing", this event will notify that a window is about to close, the subscribers will have the power to pass information through the event arguments to cancel or modify the incoming action (in this case the window closing), this is really useful if the changes in the app are not saved.


  In some rare occasions these name conventions will not satisfy your necessities to name your events due they don't describe properly what your events are going to do, and it is fine to name them as you want, however, is **HIGHLY RECOMMENDED** use these name conventions as much as possible, due this would lead to better readability, clarity, maintenance and scalability of the code, so, if you can name your events under the suggested name conventions **DO IT**, only use your own naming conventions if the naming conventions described in this document do not fit with what your event is going to do. 


#### EventArgs, CustomEventArgs and CancellableEventArgs class

*EventArgs* class is an empty class designed to be a base class to pass the event arguments, these arguments are going to be passed from the publisher to the subscriber in order to provide more information about what happens.

-  **Simple events** use *EventArgs* objects to pass the event arguments to the subscriber, due *EventArgs* is an empty class, no arguments are passed to the subscriber, this is the reason why these events are the simplest to implement and the ones used for *property changed* events, they only notify something happens and that's it, no more information. Worth mentioning *property changed* events are not the only use for these event types, it is just a use case example

-  **Events with arguments** use a custom class that inherit from *EventArgs* class to describe what arguments are going to be passed to the subscriber. The arguments passed to the subscriber are passed as read_only properties (properties with only getter). If a **simple event** is not enough, you might need an **Event with arguments**, in this case, you can use a custom EventArgs that contains your arguments.

    As a use case example imagine an event called *moved*, this event notifies when the object moves, but maybe only notify the movement is not enough and we want to inform how much the object moves, this is a perfect use for our custom *EventArgs* class:


    ```python
    class MovedEventArgs(EventArgs): # example of Custom EventArgs to pass event information (distance moved in this case)

        _delta:int

        def __init__(self,delta:int)->None: # Request the distance of the movement
            super().__init__()
            self._delta = delta # Save the distance

        @property
        def delta(self)->int: #encapsulate the value and placing its getter
            return self._delta
    ```

- **Events with modifiable arguments** use a custom class that inherit from *EventArgs* class to describe what arguments are going to be passed from the subscriber to the publisher, this module already include one example of this approach *CancellableEventargs*:

    ```python
    
    class CancellableEventArgs(EventArgs):
    
        _cancel:bool
    
        def __init__(self)->None:
            super().__init__()
            self._cancel = False 
    
        
        @property
        def cancel(self)->bool: #to show the value of _cancel attribute
            return self._cancel
        
        @cancel.setter
        def cancel(self,value:bool)->None: #to let the subscriber set a value into _cancel
            self._cancel = value
    ```

    as you can see, this implementation is really similar to **Events with arguments**, the only difference is we are placing a setter method to let modify the cancel value, this value can be used for the publisher at the end of the execution of all the callbacks stored.

    It is **REALLY IMPORTANT** to remark, CancellableEventArgs is only an example of an *EventArgs* used for **Events with modifiable arguments** and is not the only way to implement it, you don't even need to inherit necessarily from it. In order to consider an *EventArgs* used for **Events with modifiable arguments** it has to implement a setter on it, in this way this new *EventArgs* can provide and store information about the event, and this information can be used by the publisher and subscribers. Another way to see it is as a bidirectional channel to communicate the publisher and subscribers, publisher can provide information with the getters and subscribers can store information in it with the setters.


#### Implementation

Below this text, the use cases and explanation about the events are shown, please read the examples and after READ THE EXPLANATION OF THE EXAMPLE CODE, this is really important because it specifies step by step the "WHY"s of the implementation.

##### Simple events

  ```python
  from python_sharp import *

  class Person: 
    
    def __init__(self, name:str)->None: 
      self._name = name 
      self._name_changed = Delegate() #collection of future callbacks

    @property 
    def name(self)->str:
      return self._name

    @name.setter 
    def name(self,value:str)->None:
      self._name = value
      self._on_name_changed(EventArgs()) 

    def _on_name_changed(self,e:EventArgs)->None:
      self._name_changed(self,e) 

    @event 
    def name_changed(self,value)->None: # This example doesn't contain the parameter annotations for simplicity due it is the first example, however (as the document will explain in the summary of simple events), it is really important to place the event annotations. (There is a link at the end of this code block to go to the explanation)
      self._name_changed += value

    @name_changed.remove
    def name_changed(self,value)->None: # Annotations are not included for simplicity due it is the first example
      self._name_changed -= value 


  def person_name_changed(sender:object,e:EventArgs)->None:
    print("person change its name to %s" % sender.name)

  person = Person("Juan")
  person.name_changed += person_name_changed 
  person.name = "Carlos" 
  person.name_changed -= person_name_changed 
  person.name = "Something" 
  ```

  OUTPUT
  ```
  person change its name to Carlos
  ```

[Link to event annotation convention explanation](#event-annotation-convention)

*"simple events"* "notify" that something relevant happens, they do not provide extra information about the event like why, when, where, etc.

On this example an event *name_changed* is implemented to notify when the person's name change.

To implement a *simple event* the first thing you have to do is create a variable to store the subscribers, look at this variable as a "To do list" due it contains the callables that are going to be executed at some specific time.

```python
self._name_changed = Delegate() # it can be viewed as a "To do list"
```

As you might notice the variable that is going to store the subscribers is a Delegate and the name starts with '_' to "protect" the attribute. Expose the attribute "publicly" is not a good practice, due other part of the code can manipulate the attribute wrongly or get/set information in a way that was not mean to. To fix this, we can define 2 methods to encapsulate the delegate (add/remove methods), Through these 2 methods the other objects in the code can subscribe/unsubscribe (add/remove) callables to our delegate.

```python
  @event 
  def name_changed(self,value)->None:
    self._name_changed += value # add the new callable to the attribute with a delegate

  @name_changed.remove
  def name_changed(self,value)->None:
    self._name_changed -= value # remove the callable to the attribute with a delegate
```

Code above implements add/remove logic to the delegate. Function below *@event* decorator defines the logic for the *add* or how a callable should be added to our "To do list". Function below *@name_changed.remove* defines the logic for the *remove* or how a callable should be removed from the delegate

Notice the functions HAVE to be named exactly with the same name, and if an *@event* is defined you **must** implement *@IDENTIFIER.remove* or the code will throw a traceback, this is to protect the integrity of the code and provide instructions about how to add AND remove a callable.

The callable to be added/removed will be passed through the "value" parameter. Notice in this example "value" parameter doesn't have any type annotation, this is only to keep this first example "simple/readable" at first sight, however it is **HIGHLY RECOMMENDED** annotate the type as the following examples on this document (Events with arguments or Events with modifiable arguments examples contain these annnotations), due this is the way to indicate clearly what is the signature expected from the event to their subscribers (callables). [Link to event annotation convention explanation](#event-annotation-convention)

Once this is in place, we have:

- A place to store the callables 
- Logic to let to other parts of the code add/remove callables

Now we need to execute the callables in the right momment, in this case the event is called "name_changed" so the callables should be executed when the name changes, this means our extra logic needs to be added in the *name* setter due that is the part of the code that has this responsability (change the person's name).

```python
  @name.setter 
  def name(self,value:str)->None:
    self._name = value
    # execute our "To do list" or delegate
```

In the snippet code above the comment defines where the "To do list" needs to be executed, however, sometimes the own object needs to implement its own logic when (in this case) the property *name* change, for this purpose is **HIGHLY RECOMMENDED** as a good practice define another function/method called "\_on\_[EVENT NAME]"

```python
  @name.setter 
  def name(self,value:str)->None:
    self._name = value
    self._on_name_changed()

  def _on_name_changed(self)->None:
    #logic when the name change (if any)
    self._name_changed() #external logic
```
Inside of this method the own internal and external logic when the name change must be implemented, in other words, *What as a Person I need to do when my name changes?* (own/internal logic), and after, attend external logic (To do list) in other words instructionss provided by other objects or parts of the code. *What others needs to do when my name changes?*

In this case the class Person doesn't need to do "something" when the name changes (internal logic), so we only need to execute the external logic (execute the delegate)


Now we have a way to add/remove subscribers and trigger the event, however, you might notice the code above is not exactly the same as the example code, this is because despite the event is now implemented and working is not following a good practice CONVENTION. So even with a working code, is **HIGHLY RECOMMENDED** follow next convention:

```python
  @name.setter 
  def name(self,value:str)->None:
    self._name = value
    self._on_name_changed(EventArgs())

  def _on_name_changed(self,e:EventArgs)->None:
    #internal logic if any
    self._name_changed(self,e)
```

You can notice 2 things

1. *\_on\_name_changed* now requires a parameter called 'e' which is an EventArgs, this is a safety implementation, every "\_on\_[EVENT NAME]" must require an EventArgs (or any other class that inherits from it), this is a way to say "Are you sure the event happens? show me the evidence!", in this case there is no arguments so the evidence is an empty *EventArgs* object. *EventArgs* object is used first for the internal logic and then passed to the external logic as a parameter.

2. 'self' is passed to the external logic as first parameter, this is to allow the subscribers know 'Who is executing my piece of code"



**As summary:** 

- There are 2 main sections to implement when you want to define an event: 

    1. Part that store and define how to add/remove callables
    2. Part that executes/trigger those callables stored

<a id="event-annotation-convention"></a>
- There are conventions about how the logic must be implemented to facilitate readability and maintenance of the code.

- Callables to be subscribed to a simple event should follow the next signature:

    *Callable[[object, EventArgs], None]* (a callable with 2 parameters, first one contains the publisher and second the event arguments, the function must return None)

The next snipped code shows and example of how the *simple events* should be implemented with the **HIGHLY RECOMMENDED** event annotation convention: 

```python
  @event 
  def name_changed(self,value:Callable[[object, EventArgs], None])->None:
    self._name_changed += value

  @name_changed.remove
  def name_changed(self,value:Callable[[object, EventArgs], None])->None:
    self._name_changed -= value 
```

This is done with the intention of clarify what is the event expecting from its subscribers signature.

The omission of this event annotation convention do not affect how the code works, however, it could lead to problems of readability, clarity, maintenance and scalability. For these reasons **ALWAYS** place the event annotations, this is the only way for the event to communicate what is he expecting from its subscribers.


To use the event:

```python
def person_name_changed(sender:object,e:EventArgs)->None: #function to be executed when the name changes (subscriber)
  print("person change its name to %s" % sender.name)

person = Person("Juan")  #creates a person
person.name_changed += person_name_changed # we add 'person_name_changed' (subscriber) to event name_changed of 'person', this line will execute function under @event decorator (add function)
person.name = "Carlos" # change the name to trigger the event (this will execute 'person_name_changed') 
person.name_changed -= person_name_changed #unsubcribe the function, this line will execute function under @name_changed.remove decorator (remove function)
person.name = "Something" # change the name again to prove 'person_name_changed' is not executed anymore
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
    def delta(self)->int:
      return self._delta


  class Person:
    
    def __init__(self)->None:
      self._location = 0
      self._moved = Delegate()

    @property
    def location(self)->int:
      return self._location

    @location.setter
    def location(self,value:int)->None:      
      previous = self.location 
      self._location = value
      self._on_moved(MovedEventArgs(self.location - previous))

    def move(self,distance:int)->None:
      self.location += distance

    def _on_moved(self,e:MovedEventArgs)->None:
      self._moved(self,e)

    @event 
    def moved(self,value:Callable[[object, MovedEventArgs], None])->None:
      self._moved += value

    @moved.remove
    def moved(self,value:Callable[[object, MovedEventArgs], None])->None:
      self._moved -= value  


  def person_moved(sender:object,e:MovedEventArgs)->None:
    print("Person moves %d units" % e.delta)

  person = Person()
  person.move(15)
  person.moved += person_moved
  person.location = 25
  person.moved -= person_moved
  person.location = 0
  ```

  OUTPUT
  ```
  Person moves 10 units
  ```

*Events with arguments* are almost the same as *simple events* so, the next explanation will only address the differences between the 2 cases.

On this example an event named "moved" is implemented to notify when a person moves and provide how much does the person move.

```python
class MovedEventArgs(EventArgs):

  _delta:int

  def __init__(self,delta:int)->None:
    super().__init__()
    self._delta = delta

  @property
  def delta(self)->int:
    return self._delta
```

In this case a custom EventArgs is created in order to be capable of store the event arguments, on this example the event is named "moved", and is going to be triggered when the person changes its location, in addition, it will provide HOW MUCH the person moves, this is the job of the *MovedEventArgs* and the main difference with a *simple event*.

In the next code block we can see how the event is being defined:

```python
  @event 
  def moved(self,value:Callable[[object, MovedEventArgs], None])->None:
    self._moved += value

  @moved.remove
  def moved(self,value:Callable[[object, MovedEventArgs], None])->None:
    self._moved -= value  
```

in this case the only difference is the 'value' parameter annotation,  this indicates that the event requires a *Callable[[object, MovedEventArgs], None]* subscriber signature, in other words a *MovedEventArgs* will be provided to the subscriber.

It is **HIGHLY IMPORTANT** to realize *moved* event signature is *Callable[[object, MovedEventArgs], None]* therefore it can accept subscribers with the next signatures:

- *Callable[[object, MovedEventArgs], None]*
- *Callable[[object, EventArgs], None]*

This 2 signatures are ok due polymorphism, it can be confusing due at first sight seems like we are assigning an *EventArgs* objeect to a *MovedEventArgs* variable (*MovedEventArgs* <- *EventArgs*), this case in OOP (Object Oriented programming) is not valid, due it might throw a Traceback if a *MovedEventArgs* member is trying to be accessed in a *EventArgs* object. 

However in this example is not the case, the subscriber with *Callable[[object, EventArgs], None]* signature defines how the parameter object is going to be treated by the callable, in this case, the parameter will be used/treated as an *EventArgs*, and the event will provide a *MovedEventArgs* object to the callable so in reallity we are assigning a *MovedEventArgs* object to an *EventArgs* variable (*EventArgs* <- *MovedEventArgs*) which by polymorphism will not cause any issue trying to access any of the *EventArgs* members in a *MovedEventArgs* object.

Next code block explains a general case for what was explained above (subscriber signatures accepted by an event).

"..." indicates that there is code is being omitted due it is not relevant to show the desire concept:

```python
class EventArgs:...
class FirstCustomEventArgs(EventArgs):...
class SecondCustomEventArgs(FirstCustomEventArgs):...
class ThirdCustomEventArgs(SecondCustomEventArgs):...
class FourthCustomEventArgs(ThirdCustomEventArgs):...
class FifthCustomEventArgs(FourthCustomEventArgs):...

class MyClassPublisher:

  @event
  def event_name(self,value:Callable[[object,ThirdCustomEventArgs],None])->None:... #Example event that will provide a ThirdCustomEventArgs object to its subscribers.
  ...


def subscriber(sender:object,e:EventArgs)->None: ...                # Assignable
def subscriber_1(sender:object,e:FirstCustomEventArgs)->None: ...   # Assignable
def subscriber_2(sender:object,e:SecondCustomEventArgs)->None: ...  # Assignable
def subscriber_3(sender:object,e:ThirdCustomEventArgs)->None: ...   # Assignable
def subscriber_4(sender:object,e:FourthCustomEventArgs)->None: ...  # NO assignable
def subscriber_5(sender:object,e:FifthCustomEventArgs)->None: ...   # NO assignable


publisher = new MyClassPublisher()

publisher.event_name += subscriber    # Correct
publisher.event_name += subscriber_1  # Correct
publisher.event_name += subscriber_2  # Correct
publisher.event_name += subscriber_3  # Correct
publisher.event_name += subscriber_4  # Wrong
publisher.event_name += subscriber_5  # Wrong

```

This feature allow you to have a subscriber being able to subscribe to a huge variety of event signatures, for example, if you have a piece of logic that needs to be executed by 2 events with different signatures is totally possible.

In order to get advantage of this, you need to keep in mind what is going to be the subscriber signature, if your subscriber signature is closer to *EventArgs* it is going to be more probable to be compatible with more event signatures. So as a good practice try to keep your *EventArgs* parameter as close as *EventArgs* possible.

Example:

If you create a subscriber for an event with a signature *Callable[[object, ThirdCustomEventArgs],None]* and you do not need any specific information of a *ThirdCustomEventArgs* in your subsciber logic, you can consider lower your *EventArgs* to *SecondCustomEventArgs* (get closer to *EcentArgs*) or even lower, depending on what information you require in your subscriber logic, in this way your subscriber will be compatible with more event signatures in case you want to assign it to another events with different signature.


Subscribers naming convention is not rigid, however it is **HIGHLY RECOMMENDED** that the name expresses in some way what is going to trigger its execution, most of the cases can be accomplish with:

 "[your identifier]_[event name(s)]"

 - persons_name_changed
 - elements_moved
 - compenents_rendering

 In that way is easy to understand/know what is going to cause the subscriber execution due its name contains the name of its triggers (event names).


And the last difference but not less important is how the event is going to be triggered:

```python
  @location.setter
  def location(self,value:int)->None:      
    previous = self.location 
    self._location = value
    self._on_moved(MovedEventArgs(self.location - previous))

  def _on_moved(self,e:MovedEventArgs)->None:
    self._moved(self,e)
```

We can see in the code block above now *\_on\_moved* method now requires a *MovedEventArgs*, as *simple events* did, this is for security reasons, if we are going to execute *\_on\_moved* method because the event happens, that is a way to say "prove it or show the evidence!".

Second difference is when *location* settter is calling *\_on\_moved* method, now it needs to create an instance of *MovedEventArgs* and to do so, it requires a quantity to be passed to the constructor, this quantity of "how much the person moves" can be calculated with a subtraction of previous and current location.


**As summary:** 

*Events with arguments* and *simple arguments* are really similar and there are only some differences:

- Needs a custom *EventArgs* class defined.
- Events with custom *EventArgs* can accept different subscriber signatures
- \_on\_[Event name] method uses the custom *EventArgs* class and this causes an extra security layer
- Trigger code now needs to create an instance of the new custom *EventArgs* and to do so, it needs to provide/calculate the arguments needed by the custom *EventArgs* constructor


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
    def value(self)->int:
      return self._value


  class Person:
    
    def __init__(self)->None:
      self._location = 0
      self._location_changing = Delegate()

    @property
    def location(self)->int:
      return self._location

    @location.setter
    def location(self,value:int)->None:
      locationEventArgs = LocationChangingEventArgs(value)
      self._on_location_changing(locationEventArgs)

      if(not locationEventArgs.cancel):
        self._location = value


    def _on_location_changing(self,e:LocationChangingEventArgs)->None:
      self._location_changing(self,e)


    @event
    def location_changing(self,value:Callable[[object, LocationChangingEventArgs], None])->None:
      self._location_changing += value

    @location_changing.remove
    def location_changing(self,value:Callable[[object, LocationChangingEventArgs], None])->None:
      self._location_changing -= value


  def person_location_changing(sender:object,e:LocationChangingEventArgs):
    if e.value > 100:
      e.cancel = True

  person = Person()
  person.location = 50
  person.location_changing += person_location_changing
  person.location = 150
  print(person.location)
  ```

 OUTPUT
 ```
 50
 ```

*Events with modifiable arguments* are really similar to *Events with arguments* this explanation will address only the differences, so if you have doubts about the implementation go back to that section. 

*Events with modifiable arguments* are most likely implemented as **pre-events** this means the event advertise something that is about to happen, and it will let the subscribers provide information (Thorugh a custom *EventArgs*) to determine the future, like cancelling what was about to happen or modify how it was going to be done.

On this example an event named "location_changing" is implemented to notify when the person's location is about to be changed, this will let the subscribers cancel or modify the future behavior of that action.

Key difference is the way the custom *EventArgs* is defined:

```python
class CancellableEventArgs(EventArgs): #Defined already on python_sharp module
  
  _cancel:bool

  def __init__(self)->None:
    super().__init__()
    self._cancel = False 

    
  @property
  def cancel(self)->bool:
    return self._cancel
    
  @cancel.setter
  def cancel(self,value:bool)->None:
    self._cancel = value


class LocationChangingEventArgs(CancellableEventArgs):

  _value:int

  def __init__(self,value:int)->None:
    super().__init__()
    self._value = value

  @property
  def value(self)->int:
    return self._value
```

As you can see our custom *EventArgs* is *LocationChangingEventArgs* this class inherits from *CancellableEventArgs*, an *IMPORTANT* remark is Inherit from *CancellableEventArgs* is not necessary to create an *Event with modifiable argument*. *CancellableEventArgs* is just a built in custom *EventArgs* used for *Event with modifiable argument*, the fact *LocationChangingEventArgs* inherits from it is just to show case a use of it.

Key factor to know when an event is an *Event with modifiable argument* is if the ***EventArgs* class class contains a property with a setter**.

*LocationChangingEventArgs* does not contain a property with a setter by itself, but due it inherits from an *EventArgs* which contains it (*CancellableEventArgs*), we can consider that *LocationChangingEventArgs* actually contains a property with a setter.

For this particular example *cancel* property is set to *False* by default, when the  *EventArgs* object is passed to the subscribers now they have the ability to change *cancel* value property:

```python
def person_location_changing(sender:object,e:LocationChangingEventArgs):
  if e.value > 100:
    e.cancel = True
```

In the code block above is shown how the subscriber uses *e.value* to determine if *e.cancel* is going to be set to *True*, subsequently the publisher can use this value to modify some behavior:

```python
  @location.setter
  def location(self,value:int)->None:
    locationEventArgs = LocationChangingEventArgs(value)
    self._on_location_changing(locationEventArgs)

    if(not locationEventArgs.cancel):
      self._location = value
```

Code above shows how the *LocationChangingEventArgs* is created and stored in *locationEventArgs* variable in order to keep a reference to the object, once that is done, the *LocationChangingEventArgs* object is send to *\_on\_location_changing* method to execute internal and external logic (external logic will execute all subscribers that might change *cancel* property value), and at the end of the  *\_on\_location_changing* execution we can check the *locationEventArgs* variable to evaluate if the *LocationChangingEventArgs* object *cancel* property is *True* or *False*, with this value we can alter the code behavior. For this particular example *cancel* property is being use to determine if the person should change its location or not


##### Implementation summary

In the Implementation section there were examples about how to implement every single "flavor"/type of event, however the subscribers shown in those examples where a simple function that matches the event signature to keep the examples as understanding as possible. 

It is important to remember that:

- A subscriber can be subscribed to different event signatures
- you can subscribe any callable to an event: function, method, class with \_\_call\_\_ implemented or even another delegate.
- When a class contains a callable that is going to be subscribed to an event, and the subscription (+= operator over the event) is going to happen inside of the same class, is **HIGHLY RECOMMENDED** to keep the subscriber protected with "_" at the beginning of the subscriber identifier if the logic contained there is only of the class interest (only the class makes use of that logic).

### Static events

Static events are almost the same as the events described previoulsy, they can be implemented as well as "simple events", "with arguments" or "with modifiable arguments", key difference is the event is applied as a class event, no an instance event.

For this section the example provided is a *simple static event* due it is the simplest way to show the differences, in case you want implement a *static event with arguments* go back to [Events with arguments](#Events-with-arguments) section and apply it to the class instead of the instance as the example of *simple static event* shows.

Imagine a class that provides the number of instances that it creates, this variable should be defined as an *static variable*, due there is no necessity for every single class instance to contain the same exactly number, and even worse, if the number changes it needs to be updated on every single instance created , that is the reason why this variable should be implemented as *static variable*.

Now imagine we want to notify when an instance is created, in other words when the *static variable* changes its value, as this event is going to notify something is going on with a static variable, we need a static event:

```python
from python_sharp import *

class Person:
    
  _instance_created:int = 0
  _person_created:Delegate = Delegate()

  def __init__(self)->None:
    Person._on_person_created(EventArgs())

  @staticmethod
  def get_instance_created()->int:
    return Person._instance_created
    
  @staticmethod
  def _set_instance_created(value:int)->None:
    Person._instance_created = value


  @staticmethod
  def _on_person_created(e:EventArgs)->None:
    Person._set_instance_created(Person.get_instance_created() + 1)
    Person._person_created(None,e)
        
  @staticevent
  def person_created(value:Callable[[object, EventArgs], None])->None:
    Person._person_created += value

  @person_created.remove
  def person_created(value:Callable[[object, EventArgs], None])->None:
    Person._person_created -= value

def person_created(sender:object,e:EventArgs)->None:
  print("There are %d persons created" % Person.get_instance_created())

person_1 = Person()
person_2 = Person()

Person.person_created += person_created

person_3 = Person()
```

OUTPUT
```
There are 3 persons created
```

As you can see a *simple event* implementation is almost identical to *simple static event*

Key differences:

- All members used (variable, methods and event) are static (use of @staticevent instead of @event)
- Get/Set methods to encapsulate the static variable are implemented as static methods due a lack of static properties python implementation

And that is it, those are all differences, so if you have questions about how this code works, is **HIGHLY RECOMMENDED** go back to [Events](#Events) section or raise a question on the [issues](https://github.com/juanclopgar97/python_sharp/issues) section of this repository.
