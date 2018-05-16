# Read in data
tv <- read.table(header = TRUE, text = '
                 Year TVaud Tigers AtBreak DNP Bullpen
                 2003 200.9 1 0.272 6 11
                 2004 235.6 2 0.483 1 10
                 2005 436.6 1 0.488 4 10
                 2006 290.9 3 0.670 7 10
                 2007 305.1 5 0.605 2 10
                 2008 223.3 1 0.500 4 11
                 2009 302.1 5 0.552 19 13
                 2010 260.8 3 0.558 10 16
                 2011 201.9 5 0.533 15 13
                 2012 296.2 3 0.512 6 9
                 2013 374.7 6 0.553 8 14
                 2014 279.9 4 0.582 17 12
                 2015 190.4 4 0.500 8 12
                 2016 122.1 1 0.517 11 14
                 2017 111.2 2 0.448 7 11')

# Tigers All-stars were Michael Fullmer and Justin Upton

# Find means and standard deviations for each variable 
summary(tv)
sd(tv$TVaud)
sd(tv$Tigers)
sd(tv$AtBreak)
sd(tv$DNP)
sd(tv$Bullpen)

# Find correlation between each explanatory variable and the response variable
cor(tv$Tigers, tv$TVaud)
cor(tv$AtBreak, tv$TVaud)
cor(tv$DNP, tv$TVaud)
cor(tv$Bullpen, tv$TVaud)

# Fit model
out.tv <- lm(TVaud ~ Tigers + AtBreak + DNP + Bullpen, data = tv)

# Compute leverage for 2010
leverage.tv <- lm.influence(out.tv)$hat 
subset(leverage.tv, tv$Year == 2010)

# Compute Cook's Distance for 2003
cd.tv <- cooks.distance(out.tv)
subset(cd.tv, tv$Year == 2003)

# Compute R-studentized residual for 2013
R.tv <- rstudent(out.tv)
subset(R.tv, tv$Year == 2013)

# Confirm that 2005 has R-studentized residual that exceeds rule of thumb
# Rule of thumb: > 2
subset(R.tv, tv$Year == 2005)

# The 2005 MLB All-Star Game was played in Detroit so the viewership increased 
# greatly.

# Compute VIF for AtBreak
library(car)
vif(out.tv)
# The VIF for AtBreak is not greater than 10 so we do not need to worry about 
# taking it out.

# Check for collinearity
plot(~Tigers + AtBreak + DNP + Bullpen, data = tv)

# Cut-offs for Leverage and Cook's distance are 2/3 and 2/5
subset(leverage.tv, leverage.tv > (2/3))
subset(cd.tv, cd.tv > (2/5))
# There are no observations that exceed the limitations for leverage and 
# Cook's Distance. The year 2005 exceeded the rule of thumb for R-studentized
# residuals

# Plot each explanatory variable to the response variable to see if 2005 is  a 
# bad influential observation
plot(tv$TVaud ~ tv$Tigers)
points(tv$Tigers[3], tv$TVaud[3], col="red", pch=19)

plot(tv$TVaud ~ tv$AtBreak)
points(tv$AtBreak[3], tv$TVaud[3], col="red", pch=19)

plot(tv$TVaud ~ tv$DNP)
points(tv$DNP[3], tv$TVaud[3], col="red", pch=19)

plot(tv$TVaud ~ tv$Bullpen)
points(tv$Bullpen[3], tv$TVaud[3], col="red", pch=19)

# We will throw out 2005 observation because it is a bad influential observation

# Create new dataframe after throwing out 2005
tv1 <- tv[-3,]
dim(tv1)
names(tv1)

# Fit model for TV aud and report parameter esimates and standard errors
out.tv1 <- lm(TVaud ~ Tigers + AtBreak + DNP + Bullpen, data = tv1)
summary(out.tv1)

# Find confidence intervals for estimates for explanatory variables
confint(out.tv1)

# Create data frame for reduced model
reduced.out.tv1 <- lm(TVaud ~ Tigers + AtBreak, data = tv1)
anova(reduced.out.tv1, out.tv1)

# Predict Successful Tigers
predict(out.tv1, newdata = data.frame(Tigers = 5, AtBreak = 0.6, DNP = 7, 
                                      Bullpen = 11), interval = "confidence")

# Predict Tanking Tigers
predict(out.tv1, newdata = data.frame(Tigers = 1, AtBreak = 0.4, DNP = 7, 
                                      Bullpen = 11), interval = "confidence")

