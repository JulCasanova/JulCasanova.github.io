
import urllib.request

# I can only find a url that gives the first 24 results. I would like one with all appliances
# ultimately ill just make a database of the product ids in the showroom
# this code just takes the first page of the section of the site for electric ranges and reads it in as a file
# I need to figure out how to do all pages
def readinurl() :
    searchurl = 'https://www.homedepot.com/b/Appliances-Ranges-Electric-Ranges/30-in/N-5yc1vZc3obZ1z0yhyo?experienceName=newappliancev3/'
    with urllib.request.urlopen(searchurl) as f:
        html = f.read().decode('utf-8')
        htmlsplit = html.splitlines()
    return htmlsplit

# takes the entire html file and takes out the lines with the data-itemId which are the product internet ID number of each stove (kind of like the model number)
# basically I am just building a dictionary with product internet ID numbers as keys and a list containing the product name and an image url
# for some reason the model number is not available here so I am adding it in the next step when we use the availibility checking url
def createitemdict(htmlsplit):
    itemiddict = {}
    for x in range(len(htmlsplit)):
        # this finds the line which has the internet ID for each unique stove in it
        if htmlsplit[x].startswith("     data-itemId"):
            # this slices out the ID and adds it as a key for a dictionary which has lists for each internet ID
            # sample line looks like this:      data-itemId="314138205"
            itemiddict[htmlsplit[x][18:27]] = []

            # The product name is one line after this in the file so we slice it out of the line in the file and add it as an element in the list for that internet ID
            # sample line looks like this:      data-productLabel="30 in. 5.3 cu. ft. Electric Range with Self-Cleaning Convection Oven and Air Fry in Stainless Steel"
            itemiddict[htmlsplit[x][18:27]].append(htmlsplit[x+1][24:-1])

            # a url with the product image is 3 lines after the item ID code so I add that to the dictionary also (we need to cut off the end and choose an image size in the url which is what the '400.jpg' is
            # sample line looks like this:      data-imageUrl="https://images.homedepot-static.com/productImages/4ff5346f-3ba8-49b3-8261-ccca2edf8bbd/svn/stainless-steel-ge-single-oven-electric-ranges-jb735spss-64_&lt;SIZE&gt;.jpg"
            itemiddict[htmlsplit[x][18:27]].append(htmlsplit[x+3][20:-17]+'400.jpg')
    return itemiddict

# when you type a zip code into the product page, the home depot website sends it to a url to check availability based on the zip code and product internet ID number
# here is a sample of what the input and output looks like
# input in web browser: https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/314138205/zipCode/02896
# output in web browser: {"DeliveryAvailabilityResponse":{"deliveryAvailability":{"zipCode":"02896","primaryStrNbr":"4282","availability":[{"itemId":"314138205","modelNbr":"JB735SPSS","status":"BACK_ORDERED","etaDate":"2021-05-02T20:28:45.968Z"}]}}}

# for each item code in the list of codes open the availability checker url and if it's available add it to the availdict, if theyre not available add to the unavaildict
# takes dictionary of all items and a zipcode and splits into available and unavailable based on zip code
# this takes a while to run
def splitdict(itemiddict, zipcode):
    availdict = {}
    unavaildict = {}
    for itemid in itemiddict:
            with urllib.request.urlopen("https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/" + itemid + "/zipCode/" + str(zipcode) ) as g:
                availhtml = g.read().decode('utf-8')

            # the model number is sandwiched between these two substrings, the output isnt a constant length so I find it by taking whatever is between these two strings
            start = 'modelNbr":"'
            end = '","status"'

            # if the string '\"AVAILABLE\"' is in the output it is available so add it to the availdict
            # I THINK IF ITS BACKORDERED WE CAN STILL ORDER IT SO CHANGE THIS LATER
            # I THINK IF ITS BACKORDERED WE CAN STILL ORDER IT SO CHANGE THIS LATER
            # I THINK IF ITS BACKORDERED WE CAN STILL ORDER IT SO CHANGE THIS LATER
            # add whatever the string is for backordered
            # also add the date available, that would be nice
            if "\"AVAILABLE\"" in availhtml:
                # This line adds the item id to the availdict and adds the model number to the list in the dictionary for that item id
                availdict[itemid] = itemiddict[itemid]
                availdict[itemid].append( str( availhtml[availhtml.index(start)+len(start) : availhtml.index(end)] ) )
                #print("Item "+itemid+" is AVAILABLE")
            else :
                # This line adds the item id to the unavaildict and adds the model number to the list in the dictionary for that item id
                unavaildict[itemid] = itemiddict[itemid]
                unavaildict[itemid].append( str( availhtml[availhtml.index(start)+len(start) : availhtml.index(end)] ) )
                #print("Item "+itemid+" is UNAVAILABLE")
    return (availdict,unavaildict)


# we are left with one dictionary itemiddict with all scraped item ids as keys with their product name and image url in a list as values
# itemiddict[itemid] = [name, imageurl]
# and two dictionaries availdict and unavaildict which break it down into available and unavailable and have the model number attached
# availdict[itemid] = [name, imageurl, modelno]