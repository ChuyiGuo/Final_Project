# Final_Project
### **IS590PR Spring 2019**

### **Title:**
Monte Carlo Simulation of the daily revenue for Champaign-Urbana Amtrak

### **Team Member:**
Chuyi Guo

### **Scenario & Purpose:**
This project is aimed to simulate the daily revenue of Champaign-Urbana Amtrak for trains departing from Champaign-Urbana.

The revenue comes from selling train tickets and is determined by the number of passengers and their fares. Generally, Amtrak provides two categories of fares. One is business and another is sleeper. The sleeper provides sleeping accommodation and is usually chosen by passengers on a long journey. Fares are also affected by the travel distance. Moreover, Amtrak allows add-ons such as pets, bicycles and Golf Clubs for a fee. 


### **Simulation's variables of uncertainty:**

According to Amtrak Ridership Statistics from Rail Passengers Association(https://www.railpassengers.org/site/assets/files/1800/chm.pdf), distributions of Number of passengers, Travel distance and Fare type are made as follows:

**Number of passengers:**

Champaign—Urbana Amtrak (CHM) served 153,470 passengers in 2018, including arrivals and departures. The averaged daily departures are around 210. Thus, assume the number of passengers follows Poisson distribution with lambda equalling to 210.

**Travel distance:**

All the trips are divided into 9 intervals by its length. The lengths and proportions are as follows:

0-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, 800+ miles

5.9%, 89.9%, <0.1%, 1.3%, <0.1%, 0.2%, 0.8%, 0.3%, 1.5%

Notice the nearest train station is in Mattoon (IL), with a length of 45 miles. One of the top city pairs by ridership is Champaign-New Orleans, with a length of 805 miles. So a reasonable guess is most of the trips in the 800+ miles interval are trips to New Orleans. The longest trip could be from Champaign to CA, with a length around 2200 miles.
Thus redefine the intervals as:

45-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, 805, 806-2200

Define probability for intervals as:

[0.059, 0.899, 0.0005, 0.013, 0.0005, 0.002, 0.008, 0.003, 0.014, 0.001]

Assume within each interval, the exact travel distance follows a uniform distribution. Each travel distance range is randomly picked first with the above probabilities. Then randomly pick a value within an range as the travel distance for a passenger.

**Fare type:**

98.5% passengers choose business fare. However, passengers on a long journey are more likely to choose sleeper fare. So for passengers who travel less than 200 miles, assume the probability of choosing sleeper fare is 0.05. For the other passengers, assume its probability of choosing sleeper fare is changed with distance and equals to 0.05 * ((distance - 200) / 250 + 1)**2.

**Age structure of passengers:**

Amtrak provides different discounts to different ages (10% discount for seniors and 50% discount for children between the ages of 2 to 12). So the project divided passengers into three groups:  children, adults and seniors. According to US Census Bureau 2018 quick facts of Champaign County(https://www.census.gov/quickfacts/fact/table/champaigncountyillinois/AGE295217), assume the proportions of those three groups are 15%, 72.6% and 12.4%, respectively. 
Each passenger will be randomly assigned to a group with corresponding probability.

**Add-ons:**

Assume the probability of carrying a pet, a bicycle and a golf clubs are 5%, 10%, 5%, respectively. 

### **Assumptions:**
1. The trains will not be full.
2. Only two types of fare available: business and sleeper. 

### **Hypothesis:**

According to Transportation Research Board Report 95, the railroad fare elasticity (the percentage change in quantity demanded in response to a one percent change in price) is about -0.2. The elasticity indicates the rate of decrease in passenger number with increasing fare.
In order for Amtrak to increase its revenue, should it increase the fare rate to have more gain of a single ticket sold or decrease fare rate to attract more passengers?

**Hypotheses 1:**
If the fare is increased by 10%, although the number of passengers will shrink proportionally, the total revenue will increase.

**Hypotheses 2:**
Total revenue of increasing fare by 10% is larger than that of decreasing fare by 10%.

### **Results:**
1. Increase fare generates the highest revenue;
2. Decrease fare generates the lowest revenue;
3. The revenue from the current fare is somewhere in the middle.


### **Limitations and Future Work:**
1. Travel distance should estimated by the distance among train stations.
2. There are other types of fare, like saver fare.
3. Refunds are not considered. 
4. Some of the train routine do not provide service for all of the three add-ons.
5. The elasticity used may be out of date.

### **Data Sources:**
https://www.railpassengers.org/site/assets/files/1800/chm.pdf

https://www.census.gov/quickfacts/fact/table/champaigncountyillinois/AGE295217

http://onlinepubs.trb.org/onlinepubs/tcrp/tcrp_rpt_95c12.pdf