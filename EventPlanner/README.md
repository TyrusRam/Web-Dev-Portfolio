# my final: event

  This website is an event planner where people can host or rsvp for events, 
  and just in case this is classified as being similar to Project 2 I will 
  provide the differences first.

  This Project differs from Project 2 as it is not just using Django and HTMLl/CSS,
  it incorporates javascript and Ajax with the fetch API to do some of the things 
  in the background. I will go further into detail later in this readme.

  My project allows users to create a profile, then they can start creating or RSVPing for events.
  There is only one way to create an event and that is by clicking on create which they are directed to an 
  HTML where they can fill out and submit a form and the event is created with a unique ID number. There
  are multiple ways to view the events as one can go to the calendar page which shows the events that the 
  rsvp deadline is approaching, soonest at the top. They can also go to discover which displays the event 
  categories and the user can click on one category and using Ajax, a fetch requests sends 
  the user's selection and then dynamically updates the inner HTML with the results of the selected category.
  The last way to see the events is the events you host or are rsvp'd for which if there are any are displayed 
  on the home page, index, and if the user selects any of the events from any of these they will be directed to a 
  page where the single selected event is displayed and if they haven't already 
  they can rsvp for the event.


# Distinctiveness and Complexity

  This project is distinct and more complex than any of the projects so far as it incorporates almost everything 
  from the whole cs50w course including HTML, CSS, database management, Django, models, JavaScript and Ajax in 
  order to operate. It uses event listeners and handlers for several things such as when selecting a category on 
  the discovery page and it manipulates the dom by filling out the entire dom with the resulting page after the 
  promise is received from the fetch request essentially having multiple pages in one depending on the screen size 
  and displaying multiple events when applicable. It uses cron jobs to manage the database by updating event status 
  and clearing the events once they are completed after 24 hours upon the event ending provided the command was run 
  to start the one minute intervals or someone manually runs the command. It not only allows for events to be sorted 
  but recognizes and sorts them by date and time when displaying them to the user depending on where they are viewing 
  the events as there are multiple ways to view the events. It has mobile responsiveness via media queries and event 
  listeners for when  the screen is resized so not only will it display different versions of the site when opened but 
  when the window is resized too, also uses flexbox for mobile friendly and resize friendly design as well for things 
  like arrays of events in their own divs. All the Javascript and CSS is currently in layout.html but in a future refined 
  version, they will be in their own separate files.


# File Descriptions

-styles.css: this is where the styling will be moved to in a later itaration of the website but currently all styling is in layout.html
-calendar.html: This is the HTML page that displays all events and ordered by what rsvp deadline will reach soonest on top so users can rsvp before time runs out if they are interested.
-create.html: This HTML is for allowing the user to input the information for their event and submits it in a form to submit to the back end via post
-discover.html: This displays all the possible categories for the events in a div with an event listener differentiated by category and the empty divs will then be propagated with the events based on the category clicked via Ajax.
-event_partial.html: This is for a future version of the website so when the page is redone using Ajax it does not update the inner HTML with the original html + the layout causing two of the layouts to be displayed when it is handled in the back end when a post is sent which is currently commented out as it doesn't send any sensitive information so post isn't fully necessary.
-event.html: This HTML simply displays the event selected, which the user can select the event in different parts of the website and they all redirect here when applicable and where the user can actually rsvp for the selected event.
-index.html: This HTML shows different things if the user is or is not logged in, if not it is a simple welcome, if they are logged in it shows a more personal welcome message as well as it shows two categories, all events the user is hosting or rsvp for unless there is none then it displays only one category or neither categories.
-layout.html: In this HTML has the major layout of the website that the other layouts extend. It also contains the styling for now and the scripting for now. There are media queries and flexbox CSS stylings in here for mobile responsiveness and some things, specifically the discovery.html are handled with Ajax using the clicked category to then dynamically change the inner HTML to update the page based on the selected event category and the events in the database that have that category as well. It also has a hamburger menu for when on mobile so the top part of the website layout still keeps all its functionality.
-login.html: This HTML allows the user to either input their login info if their account already exists and a register link in case they aren't already registered.
-register.html: This html allows the user to create a new profile with the login info they choose.
-cron.py: This file has a cron job that changes the status of the events based on parameters such as if the event passed or if the rsvp date passed and within settings.py if the cron job and the server is running it will run every minute and do it automatically or the job can be manually run and the command it runs is in update_events.py.
-update_events.py: The command to actually update the event status variable for the events when the cron job is run via timed intervals or manually running. It will also remove completed events after 24 hours of their end time/date to keep the database clean rather than having infinite events that have already passed continue to take up space in the database.


# How to run

  you start up the server by running python manage.py runserver and you start running the cronjobs with python manage.py runcrons or you run it manually with this   command python manage.py runcrons "event.cron.EventCleanup" and the server does not have to be running to manually execute the cronjob


