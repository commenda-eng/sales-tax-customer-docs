# How to run the project locally ?

1. Install the temporal CLI using 

```shell
brew install temporal
```

2. Clone the github repo from here \- [https://github.com/commenda-eng/commenda-temporal-dsl](https://github.com/commenda-eng/commenda-temporal-dsl)  
3. Create a .env file  
   1. **COMMENDA\_LOGICAL\_BACKEND\_API\_KEY \-** used to interact with the logical backend.  
   2. **COMMENDA\_LOGICAL\_BACKEND\_CLIENT\_KEY** \- to validate the requests coming from the logical backend.  
      

```ts
COMMENDA_TEMPORAL_BACKEND_API_KEY=RjrbIP9ZNYkuMf6ICRQLDwTdcfeoIaQU6T0DcIl3UjcXsXFC2JsrThQ6FLE8W3qk
COMMENDA_LOGICAL_BACKEND_API_KEY=5d19648dc2800784225ff909cb1682bf3d5f51d6181114eaae8ee2396320b8c2
COMMENDA_LOGICAL_BACKEND_API_URL=http://localhost:8000/api/v1
TEMPORAL_NAMESPACE=default
TEMPORAL_WORKER_ROLE=DSL_ENGINE
TEMPORAL_TASK_QUEUE=dsl-engine
TEMPORAL_API_KEY='xxxx' // only required for the staging and prod
TEMPORAL_ADDRESS='xxxx' // only required for the staging and prod
TEMPORAL_WORKER_BUILD_ID=1
AWS_ACCESS_KEY_ID="Use the same from Commenda Logical Backend"
AWS_SECRET_ACCESS_KEY="Use the same from Commenda Logical Backend"
AWS_REGION=ap-south-1
PORT=8001
NODE_ENV=development
```

4. In the commenda logical backend, add the following keys   
   1. **TEMPORAL\_BACKEND\_CLIENT\_KEY** \- It is used in the logical backend to validate the requests coming from the temporal-backend.  
   2. **COMMENDA\_TEMPORAL\_BACKEND\_API\_KEY** \- used to interact with the temporal backend.

```ts
COMMENDA_TEMPORAL_BACKEND_API_KEY=RjrbIP9ZNYkuMf6ICRQLDwTdcfeoIaQU6T0DcIl3UjcXsXFC2JsrThQ6FLE8W3qk
COMMENDA_TEMPORAL_BACKEND_URL=http://localhost:8001
TEMPORAL_BACKEND_CLIENT_KEY=5d19648dc2800784225ff909cb1682bf3d5f51d6181114eaae8ee2396320b8c2
```

**COMMENDA\_LOGICAL\_BACKEND\_CLIENT\_KEY** of the temporal backend should match the **COMMENDA\_TEMPORAL\_BACKEND\_API\_KEY** of the logical backend.

**TEMPORAL\_BACKEND\_CLIENT\_KEY** of the logical backend should map to the **COMMENDA\_LOGICAL\_BACKEND\_API\_KEY** of the temporal backend.

5. First run the “**npm run temporal:dev**”. This will start the temporal server for you on “[**http://localhost:8233**](http://localhost:8233)”. You will also see a [temporal.db](http://temporal.db) created in the root directory. This db stores all the executions.   
6. Secondly, run “**npm run start:dev**”, this will just start the node project server on 8001 port.  
7. Lastly, run “**npm run temporal:worker**”, this will start the temporal worker which will actually run your code, 

   

Note :-   
Always remember, if you are making any changes to the environment variables, then add it on **github** and update the same in **deploy-app.yaml** file as well.

### Now your temporal backend is up and running.