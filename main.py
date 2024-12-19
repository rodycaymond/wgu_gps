# Student ID: 007462919

import math
import time

# Maps addresses to indexes for easier use later
ADDRESS_MAP = [
    '4001 S 700 E',
    '1060 Dalton Ave S',
    '1330 2100 S',
    '1488 4800 S',
    '177 W Price Ave',
    '195 W Oakland Ave',
    '2010 W 500 S',
    '2300 Parkway Blvd',
    '233 Canyon Rd',
    '2530 S 500 E',
    '2600 Taylorsville Blvd',
    '2835 Main St',
    '300 State St',
    '3060 Lester St',
    '3148 S 1100 W',
    '3365 S 900 W',
    '3575 W Valley Station bus loop',
    '3595 Main St',
    '380 W 2880 S',
    '410 S State St',
    '4300 S 1300 E',
    '4580 S 2300 E',
    '5025 State St',
    '5100 S 2700 W',
    '5383 S 900 E #104',
    '600 E 900 S',
    '6351 S 900 E'
]

# conversion function for address to integer for easier distance
# matrix access. Returns [row, col]
# O(N) time complexity, length of rowCol
# S(N) space complexity, length of rowCol array
def addressesToInts(a1: str, a2: str) -> list[int]:
    rowCol: list[int] = []
    rowCol.append(ADDRESS_MAP.index(a1))
    rowCol.append(ADDRESS_MAP.index(a2))
    return rowCol

# The distance matrix is a 2D array as a hashtable which accepts
# a column and a row index to find the distance. This is a direct
# hashtable, and its pulled from the distance Map provided.
DISTANCE_MATRIX = [
    [0,7.2,3.8,11,2.2,3.5,10.9,8.6,7.6,2.8,6.4,3.2,7.6,5.2,4.4,3.7,7.6,2,3.6,6.5,1.9,3.4,2.4,6.4,2.4,5,3.6],
    [7.2,0,7.1,6.4,6.0,4.8,1.6,2.8,4.8,6.3,7.3,5.3,4.8,3.0,4.6,4.5,7.4,6.0,5.0,4.8,9.5,10.9,8.3,6.9,10,4.4,13],
    [3.8,7.1,0,9.2,4.4,2.8,8.6,6.3,5.3,1.6,10.4,3.0,5.3,6.5,5.6,5.8,5.7,4.1,3.6,4.3,3.3,5.0,6.1,9.7,6.1,2.8,7.4],
    [11.0,6.4,9.2,0,5.6,6.9,8.4,4.0,11.1,7.3,1.0,6.4,11.1,3.9,4.3,4.4,7.2,5.3,6.0,10.6,5.9,7.4,4.7,0.6,6.4,10.1,10.1],
    [2.2,6.0,4.4,5.6,0.0,1.9,7.9,5.1,7.5,2.6,6.5,1.5,7.5,3.2,2.4,2.7,1.4,0.5,1.7,6.5,3.2,5.2,2.5,6.0,4.2,5.4,5.5],
    [3.5,4.8,2.8,6.9,1.9,0.0,6.3,4.3,4.5,1.5,8.7,0.8,4.5,3.9,3.0,3.8,5.7,1.9,1.1,3.5,4.9,6.9,4.2,9.0,5.9,3.5,7.2],
    [10.9,1.6,8.6,8.6,7.9,6.3,0.0,4.0,4.2,8.0,8.6,6.9,4.2,4.2,8.0,5.8,7.2,7.7,6.6,3.2,11.2,12.7,10.0,8.2,11.7,5.1,14.2],
    [8.6,2.8,6.3,4.0,5.1,4.3,4.0,0.0,7.7,9.3,4.6,4.8,7.7,1.6,3.3,3.4,3.1,5.1,4.6,6.7,8.1,10.4,7.8,4.2,9.5,6.2,10.7],
    [7.6,4.8,5.3,11.1,7.5,4.5,4.2,7.7,0.0,4.8,11.9,4.7,0.6,7.6,7.8,6.6,7.2,5.9,5.4,1.0,8.5,10.3,7.8,11.5,9.5,2.8,14.1],
    [2.8,6.3,1.6,7.3,2.6,1.5,8.0,9.3,4.8,0.0,9.4,1.1,5.1,4.6,3.7,4.0,6.7,2.3,1.8,4.1,3.8,5.8,4.3,7.8,4.8,3.2,6.0],
    [6.4,7.3,10.4,1.0,6.5,8.7,8.6,4.6,11.9,9.4,0.0,7.3,12.0,4.9,5.2,5.4,8.1,6.2,6.9,11.5,6.9,8.3,4.1,0.4,4.9,11.0,6.8],
    [3.2,5.3,3.0,6.4,1.5,0.8,6.9,4.8,4.7,1.1,7.3,0.0,4.7,3.5,2.6,2.9,6.3,1.2,1.0,3.7,4.1,6.2,3.4,6.9,5.2,3.7,6.4],
    [7.6,4.8,5.3,11.1,7.5,4.5,4.2,7.7,0.6,5.1,12.0,4.7,0.0,7.3,7.8,6.6,7.2,5.9,5.4,1.0,8.5,10.3,7.8,11.5,9.5,2.8,14.1],
    [5.2,3.0,6.5,3.9,3.2,3.9,4.2,1.6,7.6,4.6,4.9,3.5,7.3,0.0,1.3,1.5,4.0,3.2,3.0,6.9,6.2,8.2,5.5,4.4,7.2,6.4,10.5],
    [4.4,4.6,5.6,4.3,2.4,3.0,8.0,3.3,7.8,3.7,5.2,2.6,7.8,1.3,0.0,0.6,6.4,2.4,2.2,6.8,5.3,7.4,4.6,4.8,6.3,6.5,8.8],
    [3.7,4.5,5.8,4.4,2.7,3.8,5.8,3.4,6.6,4.0,5.4,2.9,6.6,1.5,0.6,0.0,5.6,1.6,1.7,6.4,4.9,6.9,4.2,5.6,5.9,5.7,8.4],
    [7.6,7.4,5.7,7.2,1.4,5.7,7.2,3.1,7.2,6.7,8.1,6.3,7.2,4.0,6.4,5.6,0.0,7.1,6.1,7.2,10.6,12.0,9.4,7.5,11.1,6.2,13.6],
    [2.0,6.0,4.1,5.3,0.5,1.9,7.7,5.1,5.9,2.3,6.2,1.2,5.9,3.2,2.4,1.6,7.1,0.0,1.6,4.9,3.0,5.0,2.3,5.5,4.0,5.1,5.2],
    [3.6,5.0,3.6,6.0,1.7,1.1,6.6,4.6,5.4,1.8,6.9,1.0,5.4,3.0,2.2,1.7,6.1,1.6,0.0,4.4,4.6,6.6,3.9,6.5,5.6,4.3,6.9],
    [6.5,4.8,4.3,10.6,6.5,3.5,3.2,6.7,1.0,4.1,11.5,3.7,1.0,6.9,6.8,6.4,7.2,4.9,4.4,0.0,7.5,9.3,6.8,11.4,8.5,1.8,13.1],
    [1.9,9.5,3.3,5.9,3.2,4.9,11.2,8.1,8.5,3.8,6.9,4.1,8.5,6.2,5.3,4.9,10.6,3.0,4.6,7.5,0.0,2.0,2.9,6.4,2.8,6.0,4.1],
    [3.4,10.9,5.0,7.4,5.2,6.9,12.7,10.4,10.3,5.8,8.3,6.2,10.3,8.2,7.4,6.9,12.0,5.0,6.6,9.3,2.0,0.0,4.4,7.9,3.4,7.9,4.7],
    [2.4,8.3,6.1,4.7,2.5,4.2,10.0,7.8,7.8,4.3,4.1,3.4,7.8,5.5,4.6,4.2,9.4,2.3,3.9,6.8,2.9,4.4,0.0,4.5,1.7,6.8,3.1],
    [6.4,6.9,9.7,0.6,6.0,9.0,8.2,4.2,11.5,7.8,0.4,6.9,11.5,4.4,4.8,5.6,7.5,5.5,6.5,11.4,6.4,7.9,4.5,0.0,5.4,10.6,7.8],
    [2.4,10.0,6.1,6.4,4.2,5.9,11.7,9.5,9.5,4.8,4.9,5.2,9.5,7.2,6.3,5.9,11.1,4.0,5.6,8.5,2.8,3.4,1.7,5.4,0.0,7.0,1.3],
    [5.0,4.4,2.8,10.1,5.4,3.5,5.1,6.2,2.8,3.2,11.0,3.7,2.8,6.4,6.5,5.7,6.2,5.1,4.3,1.8,6.0,7.9,6.8,10.6,7.0,0.0,8.3],
    [3.6,13.0,7.4,10.1,5.5,7.2,14.2,10.7,14.1,6.0,6.8,6.4,14.1,10.5,8.8,8.4,13.6,5.2,6.9,13.1,4.1,4.7,3.1,7.8,1.3,8.3,0.0]
]

# Greatest Time Complexity in Package is O(1)
# Package class represents all the components a package might need to be useful in the delivery system
class Package:
    def __init__(self, ID: int, address: str, city: str, state: str, zipCode: int, deadline: str, weight: int, notes: str, status: str, leftHub: str) -> None:
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.leftHub = leftHub

    # improves print formatting in console/terminal
    def __repr__(self):
        return "[ID: {}, Address: {}, City: {}, State: {}, Zipcode: {}, Deadline: {}, Weight: {}, Notes: {}, Status: {}, LeftHub: {}]".format(self.ID, self.address, self.city, self.state, self.zipCode, self.deadline, self.weight, self.notes, self.status, self.leftHub)

    # O(1) time complexity, constant time to reassign value
    # S(1) space complexity
    def updateAddress(self, address: str) -> str:
        self.address = address

    # O(1) time complexity, constant time to reassign value, return self as the updated package
    # S(1) space complexity
    def updateDeliveryStatus(self, status: str):
        self.status = status
        return self

    # O(1) time complexity
    # S(1) space complexity
    def updateTimeLeftHub(self, time: str):
        self.leftHub = time


WGUPS_PACKAGE_FILE: list[Package] = [
    Package(1, "195 W Oakland Ave", "Salt Lake City", "UT", 84115, "10:30AM", 21, "", "HUB", ""),
    Package(2, "2530 S 500 E", "Salt Lake City", "UT", 84106, "EOD", 44, "", "HUB", ""),
    Package(3, "233 Canyon Rd", "Salt Lake City", "UT", 84103, "EOD", 2, "Can only be on truck 2", "HUB", ""),
    Package(4, "380 W 2880 S", "Salt Lake City", "UT", 84115, "EOD", 4, "", "HUB", ""),
    Package(5, "195 W Oakland Ave", "Salt Lake City", "UT", 84111, "EOD", 5, "", "HUB", ""),
    Package(6, "3060 Lester St", "West Valley City", "UT", 84119, "10:30AM", 88, "Delayed on flight--will not arrive until 9:05 am", "HUB", ""),
    Package(7, "1330 2100 S", "Salt Lake City", "UT", 84106, "EOD", 8, "", "HUB", ""),
    Package(8, "300 State St", "Salt Lake City", "UT", 84103, "EOD", 9, "", "HUB", ""),
    Package(9, "300 State St", "Salt Lake City", "UT", 84115, "EOD", 2, "Wrong address listed", "HUB", ""),
    Package(10, "600 E 900 S", "Salt Lake City", "UT", 84105, "EOD", 1, "", "HUB", ""),
    Package(11, "2600 Taylorsville Blvd", "Salt Lake City", "UT", 84118, "EOD", 1, "", "HUB", ""),
    Package(12, "3575 W Valley Station bus loop", "West Valley City", "UT", 84119, "EOD", 1, "", "HUB", ""),
    Package(13, "2010 W 500 S", "Salt Lake City", "UT", 84104, "EOD", 1, "", "HUB", ""),
    Package(14, "4300 S 1300 E", "Millcreek", "UT", 84117, "10:30AM", 88, "Must be delivered wth 15, 19", "HUB", ""),
    Package(15, "4580 S 2300 E", "Holladay", "UT", 84117, "9:00AM", 4, "", "HUB", ""),
    Package(16, "4580 S 2300 E", "Holladay", "UT", 84117, "10:30AM", 88, "Must be delivered with 13, 19", "HUB", ""),
    Package(17, "3148 S 1100 W", "Salt Lake City", "UT", 84119, "EOD", 2, "", "HUB", ""),
    Package(18, "1488 4800 S", "Salt Lake City", "UT", 84123, "EOD", 6, "Can only be on truck 2", "HUB", ""),
    Package(19, "177 W Price Ave", "Salt Lake City", "UT", 84115, "EOD", 37, "", "HUB", ""),
    Package(20, "3595 Main St", "Salt Lake City", "UT", 84115, "10:30AM", 37, "Must be delivered with 13, 15", "HUB", ""),
    Package(21, "3595 Main St", "Salt Lake City", "UT", 84115, "EOD", 3, "", "HUB", ""),
    Package(22, "6351 S 900 E", "Murray", "UT", 84121, "EOD", 2, "", "HUB", ""),
    Package(23, "5100 S 2700 W", "Salt Lake City", "UT", 84118, "EOD", 5, "", "HUB", ""),
    Package(24, "5025 State St", "Murray", "UT", 84107, "EOD", 7, "", "HUB", ""),
    Package(25, "5383 S 900 E #104", "Salt Lake City", "UT", 84117, "10:30AM", 7, "Delayed on flight--will not arrive to depot until 9:05 am", "HUB", ""),
    Package(26, "5383 S 900 E #104", "Salt Lake City", "UT", 84117, "EOD", 25, "", "HUB", ""),
    Package(27, "1060 Dalton Ave S", "Salt Lake City", "UT", 84104, "EOD", 5, "", "HUB", ""),
    Package(28, "2835 Main St", "Salt Lake City", "UT", 84115, "EOD", 7, "Delayed on flight--will not arrive to depot until 9:05 am", "HUB", ""),
    Package(29, "1330 2100 S", "Salt Lake City", "UT", 84106, "10:30AM", 2, "", "HUB", ""),
    Package(30, "300 State St", "Salt Lake City", "UT", 84103, "10:30AM", 1, "", "HUB", ""),
    Package(31, "3365 S 900 W", "Salt Lake City", "UT", 84119, "10:30AM", 1, "", "HUB", ""),
    Package(32, "3365 S 900 W", "Salt Lake City", "UT", 84119, "EOD", 1, "Delayed on flight--will not arrive to depot until 9:05am", "HUB", ""),
    Package(33, "2530 S 500 E", "Salt Lake City", "UT", 84106, "EOD", 1, "", "HUB", ""),
    Package(34, "4580 S 2300 E", "Holladay", "UT", 84117, "10:30AM", 2, "", "HUB", ""),
    Package(35, "1060 Dalton Ave S", "Salt Lake City", "UT", 84104, "EOD", 88, "", "HUB", ""),
    Package(36, "2300 Parkway Blvd", "West Valley City", "UT", 84119, "EOD", 88, "Can only be on truck 2", "HUB", ""),
    Package(37, "410 S State St", "Salt Lake City", "UT", 84111, "10:30AM", 2, "", "HUB", ""),
    Package(38, "410 S State St", "Salt Lake City", "UT", 84111, "EOD", 9, "Can only be on truck 2", "HUB", ""),
    Package(39, "2010 W 500 S", "Salt Lake City", "UT", 84104, "EOD", 9, "", "HUB", ""),
    Package(40, "380 W 2880 S", "Salt Lake City", "UT", 84115, "10:30AM", 45, "", "HUB", "")
]

# Greatest Time Complexity in Truck is O(Nlog(N))
# Greatest Space Complexty in Truck is S(N)
# Truck class represents a delivery vehicle used in the delivery system.
# It transports/hold packages, and can track its own distance traveled,
# as well as define its route to the next package
class Truck:
    def __init__(self) -> None:
        self.maxCapacity: int = 16
        self.packages: list[Package] = []
        self.route: float = 0
        self.totalDistance: float = 0
        self.previousDelivery: Package = None

    # O(1) time complexity, constant time for bool evaluation
    # S(1) space complexity
    def atMaxCapacity(self) -> bool:
        return len(self.packages) == self.maxCapacity
    
    # O(1) time complexity, constant time for append
    # S(1) space complexity
    def addPackage(self, package: Package) -> None:
        if len(self.packages) < self.maxCapacity:
            self.packages.append(package)
    
    # O(N) time complexity, length of packages
    # S(1) space complexity, it doesnt create a new array
    # or store any new values
    def getPackage(self, packageID: int) -> Package | None:
        for p in self.packages:
            if p.ID == packageID:
                return p
            else:
                return None
    
    # Sorts packages by distance for more optimal route calculation
    # O(Nlog(N)) time complexity, full length of while loop -> O(N)
    # and iteratively reduced length of for loop log(N)
    # This algorithm is a "play" on Floyd Warshall's intermediate segment
    # shortest path algorithm. It finds the shortest distance to the next
    # package from the current location iteratively.
    # (GeeksforGeeks, 2024)
    #
    # S(N) space complexity, instantiates a new array. The array space takes
    # precendence over hubDist and firstPackage and shortestDistance
    def sortPackagesByDistance(self, unsortedPackages: list[Package], fromHub=True) -> list[Package]:
        sortedByDistance = []
        
        # get the distance from the hub to first package, first
        # O(N) time complexity, length of unsorted packages
        if fromHub:
            hubDist = 999
            firstPackage = None
            for p in unsortedPackages:
                if DISTANCE_MATRIX[0][ADDRESS_MAP.index(p.address)] < hubDist:
                    hubDist = DISTANCE_MATRIX[0][ADDRESS_MAP.index(p.address)]
                    firstPackage = p

            sortedByDistance.append(firstPackage)
            unsortedPackages.remove(firstPackage)
        else:
            sortedByDistance.append(unsortedPackages[0])
            unsortedPackages.pop(0)

        # O(Nlog(N)) time complexity, the while loop will iterate each package
        # even though it is shrinking, so its linear time. The for loop
        # runs log(N) time because each iteration is shortened as a result
        # of removing a package.
        while len(unsortedPackages) > 0:
            shortestDistance = 999
            p = None
            for i in range(len(unsortedPackages)):
                if DISTANCE_MATRIX[ADDRESS_MAP.index(sortedByDistance[-1].address)][ADDRESS_MAP.index(unsortedPackages[i].address)] < shortestDistance:
                    shortestDistance = DISTANCE_MATRIX[ADDRESS_MAP.index(sortedByDistance[-1].address)][ADDRESS_MAP.index(unsortedPackages[i].address)]
                    p = unsortedPackages[i]
            unsortedPackages.remove(p)
            sortedByDistance.append(p)
            p = None
        self.packages = sortedByDistance
        return sortedByDistance
                    

    # Should be called after packages are sorted
    # O(1) time complexity, append is constant time
    # S(1) space complexity, no new values are created
    def addRouteSegmentDistance(self, dist: float) -> None:
        self.route = self.route + dist

    # O(1) time complexity
    # S(1) space complexity, no new values are created
    def updateTotalDistance(self, dist: float) -> float:
        self.totalDistance = self.totalDistance + dist
        return self.totalDistance
    
    # Returns an integer as a package ID if the route has been updated to a negative value,
    # indicating that the current segment has been met and should be removed
    # O(1) time complexity, all operations are atomic
    # S(1) space complexity, no new values are created
    def updateCurrentSegment(self, dist: float) -> int | None:
        self.route = self.route - dist

        # if the route is now negative, it should be delivered
        if self.route < 0:
            return self.packages[0].ID
        # if the route segment still needs to be traveled, return None
        return None

    # Deliver package will deliver ALL packages on the truck that correspond
    # to the current address the truck is at.
    # O(N) time complexity, both getPackage and the filter run linear
    # S(log(N)) space complexity, new array instantiated - additionalDeliveries
    # but its length may be less than the entire package array
    def deliverPackage(self, packageID: int) -> list[int]:
        package = self.getPackage(packageID)
        additionalDeliveries: list[int] = [package.ID]
        for p in self.packages:
            if p.address == package.address:
                additionalDeliveries.append(p.ID)
        # O(N) time complexity, compares each package to filter condition
        self.packages = list(filter(lambda pkg: pkg.address != package.address, self.packages))
        self.previousDelivery = package
        if len(self.packages) > 0:
            rowCol = addressesToInts(package.address, self.packages[0].address)
            self.addRouteSegmentDistance(DISTANCE_MATRIX[rowCol[0]][rowCol[1]])

        return additionalDeliveries

# Greatest Time Complexity in PackageHashTable is O(N^2)
# Greatest Space Complexity in PackageHashTable is S(N^2)
# PackageHashTable class is a direct hashtable with lookup and insert functions
class PackageHashTable:
    def __init__(self, size: int) -> None:
        # Direct hashtable needs a size equivalent to the highest key,
        # in this case its 40 based on the provided package list.
        # Add one to the hashtable size to account for non-zero indexed
        # package ID's to avoid a resize on the first batch of packages
        # O(N^2) time complexity, length of size argument, multiplied be
        # each sub array
        # S(N^2) space complexity, 2D array
        self.hashTable: list[list] = [[None] for j in range(size + 1)]

    # Direct hashing with chaining to store related values of the same Package
    # This function also functions as an update function when package data changes
    # Avoids collisions based on unique package ID's
    # O(N^2) time complexity, hashTable can be extended by looping current table
    # range
    # S(Nlog(N^2)) space complexity, length of array can be extended. The extension
    # would have a S(N^2) space complexity, multiplied by the new length of the array
    # being S(Nlog(N))
    def hashInsert(self, package: Package) -> None:
        # Check if packageID is within hashtable range
        # if not, double hashtable size
        if package.ID > len(self.hashTable) - 1:
            self.hashTable.extend([[None] for j in range(len(self.hashTable))])
        self.hashTable[package.ID] = [package.address, package.city, package.state, package.zipCode, package.deadline, package.weight, package.notes, package.status, package.leftHub]

    # Lookup a Package by its ID, returns all components of the package from the hashtable
    # O(1) time complexity, constant time because of array index access
    # S(1) space complexity, package value is saved, nothing new is created
    def hashLookupPackage(self, packageID: int) -> Package | None:
        p = self.hashTable[packageID]
        if p == None:
            return None
        return Package(packageID, p[0], p[1], p[2], p[3], p[4] , p[5], p[6], p[7], p[8])

# Greatest Time Complexity in Hub is O(N^2), as a result of creating the hashtable
# Greate Space Complexity in Hub is S(N^2), as a result of creating the hashtable
class Hub:
    def __init__(self, numTrucks: int, numPackages: int) -> None:
        self.trucksAtHub: list[Truck] = [Truck() for i in range(numTrucks)]
        self.packages: PackageHashTable = PackageHashTable(numPackages)

    # addPackages will insert all packages at the hub into the hubs "database"
    # as a hashtable
    # O(N) time complexity, length of packages
    # S(1) space complexity, new packages are being placed into the hashtable,
    # but those locations in memory are already initialized
    def addPackages(self, packages: list[Package]) -> None:
        for p in packages:
            self.packages.hashInsert(p)

    # loadTrucks will load all trucks at the hub with all packages currently
    # at the hub, up to a maximum capacity for each truck
    # Utilizes the heuristic that we don't care what the optimal package to
    # truck placement is, the optimal route will be determined once the truck
    # is loaded
    # O(Nlog(N)) time complexity
    # S(N) space complexity for arrays instantiated to hold ints
    def loadTrucks(self) -> None:
        # setup lists to hold pre-sorted (by special notes) packages onto trucks
        nonSpecialNotes: list[int] = []
        withOtherPackage: list[int] = []
        onlyTruck2: list[int] = []
        delayedArrival: list[int] = []
        # O(N) time complexity, length of packages.hashTable
        for index, p in enumerate(self.packages.hashTable):
            if p == [None]: continue
            if p[6] == "":
                nonSpecialNotes.append(index)
                continue
            if p[6].count("Can only be") > 0:
                onlyTruck2.append(index)
                continue
            if p[6].count("Must be delivered") > 0:
                withOtherPackage.append(index)
                continue
            if p[6].count("Delayed on flight") > 0 or p[6] == "Wrong address listed":
                delayedArrival.append(index)
                continue
        #combine "sorted" packages lists into one for distribution to trucks, except delayed
        distribution = []
        distribution.extend(withOtherPackage)
        distribution.extend(nonSpecialNotes)

        # go ahead and sort these packages by distance, they will be resorted later as needed
        # this section and the section below are "after thought" sections. I had made a mistake
        # that wasn't caught until my program was completed (two drivers, three trucks, they can't
        # all be out at the same time...). The sorting was done on the trucks, which is why the
        # truck class has the method. But after refactoring the driving situation, my deadlines
        # were no longer being met. So I decided to sort the packages here first, and on the trucks
        # later, which ended up actually shortening the total distance traveled (yay). But to
        # change the least amount of code, i decided to refactor the sort method on the truck
        # class to return the sorted packages so i could use it here to pre-sort the packages.
        # The conversions occuring with the maps here were to avoid having to refactor the above
        # section that places the packages into their respective distribution arrays. So it's
        # int -> Package -> sort -> int -> place on trucks.
        distribution = list(map(lambda i: self.packages.hashLookupPackage(i), distribution))
        distribution = self.trucksAtHub[0].sortPackagesByDistance(distribution)
        distribution = list(map(lambda p: p.ID, distribution))

        # clear the packages from truck[0], a side effect of non-static method. By the time
        # this utility was discovered, the program was VERY built-out. And instead of either
        # refactoring the truck class or duplicating code, im just going to clear the packages
        # from the truck that provided the method.
        self.trucksAtHub[0].packages.clear()

        # use the distribution list to place packages on trucks until they reach max capacity,
        # then move to the next truck, ending with the last truck having all delayed packages
        # load truck two first with all truck two exclusive packages
        # O(N) time complexity, length of onlyTruck2
        # S(N) space complexity, memory for each array location is created
        for p in range(len(onlyTruck2)):
            self.trucksAtHub[1].addPackage(self.packages.hashLookupPackage(onlyTruck2[p]))

        # load trucks with all packages from distribution
        # O(Nlog(N)) time complexity, the while loop could be shortened
        # to less than the max length of a truck if its at max capacity,
        # or if the distribution length is out of range
        # S(N) space complexity, memory for each array location is created in truck package array
        i = 0
        for t in self.trucksAtHub:
            while not t.atMaxCapacity() and i < len(distribution):
                t.addPackage(self.packages.hashLookupPackage(distribution[i]))
                i = i + 1

        # load last truck with remaining packages
        # O(N) time complexity, length of delayedArrival
        # S(N) space complexity, memory for each array location is created in truck package array
        for p in delayedArrival:
            pack = self.packages.hashLookupPackage(p)
            self.trucksAtHub[2].addPackage(pack)




# Truck driving speed
SPEED = 18
MILES_PER_MINUTE = SPEED/60

# (N^2log(N)) time complexity for the while loop with nested for loops
# S(N^2) space complexity, building hashtable in Hub
def main():
    print("- WGUPS -")
    h = Hub(3, len(WGUPS_PACKAGE_FILE))
    print("Hub is open for business")
    time.sleep(1)
    h.addPackages(WGUPS_PACKAGE_FILE)
    print("Packages have arrived at the Hub")
    time.sleep(1)
    h.loadTrucks()
    print("Trucks have been loaded with Hub packages")
    time.sleep(1)
    for t in h.trucksAtHub:
        t.sortPackagesByDistance(t.packages)
    print("Packages sorted on trucks for optimal routing")
    time.sleep(1)
    print("-----------------------------------------------------------------------------")
    print("")
    
    # start time corresponds to 8:00am -> 8 hours * 60 minutes to convert to a "per minute" time tracking system
    startTime = 8 * 60
    
    # O(log(N)) time complexity, the loop could break before it reads each index
    # S(1) space complexity
    def allPackagesDelivered(hub: Hub) -> bool:
        for p in range(len(hub.packages.hashTable)):
            if p == 0: continue
            if hub.packages.hashLookupPackage(p).status == "En Route" or hub.packages.hashLookupPackage(p).status == "HUB":
                return False
        if startTime < 17 * 60: return False
        return True
    
    # add routes segments distances to each truck
    # O(N) time complexity, length of trucksAtHub
    # S(N) addressToInts function builds and array stored as rowCol
    for t in h.trucksAtHub:
        # find the distance between the current package and the next package
        rowCol = addressesToInts(t.packages[0].address, t.packages[1].address)
        t.addRouteSegmentDistance(DISTANCE_MATRIX[rowCol[0]][rowCol[1]])

    # update trucks 1 and 2 to En Route for all packages, truck 3 is delayed to start
    # until packages "arrive" (they are "loaded" on the truck now, but this delay is to simulate
    # the packages not being on the truck until they arrive, for simplicity)
    # O(N^2) time complexity, double for loop
    # S(1) space complexity, package value instantiated
    for t in range(2):
        for p in h.trucksAtHub[t].packages:
            package = p.updateDeliveryStatus("En Route")
            package.updateTimeLeftHub(str(math.floor(startTime / 60)).zfill(2) + ":" + str(startTime % 60).zfill(2))
            h.packages.hashInsert(package)

    # Truck 3 is waiting on packages at the startTime until 9:05am
    truck3Ready = False

    # Package 9 updated waits on address change
    package9Updated = False

    # Track all trucks and packages by the minute until all packages are delivered
    # O(N^2log(N)) time complexity, the while loop could be shortened to less than
    # linear time because of multiple packages being delivered simultaneously O(log(N)). The
    # nest for loops inside the while are O(N^2)
    # Keep looping until all packages are delivered and the time is at least 5:00pm
    #
    # S(1) space complexity, constant values are instantiated, but assuming garbage collection,
    # they are destroyed after each iteration. There are no new arrays instantiated
    while allPackagesDelivered(h) == False:
        startTime = startTime + 1
        # check if start time is 9:15am to dispatch truck 3
        if truck3Ready == False:
            if len(h.trucksAtHub[0].packages) == 0:
                truck3Ready = True
                # add the distance back to hub to this truck so the driver can switch trucks
                h.trucksAtHub[0].updateTotalDistance(DISTANCE_MATRIX[0][ADDRESS_MAP.index(h.trucksAtHub[0].previousDelivery.address)])
                for p in h.trucksAtHub[2].packages:
                    package = p.updateDeliveryStatus("En Route")
                    package.updateTimeLeftHub(str(math.floor(startTime / 60)).zfill(2) + ":" + str(startTime % 60).zfill(2))
                    h.packages.hashInsert(package)
            elif len(h.trucksAtHub[1].packages) == 0:
                truck3Ready = True
                # add the distance back to hub to this truck so the driver can switch trucks
                h.trucksAtHub[1].updateTotalDistance(DISTANCE_MATRIX[0][ADDRESS_MAP.index(h.trucksAtHub[1].previousDelivery.address)])
                for p in h.trucksAtHub[2].packages:
                    package = p.updateDeliveryStatus("En Route")
                    package.updateTimeLeftHub(str(math.floor(startTime / 60)).zfill(2) + ":" + str(startTime % 60).zfill(2))
                    h.packages.hashInsert(package)

        # update package ID 9 with correct address
        if startTime == (10 * 60 + 20) and package9Updated == False:
            package9Updated = True
            toUpdate = h.packages.hashLookupPackage(9)
            toUpdate.updateAddress("410 S State St")
            h.packages.hashInsert(toUpdate)
            p9 = None
            # O(N) time complexity, linear time
            for p in range(len(h.trucksAtHub[2].packages)):
                if h.trucksAtHub[2].packages[p].ID == 9:
                    p9 = p
            h.trucksAtHub[2].packages[p9] = toUpdate
            h.trucksAtHub[2].sortPackagesByDistance(h.trucksAtHub[2].packages, False)

        
        # O(N^2) time complexity for each if/else block, double for loop
        if truck3Ready:
            for t in h.trucksAtHub:
                if len(t.packages) == 0: continue
                _ = t.updateTotalDistance(MILES_PER_MINUTE)
                deliver = t.updateCurrentSegment(MILES_PER_MINUTE)
                if deliver != None:
                    pID = t.deliverPackage(deliver)
                    for i in pID:
                        packageToUpdate = h.packages.hashLookupPackage(i)
                        newPackage = packageToUpdate.updateDeliveryStatus("Delivered - " + str(math.floor(startTime / 60)).zfill(2) + ":" + str(startTime % 60).zfill(2))
                        h.packages.hashInsert(newPackage)
        else:
            for index, t in enumerate(h.trucksAtHub):
                if index > 1: break
                if len(t.packages) == 0: continue
                _ = t.updateTotalDistance(MILES_PER_MINUTE)
                deliver = t.updateCurrentSegment(MILES_PER_MINUTE)
                if deliver != None:
                    pID = t.deliverPackage(deliver)
                    for i in pID:
                        packageToUpdate = h.packages.hashLookupPackage(i)
                        newPackage = packageToUpdate.updateDeliveryStatus("Delivered - " + str(math.floor(startTime / 60)).zfill(2) + ":" + str(startTime % 60).zfill(2))
                        h.packages.hashInsert(newPackage)
    
    # Finally, add the distance from the last package delivered to the hub for each truck's calculation
    print("-----------------------------------------------------------------------------")
    print("Truck 1 Distance Traveled: ", f"{h.trucksAtHub[0].updateTotalDistance(DISTANCE_MATRIX[ADDRESS_MAP.index(h.trucksAtHub[0].previousDelivery.address)][0]):3.2f}")
    print("Truck 2 Distance Traveled: ", f"{h.trucksAtHub[1].updateTotalDistance(DISTANCE_MATRIX[ADDRESS_MAP.index(h.trucksAtHub[1].previousDelivery.address)][0]):3.2f}")
    print("Truck 3 Distance Traveled: ", f"{h.trucksAtHub[2].updateTotalDistance(DISTANCE_MATRIX[ADDRESS_MAP.index(h.trucksAtHub[2].previousDelivery.address)][0]):3.2f}")
    print("Total Distance Traveled: ", f"{h.trucksAtHub[0].totalDistance + h.trucksAtHub[1].totalDistance + h.trucksAtHub[2].totalDistance:3.2f}")

    inpt = input("Would you like to see the delivery statuses at a particular time? [y]es or [n]o\n")
    # O(N) time complexity, the while loop goes indefinitely, but always linear
    # S(N) space complexity for newly instantiated arrays
    if inpt == 'y' or inpt == 'n':
        while inpt != "n":
            whatTime = input("What time would you like to see? Format your time as 24hour time. I.E. 5:30pm = 17:30 | 6:30am = 06:30\n")
            if len(whatTime) != 5 or whatTime[2] != ":":
                print("Improper format, exiting program...")
                break
            t = whatTime.split(":")
            val = int(t[0]) * 60 + int(t[1])
            hub = []
            route = []
            delivered = []
            for p in range(len(h.packages.hashTable)):
                if p == 0: continue
                pT = h.packages.hashLookupPackage(p)
                pSplit = pT.leftHub.split(":")
                pDel = pT.status[-6:].split(":")
                pDelVal = int(pDel[0]) * 60 + int(pDel[1])
                # Please note at lines 514-526 that the address is programatically
                # updated to the correct address at 10:20am. However, since
                # this user interface occurs after all calculations have completed,
                # to render the "proper" address for this time, it must be 
                # temporarily changed back to the original address for the user's
                # understanding.
                if p == 9 and val < (10 * 60 + 20):
                    pT.updateAddress('300 State St')
                if pDelVal <= val:
                    delivered.append(pT)
                    continue
                pVal = int(pSplit[0]) * 60 + int(pSplit[1])
                if pVal > val:
                    hub.append(pT)
                    continue
                route.append(pT)
            print("At Hub:")
            for h in hub:
                print(h)
            print("----------------------------------------")
            print("En Route:")
            for r in route:
                print(r)
            print("----------------------------------------")
            print("Delivered:")
            for d in delivered:
                print(d)
            print("----------------------------------------")
            inpt = input("Would you like to see another time? [y]es or [n]o\n")

main()