library(tidyverse)
library(lattice)
library(latticeExtra)

setwd("C:/Users/brand/OneDrive - Duke University/BIOS_702")
dat <- read.csv(file="NHANES702.csv", header=TRUE, na.strings="",
                stringsAsFactors=TRUE)

########## Data cleaning ###########
# Take out values that should not be possible
dat$BMI[dat$BMI > 70] <- NA
dat$SBP[dat$SBP >= 180] <- NA
dat$ACR[dat$ACR >= 6000] <- NA
dat$A1C[dat$A1C >= 11] <- NA
dat$DBP[dat$DBP < 40] <- NA

dat <- dat %>% mutate(CKD = case_when(eGFR >= 60 & ACR < 30 ~ 0,
                                      eGFR < 60 | ACR >= 30 ~ 1),
                      serumK2cat = case_when(serumK <= 4 ~ "0: Low-normal",
                                             serumK > 4 ~ "1: Normal"),
                      dietK2cat = case_when(dietK1000 < 1534 ~ "1: Inadequate intake",
                                            dietK1000 >= 1534 & dietK1000 < 2238 ~ "2: Borderline adequate intake",
                                            dietK1000 >= 2238 ~ "3: Adequate intake"))

######### Get rid of missing values #########
# Take out participants with missing CKD status
dat <- dat[is.na(dat$CKD) == FALSE,]

# Take out participants with missing serumK value
dat <- dat[is.na(dat$serumK) == FALSE,]

########## Preliminary plots ###########
hist(dat$eGFR)
summary(dat$eGFR)

hist(dat$serumK)
summary(dat$serumK)

summary(dat$dietK1000)
boxplot(dat$dietK1000)

boxplot(dat$Age)
summary(dat$Age)

plot(dat$Marital)

summary(dat$PHQ9)
hist(dat$PHQ9)

boxplot(serumK ~ CKD, data = dat)
boxplot(dietK1000 ~ CKD, data = dat)

# Graphs for each important variable
hist(dat$Age, main = "Age", xlab = "Age")
hist(dat$BMI, main = "BMI", xlab = "BMI")
hist(dat$serumK, main = "Serum K", xlab = "Serum K")
hist(dat$dietK1000, main = "Diet K", xlab = "Diet K")
hist(dat$eGFR, main = "eGFR", xlab = "eGFR")

boxplot(dat$Age, main = "Age")
boxplot(dat$BMI, main = "BMI")
boxplot(dat$serumK, main = "Serum K")
boxplot(dat$dietK1000, main = "Diet K")
boxplot(dat$eGFR, main = "eGFR")

############ Characteristics of patients (table 1) ############
# Age
median(dat$Age)
IQR(dat$Age)
median(dat$Age[dat$serumK2cat == "0: Low-normal"])
IQR(dat$Age[dat$serumK2cat == "0: Low-normal"])
median(dat$Age[dat$serumK2cat == "1: Normal"])
IQR(dat$Age[dat$serumK2cat == "1: Normal"])
wilcox.test(x = dat$Age[dat$serumK2cat == "0: Low-normal"],
            y = dat$Age[dat$serumK2cat == "1: Normal"],
            alternative = "two.sided", paired = FALSE,
            exact = TRUE, correct = FALSE)

# Sex
table(dat$Sex)
table(dat$Sex) / nrow(dat)
table(dat$Sex[dat$serumK2cat == "0: Low-normal"])
table(dat$Sex[dat$serumK2cat == "0: Low-normal"]) / 
  nrow(dat[dat$serumK2cat == "0: Low-normal",])
table(dat$Sex[dat$serumK2cat == "1: Normal"])
table(dat$Sex[dat$serumK2cat == "1: Normal"]) / 
  nrow(dat[dat$serumK2cat == "1: Normal",])

chisq.test(x = table(dat$Sex, dat$serumK2cat),
           correct = FALSE)

# Income
table(dat$Income5cat)
table(dat$Income5cat) / sum(table(dat$Income5cat))
table(dat$Income5cat[dat$serumK2cat == "0: Low-normal"])
table(dat$Income5cat[dat$serumK2cat == "0: Low-normal"]) / 
  sum(table(dat$Income5cat[dat$serumK2cat == "0: Low-normal"]))
table(dat$Income5cat[dat$serumK2cat == "1: Normal"])
table(dat$Income5cat[dat$serumK2cat == "1: Normal"]) / 
  sum(table(dat$Income5cat[dat$serumK2cat == "1: Normal"]))
chisq.test(x = table(dat$Income5cat, dat$serumK2cat),
           correct = FALSE)

# dietK
mean(dat$dietK1000, na.rm = TRUE)
sd(dat$dietK1000, na.rm = TRUE)
mean(dat$dietK1000[dat$serumK2cat == "0: Low-normal"], na.rm = TRUE)
sd(dat$dietK1000[dat$serumK2cat == "0: Low-normal"], na.rm = TRUE)
mean(dat$dietK1000[dat$serumK2cat == "1: Normal"], na.rm = TRUE)
sd(dat$dietK1000[dat$serumK2cat == "1: Normal"], na.rm = TRUE)
t.test(x = dat$dietK1000[dat$serumK2cat == "0: Low-normal"],
       y = dat$dietK1000[dat$serumK2cat == "1: Normal"],
       alternative = "two.sided")

# dietK groups
table(dat$dietK2cat)
table(dat$dietK2cat) / sum(table(dat$dietK2cat))
table(dat$dietK2cat[dat$serumK2cat == "0: Low-normal"])
table(dat$dietK2cat[dat$serumK2cat == "0: Low-normal"]) / 
  sum(table(dat$dietK2cat[dat$serumK2cat == "0: Low-normal"]))
table(dat$dietK2cat[dat$serumK2cat == "1: Normal"])
table(dat$dietK2cat[dat$serumK2cat == "1: Normal"]) / 
  sum(table(dat$dietK2cat[dat$serumK2cat == "1: Normal"]))
dat <- dat %>% mutate(dietK2catUpdate = case_when(dietK1000 < 1534 ~ "Inadequate",
                                                  dietK1000 >= 1534 ~ "Borderline"))
chisq.test(x = table(dat$dietK2catUpdate, dat$serumK2cat),
           correct = FALSE)

######## Is 68% of eGFR normally distributed #########
ub68 <- mean(dat$eGFR) + sd(dat$eGFR)
lb68 <- mean(dat$eGFR) - sd(dat$eGFR)
sum(dat$eGFR >= lb68 & dat$eGFR <= ub68) / nrow(dat)

ub95 <- mean(dat$eGFR) + sd(dat$eGFR)*2
lb95 <- mean(dat$eGFR) - sd(dat$eGFR)*2
sum(dat$eGFR >= lb95 & dat$eGFR <= ub95) / nrow(dat)

########## EDA: 95% CI for each test with eGFR ##########
# 95% CI of eGFR within two subgroups of serumK
t.test(x = dat$eGFR[dat$serumK2cat == "0: Low-normal"])
t.test(x = dat$eGFR[dat$serumK2cat == "1: Normal"])

# Look at 95% CI of eGFR within three subgroups of dietK
t.test(x = dat$eGFR[dat$dietK2cat == "1: Inadequate intake"])
t.test(x = dat$eGFR[dat$dietK2cat == "2: Borderline adequate intake"])
t.test(x = dat$eGFR[dat$dietK2cat == "3: Adequate intake"])
# Combine borderline adequate and adequate into one group
t.test(x = dat$eGFR[dat$dietK2cat %in% c("2: Borderline adequate intake", 
                                         "3: Adequate intake")])


########## Assumptions for the data given CKD status ############
# CKD positive
qqnorm(dat$serumK[dat$CKD == 1], main = "Q-Q plot for CKD Positive")
qqline(dat$serumK[dat$CKD == 1], col = "blue")
hist(dat$serumK[dat$CKD == 1], xlab = "Serum K",
     main = "Frequency of Serum K for CKD Positive")

# CKD negative
qqnorm(dat$serumK[dat$CKD == 0], main = "Q-Q plot for CKD Negative")
qqline(dat$serumK[dat$CKD == 0], col = "blue")
hist(dat$serumK[dat$CKD == 0], xlab = "Serum K",
     main = "Frequency of Serum K for CKD Negative")

############## Assumptions for the data given eGFR ############
# Low-normal serum K
qqnorm(dat$eGFR[dat$serumK <= 4], main = "Q-Q plot for low-normal serum K")
qqline(dat$eGFR[dat$serumK <= 4], col = "blue")
hist(dat$eGFR[dat$serumK <= 4], xlab = "eGFR",
     main = "Frequency of eGFR for low normal serum K")

# Normal serum K
qqnorm(dat$eGFR[dat$serumK > 4], main = "Q-Q plot for normal serum K")
qqline(dat$eGFR[dat$serumK > 4], col = "blue")
hist(dat$eGFR[dat$serumK > 4], xlab = "eGFR",
     main = "Frequency of eGFR for normal serum K")

############## Analysis for Serum K and CKD status ################
sum(dat$CKD == 1)
sum(dat$CKD == 0)

# Compare variances
# Rule of thumb -- ratio of variances
(sd(dat$serumK[dat$CKD == 1])^2) / (sd(dat$serumK[dat$CKD == 0])^2)
# Variance ratio test
fstat <- (sd(dat$serumK[dat$CKD == 1])^2) / (sd(dat$serumK[dat$CKD == 0])^2)
2*(1-pf(fstat, 63, 235))

# Pool variances
n1 <- sum(dat$CKD == 1)
n2 <- sum(dat$CKD == 0)
s1 <- sd(dat$serumK[dat$CKD == 1])
s2 <- sd(dat$serumK[dat$CKD == 0])
s2pool <- (((n1-1) * s1^2) + (n2-1)*s2^2) / ((n1-1) + (n2-1))

# Do two sample t test
ybar1 <- mean(dat$serumK[dat$CKD == 1])
ybar2 <- mean(dat$serumK[dat$CKD == 0])
tstat <- (ybar1 - ybar2) / sqrt((s2pool / n1) + (s2pool / n2))
2*(1-pt(tstat, n1 + n2 - 2))

# 95% confidence interval
(ybar1 - ybar2) + c(-1,1) * qt(0.975, 64+236-2) *
  sqrt((s2pool / n1) + (s2pool / n2))

# Chi-square test
table(dat$serumK2cat, dat$CKD)
chisq.test(x = table(dat$serumK2cat, dat$CKD), correct = FALSE)

# Relative Risk
pi1 <- 37 / (126+37)
pi2 <- 27 / (27+110)
pi1 / pi2

logCI <- log(pi1/pi2) + c(-1,1) * qnorm(0.975) * 
          sqrt((126/(37*(126+37))) + (110/(27*(110+27))))
exp(logCI)

# Odds ratio
OR <- (pi1 / (1-pi1)) / (pi2 / (1-pi2))
logCI <- log(OR) + c(-1,1) * qnorm(0.975) * 
          sqrt((1/110)+(1/27)+(1/126)+(1/37))
exp(logCI)

# MH test adjusting for age
dat <- dat %>% mutate(age60 = case_when(Age < 60 ~ "Below 60",
                                        Age >= 60 ~ "60 and older"))
table(dat$age60)
over60 <- dat[dat$age60 == "60 and older",]
under60 <- dat[dat$age60 == "Below 60",]

# Over 60
pi1 <- 28 / (28+41)
pi2 <- 15 / (15+25)
OR <- (pi1 / (1-pi1)) / (pi2 / (1-pi2))
logCI <- log(OR) + c(-1,1) * qnorm(0.975) * 
  sqrt((1/25)+(1/15)+(1/41)+(1/28))
exp(logCI)

# Under 60
pi1 <- 9 / (85+9)
pi2 <- 12 / (12+85)
OR <- (pi1 / (1-pi1)) / (pi2 / (1-pi2))
logCI <- log(OR) + c(-1,1) * qnorm(0.975) * 
  sqrt((1/85)+(1/85)+(1/12)+(1/9))
exp(logCI)

# MH test
library(abind)
S1 <- matrix(c(28,15,41,25), nrow = 2)
S2 <- matrix(c(9,12,85,85), nrow = 2)
mantelhaen.test(abind(S1, S2, along = 3), correct = FALSE)

############# Analysis for dietary K and CKD status ###################
sum(dat$CKD == 1)
sum(dat$CKD == 0)

# Compare variances
# Rule of thumb -- ratio of variances
(sd(dat$dietK1000[dat$CKD == 0], na.rm = TRUE)^2) / 
  (sd(dat$dietK1000[dat$CKD == 1], na.rm = TRUE)^2)
# Variance ratio test
fstat <- (sd(dat$dietK1000[dat$CKD == 0], na.rm = TRUE)^2) / 
  (sd(dat$dietK1000[dat$CKD == 1], na.rm = TRUE)^2)
2*(1-pf(fstat, 63, 235))

# Pool variances
n1 <- sum(dat$CKD == 0)
n2 <- sum(dat$CKD == 1)
s1 <- sd(dat$dietK1000[dat$CKD == 0], na.rm = TRUE)
s2 <- sd(dat$dietK1000[dat$CKD == 1], na.rm = TRUE)
s2pool <- (((n1-1) * s1^2) + (n2-1)*s2^2) / ((n1-1) + (n2-1))

# Do two sample t test
ybar1 <- mean(dat$dietK1000[dat$CKD == 0], na.rm = TRUE)
ybar2 <- mean(dat$dietK1000[dat$CKD == 1], na.rm = TRUE)
tstat <- (ybar1 - ybar2) / sqrt((s2pool / n1) + (s2pool / n2))
2*(pt(tstat, n1 + n2 - 2))

# 95% confidence interval
(ybar1 - ybar2) + c(-1,1) * qt(0.975, 64+236-2) *
  sqrt((s2pool / n1) + (s2pool / n2))

# Chi-square test
table(dat$dietK2catUpdate, dat$CKD)
chisq.test(x = table(dat$dietK2catUpdate, dat$CKD), correct = FALSE)

# Relative Risk
pi1 <- 13 / (48+13)
pi2 <- 43 / (43+164)
pi1 / pi2

logCI <- log(pi1/pi2) + c(-1,1) * qnorm(0.975) * 
  sqrt((164/(43*(164+43))) + (48/(13*(48+13))))
exp(logCI)

# Odds ratio
OR <- (pi1 / (1-pi1)) / (pi2 / (1-pi2))
logCI <- log(OR) + c(-1,1) * qnorm(0.975) * 
  sqrt((1/48)+(1/13)+(1/164)+(1/43))
exp(logCI)

# Over 60
pi1 <- 11 / (16+11)
pi2 <- 27 / (27+45)
OR <- (pi1 / (1-pi1)) / (pi2 / (1-pi2))
logCI <- log(OR) + c(-1,1) * qnorm(0.975) * 
  sqrt((1/16)+(1/11)+(1/27)+(1/45))
exp(logCI)

# Under 60
pi1 <- 2 / (32+2)
pi2 <- 16 / (16+119)
OR <- (pi1 / (1-pi1)) / (pi2 / (1-pi2))
logCI <- log(OR) + c(-1,1) * qnorm(0.975) * 
  sqrt((1/2)+(1/32)+(1/16)+(1/119))
exp(logCI)

# MH test
S1 <- matrix(c(11,27,16,45), nrow = 2)
S2 <- matrix(c(2,16,32,119), nrow = 2)
mantelhaen.test(abind(S1, S2, along = 3), correct = FALSE)

############# Analysis for serum K and eGFR ######################
table(dat$serumK2cat)

# Compare variances
# Rule of thumb -- ratio of variances
(sd(dat$eGFR[dat$serumK2cat == "1: Normal"])^2) / 
  (sd(dat$eGFR[dat$serumK2cat == "0: Low-normal"])^2)
# Variance ratio test
fstat <- (sd(dat$eGFR[dat$serumK2cat == "1: Normal"])^2) / 
  (sd(dat$eGFR[dat$serumK2cat == "0: Low-normal"])^2)
2*(1-pf(fstat, 162, 136))

# Pool variances
n1 <- sum(dat$serumK2cat == "1: Normal")
n2 <- sum(dat$serumK2cat == "0: Low-normal")
s1 <- sd(dat$eGFR[dat$serumK2cat == "1: Normal"])
s2 <- sd(dat$eGFR[dat$serumK2cat == "0: Low-normal"])
s2pool <- (((n1-1) * s1^2) + (n2-1)*s2^2) / ((n1-1) + (n2-1))

# Two sample t test
ybar1 <- mean(dat$eGFR[dat$serumK2cat == "1: Normal"])
ybar2 <- mean(dat$eGFR[dat$serumK2cat == "0: Low-normal"])
tstat <- (ybar1 - ybar2) / sqrt((s2pool / n1) + (s2pool / n2))
2*(pt(tstat, n1 + n2 - 2))

# 95% confidence interval
(ybar1 - ybar2) + c(-1,1) * qt(0.975, 137+163-2) *
  sqrt((s2pool / n1) + (s2pool / n2))

############# Analysis for dietary K and eGFR ######################
sum(dat$dietK1000 < 1534, na.rm = TRUE)
sum(dat$dietK1000 >= 1534, na.rm = TRUE)

# Compare variances
# Rule of thumb -- ratio of variances
(sd(dat$eGFR[dat$dietK1000 < 1534], na.rm = TRUE)^2) / 
  (sd(dat$eGFR[dat$dietK1000 >= 1534], na.rm = TRUE)^2)
# Variance ratio test
fstat <- (sd(dat$eGFR[dat$dietK1000 < 1534], na.rm = TRUE)^2) / 
          (sd(dat$eGFR[dat$dietK1000 >= 1534], na.rm = TRUE)^2)
2*(1-pf(fstat, 206, 60))

# Satterthwaite approximation
n1 <- sum(dat$dietK1000 < 1534, na.rm = TRUE)
n2 <- sum(dat$dietK1000 >= 1534, na.rm = TRUE)
s1 <- sd(dat$eGFR[dat$dietK1000 < 1534], na.rm = TRUE)
s2 <- sd(dat$eGFR[dat$dietK1000 >= 1534], na.rm = TRUE)
v1 <- (s1^2) / n1
v2 <- (s2^2) / n2
v <- ((v1+v2)^2) / (((v1^2)/(n1-1)) + ((v2^2)/(n2-1)))

# Two sample t test
ybar1 <- mean(dat$eGFR[dat$dietK1000 < 1534], na.rm = TRUE)
ybar2 <- mean(dat$eGFR[dat$dietK1000 >= 1534], na.rm = TRUE)
tstat <- (ybar1 - ybar2) / sqrt(((s1^2) / n1) + ((s2^2) / n2))
2*(1-pt(tstat, v))

# 95% confidence interval
(ybar1 - ybar2) + c(-1,1) * qt(0.975, v) *
  sqrt(((s1^2) / n1) + ((s2^2) / n2))

