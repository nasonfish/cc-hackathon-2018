# cc-hackathon-2018

For this hackathon I took on the challenge of making something which is useful for the CC community and students.

Everybody recieves a digest every day and it's horribly unreadable. A list of links show up with no hint of what department submitted them, or what kind of event they are. The current solution is not attractive to the eye, and is abused with people trying to get their event seen by adding ~~~~^&$$%^EMPHASIS^%$$&^~~~~ on the title.

We created a better solution which creates a portal for people to submit things to go out to the CC community, and a way for students to see the events in categories, and prioritize the events they want to see.

This creates a much more attractive alternative which may, ideally, be productionized, by making it available using CC Single Sign In, and integrating it with the current Digest system, such that people in the CC community may use the same portal they currently use, but the digest would be accessed through this website instead of by e-mail every day.

This project is created in Python using Flask and SQLAlchemy. Our user account system hashes passwords, salted, with pbkdf2. This entire application is based loosely on a previous project I created, [bhsnotes.com](http://bhsnotes.com/) which was a node-sharing web application I created in high school. (You'll notice similarities in the design, I'm sure...)

## How to access

Visit [the website](http://danielbarnes.me:60001)
