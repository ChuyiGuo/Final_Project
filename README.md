# Final_Project
### **IS590PR Spring 2019**

#### **Title:**
Monte Carlo Simulation of the daily revenue for Champaign-Urbana Amtrak service.

#### **Team Member:**
Chuyi Guo

#### **Scenario & Purpose:**
This project is aimed to simulate the daily revenue for trains’ departure from Champaign-Urbana. 
The main revenue comes from selling train tickets and is determined by the number of passengers and their fares. 
Generally, Amtrak provides two categories of fares. One is business and the other one is sleeper. 
The second one provide sleeping accommodations and usually chosen by passengers on a long journey. 
Fares are also determined by the travel distance.
Moreover, Amtrak allows pets, bicycles and Golf Clubs for a fee.

#### **Simulation's variables of uncertainty:**

**Number of passengers:**

According to Rail Passengers Association, Champaign—Urbana Amtrak (CHM) served 153,470 passengers in 2018, including arrivals and departures. The averaged daily departures are around 210. Thus, assume the number of passengers obeys Poisson distribution with lambda equalling to 210.

**Age structure of passengers:**

Amtrak provides different discounts to different ages (10% discount for seniors and 50% discount for children between the ages of 2 to 12). So the project divided passengers into three groups:  children, adults and seniors. According to US Census (2000), assume the proportions of those three groups are 10%, 81.5% and 8.5%, respectively. 

**Travel distance:**

According to Rail Passengers Association, all the travels are divided into 9 intervals by its length. The proportions are as follows.

0-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, 800+ miles

5.9%, 89.9%, <0.1%, 1.3%, <0.1%, 0.2%, 0.8%, 0.3%, 1.5%

Notice the nearest train station is in Mattoon (IL), with a length of 45 miles. One of the top city pairs by ridership is Champaign- New Orleans, with a length of 805 miles. So it is reasonable to assume most of the trips in the 800+ miles interval are trips to New Orleans. The longest trip could be from Champaign to CA, with a length around 2200 miles.
Thuse redefine the intervals as:

45-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, 805, 806-2200

Define probability for intervals as:

[0.059, 0.899, 0.0005, 0.013, 0.0005, 0.002, 0.008, 0.003, 0.014, 0.001]

Assume within each interval, the exact travel distance follows a uniform distribution.  

**Fare type:**

According to Rail Passengers Association, 98.5% passengers choose business fare. However, passengers on a long journey are more likely to choose sleeper fare. So for passengers, who travel less than 200 miles, assume the probability of choosing sleeper fare is 0.05. For the other passengers, assume its probability of choosing sleeper fare is changed with distance and equals to 0.05 * ((distance - 200) / 250 + 1)**2.

**Add-ons:**

Assume the probability of carrying a pet, a bicycle and a golf clubs are 5%, 10%, 5%, respectively. 

#### **Assumptions:**
1. The trains will not be full.


#### **Hypothesis:**



#### **Data Sources:**
https://www.railpassengers.org/site/assets/files/1800/chm.pdf
http://champaign.areaconnect.com/statistics.htm
http://onlinepubs.trb.org/onlinepubs/tcrp/tcrp_rpt_95c12.pdf