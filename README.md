# California DMV behind-the-wheel auto appointment check using Selenium and AWS Lambda

This is a test project used for checking latest california behind-the-wheel test appointment date, it is **not working** because the DMV website now using [reCAPTCHA v3](https://developers.google.com/recaptcha/docs/v3).

### File Structure

- seleniumLayer -  Selenium
- lambda

```bash
── /seleniumLayer/  # lambda layers
  ├── /selenium  lambda layer of selenium lib
  │  └──/python/      # python libs
  │   └── /lib/    
  │     └── /python3.6/*    
  ├── /chromedriver/    # lambda layer of headless Chrome 
  │ ├── /chromedriver   # chrome driver
  │ └── /headless-chromium # headless chrome binary
  └── /serverless.yaml     
── /lambda/            # lambda function
  ├── /handler.py      # source code of lambda function 
  └── /serverless.yaml # serverless config
```
### Stack

- Python3.6
- Selenium2.37
- [ChromeDriver2.37](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- [Serverless Chrome v1.0.0.41 ](https://github.com/adieuadieu/serverless-chrome/releases?after=v1.0.0-46)


### Install
Go to root directory of project

```shell
# download Selenium 2.37
pip install -t seleniumLayer/selenium/python/lib/python3.6/site-packages selenium==2.37
pip install -t seleniumLayer/selenium/python/lib/python3.6/site-packages boto==2.49

# download chrome driver
cd seleniumLayer
mkdir chromedriver
cd chromedriver
curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
unzip chromedriver.zip
rm chromedriver.zip

# download chrome binary
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
unzip headless-chromium.zip
rm headless-chromium.zip
```

### Deploy Lambda Layers
Go to root directory of project
```shell
cd seleniumLayer
sls deploy 
```

### S3 Set Up
Change the S3 bucket name in `lambda/serverless.yml`:
```yml
Resource: arn:aws:s3:::selenium-screenshot/*
```

### Deploy Lambda Function
Go to root directory of project
```shell
cd lambda
sls deploy 
```

### Start Testing 
Go to root directory of project
```shell
cd lambda
sls invoke --function hello
```
