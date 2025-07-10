# How to run the application
## Using Docker
checkout the code
`docker build -t interactive-map .`
`docker run -p 8050:8050 interactive-map`
Application should start successfully and should be accessible at http://0.0.0.0/8050
## Using UV
Install uv, 
Sync uv project by running `uv sync`
`uv run app.py` will open a Dash server locally to run on http://127.0.0.1:8050/ should display the interactive map as below
![image info](./pictures/Countries.png)
![image info](./pictures/Countries_Low_High_GDP.png)
![image info](./pictures/Countries_High_Low_GDP.png)


