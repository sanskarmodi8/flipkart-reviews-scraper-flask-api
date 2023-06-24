
#this flask api code is hosted at https://salmon-policeman-fothu.pwskills.app:5000/result




from flask import Flask, request,jsonify, json
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

@app.route('/result', methods=['POST', 'GET'])
def scrape():
  if request.method == 'POST':
    try:
        product_name = request.json.get('productName').replace(" ","")
        flipkart_url = "https://www.flipkart.com/search?q=" + product_name
        uClient = uReq(flipkart_url)
        flipkartpage = uClient.read()
        uClient.close()
        flipkart_html = bs(flipkartpage, "html.parser")
        bigdivs = flipkart_html.findAll("div", {"class":"_1AtVbE col-12-12"})
        del bigdivs[0:3]
        box = bigdivs[0]
        productlink = "https://www.flipkart.com" + box.div.div.div.a['href']
        product = requests.get(productlink)
        product.encoding = 'utf-8'
        product_html = bs(product.text, "html.parser")
        commentboxes = product_html.findAll('div', {'class': "_16PBlm"})
        reviews = []
        for commentbox in commentboxes:
            try:
                name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                
            except:
                name = "N/A"
            try:
                rating = commentbox.div.div.div.div.text
            except:
                rating = "N/A"
            try:
                commentheading = commentbox.div.div.div.p.text
            except:
                commentheading = "N/A"
            try:
                commentmsg = commentbox.div.div.find_all('div', {'class': ''})[0].div.text
            except:
                commentmsg = "N/A"
                
            mydict ={"Product": product_name, "Customer Name": name, "Rating": rating, "Comment Heading": commentheading,
                                "Comment Message": commentmsg}
            reviews.append(mydict)
    except:
        return "something is wrong"

    return jsonify(reviews)
  else:
      return "backend flask api"


if __name__ == "__main__":
    app.run(debug=True)
