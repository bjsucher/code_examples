# webscraper for Q1 data from http://www.boxofficemojo.com/quarterly/?chart=byquarter&quarter=Q1

# function that allows reading in data of the form $xxx,xxx,xxx.xx
setClass("AccountingNumber")
setAs("character", "AccountingNumber", 
      function(from) as.numeric(gsub(",", "", gsub("[:$:]", "", from) ) ) )
# data from webpage
library(XML)
# Q1 box office url
q1boxoffice.url<-paste("http://www.boxofficemojo.com/quarterly/?chart=byquarter&quarter=Q1")
# read webpage and store in memory
q1boxoffice.webpage<-htmlParse(q1boxoffice.url)
# create R dataset from webpage contents
q1boxoffice<-readHTMLTable(q1boxoffice.webpage,
                           header=TRUE,which=4,
                           colClasses=c("numeric","AccountingNumber","Percent","numeric",
                                        "AccountingNumber","Percent","character",
                                        "AccountingNumber","Percent") )
# keep only year and gross
q1boxoffice<-q1boxoffice[,1:2]
# change variable name so it doesn't have a space
names(q1boxoffice)<-c("year","gross")
# Create variable qtr
q1boxoffice$qtr <- 1

# Q2 box office url
q2boxoffice.url<-paste("http://www.boxofficemojo.com/quarterly/?chart=byquarter&quarter=Q2")
# read webpage and store in memory
q2boxoffice.webpage<-htmlParse(q2boxoffice.url)
# create R dataset from webpage contents
q2boxoffice<-readHTMLTable(q2boxoffice.webpage,
                           header=TRUE,which=4,
                           colClasses=c("numeric","AccountingNumber","Percent","numeric",
                                        "AccountingNumber","Percent","character",
                                        "AccountingNumber","Percent") )
# keep only year and gross
q2boxoffice<-q2boxoffice[,1:2]
# change variable name so it doesn't have a space
names(q2boxoffice)<-c("year","gross")
# Create variable qtr
q2boxoffice$qtr <- 2

# Q3 box office url
q3boxoffice.url<-paste("http://www.boxofficemojo.com/quarterly/?chart=byquarter&quarter=Q3")
# read webpage and store in memory
q3boxoffice.webpage<-htmlParse(q3boxoffice.url)
# create R dataset from webpage contents
q3boxoffice<-readHTMLTable(q3boxoffice.webpage,
                           header=TRUE,which=4,
                           colClasses=c("numeric","AccountingNumber","Percent","numeric",
                                        "AccountingNumber","Percent","character",
                                        "AccountingNumber","Percent") )
# keep only year and gross
q3boxoffice<-q3boxoffice[,1:2]
# change variable name so it doesn't have a space
names(q3boxoffice)<-c("year","gross")
# Create variable qtr
q3boxoffice$qtr <- 3

# Q4 box office url
q4boxoffice.url<-paste("http://www.boxofficemojo.com/quarterly/?chart=byquarter&quarter=Q4")
# read webpage and store in memory
q4boxoffice.webpage<-htmlParse(q4boxoffice.url)
# create R dataset from webpage contents
q4boxoffice<-readHTMLTable(q4boxoffice.webpage,
                           header=TRUE,which=4,
                           colClasses=c("numeric","AccountingNumber","Percent","numeric",
                                        "AccountingNumber","Percent","character",
                                        "AccountingNumber","Percent") )
# keep only year and gross
q4boxoffice<-q4boxoffice[,1:2]
# change variable name so it doesn't have a space
names(q4boxoffice)<-c("year","gross")
# Create variable qtr
q4boxoffice$qtr <- 4

# Combine the four dataframes
boxoffice <- rbind(q1boxoffice, q2boxoffice, q3boxoffice, q4boxoffice)

# Reorder the dataframe to order by year
boxoffice <- boxoffice[order(boxoffice$year, boxoffice$qtr),]

# Remove row for current quarter
boxoffice <- boxoffice[-145,]

tail(boxoffice)

# Plot time series for quarterly total gross box office
plot(boxoffice$gross, type = 'b', xlab = "Quarters Since 1982", 
     ylab = "Box Office Gross (in millions)")

# Fit the ARIMA(1,1,1) x (1,1,1)_4 model
library(astsa)
boxoffice.out <- sarima(boxoffice$gross,1,1,1,1,1,1,4)

# Table of estimates
boxoffice.out$ttable

# Predictions for the next 3 years
boxoffice.future <- sarima.for(boxoffice$gross, n.ahead = 12,1,1,1,1,1,1,4)

# Find 95% prediction intervals
lower <- boxoffice.future$pred - 1.96 * boxoffice.future$se
upper <- boxoffice.future$pred + 1.96 * boxoffice.future$se

# Table of predictions
cbind(boxoffice.future$pred, lower, upper)

# Publication quality graphic
plot(boxoffice$gross, type = 'b', xlab = "Quarters Since 1982", 
     ylab = "Box Office Gross (in millions)", main = "Box Office Gross by Quarter",
     xlim = c(0,160))
lines(145:156, boxoffice.future$pred, col="darkorange2", type = 'b',
      pch=19)
lines(145:156, lower,col="green", lty=2)
lines(145:156, upper,col="blue", lty=2)
