# mvp-haystack
https://www.notion.so/Haystack-Test-770b81bc302d4997a98be926cc207b97


Data Method and Source

Means: External API
Orginal Source: https://data.cityofnewyork.us/resource/8b6c-7uty.json
Appended later: https://data.cityofnewyork.us/resource/kybe-9iex.json


Develop a data model of all relevant datasets

The data source was seleced from [https://opendata.cityofnewyork.us/](https://opendata.cityofnewyork.us/), which is a NYC public platform to extract local information like Education, Health, Business, Housing Development etc.

The dataset that I chose to work with pertains particuarly to school information, providing general details about each available school such as Address, Graduation rate, and Gradespan. I chose this data source because it has been my experience working in real estate that the quality of schools and the gradespan available has a significant affect on the value of the residence. 

In the case of nyc, most residential units are considered a condominium or cooperative "apartment" not your regular single family "house". However this difference still doesn't remove the strong demand existing from parents for their children to have a good education. Albeit, it would probably be true that this value is not as concentrated in NYC versus the suburbs because of the high contrast in lifestyle/demographic variability.

In regards to the code, I set up a very simple ETL with python that leverages libraries Prefect for workflow orchestration and Pandas for transformation. Prefect has the same ostentible purpose as Airflow, to help automate the data workflow, but in my opinion is a far more elegant solution in part by its applications of decorators to modularize each component of pipeline,minimal module complexity, and native integration with Dask. Pandas effectively creates a table out of the data that can be easily manipulated and is technically performant through vectorized operations. 

There are a couple notes to add for the pipeline, first I would use the Dask integration if the size of the data warrants it, in this case it does not. [Dask](https://en.wikipedia.org/wiki/Dask_(software)) is a great tool for parallel computing. Second, I only have very basic transformations at the moment, this is generally not the case because typically datasets have prexisting issues or there is misalignment with how you intend to use it. Additionally a second dataset was added later to augment the school results and showcase the flexibility of the data. This has not been reflected in the ERD due to time contraints.

Lastly, I would load this data into the bucket or BLOB storage from an external source
as a data lake/staging area for other services. Athena was added to the infrastructure because it's a cost efficient and robust way to query the data directly from the bucket. I would most likely support an Aurora RLDB for continous CRUD operations and Redshift for business intelligence.

Potential Areas of Improvement improvement

Other potential sources of value include zoning data, particularly by stages of approval.

Table could be denormalized to results table and school table. 
More maintenance but improved read speed if behavior warrants it. 

Pipeline can be decoupled into interface layer and pipeline(s).

CI/CD tool implemented using Github > CodePipeline(integrates) > Elastic BeanStalk(deploys app and severless)
Terraform added as an Iaas to automate infrastructure set up.

Additional storage for failover/emergency copies.
