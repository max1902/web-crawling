
import sys
import datetime as dt
import urllib
import datetime
import pandas as pd

from lxml import html, etree


def monster(search_word):
    
    base_url = 'https://www.monster.de/jobs/suche/?q=' + search_word
    
    response = urllib.urlopen(base_url)
    tree = html.fromstring(response.read())
    
    columns = ['title','company_name','location', 'date_of_submission', 'url']
    df = pd.DataFrame(columns=columns)
    
    max_pages = tree.xpath('.//input[@id="totalPages"]/@value')
    if max_pages:
        max_pages = int(max_pages[0])
        for index in range(1, max_pages)[:10]:
            # pagination
            next_url = base_url + '&page=' + str(index)
            page = urllib.urlopen(next_url)
            _tree = html.fromstring(page.read())
            df = get_necessery_data(_tree, columns, df)
    else:
        df = get_necessery_data(tree, columns, df)

    df = df.reset_index(drop=True)
    now = datetime.datetime.today().strftime("%d/%m/%Y")
    df['search_date'] = now
    csv_file = 'monster.csv'
    df.to_csv(csv_file, encoding='utf-8')
    print len(df), 'result saved as \'', csv_file, '\''

def get_necessery_data(tree, columns, df):
    xp_urls = '//div[@class="jobTitle"]/h2/a/@href'
    xp_company_name = '//span[@itemprop="name"]/text()'
    xp_title = '//span[@itemprop="title"]/text()'
    xp_location =  '//span[@itemprop="address"]'
    xp_data = '//time[@itemprop="datePosted"]/@datetime'

    date_of_submission, company_name, location, title, url = \
            [], [], [], [], []
    # get link to job
    for val in tree.xpath(xp_urls):
        url.append(val)
    # get company name
    for val in tree.xpath(xp_company_name):
         company_name.append(val)
    # get title of a job
    for val in tree.xpath(xp_title):
        title.append(val)
    # get location
    for val in tree.xpath(xp_location):
        location.append(val.text.strip())
    # get published date
    for val in tree.xpath(xp_data):
        date_of_submission.append(val)
        
    # prepare headers to temporary frame
    data = [title, company_name, location, date_of_submission, url]
    # create temporary frame
    temp_df= pd.DataFrame(data)
    temp_df = temp_df.transpose()
    temp_df.columns = columns
    frames = [df, temp_df]
    # concatination temporary frame to main frame
    df = pd.concat(frames)
    return df

if __name__ == '__main__':
    search_word = sys.argv[1]
    monster(search_word)