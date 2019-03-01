#!/usr/bin/env python3
import psycopg2 as pg

#  database name
DATA_BASE = "news"
#  Query for most popular three articles of all time
query1 = """select articles.title,count(*) from log,articles
        where log.path=('/article/'||articles.slug)
        group by articles.title order by count(*) desc limit 3"""

#  Query for most popular article authors of all time
query2 = """select authors.name,count(*) from log,articles,authors
        where log.path='/article/'||articles.slug and
        articles.author=authors.id group by authors.name
        order by count(*) desc"""

#  Query for more than 1% of requests leads to errors
query3 = """select
            to_char(errors_by_day.date,'Month DD, YYYY') as date,
            to_char(((errors_by_day.count::decimal
                    /requests_by_day.count::decimal)*100)
                    ,'9.99')
                    || '%' as percentage
        from
            (select date(time),count(*) from log
                        group by date(time)) as requests_by_day,
            (select date(time),count(*) from log where status != '200 OK'
                        group by date(time)) as errors_by_day
        where
            requests_by_day.date = errors_by_day.date
            and ((errors_by_day.count::decimal
                    /requests_by_day.count::decimal)*100) > 1;"""


#  Query execution and declaration
def get(query):
    db = pg.connect(database=DATA_BASE)
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    for r in result:
        print('{title}  <-  {count} views'.format(title=r[0], count=r[1]))
    print("\n")
    db.commit()
    db.close()


#  call for first query
def query1_result():
    print("Most popular three articles of all time")
    return get(query1)


#  call for second query
def query2_result():
    print("Most popular article authors of all time")
    return get(query2)


#  call for third query
def query3_result():
    print("More than 1% of request leads to errors")
    return get(query3)


#  Main function
if __name__ == "__main__":
    query1_result()
    query2_result()
    query3_result()
