# For getting Jobs From Hasgeek Hasjobs
 
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
src = 'https://hasjob.co'
scrape_content(src)
