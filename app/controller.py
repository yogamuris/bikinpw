from app.helpers import generate_url

class UrlController:
    def post_url(self, request, db):
        long_url = request.form['long_url']
        short_url = request.form['short_url']
        rnd_url = generate_url()
        
        conn = db.connect()
        cur = conn.cursor()

        result = cur.execute("SELECT shorturl FROM urlshortener where shorturl = %s", [short_url])
        
        if(result == 0):
            if(short_url == ""):
                cur.execute("INSERT INTO urlshortener(longurl, shorturl, tanggal) values (%s, %s, now())", (long_url, rnd_url))
                conn.commit()
                conn.close()

                return "found", rnd_url
            elif(not short_url.isalnum()):
                message = "Use letters, numbers, or both for Custom URL"

                return "error", message
            else:
                cur.execute("INSERT INTO urlshortener(longurl, shorturl, tanggal) values (%s, %s, now())", (long_url, short_url))
                conn.commit()
                conn.close()
                
                return "found", short_url
        else:
            message = "This Custom URL is already used by someone"
            return "used", message


    def get_short_url(self, db, shorturl):
        conn = db.connect()
        cur = conn.cursor()
        result = cur.execute("SELECT longurl FROM urlshortener where shorturl = binary %s", [shorturl])

        if result == 0:
            return ""
        else:
            longurl = cur.fetchone()
            url = longurl[0]
            return url