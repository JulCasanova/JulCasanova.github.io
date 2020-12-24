
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request

from stoveavailabilitychecker import readinurl, createitemdict, splitdict

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=["GET","POST"])


def first_page():
    errors = ""
    if request.method == "POST":
        zipcode = None
        try:
            testvar = float(request.form["zipcode"])
            if len(request.form["zipcode"]) != 5 :
                raise Exception("it isn't 5 digits long")
            zipcode = request.form["zipcode"]
        except:
            errors += "<p>{!r} is not a valid zip code.</p>\n".format(request.form["zipcode"])

        if zipcode is not None:
            #itemiddict = createitemdict(readinurl() )
            itemiddict = createitemdict('class="bttn-outline bttn-outline--dark js-trigger-custom-package"\n     data-itemId="314138205"\n     data-productLabel="30 in. 5.3 cu. ft. Electric Range with Self-Cleaning Convection Oven and Air Fry in Stainless Steel"\n     data-productType="MAJOR_APPLIANCE"\ndata-imageUrl="https://images.homedepot-static.com/productImages/4ff5346f-3ba8-49b3-8261-ccca2edf8bbd/svn/stainless-steel-ge-single-oven-electric-ranges-jb735spss-64_&lt;SIZE&gt;.jpg"\ndata-categoryHierarchy="[Appliances, Ranges, Electric Ranges, Single Oven Electric Ranges]"'.splitlines())
            finaldicts = splitdict(itemiddict, zipcode)
            result = finaldicts[0]
            #result = "testing"
            return '''
                <html>
                    <body>
                        <p>The result is {result}</p>
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=str(result))


    return '''
        <html>
            <body>
            {errors}
                <p>Enter zip code:</p>
                <form method="post" action=".">
                    <p><input name="zipcode" /></p>
                    <p><input type="submit" value="Submit" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)