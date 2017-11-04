Title: Can testers prevent problems?
Date: 2017-09-25 14:59
Category: None
Author: Rob Day
Slug: can-testers-prevent-problems

I read recently that testers can't prevent problems, with the specific example that if a tester found an issue while reviewing a design or prototype before any code had been written, the mistake had still been made and caught by testing. I thought that in one sense this was pretty close to being true, and that in another sense it was completely wrong.

What I actually think is that *testing* (the activity) can't prevent problems - if testing is the evaluation of a product or artifact to see whether it's fit for purpose, then yes, the most it can do is judge that something isn't fit for purpose. It can't anticipate problems, or even make something fit for purpose.

However, *testers* (the people) can prevent problems, but what they're doing then isn't testing - it's technical leadership. In the example of issues found while reviewing a design or prototype, testing has found the issue, but I'd argue that what's really *prevented* the later problem is the culture of prototyping and collaboration - getting that design or prototype written, and circulating it for feedback rather than just forging ahead and writing the code, is what means that finding a problem (by testing) at that stage prevents further problems down the line. Whoever encouraged and fostered that culture of openness and early feedback was the one who really prevented the problem - without that, the testing would have come too late.

Similarly, educating the wider team (on what users and customers actually want, or just on common sources of bugs like Unicode handling) is a good way to prevent problems. This isn't something you could describe as testing - but even so, testers are probably very well-placed to do it, and it's almost certainly a good way to spend time to improve overall product quality.

There are a lot of problems that testing can't solve (in fact, I'm not sure it can actually solve any) - because testing is just about gathering information. It's what information you look for, and how you use that information to guide the rest of your work, that makes the real impact.