Surface Realization for a Controlled Natural Language
=====================================================

SIGGEN Hackathon at INLG 2016, Edinburgh, Scotland

Hackathon Description
---------------------

**Realization for a Controlled Natural Language (CNL) Fragment**  
In this hackathon, participants get first-hand experience developing a surface realization system for a controlled natural language. 
Hackers will face decisions like whether to store morphological information in a database or to use general rules or transducers to produce surface forms. 
These forms then need to interact sensibly with a syntactic realization module. 
The use of a controlled natural language in this task makes the goal of developing a prototype surface realization system within 24-36 hours a more realistic one.

Proposed CNLs
-------------
We provide guidelines for developing a generation system compatible with the Simplified Technical English Standard (ASD 2013). 
If hackers are passionate about another language specification, they are welcome to form a team focusing on that language.

*Simplified Technical English* (STE) is a very limited subset of the English language designed for use by non-native and native speakers alike in the international aerospace industry. 

The lexicon is built with one primary principle: one word, one meaning. 
Therefore the specification allows only one meaning for polysemous words and selects only one synonym to refer to an idea when several exist. 
Spelling is normalized according to American English.

The grammar allows for only a restricted set of tenses: simple past, simple present, and simple future. 
Only the declarative and imperative moods are allowed. 
Past participle forms of verbs can be used, but only as an adjective (no use of the past perfect is allowed).
ING forms of verbs can only be used when they are part of a Technical Name (i.e., the present progressive and gerunds are not allowed).

Example Sentences from STE with a proposed semantics

Measure the time necessary for the silica gel to absorb the moisture.
measure(necessary(time, absorb(silica_gel, moisture)))

Clean your skin with a large quantity of clean water.
clean(you(skin)), with(large(quantity(clean(water))))

The shock mount absorbs the vibration.
absorbs(shock_mount, vibration)


Guidelines
----------
* **Teams should form and choose an idea fairly quickly.** 
  Our minimum goal is that every team has a system capable of generating some subset of a controlled natural language. 
  Where you choose to place your focus is up to you. 
  You can focus on complete coverage for STE or xkcd's up-goer five language, or you could choose a small fragment and focus on developing an abstract library that will be easily extensible. 
  The point is to find a team and work together. 
  We'll come together at the end to see what creative projects everyone has come up with!
* We are providing some guidelines and suggesting some libraries to get you started, but there is no fixed time course. 
  We will wander around and check in with each group periodically to try to keep things moving, but we also want to avoid interrupting you when you're going strong.
* **This is not a competition.** Try to accomplish as much as you can, but **help each other out**. 
  If you see someone struggling to get something working, offer assistance. 
  If you need help, ask for it. If you feel uncomfortable approaching someone, feel free to approach us and we can find someone to help.

References
----------
You can request your own copy of the STE-100 guidelines from the ASD by following the instructions at http://www.asd-ste100.org/request.html

AeroSpace and Defence (ASD) Industries Association of Europe. 2013. *Simplified Technical English, Specification ASD-STE100: International Specification for the preparation of maintenance documentation in a controlled language*. January. Filename: `ASD-STE100-ISSUE-6.pdf`


Metadata
--------

Hackathon organized by Yaji Sripada and Dave Howcroft.
This repo prepared by Dave Howcroft.
