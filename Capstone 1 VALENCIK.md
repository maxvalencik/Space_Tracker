**CAPSTONE PROJECT 1**

__***_Title: Space Tracker_***__

1.	**What goal will your website be designed to achieve?** 

	My website will help users to track satellites/space debris according to the following parameters:

	-	Satellite Identification
	-	Satellite Orbital Inclination
	-	Satellite Elevation 

	Using this information, users will be able to determine if they can use a given orbit safely for a space mission. Users will also be able to track a satellite in the sky.


2.	**What kind of users will visit your site? In other words, what is the demographic of your users?**

	The targeted users are space professionals and enthusiasts:

	-	Spaceports: will be able to determine their marketability based on what orbits the clients will be able to achieve from the facilities. A spaceport can typically launch to specific azimuths, which determines the orbital inclination reachable.
	-	Commercial Space Companies: will be able to know how “crowded” is an orbit and from where they will be able to launch to reach it.
	-	Space Enthusiasts: will be able to track satellites around the earth and know where to look for it in the sky.
 

3.	**What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.**

	API to be used:
	
	https://www.space-track.org/documentation#api
	
	https://www.n2yo.com/api/#tle


4. **In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information**

	*a.	What does your database schema look like?*
	
	There will be the following databases:
	
	-	**USERS**
	
		o	Credentials
		
		o	Type (spaceport, enthusiast, launcher)
		
		o	Enthusiasts will have multiple satellites they want to save and track. They can save satellites as favorites.
		
		o	Launchers will be able to create and save new satellites for future missions. One launcher can have multiple satellites and save them as favorites.
			
		o	Spaceports will be able to create and save new launch sites and save them as favorites.
	
	-	**SATELLITES**
	
		o	Will include parameters needed for analysis and identification based on if they already exist or are for future missions. Can be already created in the db or not.
		
		o	One satellite has one launcher but could be launched from multiple launch sites (future missions).
		
		o	One satellite can have multiple enthusiasts following it.
	
	-	**LAUNCH_SITES**
	
		o	Will include parameters needed for analysis and identification based on if they already exist or are for future missions.
		
		o	One launch site has one operator (spaceport) but can have multiple users (launchers).



	*b.	What kinds of issues might you run into with your API?*
	
	The main issue I foresee is the limited number of requests, which can be challenging during the development phase of the project. Will require a copy of the data for development as a test API.

	*c.	Is there any sensitive information you need to secure?*
	
	User credentials will be the main sensitive information on the site. Future satellites parameters might also be sensitive.

	*d.	What functionality will your app include?*
	
	-	Three main interfaces for each type of users. 
	-	Users will be able to create satellites or launch sites and store them in the appropriate db based on their user type.
	-	If satellites or launch sites already exist in the db, they will not be duplicated.
	-	Users will be able to conduct their analysis against API data:
	o	Spaceport: given a launch site, what orbit can be reached and how many satellites already use it. Save, update, and store the result.
	o	Launchers: given a satellite and mission orbit, how many satellites already use it and where can I launch (out of existing launch sites). Save, update, and store results.
	o	Enthusiasts: tracking satellites of their choice and extract fun facts about it.


	*e.	What will the user flow look like?*
	
	A user will access the website and login to access their dedicated interface where they will be able to access the appropriate functionality.
