===========
DevReminder
===========

- `Project Description`_

- `Installation`_

- `How to Use`_

- `Examples`_

- `General Info`_

- `Contribution`_

- `License`_


====================
Project Description
====================

DevReminder is a pure python project that works as a reminder for developers who are engaged in fields having long execution time such as machine learning and deep learning.

It has `own REST API`_ and uses `Telegram bot API`_ as interface. Telegram is a mobile and desktop messaging app. Thereby, this project offers developers to be aware of running code's status using their mobile phone.


.. _`own REST API`: https://devreminderapi.herokuapp.com/welcome
.. _`Telegram bot API`: https://core.telegram.org/bots/api


Source code available at https://github.com/cagataygulten/devreminder

============
Installation
============
Install package by pip::

  pip install devreminder

Or you can install from source with::

  $ git clone https://github.com/cagataygulten/devreminder
  $ cd devreminder
  $ python setup.py install


And install telegram application on your mobile phone.

==========
How to Use
==========

STEP 1: Open Telegram application, type DevReminder in search field.

|

.. image:: https://github.com/cagataygulten/devreminder/blob/master/pic/picture1.JPG?raw=true

|

STEP 2: Start a chat with DevReminder bot.

|

.. image:: https://github.com/cagataygulten/devreminder/blob/master/pic/picture2.JPG?raw=true

|

STEP 3: Then copy your chat id.

Turn back to IDE and import devreminder package, call class with three arguments and use "me" function to trigger bot::

    from devreminder import DevReminder

    remind = DevReminder(chat_id = 1932126911, auto_remind = False , time_threshold = 0)
    remind.me("Test")


Output:

.. image:: https://github.com/cagataygulten/devreminder/blob/master/pic/picture3.JPG?raw=true

|

Class Arguments:

Auto remind: If auto remind mode is activated, bot reminds after every executed cell in Ipython. Not suitable for python interpreter.


Time threshold: DevReminder Bot only reminds if the execution time is greater than given threshold value as seconds. It is useful when combined with auto remind mode. Default value is 0, it means reminds every cell without considering execution time.

Functions:

DevReminder.me(str) : Triggers bot with given process description after execution. If process info is not given, bot reminds without process info.::

    remind = DevReminder(chat_id = 1932126911)
    remind.me("Process info")

DevReminder.set_time_threshold(int): Sets time threshold as seconds.::

    remind.set_time_threshold(3)

DevReminder.auto_remind(bool): Sets auto remind mode. If no input is given, acts as a switch.::

    remind.auto_remind(True)


NOTE: DevReminder class is a singleton class that lets you to call it many times with different inputs. So you can change auto remind mode or time threshold value by calling it again in Ipython except using functions.


========
Examples
========
Without Auto Reminder:::

    In [1]>>
        from devreminder import DevReminder
        import time

    In [2]>>
        remind = DevReminder(1932126911,False,5)

    In [3]>>
        remind.me("Example")
        time.sleep(6) # Less than 5 does not warn

Output:

.. image:: https://github.com/cagataygulten/devreminder/blob/master/pic/picture4.JPG?raw=true

|

With Auto Reminder:::

    In [1]>>
        from devreminder import DevReminder
        import time

    In [2]>>
        remind = DevReminder(1932126911,True,3)

    ...

    In [9]>>
        time.sleep(8) # Less than 3 does not warn

Output:

.. image:: https://github.com/cagataygulten/devreminder/blob/master/pic/picture5.JPG?raw=true

|

============
General Info
============

DevReminder uses own API as a transition API to keep Telegram Bot token private.

DevReminder API does not record any information (including telegram chat id) that sent as an input by users. Source code of the API is also in github repository.

DevReminder also works on python interpreter (.py scripts), shows execution count as 0.

============
Contribution
============

Questions and contributions of all kinds are welcome. You can get in contact with me via mail or create an `issue`_.

.. _`issue`: https://github.com/cagataygulten/devreminder/issues

Contact: cagataygulten@gmail.com

=======
License
=======

DevReminder is under the MIT license. See LICENSE.txt for more information.


