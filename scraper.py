# This is a template for a Python scraper on Morph (https://morph.io)
# including some code snippets below that you should find helpful
 
import scraperwiki
import lxml.html
 
def save_data(elem, jobs):
    # Get all the span elements which has the data we look for
    for span in elem.cssselect('span'):
        jobs[span.attrib['class']] = span.text_content()
    # Saving to the DB. Needs a dict and a unique key
    print scraperwiki.sqlite.save(unique_keys=['link'], data=jobs)
 
def scrape_content(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # select all the stickies except the first one
    # Technically siblings of the first stickie that says POST A JOB
    # Refer http://api.jquery.com/next-siblings-selector/ 
    for job in root.cssselect('ul#stickie-area li#newpost ~ li'):
        jobs = dict()
        # Have to build the URL as the anchor is relative
        jobs['link'] = url + job.cssselect('a')[0].attrib['href']
        if (job.attrib['class'] == "stickie grouped"): # group postings
            # Get all direct children of the grouped stickie
            # Refer http://api.jquery.com/child-selector/
            for elem in job.cssselect('li > *'):
                save_data(elem, jobs)
        else:
            save_data(job, jobs)
 
# Let's get started
src = 'http://jobs.hasgeek.in'
scrape_content(src)
# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries. You can use whatever libraries are installed
# on Morph for Python (https://github.com/openaustralia/morph-docker-python/blob/master/pip_requirements.txt) and all that matters
# is that your final data is written to an Sqlite database called data.sqlite in the current working directory which
# has at least a table called data.
