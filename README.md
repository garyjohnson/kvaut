# kvaut
UI automation to enable BDD-style testing for Kivy apps.

## Requirements
kivy must be installed. Currently tested with kivy 1.9.x.

## Getting Started
kvaut is a client / server library that enables BDD-style testing in your kivy apps. We use kvaut with [behave](http://pythonhosted.org/behave/) to make test assertions against our UI.

First, you need to get *kvaut* and *behave* installed. Assuming you are using pip, add them to your requirements.txt file and install them from PyPi.

### Running the Automation Server
In your application, you need to run the kvaut server. Here's an example of doing this in main.py of your kivy app. Even though it looks like it's always being run, it will only do any work if **KVAUT_ENABLE=1** is in your environment variables.

```
import kvaut.server

if __name__ == '__main__':
    kvaut.server.start_automation_server()

    # Start up our kivy application down here
```

### Setting up the Automation Client
Now we need to set up our first behave test to launch our app. In your `features\environment.py` file (create it if you don't have it), add something like this:

```
import os
import subprocess
import kvaut.client

APP_PATH = '<path to your app>'

def before_scenario(context, scenario):
    os.environ['KVAUT_ENABLE'] = '1'
    context.test_app_process = subprocess.Popen([APP_PATH], {'env':os.environ})
    kvaut.client.wait_for_automation_server()

def after_scenario(context, scenario):
    if context.test_app_process:
        subprocess.Popen.kill(context.test_app_process)
```

### Testing the App
Now it's time to make assertions against the UI. Make a feature file `features/hello_world.feature`:

```
Feature: Hello World
  As a developer
  I want to do automated testing
  So I can refactor without worry

  Scenario: Hello World
    When I tap button "Say Hello"
    Then I see "Hello World!"
```

Make a steps definition file `features/steps/hello_world_steps.py`:

```
import kvaut.client
from behave import *

use_step_matcher("re")

@when(u'I tap button "(?P<button_text>[^"]*)"')
def i_tap_button(step, button_text):
  kvaut.client.tap(button_text)

@then(u'I see "(?P<text>[^"]*)"')
def i_see(step, text):
  kvaut.client.assert_is_visible(text)
```

This, of course, assumes your kivy app has a button labeled 'Say Hello', and tapping that button will display the text 'Hello World!' somewhere. You should be able to run `behave` from your project directory and see the app launch and the button press down.

## Other Examples
To see a practical example of kvaut in action, check out [ci_screen_2](https://github.com/garyjohnson/ci_screen_2).

Also, kvaut uses itself for testing. You can run `behave` from the project directory to run the tests, and see the kivy apps used for testing in the `test_apps/` directory

## Contributing
To run kvaut tests, run `shovel test`. Tests are currently run against python2.7 and python3.4, so kivy needs to be installed and available in the $PYTHONPATH for both instances. (To install kivy as a python package on OSX, you can use [this gist](https://gist.github.com/garyjohnson/53c1eef4adaf57c247a4) for reference).

