# Decagon_test

DOCUMENTATION FOR DECAGON TEST FOR  A DATA ENGINEERING ROLE

I loaded all the tables into postgresql database using python script.

2A. I joined the two tables(Countries and Continent to achieve the result)

***select co."Continent", count(c."CountryCode") as "Country Count" from public."Continent" as co 
join public.countries as c 
on co."ContinentCode" = c.continent
group by co."Continent"***


2B. I created a view to unnest the column "languages" in the countries table and then clean up the column to remove curly brackets({})

***create view languages as select "Country",replace(replace("language",'}',''),'{','')  as lang from public.countries,
unnest(string_to_array("languages", ',')) as language***

I then did a join of the view with the sql table language by aggregating the country column from the view and joining the table/view on the language code column

***select lg."native" as Language,
  string_agg(ls."Country", ',') as Countries
from language as lg
join languages as ls on lg."LangCode" = ls."lang"
group by native
order by native asc***


2C. I did a count of each occurrence of language in languages column from the countries table against countries to achieve 2c.

***SELECT "Country", array_length(string_to_array(languages, ','), 1)  as "Lng Count" FROM public.countries***
