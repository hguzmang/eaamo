## Guide

#### Welcome
Welcome to the user guide! The goal of the platform is to guide you in allocating a fixed number of tests across a university population optimally. In the following sections, we explain how to use this tool.

#### Background
This web app assists you in finding a test allocation that best suits your priorities. We have preloaded data matching a model university. The following [model details section](#modeldetails) describes the full parameter settings. In a future version, the data will be replaced by real data obtained from our partner university.

#### Instructions
For each possible solution, the bar chart shows how well it does on each of the four objectives. The purple containment objectives denote the expected number of people self-isolating unnecessarily in each category (smaller is better). The orange health objective denotes the number of prevented infections (larger is better).

As an administrator, your task is to select the solution that best matches the priorities of your institution. To help you with this, the application allows you to set thresholds for the different objectives.  For example, if you want to avoid as many new infections as possible and do not care how many individuals are self-isolating, you can set the “unnecessary self-isolations” thresholds for each population category to zero, and then select the solution that has the largest number of prevented infections. However, this could lead to solutions where the university can no longer stay open because there are too many professors self-isolating. Therefore, setting a threshold of 250 for the professors means that any solution where more than 250 professors are self-isolating in expectation are excluded. The same can be applied to any of the population categories, in order to only show the solutions that match your criteria. 

You can explore how many tests the current solution allocates to each population category in the 'Solution details' box on the right.

In general, there will be more than one solution that satisfies the thresholds. The app tells you how many solutions there are, and you can explore these one by one using the selection box.

If you want to save a solution temporarily, you can also click the ‘Save’ button and it will appear below.
