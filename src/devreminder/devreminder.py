import time
import requests


class DevReminder(object):

    _instance = None

    #Singleton
    def __new__(self, chat_id=None, auto_remind=False, time_threshold=0):
        #Controls event registrations on first __init__
        self.registered = False
        if not self._instance:
            self._instance = super(DevReminder, self).__new__(self)
        return self._instance

    def __init__(self, chat_id=None, auto_remind=False, time_threshold=0):
        """
        chat_id: Required id of chat with DevReminder bot. (Default = None)
        auto_remind: For Ipython, triggers reminder function at the end of the each cell. (Default = False)
        time_threshold (seconds): Bot doesn't remind the user if the elapsed time is less then time threshold. It is useful with auto remind mode. (Default = 0, warns without considering time threshold)
        """

        self.initialized = False
        self.info = None
        self.chat_id = chat_id
        self.auto_remind_status = auto_remind
        self.time_threshold = time_threshold

        try:
            self.ip = get_ipython()

            #Handles registrations
            if self.auto_remind_status and self.registered == False:
                get_ipython().events.register('pre_execute', self.get_start_time)
                get_ipython().events.register('post_run_cell', self.exit_func)
                self.registered = True

            elif not self.auto_remind_status and self.registered == True:
                get_ipython().events.unregister('pre_execute', self.get_start_time)
                get_ipython().events.unregister('post_run_cell', self.exit_func)
                self.registered = False

        # Python interpreter
        except:
            self.ip = None

    def set_chat_id(self, chatid):
        """
        Sets chat id externally.
        """
        self.chat_id = chatid

    #Pre execute function to calculate elapsed time on auto remind mode
    def get_start_time(self):
        self.start_time = time.time()

    #Auto remind function as a switch
    def auto_remind(self, status=None):
        if status == None:
            if self.registered:
                self.auto_remind_status = False
                get_ipython().events.unregister('pre_execute', self.get_start_time)
                get_ipython().events.unregister('post_run_cell', self.exit_func)
                self.registered = False
                print("Auto Remind is off")

            else:
                self.auto_remind_status = True
                get_ipython().events.register('pre_execute', self.get_start_time)
                get_ipython().events.register('post_run_cell', self.exit_func)
                print("Auto Remind is on")
                self.registered = True
                self.info = None

        elif status == True:
            if not self.registered:
                self.auto_remind_status = True
                get_ipython().events.register('pre_execute', self.get_start_time)
                get_ipython().events.register('post_run_cell', self.exit_func)
                print("Auto Remind is on")
                self.registered = True
                self.info = None
            else:
                print("Auto Remind is already on")

        else:
            if self.registered:
                self.auto_remind_status = False
                get_ipython().events.unregister('pre_execute', self.get_start_time)
                get_ipython().events.unregister('post_run_cell', self.exit_func)
                print("Auto Remind is off")
                self.registered = False
            else:
                print("Auto Remind is already off")

        #Disables registered post process of this function
        self.initialized = False

    def set_time_threshold(self, time_threshold):
        """
                Sets time threshold (seconds).
        """
        self.time_threshold = time_threshold

        # Disables registered post process of this function
        self.initialized = False

    #Main post execute function
    def exit_func(self, _=None):

        if self.initialized:
            now = time.time()
            time_elapsed = now - self.start_time

            try:
                exec_count = self.ip.execution_count -1 #minus this post execution

            # Python interpreter
            except:
                exec_count = 0

            if self.time_threshold < time_elapsed or self.time_threshold == 0:
                BASE = "https://devreminderapi.herokuapp.com/"
                response = requests.put(BASE + "messageinfo",
                                        {"info": self.info, "chatid": self.chat_id, "time": time_elapsed, "ec": exec_count})
            try:
                #Unregisters executed exit function on "me" function.
                if not self.auto_remind_status:
                    self.ip.events.unregister('post_execute', self.exit_func)

            # Python interpreter
            except:pass

        else:
            # Disables post process of __init__ and functions.
            self.initialized = True

    def me(self, info=None):
        '''
        Triggers devreminder bot with given input
        info = short description of running cell (Default=None)
        '''

        if self.initialized == False:
            self.initialized = True

        self.info = info
        self.start_time = time.time()

        if not self.auto_remind_status:
            try:
                self.ip.events.register('post_execute', self.exit_func)

            # Python interpreter
            except:
                import atexit
                atexit.register(self.exit_func)




