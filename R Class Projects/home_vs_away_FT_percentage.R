# Read in code
regSeason <- read.csv("https://raw.githubusercontent.com/scottgill32/Stat-251/master/DataFiles/RegularSeasonDetailedResults.csv")
teams <- read.csv("https://raw.githubusercontent.com/scottgill32/Stat-251/master/DataFiles/Teams.csv")
library(plyr)

# Home Teams
aHome <- 10
bHome <- 4

# Away Teams
aAway <- 10
bAway <- 5

# Prior Means
aHome / (aHome + bHome)
aAway / (aAway + bAway)

# Prior Variances
(aHome * bHome) / (((aHome + bHome)^2) * (aHome + bHome + 1))
(aAway * bAway) / (((aAway + bAway)^2) * (aAway + bAway + 1))

# Plot the prior distributions for home and away teams
x <- seq(0, 1, length = 1000)
plot(x, dbeta(x, 10, 4), type = 'l', col = 'red', 
     main = "Prior Distributions for Home and Away Teams", 
     ylab = "Probability Density")
lines(x, dbeta(x, 10, 5), col = 'blue')
legend("topleft", legend = c("Prior Home", "Prior Away"), 
       col = c("red", "blue"), lty = 1:1)

# Cut down data set to only what we need
data <- data.frame(regSeason$Season, regSeason$DayNum, regSeason$WTeamID,
                   regSeason$LTeamID, regSeason$WLoc, regSeason$WFTM,
                   regSeason$WFTA, regSeason$LFTM, regSeason$LFTA)

# Rename columns to make column names shorter
names(data) <- c("Season", "DayNum", "WTeamID", "LTeamID", "WLoc", "WFTM",
                 "WFTA", "LFTM", "LFTA")

# Eliminated games played at neutral sites
data <- data[!data$WLoc == "N",]

seasons <- function(year) {
  # Subset data to only use 2018 Season
  seasonData <- data[which(data$Season == year),]
  
  # Create separate data frames for home teams and away teams
  homeData <- data.frame()
  awayData <- data.frame()
  for (i in 1:nrow(seasonData)) {
    if (seasonData$WLoc[i] == "H") {
      homeData[i, "ID"] = seasonData$WTeamID[i]
      homeData[i, "FTM"] = seasonData$WFTM[i]
      homeData[i, "FTA"] = seasonData$WFTA[i]
      awayData[i, "ID"] = seasonData$LTeamID[i]
      awayData[i, "FTM"] = seasonData$LFTM[i]
      awayData[i, "FTA"] = seasonData$LFTA[i]
      awayData[i, "Stadium"] = seasonData$WTeamID[i]
    } else {
      homeData[i, "ID"] = seasonData$LTeamID[i]
      homeData[i, "FTM"] = seasonData$LFTM[i]
      homeData[i, "FTA"] = seasonData$LFTA[i]
      awayData[i, "ID"] = seasonData$WTeamID[i]
      awayData[i, "FTM"] = seasonData$WFTM[i]
      awayData[i, "FTA"] = seasonData$WFTA[i] 
      awayData[i, "Stadium"] = seasonData$LTeamID[i]
    }
  }
  
  # Set up data for each stadium for home teams and away teams
  # --# of games, # FTM and # FTA, FT%
  homeStadium <- ddply(homeData,.(ID),summarize,FTM=sum(FTM),FTA=sum(FTA), 
                       games=length(ID))
  awayStadium <- ddply(awayData,.(Stadium),summarize,FTM=sum(FTM),FTA=sum(FTA), 
                       games=length(ID))
  
  # Find posterior for beta-binomial based on data
  for (i in 1:nrow(homeStadium)) {
    homeStadium['aStar'] <- aHome + homeStadium$FTM
    homeStadium['bStar'] <- bHome + homeStadium$FTA - homeStadium$FTM
  }
  
  for (i in 1:nrow(awayStadium)) {
    awayStadium['aStar'] <- aAway + awayStadium$FTM
    awayStadium['bStar'] <- bAway + awayStadium$FTA - awayStadium$FTM
  }
  
  # Testing out new astar and bstar
  for (i in 1:nrow(homeStadium)) {
    homeStadium[i, 'Diff'] = homeStadium$aStar[i] / (homeStadium$aStar[i] + homeStadium$bStar[i]) - awayStadium$aStar[i] / (awayStadium$aStar[i] + awayStadium$bStar[i])
  }
  
  # Find posterior astar and bstar for all stadiums combined
  homeFTM <- 0
  homeFTA <- 0
  for (i in 1:nrow(homeStadium)) {
    homeFTM <- homeFTM + homeStadium$FTM[i]
    homeFTA <- homeFTA + homeStadium$FTA[i]
  }
  awayFTM <- 0
  awayFTA <- 0
  for (i in 1:nrow(awayStadium)) {
    awayFTM <- awayFTM + awayStadium$FTM[i]
    awayFTA <- awayFTA + awayStadium$FTA[i]
  }
  
  out <- NULL
  out$ID <- homeStadium$ID
  out$aStarHome <- homeStadium$aStar
  out$bStarHome <- homeStadium$bStar
  out$aStarAway <- awayStadium$aStar
  out$bStarAway <- awayStadium$bStar
  out$Diff <- homeStadium$Diff
  out$homeFTM <- homeFTM
  out$homeFTA <- homeFTA
  out$awayFTM <- awayFTM
  out$awayFTA <- awayFTA
  out$homePct <- homeStadium$FTM / homeStadium$FTA
  out$awayPct <- awayStadium$FTM / awayStadium$FTA
  out
}

df <- data.frame()
aStarHome <- aHome
bStarHome <- bHome
aStarAway <- aAway
bStarAway <- bAway

for (i in 2003:2019) {
  season <- seasons(i)
  thisYear <- data.frame("ID" = season$ID, "Diff" = season$Diff, 
                         "Year" = i, "homeFTpct" = season$homePct,
                         "awayFTpct" = season$awayPct)
  df <- rbind(df, thisYear)
  aStarHome <- aStarHome + season$homeFTM
  bStarHome <- bStarHome + season$homeFTA - season$homeFTM
  aStarAway <- aStarAway + season$awayFTM
  bStarAway <- bStarAway + season$awayFTA - season$awayFTM
}

# Plot the posterior for home and away
x <- seq(0, 1, length = 1000)
plot(x, dbeta(x, aStarHome, bStarHome), type = 'l', col = 'red', 
     main = "Posterior Distributions for Home and Away Teams", 
     ylab = "Probability Density", xlim = c(0.68, 0.71),
     ylim = c(0, 1000))
lines(x, dbeta(x, aStarAway, bStarAway), col = 'blue')
legend("topright", legend = c("Posterior Home", "Posterior Away"), 
       col = c("red", "blue"), lty = 1:1)

# Credible interval for each home and away teams
qbeta(c(0.025, 0.975),aStarHome, bStarHome)
qbeta(c(0.025, 0.975),aStarAway, bStarAway)

# Histogram of differences for each stadium each season
hist(df$Diff, xlab = "Difference in Home and Away Percentages", 
     main = "Differences for Each Stadium Each Season",
     breaks = 10)

# Posterior Means
postMeanHome <- aStarHome / (aStarHome + bStarHome)
postMeanAway <- aStarAway / (aStarAway + bStarAway)

# Posterior Variances
postVarHome <- (aStarHome * bStarHome) / (((aStarHome + bStarHome)^2) * (aStarHome + bStarHome + 1))
postVarAway <- (aStarAway * bStarAway) / (((aStarAway + bStarAway)^2) * (aStarAway + bStarAway + 1))

# Posterior difference in means
postMeanHome - postMeanAway

# Posterior ratio of variances
postVarHome / postVarAway
