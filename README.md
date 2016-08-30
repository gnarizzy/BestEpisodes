# BestEpisodes
Allows users to rank TV episodes in head-to-head comparisons, and uses the Elo algorithm to compute the best episodes. 

**How it works**

Users are shown two episodes of a tv show, and choose which one is better (or a tie if they're equally good, or "skip" if they don't know). This event is treated as a head-to-head match (a la chess) and elo ratings are computed based on these head to 

**Why is this better than the 1-10 ratings on IMDB?**

It's better than traditional 1-10 (or 1-5) ratings for a few reasons, but in essence it's better because people are inconsistent with explicit, 1-10 ratings. The system used in this software, which asks for a qualitative "Is episode X better than episode Y" and implicitly creates a quantitative ranking, is easier for humans to accurately and consistently respond to than software that asks for a quantitative, "How close numerically is this episode to the perfect TV episode?" (which is what a 1-10 system is essentially asking you to do). 

Here are a few issues with 1-10 ratings:

* Explicit ratings are disproportionately represent the extremes. Typically, the only people motivated enough to review a TV episode (or most other things, for that matter) are people who really loved it or people who really hated it. For example, [YouTube replaced it's 1-5 rating system](https://youtube.googleblog.com/2009/09/five-stars-dominate-ratings.html) with a simple "thumbs up" and "thumbs down" system for a similar reason.

* Ratings are inherently relative to expectations, rather than objective. For instance, when . Think of the best pizza you've ever had. Presumably, you'd rate this pizza 10/10. But if tomorrow you tried a new pizza that was even better, how does that figure into your rating system? Either the new pizza is greater than 10/10 (impossible), or you'd have to revise the previous pizza rating to 9/10, which shows that ratings are relative measure of satisfaction that shifts with changing expectations. As another example, imagine a 5/5 iOS app in 2007, when the iPhone first came out, and a 5/5 iOS app now. How would they compare? People were probably much more tolerant of apps that were rough around the edges in 2007, but now people have come to expect highly polished, profesional apps. A five star app in 2007 may only be a three star app in 2016. 

* Ratings can fluctuate based on mood, recent experiences, etc. since they are based on changing expectations. The result of comparing two episodes head-to-head is an objective measure. Your criteria may be subjective, but the conclusion you come to based on that criteria is objective--episode X is better than episode Y. And unless your criteria changes (not common for TV episodes), that's an objective "truth".  

**TODO: Simplify readme text!**
