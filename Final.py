"""
IS590PR Spring2019 Final Project

Monte Carlo Simulation of the daily revenue for Champaign-Urbana Amtrak service.

Chuyi Guo (cguo12)
"""

import numpy as np
from random import randint
import matplotlib.pyplot as plt
import seaborn as sns

# define class
class Passenger:

    def __init__(self, age_group, distance, add_ons):

        self.age_group = age_group
        self.distance = distance
        self.add_ons = add_ons

    def discount(self):
        """For different types of passengers, different discount rate are provided.
        Seniors will get 10% discount and children will get 50% discount.
        Get the discount for the passenger.

        :return: discount for the passenger
        >>> self.age_group = 'child'
        0.5
        >>> self.age_group = 'senior'
        0.9
        >>> self.age_group = 'adult'
        1
        """
        if self.age_group == 'child':
            discount = 0.5
        elif self.age_group == 'senior':
            discount = 0.9
        elif self.age_group == 'adult':
            discount = 1
        else:
            raise ValueError('unknown type')
        return discount

    def fare_type(self):
        """Generally two types of fare are provided. One is the business and another is sleeper.
        Business fare is lower than sleeper fare and it's more suitable for short trips.
        On the opposite, passengers on a long journey are more likely to choose sleeper fare.
        Estimate the type of fare chosen by passenger, given his travel distance.

        :return: the type of fare chosen by passenger
        """
        fare_type = ['business', 'sleeper']
        fare_prob = [0.95, 0.05]

        if self.distance == None or self.distance < 200:
            type = np.random.choice(fare_type, 1, p=fare_prob)[0]
        else:
            sleeper_prob = 0.05 * ((self.distance - 200) / 250 + 1) ** 2
            if sleeper_prob > 1:
                sleeper_prob = 1
            fare_prob_long_distance = [1 - sleeper_prob, sleeper_prob]
            type = np.random.choice(fare_type, 1, p=fare_prob_long_distance)[0]

        return str(type)

    def add_pay(self):
        """Amtrak allows pets, bicycles and golf clubs for a fee.
        Calculate the total fee needed to pay for the add-ons.

        :return: the total amount needed to pay for the add-ons
        """
        add = 0
        if self.add_ons:
            if 'pet' in self.add_ons:
                add = add + 26
            if 'bike' in self.add_ons:
                add = add + 10
            if 'golf' in self.add_ons:
                add = add + 10
        return add


# simulate passenger info
def age_group():
        """ Simulate an age_group for a passenger with pre-defined probabilities.
        According to Amtrak's, each passenger are divided into different passenger type by age.
        Each passenger belongs to adult, senior or child with probabilities of
        10%, 81.5% and 8.%, respectively.

        :return: adult, senior or child
        """
        age_prob = [0.1, 0.815, 0.085]
        group = ['child', 'adult', 'senior']
        age_group = np.random.choice(group, 1, p=age_prob)[0]
        return str(age_group)

def distance():
    """Simulate an travel distance for a passenger with pre-defined probabilities.
    First divided the travel distance in to the following intervals:
    45-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, 805, 806-2200
    Then assign the following probabilities to each interval:
    [0.059, 0.899, 0.0005, 0.013, 0.0005, 0.002, 0.008, 0.003, 0.014, 0.001]
    The distance range is picked by the given probabilities.
    Assume within each distance range, the values are uniformly distributed.
    After getting the distance range, randomly pick a value as the travel distance from that range.

    :return: travel distance for a passenger
    """
    distance_prob = [0.059, 0.899, 0.0005, 0.013, 0.0005, 0.002, 0.008, 0.003, 0.014, 0.001]
    distance_group = [99, 199, 299, 399, 499, 599, 699, 799, 805, 2200]
    distance_range = np.random.choice(distance_group, 1, p=distance_prob)[0]
    if 99 < distance_range <=799:
        distance = randint(distance_range - 99, distance_range)
    elif distance_range==99:
        distance = randint(45, distance_range)
    elif distance_range==805:
        distance=805
    else:
        distance = randint(806, distance_range)
    return distance

def add_ons():
    """Simulate add-on items for a passenger with pre-defined probabilities.
    Each passenger is allowed to add a bike, pet or golf clubs to the trip.
    Bike, pet and golf clubs can be added at the same time, but the max quantity for each is one.
    Add-ons are independent of each other.
    The probabilities of carrying a pet, a bike and a golf club is 5%, 10%, 5%, respectively.

    :return: add-on items for a passenger
    """
    add = []
    pet_prob = [0.05, 0.95]
    bike_prob = [0.1, 0.9]
    golf_prob = [0.05, 0.95]

    if np.random.choice([1, 0], 1, p=pet_prob) == [1]:
        add.append('pet')
    if np.random.choice([1, 0], 1, p=bike_prob) == [1]:
        add.append('bike')
    if np.random.choice([1, 0], 1, p=golf_prob) == [1]:
        add.append('golf')
    return add


def simulate_num_passenger(mean):
    """ simulate the daily passenger number for Champaign-Urbana Amtrak
    The number of passengers follows Poisson distribution

    :param mean: expected daily passenger number
    :return: number of passgengers for a day
    """
    return np.random.poisson(mean, 1)

def get_fare_pay(fare: dict, distance: int, fare_type: str, discount: float) -> float:
    """ Calculate the exact fare for a passenger, given his travel distance, fare type and discount.

    :param fare: price per mile by taking the Amtrak train
    :param distance: travel distance (mile)
    :param fare_type: the fare type that the passgener chose. business/sleeper
    :param age_group:
    :return: total pay for getting the ticket
    >>> fare = {'business':1,'sleeper':2}
    >>> distance=100
    >>> fare_type='business'
    >>> discount=1
    >>> get_fare_pay(fare, distance, fare_type, discount)
    100
    >>> discount2=0.5
    >>> get_fare_pay(fare, distance, fare_type, discount2)
    50.0
    >>> fare_type2='sleeper'
    >>> get_fare_pay(fare, distance, fare_type2, discount)
    200
    """
    revenue = distance * fare[fare_type] * discount
    return revenue

# num = simulate_num_passenger(210)[0]
def simulate_revenue_oneday(fare,num):
    """ calculate the daily revenue, including price for the tickets and fee for the add-on items.

    :param fare: fare rate for business and sleeper fare type
    :param num: number of expected number of passengers for a day
    :return: daily revenue
    """
    total_revenue = 0
    for i in range(num):
        passenger = Passenger(age_group(), distance(), add_ons())
        revenue = get_fare_pay(fare, passenger.distance, passenger.fare_type(), passenger.discount()) + passenger.add_pay()
        total_revenue += revenue
    return round(total_revenue,2)

def simulate_revenue_moreday(times,fare,num):
    """calculate the daily revenue, including price for the tickets and fee for the add-on items.

    :param times: times for repeating the simulate_revenue_oneday process
    :param fare: fare rate for business and sleeper fare type
    :param num: number of expected number of passengers for a day
    :return: list with each day's revenue stored
    """
    sim_revenue = []
    for i in range(times):
        number = simulate_num_passenger(num)[0]
        sim_revenue.append(simulate_revenue_oneday(fare,number))
    return sim_revenue

if __name__ == '__main__':


    fare = {
        'business': 0.166,
        'sleeper': 0.283
    }

    fare_increase = {
        'business': 0.166*1.1,
        'sleeper': 0.283*1.1
    }

    fare_decrease = {
        'business': 0.166*0.9,
        'sleeper': 0.283*0.9
    }

    #
    result_fare = simulate_revenue_moreday(10000,fare,210)
    result_fare_increase = simulate_revenue_moreday(10000, fare_increase, 210*0.98)
    result_fare_decrease = simulate_revenue_moreday(10000, fare_decrease, 210*1.02)


    sns.distplot(result_fare, hist=False, kde=True,label = 'Current fare',color='r')
    plt.axvline(x = np.mean(result_fare),color='r')
    sns.distplot(result_fare_increase, hist=False, kde=True,label = 'Increase fare',color='green')
    plt.axvline(x=np.mean(result_fare_increase), color='green')
    sns.distplot(result_fare_decrease, hist=False, kde=True,label = 'Decrease fare', color='blue')
    plt.axvline(x=np.mean(result_fare_decrease), color='blue')
    plt.show()

    h1=[]
    h2=[]
    for i in range(100):
        t1 = np.mean(result_fare[i*100:i*100+100])
        t2 = np.mean(result_fare_increase[i * 100: i * 100 + 100])
        t3 = np.mean(result_fare_decrease[i * 100: i * 100 + 100])
        h1.append(t2>t1)
        h2.append(t2>t3)





