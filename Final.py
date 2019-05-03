"""
IS590PR Spring2019 Final Project

Monte Carlo Simulation of the Daily Revenue of Champaign-Urbana Amtrak

Chuyi Guo (cguo12)
"""

import numpy as np
from random import randint
import matplotlib.pyplot as plt
import seaborn as sns

# simulate passenger info
def age_group() ->str:
    """ Simulate an age_group for a passenger with pre-defined probabilities.
        According to Amtrak's, each passenger are divided into different passenger type by age.
        Each passenger belongs to adult, senior or child with probabilities of
        15%, 72.6% and 12.4%, respectively.

    :return: 'adult', 'senior' or 'child'
    >>> age_group() in ['adult', 'senior' ,'child']
    True
    """
    age_prob = [0.15, 0.726, 0.124]
    group = ['child', 'adult', 'senior']
    age_group = np.random.choice(group, 1, p=age_prob)[0]
    return age_group


def distance() ->int:
    """Simulate an travel distance for a passenger with pre-defined probabilities.
    First divided the travel distance in to the following intervals:
    45-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, 805, 806-2200
    Then assign the following probabilities to each interval:
    [0.059, 0.899, 0.0005, 0.013, 0.0005, 0.002, 0.008, 0.003, 0.014, 0.001]
    The distance range is picked by the given probabilities.
    Assume within each distance range, the values are uniformly distributed.
    After getting the distance range, randomly pick a value as the travel distance from that range.

    :return: travel distance for a passenger
    >>> 45<=distance()<=2200
    True
    """
    distance_prob = [0.059, 0.899, 0.0005, 0.013, 0.0005, 0.002, 0.008, 0.003, 0.014, 0.001]
    distance_group = [99, 199, 299, 399, 499, 599, 699, 799, 805, 2200]
    distance_range = np.random.choice(distance_group, 1, p=distance_prob)[0]
    if 199 <= distance_range <=799:
        distance = randint(distance_range - 99, distance_range)
    elif distance_range==99:
        distance = randint(45, distance_range)
    elif distance_range==805:
        distance=805
    else:
        distance = randint(806, distance_range)
    return distance

def add_ons() ->list:
    """Simulate add-on items for a passenger with pre-defined probabilities.
    Each passenger is allowed to add a bike, pet or golf clubs to the trip.
    Bike, pet and golf clubs can be added at the same time, but the max quantity for each is one.
    Add-ons are independent of each other.
    The probabilities of carrying a pet, a bike and a golf club is 5%, 10%, 5%, respectively.

    :return: add-on items for a passenger
    >>> add_ons() in [[],['pet'],['bike'],['golf'],['pet','bike'],['pet','golf'],['bike','golf'],['pet','bike','golf']]
    True
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

# define class
class Passenger:

    def __init__(self, age_group, distance, add_ons):
        """

        :param age_group: 'adult', 'senior' or 'child'
        :param distance: travel distance for a passenger
        :param add_ons: add-on items for a passenger
        """
        self.age_group = age_group
        self.distance = distance
        self.add_ons = add_ons

    def discount(self):
        """For different types of passengers, different discount rate are provided.
        Seniors will get 10% discount and children will get 50% discount.
        Get the discount for the passenger.

        :return: discount for the passenger
        >>> p = Passenger('child',150,[])
        >>> p.discount()
        0.5
        >>> p = Passenger('senior',150,[])
        >>> p.discount()
        0.9
        >>> p = Passenger('adult',150,[])
        >>> p.discount()
        1
        >>> p = Passenger('youth',150,[])
        >>> p.discount()
        Traceback (most recent call last):
        ValueError: unknown type
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
        >>> p = Passenger('adult',150,[])
        >>> p.fare_type() in ['business', 'sleeper']
        True
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
        >>> p = Passenger('senior',150,['pet'])
        >>> p.add_pay()
        26
        >>> p = Passenger('senior',150,['pet','bike','golf'])
        >>> p.add_pay()
        46
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


def simulate_num_passenger(mean: int) ->int:
    """ simulate the daily passenger number for Champaign-Urbana Amtrak
    The number of passengers follows Poisson distribution

    :param mean: expected daily passenger number
    :return: number of passengers for a day
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


def simulate_revenue_oneday(fare: dict,num: int) ->float:
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

def simulate_revenue_moreday(times: int,fare: dict,num: int) ->float:
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

    # the current fare of Amtrak
    fare = {
        'business': 0.166,
        'sleeper': 0.283
    }
    # increase the fare by 10%
    fare_increase = {
        'business': 0.166*1.1,
        'sleeper': 0.283*1.1
    }
    # decrease the fare by 10%
    fare_decrease = {
        'business': 0.166*0.9,
        'sleeper': 0.283*0.9
    }

    # simulate 10000 times for each scenarios
    # simulation for current fare with expected 210 passengers per day
    result_fare = simulate_revenue_moreday(10000,fare,210)
    # simulation for increase the fare by 10% with expected passengers lower by 2%
    result_fare_increase = simulate_revenue_moreday(10000, fare_increase, 210*0.98)
    # simulation for decrease the fare by 10% with expected passengers higher by 2%
    result_fare_decrease = simulate_revenue_moreday(10000, fare_decrease, 210*1.02)

    sns.distplot(result_fare, hist=False, kde=True,label = 'Current fare',color='r')
    plt.axvline(x = np.mean(result_fare),color='r')
    sns.distplot(result_fare_increase, hist=False, kde=True,label = 'Increase fare',color='green')
    plt.axvline(x=np.mean(result_fare_increase), color='green')
    sns.distplot(result_fare_decrease, hist=False, kde=True,label = 'Decrease fare', color='blue')
    plt.axvline(x=np.mean(result_fare_decrease), color='blue')
    plt.show()

    print("The mean of daily revenue with current fare rate is " + str(round(np.mean(result_fare),2)) +"\n" +
          "The mean of daily revenue with increasing fare rate by 10% is " + str(round(np.mean(result_fare_increase),2)) + "\n" +
          "The mean of daily revenue with decreasing fare rate by 10% is " + str(round(np.mean(result_fare_decrease),2)))









